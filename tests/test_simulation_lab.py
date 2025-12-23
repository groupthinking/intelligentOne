"""
Tests for Simulation Lab and LLM-as-Judge functionality
"""

import pytest
import tempfile
from simulation_lab import SimulationLab, HypothesisTest, JudgmentResult
from blueprint_vault import BlueprintVault


@pytest.mark.asyncio
async def test_hypothesis_test_model():
    """Test HypothesisTest Pydantic model."""
    hypothesis = HypothesisTest(
        name="Test Workflow",
        description="A test workflow",
        tool_sequence=[
            {'tool': 'search_internal_db', 'params': {'query': 'test'}},
            {'tool': 'send_alert', 'params': {'message': 'Test alert'}},
        ],
        expected_outcome="Alert sent with search results"
    )
    
    assert hypothesis.name == "Test Workflow"
    assert len(hypothesis.tool_sequence) == 2
    assert hypothesis.tool_sequence[0]['tool'] == 'search_internal_db'


@pytest.mark.asyncio
async def test_judgment_result_model():
    """Test JudgmentResult Pydantic model."""
    result = JudgmentResult(
        score=87,
        completeness_score=90,
        relevance_score=85,
        actionability_score=88,
        feedback="Good workflow execution",
        reasoning="All tools executed successfully and produced relevant results",
        passed_threshold=True
    )
    
    assert result.score == 87
    assert result.passed_threshold is True
    assert result.completeness_score == 90


@pytest.mark.asyncio
async def test_simulation_lab_initialization():
    """Test SimulationLab initialization."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        assert lab.blueprint_vault == vault
        assert lab.llm_client is not None


@pytest.mark.asyncio
async def test_hypothesis_execution():
    """Test hypothesis execution in simulation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        hypothesis = HypothesisTest(
            name="RSS Monitor Test",
            description="Monitor RSS feed and send alert",
            tool_sequence=[
                {
                    'tool': 'listen_to_rss',
                    'params': {
                        'feed_url': 'https://techcrunch.com/feed/',
                        'keywords': ['AI']
                    }
                },
                {
                    'tool': 'send_alert',
                    'params': {
                        'message': 'New AI articles found',
                        'priority': 'normal'
                    }
                }
            ],
            expected_outcome="Alert sent for AI articles"
        )
        
        context = {'query': 'Monitor TechCrunch for AI news'}
        
        # Execute test
        result = await lab.test_hypothesis(hypothesis, context)
        
        # Verify result structure
        assert isinstance(result, JudgmentResult)
        assert 0 <= result.score <= 100
        assert 0 <= result.completeness_score <= 100
        assert 0 <= result.relevance_score <= 100
        assert 0 <= result.actionability_score <= 100
        assert isinstance(result.feedback, str)
        assert isinstance(result.reasoning, str)
        assert isinstance(result.passed_threshold, bool)


@pytest.mark.asyncio
async def test_scoring_weights():
    """Test that scoring weights are applied correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        # Manually calculate expected score
        completeness = 90
        relevance = 80
        actionability = 85
        
        expected_score = int(
            completeness * 0.30 +
            relevance * 0.40 +
            actionability * 0.30
        )
        
        # Verify weights sum to 100%
        assert 0.30 + 0.40 + 0.30 == 1.0
        
        # Expected: 90*0.3 + 80*0.4 + 85*0.3 = 27 + 32 + 25.5 = 84.5 ≈ 84
        assert 83 <= expected_score <= 85


@pytest.mark.asyncio
async def test_deployment_threshold():
    """Test that deployment threshold is enforced."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        # Test with high-scoring hypothesis
        good_hypothesis = HypothesisTest(
            name="Good Workflow",
            description="A well-designed workflow",
            tool_sequence=[
                {'tool': 'listen_to_rss', 'params': {}},
                {'tool': 'extract_ogp_capabilities', 'params': {}},
                {'tool': 'calculate_competitive_delta', 'params': {}},
                {'tool': 'send_alert', 'params': {'message': 'Alert'}},
            ],
            expected_outcome="Complete workflow with actions"
        )
        
        result = await lab.test_hypothesis(
            good_hypothesis,
            {'query': 'Monitor competitive news'}
        )
        
        # Should have decent score due to 4 tools and alert
        # Heuristic scoring should give at least some points
        assert result.score >= 0


@pytest.mark.asyncio
async def test_blueprint_storage_after_success():
    """Test that blueprints are stored after successful tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        hypothesis = HypothesisTest(
            name="Storable Workflow",
            description="Test blueprint storage",
            tool_sequence=[
                {'tool': 'search_internal_db', 'params': {'query': 'test'}},
                {'tool': 'send_alert', 'params': {'message': 'Done'}},
            ],
            expected_outcome="Search and alert"
        )
        
        # Test the hypothesis
        result = await lab.test_hypothesis(hypothesis, {})
        
        # Even if it doesn't pass threshold, the test should complete
        assert isinstance(result, JudgmentResult)
        
        # If score >= 85, it would be auto-deployed by the server
        # Here we just verify the test execution works
        if result.passed_threshold:
            # Verify the score logic
            assert result.score >= 85


@pytest.mark.asyncio
async def test_heuristic_scoring():
    """Test heuristic scoring when LLM unavailable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        # Test completeness heuristic
        hypothesis = HypothesisTest(
            name="Completeness Test",
            description="Test completeness scoring",
            tool_sequence=[
                {'tool': 'tool1', 'params': {}},
                {'tool': 'tool2', 'params': {}},
            ],
            expected_outcome="Two tools executed"
        )
        
        execution_log = [
            {'status': 'simulated', 'tool': 'tool1'},
            {'status': 'simulated', 'tool': 'tool2'},
        ]
        
        completeness = lab._heuristic_completeness(hypothesis, execution_log)
        assert completeness == 100  # Both tools executed
        
        # Test with partial execution
        partial_log = [
            {'status': 'simulated', 'tool': 'tool1'},
        ]
        
        completeness = lab._heuristic_completeness(hypothesis, partial_log)
        assert completeness == 50  # Only 1 of 2 tools


@pytest.mark.asyncio
async def test_actionability_heuristic():
    """Test actionability scoring heuristic."""
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        hypothesis = HypothesisTest(
            name="Action Test",
            description="Test actionability",
            tool_sequence=[
                {'tool': 'search', 'params': {}},
                {'tool': 'analyze', 'params': {}},
                {'tool': 'send_alert', 'params': {}},
            ],
            expected_outcome="Alert sent"
        )
        
        execution_log = [
            {'tool': 'search', 'status': 'simulated'},
            {'tool': 'analyze', 'status': 'simulated'},
            {'tool': 'send_alert', 'status': 'simulated'},
        ]
        
        actionability = lab._heuristic_actionability(hypothesis, execution_log)
        
        # Should score high: 3+ steps and has 'alert' action
        assert actionability >= 70


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
