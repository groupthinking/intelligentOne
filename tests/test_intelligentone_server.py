"""
Unit tests for intelligentOne MCP server
"""

import pytest
import asyncio
from intelligentone_server import (
    listen_to_rss,
    extract_ogp_capabilities,
    calculate_competitive_delta,
    search_internal_db,
    send_alert,
)


@pytest.mark.asyncio
async def test_imports():
    """Test that all core modules can be imported."""
    try:
        from simulation_lab import SimulationLab, HypothesisTest, JudgmentResult
        from blueprint_vault import BlueprintVault
        from llm_client import LLMClient
        from router_agent import route_query, RoutingDecision
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {str(e)}")


@pytest.mark.asyncio
async def test_rss_listener():
    """Test RSS feed monitoring."""
    # Test with a known RSS feed
    entries = await listen_to_rss(
        "https://techcrunch.com/feed/",
        keywords=["technology"]
    )
    
    # Should return a list (may be empty if feed is down)
    assert isinstance(entries, list)
    
    # If entries found, validate structure
    if entries:
        assert 'title' in entries[0]
        assert 'link' in entries[0]


@pytest.mark.asyncio
async def test_ogp_extraction():
    """Test Open Graph Protocol metadata extraction."""
    # Test with a known URL (TechCrunch homepage)
    result = await extract_ogp_capabilities("https://techcrunch.com")
    
    # Should return a dictionary
    assert isinstance(result, dict)
    assert 'url' in result
    
    # Should have either valid data or error
    if 'error' not in result:
        # Valid extraction should have metadata
        assert 'title' in result or 'description' in result


@pytest.mark.asyncio
async def test_competitive_delta_urgent():
    """Test competitive delta calculation with urgent signals."""
    current = {
        'title': 'Revolutionary AI Chip Breakthrough Announced',
        'description': 'First quantum-powered neural processor launches today'
    }
    
    benchmark = {
        'title': 'Standard AI Chip',
        'description': 'Regular performance improvements'
    }
    
    delta = await calculate_competitive_delta(current, benchmark)
    
    # Should return analysis
    assert isinstance(delta, dict)
    assert 'urgency_score' in delta
    assert 'is_urgent' in delta
    
    # Should detect urgency keywords
    assert delta['urgency_score'] > 0
    assert delta['urgency_score'] <= 100


@pytest.mark.asyncio
async def test_competitive_delta_normal():
    """Test competitive delta calculation without urgent signals."""
    current = {
        'title': 'Regular Product Update',
        'description': 'Minor improvements to existing features'
    }
    
    benchmark = {
        'title': 'Standard Product',
        'description': 'Standard features'
    }
    
    delta = await calculate_competitive_delta(current, benchmark)
    
    # Should return analysis
    assert isinstance(delta, dict)
    assert 'urgency_score' in delta
    
    # Should have lower urgency
    assert delta['urgency_score'] <= 40


@pytest.mark.asyncio
async def test_search_internal_db():
    """Test internal database search."""
    # Search for anything
    results = await search_internal_db("test", limit=5)
    
    # Should return a list
    assert isinstance(results, list)
    assert len(results) <= 5


@pytest.mark.asyncio
async def test_send_alert():
    """Test alert sending."""
    result = await send_alert(
        message="Test alert",
        channel="console",
        priority="normal"
    )
    
    # Should return status
    assert isinstance(result, dict)
    assert result['status'] == 'sent'
    assert result['message'] == "Test alert"
    assert result['channel'] == "console"
    assert result['priority'] == "normal"


@pytest.mark.asyncio
async def test_send_alert_urgent():
    """Test urgent alert."""
    result = await send_alert(
        message="Urgent test",
        priority="urgent"
    )
    
    assert result['priority'] == "urgent"


def test_router_agent():
    """Test query routing."""
    from router_agent import route_query
    
    # Test actionable intent
    routing = route_query("Monitor TechCrunch and alert me")
    assert routing.intent == 'actionable'
    assert routing.confidence > 0.5
    
    # Test informational intent
    routing = route_query("What is artificial intelligence?")
    assert routing.intent == 'informational'
    assert routing.confidence > 0.5


def test_blueprint_vault():
    """Test blueprint storage and retrieval."""
    from blueprint_vault import BlueprintVault
    import tempfile
    import os
    
    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        
        # Store a test blueprint
        blueprint = {
            'name': 'Test Workflow',
            'description': 'A test workflow',
            'tool_sequence': [
                {'tool': 'search_internal_db', 'params': {'query': 'test'}}
            ],
            'score': 90,
        }
        
        success = vault.store_blueprint('Test Workflow', blueprint)
        assert success is True
        
        # Retrieve the blueprint
        retrieved = vault.get_blueprint('Test Workflow')
        assert retrieved is not None
        assert retrieved['name'] == 'Test Workflow'
        assert retrieved['score'] == 90
        
        # Load all blueprints
        all_blueprints = vault.load_all_blueprints()
        assert len(all_blueprints) == 1
        assert all_blueprints[0]['name'] == 'Test Workflow'
        
        # Get stats
        stats = vault.get_stats()
        assert stats['total_blueprints'] == 1
        
        # Delete blueprint
        deleted = vault.delete_blueprint('Test Workflow')
        assert deleted is True
        
        # Verify deletion
        retrieved = vault.get_blueprint('Test Workflow')
        assert retrieved is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
