"""
Tests for core IntelligentOne functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone import IntelligentOne, Capability


def test_initialization():
    """Test IntelligentOne initialization"""
    os = IntelligentOne()
    assert os is not None
    assert os.capabilities == {}
    assert os.discovery is not None
    assert os.executor is not None


def test_capability_creation():
    """Test Capability object creation"""
    cap = Capability(
        name="test.capability",
        description="A test capability",
        endpoint="https://api.example.com/test",
        method="GET"
    )
    
    assert cap.name == "test.capability"
    assert cap.description == "A test capability"
    assert cap.endpoint == "https://api.example.com/test"
    assert cap.method == "GET"


def test_capability_registration():
    """Test registering a capability"""
    os = IntelligentOne()
    
    cap = Capability(
        name="test.get",
        description="Test GET capability",
        endpoint="https://api.example.com/test",
        method="GET"
    )
    
    os.register_capability(cap)
    
    assert "test.get" in os.capabilities
    assert os.get_capability("test.get") == cap


def test_discover_rest():
    """Test REST API discovery"""
    os = IntelligentOne()
    
    capabilities = os.discover("https://api.example.com", "rest")
    
    assert len(capabilities) > 0
    assert all(isinstance(cap, Capability) for cap in capabilities)
    
    # Check that capabilities were registered
    assert len(os.list_capabilities()) > 0


def test_discover_openapi():
    """Test OpenAPI discovery"""
    os = IntelligentOne()
    
    capabilities = os.discover("https://api.example.com/swagger.json", "openapi")
    
    assert len(capabilities) > 0
    
    # Check for expected capabilities
    cap_names = [cap.name for cap in capabilities]
    assert any("users" in name for name in cap_names)


def test_execute_capability():
    """Test executing a capability"""
    os = IntelligentOne()
    
    # Discover and register capabilities
    os.discover("https://api.example.com", "rest")
    
    # Execute a capability
    result = os.execute("api.get", {})
    
    assert result is not None
    assert result["status"] == "success"


def test_execute_with_params():
    """Test executing a capability with parameters"""
    os = IntelligentOne()
    
    os.discover("https://api.example.com", "rest")
    
    result = os.execute("api.post", {
        "name": "Test User",
        "email": "test@example.com"
    })
    
    assert result["status"] == "success"
    assert "data" in result["result"]


def test_list_capabilities():
    """Test listing all capabilities"""
    os = IntelligentOne()
    
    # Initially empty
    assert len(os.list_capabilities()) == 0
    
    # Discover some capabilities
    os.discover("https://api.example.com", "rest")
    
    # Should now have capabilities
    caps = os.list_capabilities()
    assert len(caps) > 0


def test_unregister_capability():
    """Test unregistering a capability"""
    os = IntelligentOne()
    
    cap = Capability(
        name="temp.capability",
        description="Temporary capability",
        endpoint="https://api.example.com/temp",
        method="GET"
    )
    
    os.register_capability(cap)
    assert "temp.capability" in os.capabilities
    
    os.unregister_capability("temp.capability")
    assert "temp.capability" not in os.capabilities


def test_pipeline_creation():
    """Test creating a capability pipeline"""
    os = IntelligentOne()
    
    # Register some capabilities
    cap1 = Capability(
        name="step1",
        description="First step",
        endpoint="https://api.example.com/1",
        method="GET",
        metadata={"source": "rest"}
    )
    cap2 = Capability(
        name="step2",
        description="Second step",
        endpoint="https://api.example.com/2",
        method="GET",
        metadata={"source": "rest"}
    )
    
    os.register_capability(cap1)
    os.register_capability(cap2)
    
    # Create pipeline
    pipeline = os.pipeline([
        ("step1", {}),
        ("step2", {})
    ])
    
    assert pipeline is not None
    assert len(pipeline.steps) == 2


def test_pipeline_execution():
    """Test executing a pipeline"""
    os = IntelligentOne()
    
    # Register capabilities
    cap1 = Capability(
        name="step1",
        description="First step",
        endpoint="https://api.example.com/1",
        method="GET",
        metadata={"source": "rest"}
    )
    cap2 = Capability(
        name="step2",
        description="Second step",
        endpoint="https://api.example.com/2",
        method="GET",
        metadata={"source": "rest"}
    )
    
    os.register_capability(cap1)
    os.register_capability(cap2)
    
    # Create and execute pipeline
    pipeline = os.pipeline([
        ("step1", {}),
        ("step2", lambda prev: {})
    ])
    
    result = pipeline.execute()
    
    assert result is not None
    assert result["status"] == "success"


if __name__ == "__main__":
    # Run tests
    test_initialization()
    test_capability_creation()
    test_capability_registration()
    test_discover_rest()
    test_discover_openapi()
    test_execute_capability()
    test_execute_with_params()
    test_list_capabilities()
    test_unregister_capability()
    test_pipeline_creation()
    test_pipeline_execution()
    
    print("All tests passed!")
