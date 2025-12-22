"""
Example: OS abstraction layer demonstration

This example shows how intelligentOne provides OS-level abstractions
for web capabilities
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone import IntelligentOne, Capability
from intelligentone.os_layer import ProcessManager, FileSystem, SecurityManager
from intelligentone.os_layer.filesystem import Resource, ResourceType
from intelligentone.os_layer.security import Credential, PermissionLevel


def demonstrate_process_management():
    """Demonstrate process management"""
    print("=== Process Management ===\n")
    
    pm = ProcessManager()
    
    # Spawn processes
    print("1. Spawning processes for capability executions...")
    pid1 = pm.spawn("weather.forecast", {"location": "SF"})
    pid2 = pm.spawn("user.create", {"name": "Alice"})
    
    print(f"   ✓ Spawned process {pid1} for weather.forecast")
    print(f"   ✓ Spawned process {pid2} for user.create\n")
    
    # Start processes
    print("2. Starting processes...")
    pm.start(pid1)
    pm.start(pid2)
    print(f"   ✓ Started {len(pm.list_processes())} processes\n")
    
    # List processes
    print("3. Listing active processes:")
    for proc in pm.list_processes():
        print(f"   PID {proc.pid}: {proc.capability_name} [{proc.state.value}]")
    print()


def demonstrate_filesystem():
    """Demonstrate file system abstraction"""
    print("=== File System Abstraction ===\n")
    
    fs = FileSystem()
    
    # Mount resources
    print("1. Mounting web resources as file system...")
    
    fs.mount("/api/weather", Resource(
        path="/api/weather",
        type=ResourceType.API,
        data={"endpoint": "https://api.weather.com"},
        metadata={"version": "v1"}
    ))
    
    fs.mount("/api/users", Resource(
        path="/api/users",
        type=ResourceType.API,
        data={"endpoint": "https://api.users.com"},
        metadata={"version": "v2"}
    ))
    
    fs.mount("/services/github", Resource(
        path="/services/github",
        type=ResourceType.SERVICE,
        data={"endpoint": "https://api.github.com"},
        metadata={"type": "git"}
    ))
    
    print("   ✓ Mounted 3 resources\n")
    
    # List resources
    print("2. Listing root directory:")
    for item in fs.list("/"):
        print(f"   - {item}")
    print()
    
    # Access resource
    print("3. Accessing resource: /api/weather")
    resource = fs.get("/api/weather")
    if resource:
        print(f"   Type: {resource.type.value}")
        print(f"   Data: {resource.data}")
        print(f"   Metadata: {resource.metadata}")
    print()


def demonstrate_security():
    """Demonstrate security management"""
    print("=== Security Management ===\n")
    
    sm = SecurityManager()
    
    # Store credentials
    print("1. Storing credentials...")
    sm.store_credential("github_token", Credential(
        type="bearer",
        value="ghp_xxxxxxxxxxxx",
        metadata={"service": "github"}
    ))
    
    sm.store_credential("weather_api_key", Credential(
        type="api_key",
        value="wxkey_xxxxxxxxxxxx",
        metadata={"service": "weather"}
    ))
    
    print("   ✓ Stored 2 credentials\n")
    
    # Grant permissions
    print("2. Granting permissions...")
    sm.grant_permission("alice", "weather.forecast", PermissionLevel.READ)
    sm.grant_permission("alice", "user.create", PermissionLevel.WRITE)
    sm.grant_permission("bob", "*", PermissionLevel.ADMIN)
    
    print("   ✓ Granted permissions to users\n")
    
    # Check permissions
    print("3. Checking permissions:")
    can_alice_read = sm.check_permission("alice", "weather.forecast", PermissionLevel.READ)
    can_alice_admin = sm.check_permission("alice", "weather.forecast", PermissionLevel.ADMIN)
    can_bob_admin = sm.check_permission("bob", "anything", PermissionLevel.ADMIN)
    
    print(f"   Alice can read weather.forecast: {can_alice_read}")
    print(f"   Alice has admin on weather.forecast: {can_alice_admin}")
    print(f"   Bob has admin on anything: {can_bob_admin}")
    print()


def main():
    print("=== intelligentOne OS Abstraction Layer ===\n")
    
    demonstrate_process_management()
    demonstrate_filesystem()
    demonstrate_security()
    
    print("=== Example Complete ===")


if __name__ == "__main__":
    main()
