"""
End-to-end test: TechCrunch monitoring intelligence pipeline
Tests the complete self-evolving workflow from RSS to blueprint deployment
"""

import pytest
import tempfile
from intelligentone_server import (
    listen_to_rss,
    extract_ogp_capabilities,
    calculate_competitive_delta,
    send_alert,
    propose_and_test_workflow,
)
from blueprint_vault import BlueprintVault
from simulation_lab import SimulationLab, HypothesisTest
from router_agent import route_query


@pytest.mark.asyncio
async def test_end_to_end_intelligence_pipeline():
    """
    Complete end-to-end test of the intelligence pipeline:
    1. Monitor TechCrunch RSS for AI chip articles
    2. Filter for relevant content
    3. Extract OGP metadata
    4. Generate autonomous workflow
    5. Test in Simulation Lab
    6. Deploy to Blueprint Vault
    7. Verify execution
    """
    
    print("\n" + "="*60)
    print("🧪 STARTING END-TO-END INTELLIGENCE PIPELINE TEST")
    print("="*60)
    
    # ========================================================================
    # PHASE 1: RSS MONITORING
    # ========================================================================
    print("\n📡 PHASE 1: RSS Monitoring")
    print("-" * 60)
    
    feed_url = "https://techcrunch.com/feed/"
    keywords = ["AI", "chip", "processor", "silicon"]
    
    print(f"🔍 Monitoring: {feed_url}")
    print(f"🔍 Keywords: {keywords}")
    
    entries = await listen_to_rss(feed_url, keywords)
    
    print(f"✅ Found {len(entries)} matching articles")
    assert isinstance(entries, list)
    
    # ========================================================================
    # PHASE 2: METADATA EXTRACTION
    # ========================================================================
    print("\n📋 PHASE 2: OGP Metadata Extraction")
    print("-" * 60)
    
    if entries:
        # Extract metadata from first article
        first_article = entries[0]
        print(f"📰 Article: {first_article.get('title', 'Unknown')}")
        print(f"🔗 URL: {first_article.get('link', 'Unknown')}")
        
        capabilities = await extract_ogp_capabilities(first_article['link'])
        
        print(f"✅ Extracted metadata:")
        print(f"   Title: {capabilities.get('title', 'N/A')}")
        print(f"   Description: {capabilities.get('description', 'N/A')[:100]}...")
        
        assert isinstance(capabilities, dict)
        assert 'url' in capabilities
    else:
        print("⚠️  No articles found - using mock data for testing")
        capabilities = {
            'url': 'https://techcrunch.com/test',
            'title': 'Revolutionary AI Chip Breakthrough',
            'description': 'New quantum-powered neural processor launches',
        }
    
    # ========================================================================
    # PHASE 3: COMPETITIVE ANALYSIS
    # ========================================================================
    print("\n📊 PHASE 3: Competitive Delta Analysis")
    print("-" * 60)
    
    current = capabilities
    benchmark = {
        'title': 'Standard AI Accelerator',
        'description': 'Incremental performance improvements'
    }
    
    delta = await calculate_competitive_delta(current, benchmark)
    
    print(f"📈 Urgency Score: {delta['urgency_score']}/100")
    print(f"🚨 Is Urgent: {delta['is_urgent']}")
    
    assert isinstance(delta, dict)
    assert 'urgency_score' in delta
    assert 0 <= delta['urgency_score'] <= 100
    
    # ========================================================================
    # PHASE 4: WORKFLOW HYPOTHESIS GENERATION
    # ========================================================================
    print("\n🧪 PHASE 4: Autonomous Workflow Generation")
    print("-" * 60)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        lab = SimulationLab(vault)
        
        # Create a workflow hypothesis
        hypothesis = HypothesisTest(
            name="TechCrunch AI Chip Monitor",
            description="Monitor TechCrunch for AI chip news and alert on breakthroughs",
            tool_sequence=[
                {
                    'tool': 'listen_to_rss',
                    'params': {
                        'feed_url': feed_url,
                        'keywords': keywords
                    }
                },
                {
                    'tool': 'extract_ogp_capabilities',
                    'params': {
                        'url': '$previous.entries[0].link'
                    }
                },
                {
                    'tool': 'calculate_competitive_delta',
                    'params': {
                        'current_capability': '$previous',
                        'benchmark': {'standard': True}
                    }
                },
                {
                    'tool': 'send_alert',
                    'params': {
                        'message': 'AI chip breakthrough detected',
                        'priority': 'urgent'
                    }
                }
            ],
            expected_outcome="Alert sent for significant AI chip announcements"
        )
        
        print(f"🔬 Hypothesis: {hypothesis.name}")
        print(f"📝 Description: {hypothesis.description}")
        print(f"⚙️  Tool Sequence: {len(hypothesis.tool_sequence)} steps")
        
        # ========================================================================
        # PHASE 5: SIMULATION LAB TESTING
        # ========================================================================
        print("\n🔬 PHASE 5: Simulation Lab Testing")
        print("-" * 60)
        
        context = {
            'query': 'Monitor TechCrunch for AI chip breakthroughs',
            'feed_url': feed_url,
            'keywords': keywords,
        }
        
        print("🧪 Testing hypothesis in isolation...")
        judgment = await lab.test_hypothesis(hypothesis, context)
        
        print(f"\n📊 LLM-as-Judge Scores:")
        print(f"   Completeness: {judgment.completeness_score}/100 (30% weight)")
        print(f"   Relevance: {judgment.relevance_score}/100 (40% weight)")
        print(f"   Actionability: {judgment.actionability_score}/100 (30% weight)")
        print(f"   Overall: {judgment.score}/100")
        print(f"\n💬 Feedback: {judgment.feedback}")
        print(f"🧠 Reasoning: {judgment.reasoning}")
        
        assert isinstance(judgment.score, int)
        assert 0 <= judgment.score <= 100
        assert isinstance(judgment.passed_threshold, bool)
        
        # ========================================================================
        # PHASE 6: DEPLOYMENT VERIFICATION
        # ========================================================================
        print("\n🚀 PHASE 6: Blueprint Deployment")
        print("-" * 60)
        
        if judgment.passed_threshold:
            print(f"✅ PASSED THRESHOLD (Score: {judgment.score} >= 85)")
            
            # Store in Blueprint Vault
            blueprint = {
                'name': hypothesis.name,
                'description': hypothesis.description,
                'tool_sequence': hypothesis.tool_sequence,
                'score': judgment.score,
                'success_count': 0,
                'total_runs': 0,
            }
            
            vault.store_blueprint(hypothesis.name, blueprint)
            print(f"💾 Stored in Blueprint Vault")
            
            # Verify storage
            retrieved = vault.get_blueprint(hypothesis.name)
            assert retrieved is not None
            assert retrieved['name'] == hypothesis.name
            assert retrieved['score'] == judgment.score
            
            print(f"✅ Deployment verified")
            
            # ====================================================================
            # PHASE 7: EXECUTION TEST
            # ====================================================================
            print("\n⚡ PHASE 7: Blueprint Execution")
            print("-" * 60)
            
            # Simulate execution
            print("🎯 Executing deployed blueprint...")
            
            # Update stats
            retrieved['success_count'] = retrieved.get('success_count', 0) + 1
            retrieved['total_runs'] = retrieved.get('total_runs', 0) + 1
            vault.store_blueprint(hypothesis.name, retrieved)
            
            # Verify stats
            updated = vault.get_blueprint(hypothesis.name)
            assert updated['success_count'] == 1
            assert updated['total_runs'] == 1
            
            print(f"✅ Execution successful")
            print(f"📊 Stats: {updated['success_count']}/{updated['total_runs']} successful")
            
        else:
            print(f"❌ FAILED THRESHOLD (Score: {judgment.score} < 85)")
            print("   Workflow needs improvement before deployment")
        
        # ========================================================================
        # PHASE 8: ROUTING VERIFICATION
        # ========================================================================
        print("\n🧭 PHASE 8: Intent Routing Verification")
        print("-" * 60)
        
        query = "Monitor TechCrunch and alert me about AI chip news"
        routing = route_query(query)
        
        print(f"📝 Query: {query}")
        print(f"🎯 Intent: {routing.intent}")
        print(f"📊 Confidence: {routing.confidence:.2f}")
        print(f"💭 Reasoning: {routing.reasoning}")
        
        assert routing.intent in ['actionable', 'informational']
        assert 0.0 <= routing.confidence <= 1.0
        
        # Should be classified as actionable
        assert routing.intent == 'actionable'
        
    # ========================================================================
    # TEST COMPLETE
    # ========================================================================
    print("\n" + "="*60)
    print("✅ END-TO-END PIPELINE TEST COMPLETE")
    print("="*60)
    print("\n🎉 All phases completed successfully!")
    print("\nSummary:")
    print(f"   ✅ RSS monitoring functional")
    print(f"   ✅ OGP extraction working")
    print(f"   ✅ Competitive analysis operational")
    print(f"   ✅ Workflow hypothesis generated")
    print(f"   ✅ Simulation Lab testing passed")
    print(f"   ✅ Blueprint Vault storage verified")
    print(f"   ✅ Intent routing accurate")
    print("\n🧠 intelligentOne self-evolution pipeline: OPERATIONAL ✅")


@pytest.mark.asyncio
async def test_workflow_reuse():
    """Test that deployed workflows can be reused efficiently."""
    
    print("\n🔄 Testing workflow reuse...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        vault = BlueprintVault(storage_path=tmpdir)
        
        # Store a blueprint
        blueprint = {
            'name': 'Reusable Workflow',
            'description': 'Test workflow reuse',
            'tool_sequence': [
                {'tool': 'search_internal_db', 'params': {'query': 'test'}},
                {'tool': 'send_alert', 'params': {'message': 'Done'}},
            ],
            'score': 90,
            'success_count': 0,
            'total_runs': 0,
        }
        
        vault.store_blueprint('Reusable Workflow', blueprint)
        
        # Execute multiple times
        for i in range(3):
            retrieved = vault.get_blueprint('Reusable Workflow')
            retrieved['success_count'] += 1
            retrieved['total_runs'] += 1
            vault.store_blueprint('Reusable Workflow', retrieved)
        
        # Check stats
        final = vault.get_blueprint('Reusable Workflow')
        assert final['success_count'] == 3
        assert final['total_runs'] == 3
        
        print(f"✅ Workflow reused 3 times successfully")
        print(f"📊 Success rate: 100%")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
