"""
🤖 LLM Client - Production LLM integration
Supports both OpenAI (GPT-4o) and Anthropic (Claude 3.5 Sonnet)
"""

import os
from typing import List, Dict, Any, Optional
import asyncio

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

try:
    from anthropic import AsyncAnthropic
except ImportError:
    AsyncAnthropic = None


class LLMClient:
    """
    Production LLM integration with fallback support.
    
    Prioritizes OpenAI GPT-4o, falls back to Anthropic Claude 3.5 Sonnet.
    """
    
    def __init__(self):
        """Initialize LLM clients based on available API keys."""
        self.openai_client = None
        self.anthropic_client = None
        
        # Initialize OpenAI if API key available
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and AsyncOpenAI:
            try:
                self.openai_client = AsyncOpenAI(api_key=openai_key)
                print("🤖 OpenAI client initialized (GPT-4o)")
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {str(e)}")
        
        # Initialize Anthropic if API key available
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key and AsyncAnthropic:
            try:
                self.anthropic_client = AsyncAnthropic(api_key=anthropic_key)
                print("🤖 Anthropic client initialized (Claude 3.5 Sonnet)")
            except Exception as e:
                print(f"⚠️  Anthropic initialization failed: {str(e)}")
        
        if not self.openai_client and not self.anthropic_client:
            print("⚠️  No LLM clients available - using fallback mode")
    
    async def generate_hypotheses(
        self,
        objective: str,
        context: Dict[str, Any],
        max_hypotheses: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate workflow hypotheses for a given objective.
        
        Args:
            objective: The goal to achieve
            context: Relevant context information
            max_hypotheses: Maximum number of hypotheses to generate
        
        Returns:
            List of workflow hypotheses
        """
        print(f"🤖 Generating hypotheses for: {objective}")
        
        prompt = self._build_hypothesis_prompt(objective, context)
        
        try:
            # Try OpenAI first
            if self.openai_client:
                return await self._generate_with_openai(prompt, max_hypotheses)
            
            # Fallback to Anthropic
            elif self.anthropic_client:
                return await self._generate_with_anthropic(prompt, max_hypotheses)
            
            # Fallback to heuristics
            else:
                return self._generate_fallback_hypotheses(objective, context, max_hypotheses)
        
        except Exception as e:
            print(f"❌ LLM generation failed: {str(e)}")
            return self._generate_fallback_hypotheses(objective, context, max_hypotheses)
    
    async def judge_execution(
        self,
        hypothesis: Dict[str, Any],
        execution_log: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Judge a workflow execution using LLM.
        
        Args:
            hypothesis: The tested hypothesis
            execution_log: Log of execution steps
            context: Original context
        
        Returns:
            Judgment with scores and feedback
        """
        print(f"🤖 Judging execution: {hypothesis.get('name', 'Unnamed')}")
        
        prompt = self._build_judgment_prompt(hypothesis, execution_log, context)
        
        try:
            # Try OpenAI first
            if self.openai_client:
                return await self._judge_with_openai(prompt)
            
            # Fallback to Anthropic
            elif self.anthropic_client:
                return await self._judge_with_anthropic(prompt)
            
            # Fallback to heuristics (handled by SimulationLab)
            else:
                raise Exception("No LLM available for judgment")
        
        except Exception as e:
            print(f"❌ LLM judgment failed: {str(e)}")
            raise
    
    def _build_hypothesis_prompt(self, objective: str, context: Dict[str, Any]) -> str:
        """Build prompt for hypothesis generation."""
        return f"""You are an AI workflow architect. Generate workflow hypotheses to achieve the following objective.

Objective: {objective}

Context: {context}

Available tools:
- listen_to_rss(feed_url, keywords): Monitor RSS feeds
- extract_ogp_capabilities(url): Extract metadata from URLs
- search_internal_db(query, limit): Search knowledge base
- calculate_competitive_delta(current, benchmark): Analyze competitive advantage
- send_alert(message, channel, priority): Send notifications

Generate 1-3 workflow hypotheses as JSON array with this structure:
[{{
  "name": "Workflow name",
  "description": "What it does",
  "tool_sequence": [
    {{"tool": "tool_name", "params": {{"param": "value"}}}},
    ...
  ],
  "expected_outcome": "Expected result"
}}]

Focus on practical, actionable workflows that combine tools effectively."""
    
    def _build_judgment_prompt(
        self,
        hypothesis: Dict[str, Any],
        execution_log: List[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> str:
        """Build prompt for execution judgment."""
        return f"""You are an AI workflow judge. Evaluate this workflow execution.

Hypothesis: {hypothesis}

Execution Log: {execution_log}

Context: {context}

Rate the execution on these criteria (0-100 each):
1. Completeness (30%): Did all steps execute properly?
2. Relevance (40%): Does it address the objective effectively?
3. Actionability (30%): Does it produce useful, actionable results?

Respond with JSON:
{{
  "completeness_score": 0-100,
  "relevance_score": 0-100,
  "actionability_score": 0-100,
  "feedback": "Brief evaluation",
  "reasoning": "Detailed reasoning for scores"
}}"""
    
    async def _generate_with_openai(self, prompt: str, max_hypotheses: int) -> List[Dict[str, Any]]:
        """Generate hypotheses using OpenAI."""
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a workflow architect. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON response
        import json
        hypotheses = json.loads(content)
        return hypotheses[:max_hypotheses]
    
    async def _generate_with_anthropic(self, prompt: str, max_hypotheses: int) -> List[Dict[str, Any]]:
        """Generate hypotheses using Anthropic."""
        response = await self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        
        content = response.content[0].text
        
        # Parse JSON response
        import json
        hypotheses = json.loads(content)
        return hypotheses[:max_hypotheses]
    
    async def _judge_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Judge execution using OpenAI."""
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a workflow judge. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        
        content = response.choices[0].message.content
        
        # Parse JSON response
        import json
        return json.loads(content)
    
    async def _judge_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Judge execution using Anthropic."""
        response = await self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        
        content = response.content[0].text
        
        # Parse JSON response
        import json
        return json.loads(content)
    
    def _generate_fallback_hypotheses(
        self,
        objective: str,
        context: Dict[str, Any],
        max_hypotheses: int
    ) -> List[Dict[str, Any]]:
        """Generate simple hypotheses without LLM."""
        print("⚠️  Using fallback hypothesis generation")
        
        # Generate basic workflow based on keywords
        objective_lower = objective.lower()
        
        hypotheses = []
        
        # RSS monitoring workflow
        if any(kw in objective_lower for kw in ['monitor', 'watch', 'track', 'rss', 'feed']):
            hypotheses.append({
                'name': 'RSS Monitor Workflow',
                'description': 'Monitor RSS feed and send alerts',
                'tool_sequence': [
                    {'tool': 'listen_to_rss', 'params': {'feed_url': 'https://example.com/feed'}},
                    {'tool': 'send_alert', 'params': {'message': 'New items found'}},
                ],
                'expected_outcome': 'Alerts sent for new RSS items',
            })
        
        # Competitive analysis workflow
        if any(kw in objective_lower for kw in ['competitive', 'compare', 'analyze', 'benchmark']):
            hypotheses.append({
                'name': 'Competitive Analysis Workflow',
                'description': 'Analyze competitive landscape',
                'tool_sequence': [
                    {'tool': 'search_internal_db', 'params': {'query': 'competitors'}},
                    {'tool': 'calculate_competitive_delta', 'params': {}},
                    {'tool': 'send_alert', 'params': {'message': 'Analysis complete'}},
                ],
                'expected_outcome': 'Competitive analysis report',
            })
        
        # Generic search workflow
        if not hypotheses:
            hypotheses.append({
                'name': 'Information Gathering Workflow',
                'description': 'Search and alert on findings',
                'tool_sequence': [
                    {'tool': 'search_internal_db', 'params': {'query': objective}},
                    {'tool': 'send_alert', 'params': {'message': 'Search complete'}},
                ],
                'expected_outcome': 'Search results delivered',
            })
        
        return hypotheses[:max_hypotheses]
