#!/usr/bin/env python3
"""
intelligentOne Demo - Showcase the web as an executable operating system

This demo script demonstrates the complete intelligentOne system:
- Capability discovery from multiple sources
- Capability execution
- Pipeline composition
- OS abstraction layer features
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from intelligentone import IntelligentOne, Capability
from intelligentone.os_layer import ProcessManager, FileSystem, SecurityManager
from intelligentone.os_layer.filesystem import Resource, ResourceType
from intelligentone.os_layer.security import Credential, PermissionLevel


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_core_concept():
    """Demonstrate the core concept of intelligentOne"""
    print_section("intelligentOne: Capabilities over Information")
    
    print("Traditional systems: Retrieve INFORMATION from the web")
    print("  Example: GET https://api.weather.com/forecast")
    print("  Result: JSON data that you must parse and process")
    print()
    
    print("intelligentOne: Retrieve CAPABILITIES from the web")
    print("  Example: os.execute('weather.forecast', {'location': 'SF'})")
    print("  Result: Direct execution of the capability with structured results")
    print()
    
    print("The web becomes an executable operating system where:")
    print("  • APIs become system calls")
    print("  • Services become OS resources")
    print("  • Capabilities are composable")
    print("  • Everything is discoverable")


def demo_discovery():
    """Demonstrate capability discovery"""
    print_section("1. Capability Discovery")
    
    os = IntelligentOne()
    
    print("Discovering capabilities from multiple sources...\n")
    
    # Discover REST API
    print("→ REST API Discovery")
    rest_caps = os.discover("https://api.example.com", "rest")
    print(f"  Found {len(rest_caps)} capabilities: {[c.name for c in rest_caps]}\n")
    
    # Discover OpenAPI
    print("→ OpenAPI Specification Discovery")
    openapi_caps = os.discover("https://api.example.com/swagger.json", "openapi")
    print(f"  Found {len(openapi_caps)} capabilities:")
    for cap in openapi_caps[:3]:
        print(f"    • {cap.name}: {cap.description}")
    print()
    
    # Discover GraphQL
    print("→ GraphQL Schema Discovery")
    graphql_caps = os.discover("https://api.example.com/graphql", "graphql")
    print(f"  Found {len(graphql_caps)} capabilities: {[c.name for c in graphql_caps]}\n")
    
    print(f"✓ Total capabilities registered: {len(os.list_capabilities())}")
    
    return os


def demo_execution(os):
    """Demonstrate capability execution"""
    print_section("2. Capability Execution")
    
    print("Executing discovered capabilities...\n")
    
    # Simple execution
    print("→ Execute: api.get")
    result = os.execute("api.get", {})
    print(f"  Status: {result['status']}")
    print(f"  Result: {result['result']['message']}\n")
    
    # Execution with parameters
    print("→ Execute: users.create with parameters")
    result = os.execute("users.create", {
        "name": "Alice Smith",
        "email": "alice@example.com"
    })
    print(f"  Status: {result['status']}")
    print(f"  Created: {result['result']['data']}\n")
    
    print("✓ Capabilities executed as OS-level system calls")


def demo_composition(os):
    """Demonstrate capability composition"""
    print_section("3. Capability Composition")
    
    # Register additional capabilities for the demo
    os.register_capability(Capability(
        name="geocode.lookup",
        description="Convert address to coordinates",
        endpoint="https://api.geocode.com/lookup",
        method="GET",
        metadata={"source": "rest"}
    ))
    
    os.register_capability(Capability(
        name="weather.forecast",
        description="Get weather forecast",
        endpoint="https://api.weather.com/forecast",
        method="GET",
        metadata={"source": "rest"}
    ))
    
    os.register_capability(Capability(
        name="notify.send",
        description="Send notification",
        endpoint="https://api.notify.com/send",
        method="POST",
        metadata={"source": "rest"}
    ))
    
    print("Creating a capability pipeline:\n")
    print("  Step 1: geocode.lookup    → Convert address to coordinates")
    print("  Step 2: weather.forecast  → Get weather for coordinates")
    print("  Step 3: notify.send       → Send weather notification\n")
    
    pipeline = os.pipeline([
        ("geocode.lookup", {"address": "123 Main St, San Francisco"}),
        ("weather.forecast", lambda prev: {"location": "San Francisco"}),
        ("notify.send", lambda prev: {"message": f"Weather forecast retrieved"})
    ])
    
    print("→ Executing pipeline...")
    result = pipeline.execute()
    print(f"  ✓ Pipeline completed successfully")
    print(f"  Final result: {result['result']['message']}\n")
    
    print("✓ Capabilities composed into complex workflows")


def demo_os_layer():
    """Demonstrate OS abstraction layer"""
    print_section("4. OS Abstraction Layer")
    
    # Process Management
    print("→ Process Management\n")
    pm = ProcessManager()
    
    pid1 = pm.spawn("weather.forecast", {"location": "NYC"})
    pid2 = pm.spawn("user.query", {"id": "12345"})
    
    pm.start(pid1)
    pm.start(pid2)
    
    print(f"  Spawned process {pid1}: weather.forecast")
    print(f"  Spawned process {pid2}: user.query")
    print(f"  Active processes: {len(pm.list_processes())}\n")
    
    # File System
    print("→ File System Abstraction\n")
    fs = FileSystem()
    
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
    
    print("  Mounted resources:")
    for item in fs.list("/"):
        print(f"    /{item}/")
        for subitem in fs.list(f"/{item}"):
            print(f"      ├── {subitem}")
    print()
    
    # Security
    print("→ Security Management\n")
    sm = SecurityManager()
    
    sm.store_credential("weather_api", Credential(
        type="api_key",
        value="wx_key_xxxxxxxxx",
        metadata={"service": "weather"}
    ))
    
    sm.grant_permission("alice", "weather.forecast", PermissionLevel.EXECUTE)
    sm.grant_permission("bob", "*", PermissionLevel.ADMIN)
    
    print("  Stored credentials: 1")
    print("  Granted permissions:")
    print("    • alice: EXECUTE on weather.forecast")
    print("    • bob: ADMIN on all capabilities\n")
    
    print("✓ Full OS abstractions for web capabilities")


def demo_summary():
    """Print summary of intelligentOne capabilities"""
    print_section("Summary: The Web as an Operating System")
    
    print("intelligentOne transforms the web by:\n")
    print("  1. Discovery Over Configuration")
    print("     • Automatically discover capabilities from APIs")
    print("     • No hardcoded integrations required")
    print("     • Dynamic capability registration\n")
    
    print("  2. Execution as a First-Class Primitive")
    print("     • Web APIs become executable system calls")
    print("     • Direct invocation with parameters")
    print("     • Structured result handling\n")
    
    print("  3. Composability")
    print("     • Chain capabilities into pipelines")
    print("     • Pass data between steps")
    print("     • Build complex workflows from simple capabilities\n")
    
    print("  4. OS-Level Abstractions")
    print("     • Process management for capability lifecycle")
    print("     • File system for resource organization")
    print("     • Security for authentication and permissions\n")
    
    print("The web is no longer just information—it's EXECUTABLE.\n")
    print("Welcome to intelligentOne. Welcome to the executable web. 🚀")


def main():
    """Run the complete demo"""
    print("\n" + "=" * 70)
    print("  intelligentOne Demo: Transform the Web into an Executable OS")
    print("=" * 70)
    
    try:
        # Core concept
        demo_core_concept()
        
        # Discovery
        os = demo_discovery()
        
        # Execution
        demo_execution(os)
        
        # Composition
        demo_composition(os)
        
        # OS Layer
        demo_os_layer()
        
        # Summary
        demo_summary()
        
        print("\n" + "=" * 70)
        print("  Demo Complete!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
