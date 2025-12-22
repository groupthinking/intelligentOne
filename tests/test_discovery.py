"""
Tests for capability discovery
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone.discovery import CapabilityDiscovery


def test_discovery_initialization():
    """Test CapabilityDiscovery initialization"""
    discovery = CapabilityDiscovery()
    assert discovery is not None
    assert "rest" in discovery.adapters
    assert "openapi" in discovery.adapters
    assert "graphql" in discovery.adapters


def test_rest_discovery():
    """Test REST API discovery"""
    discovery = CapabilityDiscovery()
    
    capabilities = discovery.discover("https://api.example.com", "rest")
    
    assert len(capabilities) > 0
    assert all(hasattr(cap, 'name') for cap in capabilities)
    assert all(hasattr(cap, 'endpoint') for cap in capabilities)


def test_openapi_discovery():
    """Test OpenAPI discovery"""
    discovery = CapabilityDiscovery()
    
    capabilities = discovery.discover("https://api.example.com/swagger.json", "openapi")
    
    assert len(capabilities) > 0
    
    # Check metadata
    for cap in capabilities:
        assert cap.metadata["source"] == "openapi"


def test_graphql_discovery():
    """Test GraphQL discovery"""
    discovery = CapabilityDiscovery()
    
    capabilities = discovery.discover("https://api.example.com/graphql", "graphql")
    
    assert len(capabilities) > 0
    
    # Should have query and mutation capabilities
    cap_names = [cap.name for cap in capabilities]
    assert "graphql.query" in cap_names
    assert "graphql.mutation" in cap_names


def test_html_discovery():
    """Test HTML discovery"""
    discovery = CapabilityDiscovery()
    
    capabilities = discovery.discover("https://example.com", "html")
    
    assert len(capabilities) > 0


if __name__ == "__main__":
    test_discovery_initialization()
    test_rest_discovery()
    test_openapi_discovery()
    test_graphql_discovery()
    test_html_discovery()
    
    print("All discovery tests passed!")
