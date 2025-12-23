"""
🧪 Simulation Lab - LLM-as-Judge execution engine
Tests workflow hypotheses in isolation before deployment
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from llm_client import LLMClient


class HypothesisTest(BaseModel):
    """A workflow hypothesis to be tested."""
    name: str = Field(description="Name of the workflow hypothesis")
    description: str = Field(description="What this workflow aims to achieve")
    tool_sequence: List[Dict[str, Any]] = Field(description="Sequence of tools to execute")
    expected_outcome: str = Field(description="Expected result of execution")


class JudgmentResult(BaseModel):
    """Result of LLM-based judgment of workflow execution."""
    score: int = Field(ge=0, le=100, description="Overall score (0-100)")
    completeness_score: int = Field(ge=0, le=100, description="Completeness score")
    relevance_score: int = Field(ge=0, le=100, description="Relevance score")
    actionability_score: int = Field(ge=0, le=100, description="Actionability score")
    feedback: str = Field(description="Detailed feedback from judge")
    reasoning: str = Field(description="Reasoning for the scores")
    passed_threshold: bool = Field(description="Whether score >= 85")


class SimulationLab:
    """
    Execution engine that tests workflow hypotheses using LLM-as-Judge.
    
    Scoring breakdown:
    - Completeness: 30%
    - Relevance: 40%
    - Actionability: 30%
    
    Deployment threshold: 85+
    """
    
    def __init__(self, blueprint_vault):
        """
        Initialize the simulation lab.
        
        Args:
            blueprint_vault: Reference to BlueprintVault for storing successful tests
        """
        self.blueprint_vault = blueprint_vault
        self.llm_client = LLMClient()
        print("🧪 SIMULATION LAB initialized")
    
    async def test_hypothesis(
        self,
        hypothesis: HypothesisTest,
        context: Dict[str, Any]
    ) -> JudgmentResult:
        """
        Execute and judge a workflow hypothesis.
        
        Args:
            hypothesis: The workflow hypothesis to test
            context: Execution context and inputs
        
        Returns:
            JudgmentResult with scores and feedback
        """
        print(f"🧪 SIMULATION LAB: Testing '{hypothesis.name}'")
        print(f"   Description: {hypothesis.description}")
        print(f"   Tool sequence: {len(hypothesis.tool_sequence)} tools")
        
        try:
            # Simulate execution of tool sequence
            execution_log = await self._simulate_execution(hypothesis, context)
            
            # Judge the execution using LLM
            judgment = await self._judge_execution(hypothesis, execution_log, context)
            
            print(f"📊 JUDGMENT:")
            print(f"   Completeness: {judgment.completeness_score}/100 (30% weight)")
            print(f"   Relevance: {judgment.relevance_score}/100 (40% weight)")
            print(f"   Actionability: {judgment.actionability_score}/100 (30% weight)")
            print(f"   Overall Score: {judgment.score}/100")
            print(f"   Threshold: {'✅ PASSED' if judgment.passed_threshold else '❌ FAILED'}")
            
            return judgment
        
        except Exception as e:
            print(f"❌ Error in simulation: {str(e)}")
            # Return failed judgment
            return JudgmentResult(
                score=0,
                completeness_score=0,
                relevance_score=0,
                actionability_score=0,
                feedback=f"Simulation failed: {str(e)}",
                reasoning="Error during execution",
                passed_threshold=False,
            )
    
    async def _simulate_execution(
        self,
        hypothesis: HypothesisTest,
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Simulate execution of tool sequence in isolation.
        
        Args:
            hypothesis: The hypothesis to execute
            context: Execution context
        
        Returns:
            Execution log with results from each tool
        """
        print("   🔧 Simulating tool execution...")
        
        execution_log = []
        
        for i, tool_call in enumerate(hypothesis.tool_sequence):
            tool_name = tool_call.get('tool', 'unknown')
            params = tool_call.get('params', {})
            
            print(f"      [{i+1}/{len(hypothesis.tool_sequence)}] {tool_name}")
            
            # Simulate tool execution (in production, actually call tools)
            step_result = {
                'step': i + 1,
                'tool': tool_name,
                'params': params,
                'status': 'simulated',
                'timestamp': datetime.now().isoformat(),
            }
            
            # Add simulated output based on tool type
            if 'rss' in tool_name.lower():
                step_result['output'] = {'entries': [], 'count': 0}
            elif 'ogp' in tool_name.lower():
                step_result['output'] = {'capabilities': {}, 'extracted': True}
            elif 'search' in tool_name.lower():
                step_result['output'] = {'results': [], 'count': 0}
            elif 'alert' in tool_name.lower():
                step_result['output'] = {'status': 'sent', 'channel': 'console'}
            else:
                step_result['output'] = {'result': 'simulated'}
            
            execution_log.append(step_result)
        
        print(f"   ✅ Simulation complete: {len(execution_log)} steps")
        return execution_log
    
    async def _judge_execution(
        self,
        hypothesis: HypothesisTest,
        execution_log: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> JudgmentResult:
        """
        Use LLM to judge the quality of the execution.
        
        Args:
            hypothesis: The tested hypothesis
            execution_log: Log of execution steps
            context: Original context
        
        Returns:
            JudgmentResult with scores and feedback
        """
        print("   🤖 LLM-as-Judge evaluating...")
        
        try:
            # Call LLM for judgment
            judgment_data = await self.llm_client.judge_execution(
                hypothesis=hypothesis.dict(),
                execution_log=execution_log,
                context=context,
            )
            
            # Calculate weighted score
            completeness = judgment_data.get('completeness_score', 50)
            relevance = judgment_data.get('relevance_score', 50)
            actionability = judgment_data.get('actionability_score', 50)
            
            overall_score = int(
                completeness * 0.30 +
                relevance * 0.40 +
                actionability * 0.30
            )
            
            return JudgmentResult(
                score=overall_score,
                completeness_score=completeness,
                relevance_score=relevance,
                actionability_score=actionability,
                feedback=judgment_data.get('feedback', 'No feedback provided'),
                reasoning=judgment_data.get('reasoning', 'No reasoning provided'),
                passed_threshold=overall_score >= 85,
            )
        
        except Exception as e:
            print(f"   ⚠️  LLM judgment failed, using heuristics: {str(e)}")
            
            # Fallback to heuristic scoring
            completeness = self._heuristic_completeness(hypothesis, execution_log)
            relevance = self._heuristic_relevance(hypothesis, context)
            actionability = self._heuristic_actionability(hypothesis, execution_log)
            
            overall_score = int(
                completeness * 0.30 +
                relevance * 0.40 +
                actionability * 0.30
            )
            
            return JudgmentResult(
                score=overall_score,
                completeness_score=completeness,
                relevance_score=relevance,
                actionability_score=actionability,
                feedback="Heuristic evaluation (LLM unavailable)",
                reasoning="Used heuristic scoring based on workflow structure",
                passed_threshold=overall_score >= 85,
            )
    
    def _heuristic_completeness(
        self,
        hypothesis: HypothesisTest,
        execution_log: List[Dict[str, Any]]
    ) -> int:
        """Heuristic scoring for completeness."""
        # Check if all tools executed
        expected_steps = len(hypothesis.tool_sequence)
        completed_steps = len([s for s in execution_log if s.get('status') in ['simulated', 'success']])
        
        if expected_steps == 0:
            return 0
        
        return int((completed_steps / expected_steps) * 100)
    
    def _heuristic_relevance(
        self,
        hypothesis: HypothesisTest,
        context: Dict[str, Any]
    ) -> int:
        """Heuristic scoring for relevance."""
        # Simple keyword matching between hypothesis and context
        hypothesis_text = f"{hypothesis.name} {hypothesis.description}".lower()
        context_text = str(context).lower()
        
        # Count common meaningful words
        hypothesis_words = set(hypothesis_text.split())
        context_words = set(context_text.split())
        common = hypothesis_words & context_words
        
        if not hypothesis_words:
            return 50
        
        relevance = (len(common) / len(hypothesis_words)) * 100
        return min(int(relevance), 100)
    
    def _heuristic_actionability(
        self,
        hypothesis: HypothesisTest,
        execution_log: List[Dict[str, Any]]
    ) -> int:
        """Heuristic scoring for actionability."""
        # Check if workflow has alert/action steps
        action_keywords = ['alert', 'send', 'notify', 'execute', 'deploy']
        
        has_actions = any(
            any(keyword in step.get('tool', '').lower() for keyword in action_keywords)
            for step in execution_log
        )
        
        # Workflows with 3+ steps and actions score higher
        if len(execution_log) >= 3 and has_actions:
            return 85
        elif has_actions:
            return 70
        elif len(execution_log) >= 3:
            return 60
        else:
            return 40
