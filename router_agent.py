"""
🧭 Router Agent - Intent classification
Routes queries to appropriate handling based on intent
"""

from typing import Optional
from pydantic import BaseModel


class RoutingDecision(BaseModel):
    """Result of query routing."""
    intent: str  # 'informational' or 'actionable'
    confidence: float  # 0.0 to 1.0
    reasoning: str


def route_query(query: str) -> RoutingDecision:
    """
    Classify query intent using keyword-based heuristics.
    
    Args:
        query: User query to classify
    
    Returns:
        RoutingDecision with intent classification
    """
    query_lower = query.lower()
    
    # Actionable keywords
    actionable_keywords = [
        'monitor', 'watch', 'track', 'alert', 'notify',
        'send', 'create', 'build', 'deploy', 'execute',
        'analyze', 'compare', 'calculate', 'process',
        'automate', 'schedule', 'trigger'
    ]
    
    # Informational keywords
    informational_keywords = [
        'what', 'how', 'why', 'when', 'where', 'who',
        'explain', 'describe', 'tell me', 'show me',
        'find', 'search', 'lookup', 'get', 'list'
    ]
    
    # Count keyword matches
    actionable_count = sum(1 for kw in actionable_keywords if kw in query_lower)
    informational_count = sum(1 for kw in informational_keywords if kw in query_lower)
    
    # Determine intent
    if actionable_count > informational_count:
        intent = 'actionable'
        confidence = min(0.6 + (actionable_count * 0.1), 0.95)
        reasoning = f"Query contains {actionable_count} actionable keywords"
    elif informational_count > actionable_count:
        intent = 'informational'
        confidence = min(0.6 + (informational_count * 0.1), 0.95)
        reasoning = f"Query contains {informational_count} informational keywords"
    else:
        # Default to informational with lower confidence
        intent = 'informational'
        confidence = 0.5
        reasoning = "No clear intent signals, defaulting to informational"
    
    return RoutingDecision(
        intent=intent,
        confidence=confidence,
        reasoning=reasoning
    )
