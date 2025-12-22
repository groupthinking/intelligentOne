"""
Tests for capability execution
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone.core import Capability
from intelligentone.executor import CapabilityExecutor


def test_executor_initialization():
    """Test CapabilityExecutor initialization"""
    executor = CapabilityExecutor()
    assert executor is not None
    assert executor.capabilities == {}
    assert executor.execution_history == []


def test_capability_registration():
    """Test registering a capability with executor"""
    executor = CapabilityExecutor()
    
    cap = Capability(
        name="test.capability",
        description="Test capability",
        endpoint="https://api.example.com/test",
        method="GET",
        metadata={"source": "rest"}
    )
    
    executor.register(cap)
    assert "test.capability" in executor.capabilities


def test_execute_rest_capability():
    """Test executing a REST capability"""
    executor = CapabilityExecutor()
    
    cap = Capability(
        name="test.get",
        description="Test GET",
        endpoint="https://api.example.com/test",
        method="GET",
        metadata={"source": "rest"}
    )
    
    executor.register(cap)
    result = executor.execute("test.get", {})
    
    assert result["status"] == "success"
    assert result["capability"] == "test.get"


def test_execute_with_params():
    """Test executing with parameters"""
    executor = CapabilityExecutor()
    
    cap = Capability(
        name="user.create",
        description="Create user",
        endpoint="https://api.example.com/users",
        method="POST",
        parameters={
            "name": {"type": "string", "required": False},
            "email": {"type": "string", "required": False}
        },
        metadata={"source": "rest"}
    )
    
    executor.register(cap)
    result = executor.execute("user.create", {
        "name": "Alice",
        "email": "alice@example.com"
    })
    
    assert result["status"] == "success"
    assert "data" in result["result"]


def test_required_params_validation():
    """Test that required parameters are validated"""
    executor = CapabilityExecutor()
    
    cap = Capability(
        name="test.required",
        description="Test required params",
        endpoint="https://api.example.com/test",
        method="POST",
        parameters={
            "required_field": {"type": "string", "required": True}
        },
        metadata={"source": "rest"}
    )
    
    executor.register(cap)
    
    # Should raise ValueError for missing required param
    try:
        executor.execute("test.required", {})
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "required_field" in str(e)


def test_execution_history():
    """Test that execution history is tracked"""
    executor = CapabilityExecutor()
    
    cap = Capability(
        name="test.history",
        description="Test history",
        endpoint="https://api.example.com/test",
        method="GET",
        metadata={"source": "rest"}
    )
    
    executor.register(cap)
    
    # Execute multiple times
    executor.execute("test.history", {})
    executor.execute("test.history", {"param": "value"})
    
    history = executor.get_execution_history()
    assert len(history) == 2
    assert history[0]["capability"] == "test.history"


def test_graphql_execution():
    """Test executing GraphQL capabilities"""
    executor = CapabilityExecutor()
    
    cap = Capability(
        name="graphql.query",
        description="GraphQL query",
        endpoint="https://api.example.com/graphql",
        method="POST",
        parameters={
            "query": {"type": "string", "required": True}
        },
        metadata={"source": "graphql", "type": "query"}
    )
    
    executor.register(cap)
    result = executor.execute("graphql.query", {
        "query": "{ users { id name } }"
    })
    
    assert result["status"] == "success"
    assert result["type"] == "query"


if __name__ == "__main__":
    test_executor_initialization()
    test_capability_registration()
    test_execute_rest_capability()
    test_execute_with_params()
    test_required_params_validation()
    test_execution_history()
    test_graphql_execution()
    
    print("All executor tests passed!")
