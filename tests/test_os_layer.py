"""
Tests for OS abstraction layer
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone.os_layer import ProcessManager, FileSystem, SecurityManager
from intelligentone.os_layer.process import ProcessState
from intelligentone.os_layer.filesystem import Resource, ResourceType
from intelligentone.os_layer.security import Credential, PermissionLevel


def test_process_manager():
    """Test process management"""
    pm = ProcessManager()
    
    # Spawn process
    pid = pm.spawn("test.capability", {"param": "value"})
    assert pid >= 1000
    
    # Get process
    proc = pm.get_process(pid)
    assert proc is not None
    assert proc.capability_name == "test.capability"
    assert proc.state == ProcessState.READY
    
    # Start process
    pm.start(pid)
    proc = pm.get_process(pid)
    assert proc.state == ProcessState.RUNNING
    
    # Terminate process
    pm.terminate(pid)
    proc = pm.get_process(pid)
    assert proc.state == ProcessState.TERMINATED


def test_filesystem():
    """Test file system abstraction"""
    fs = FileSystem()
    
    # Mount resource
    resource = Resource(
        path="/api/test",
        type=ResourceType.API,
        data={"endpoint": "https://api.example.com"},
        metadata={"version": "v1"}
    )
    
    fs.mount("/api/test", resource)
    
    # Get resource
    retrieved = fs.get("/api/test")
    assert retrieved is not None
    assert retrieved.type == ResourceType.API
    
    # Check existence
    assert fs.exists("/api/test")
    assert not fs.exists("/api/nonexistent")
    
    # List directory
    items = fs.list("/")
    assert "api" in items


def test_security_manager():
    """Test security management"""
    sm = SecurityManager()
    
    # Store credential
    cred = Credential(
        type="bearer",
        value="token123",
        metadata={"service": "test"}
    )
    
    sm.store_credential("test_cred", cred)
    
    # Retrieve credential
    retrieved = sm.get_credential("test_cred")
    assert retrieved is not None
    assert retrieved.value == "token123"
    
    # Grant permission
    sm.grant_permission("alice", "test.capability", PermissionLevel.READ)
    
    # Check permission
    has_permission = sm.check_permission("alice", "test.capability", PermissionLevel.READ)
    assert has_permission
    
    # Check unauthorized permission
    has_admin = sm.check_permission("alice", "test.capability", PermissionLevel.ADMIN)
    assert not has_admin


def test_admin_permissions():
    """Test admin permissions work on all capabilities"""
    sm = SecurityManager()
    
    # Grant admin permission
    sm.grant_permission("bob", "*", PermissionLevel.ADMIN)
    
    # Should have admin on any capability
    assert sm.check_permission("bob", "any.capability", PermissionLevel.ADMIN)
    assert sm.check_permission("bob", "another.capability", PermissionLevel.ADMIN)


if __name__ == "__main__":
    test_process_manager()
    test_filesystem()
    test_security_manager()
    test_admin_permissions()
    
    print("All OS layer tests passed!")
