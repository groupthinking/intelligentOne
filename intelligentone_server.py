"""
🧠 intelligentOne MCP Server
Self-evolving autonomous intelligence platform with MCP-native architecture
"""

import asyncio
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
import feedparser

try:
    from fastmcp import FastMCP
except ImportError:
    # Fallback for testing without fastmcp
    class FastMCP:
        def __init__(self, name: str):
            self.name = name
            self.tools = []
        
        def tool(self):
            def decorator(func):
                self.tools.append(func)
                return func
            return decorator

from simulation_lab import SimulationLab, HypothesisTest
from blueprint_vault import BlueprintVault
from llm_client import LLMClient
from router_agent import route_query

# Initialize MCP server
mcp = FastMCP("intelligentOne")

# Initialize components
blueprint_vault = BlueprintVault()
simulation_lab = SimulationLab(blueprint_vault)
llm_client = LLMClient()

print("🧠 intelligentOne MCP Server initializing...")


# ============================================================================
# ATOMIC TOOLS - Core building blocks for workflows
# ============================================================================

@mcp.tool()
async def listen_to_rss(feed_url: str, keywords: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Monitor RSS feed and filter entries by keywords.
    
    Args:
        feed_url: URL of the RSS feed to monitor
        keywords: Optional list of keywords to filter entries (case-insensitive)
    
    Returns:
        List of feed entries matching the keywords
    """
    print(f"🔍 Listening to RSS feed: {feed_url}")
    
    try:
        feed = feedparser.parse(feed_url)
        entries = []
        
        for entry in feed.entries:
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            link = entry.get('link', '')
            
            # Filter by keywords if provided
            if keywords:
                text = f"{title} {summary}".lower()
                if any(keyword.lower() in text for keyword in keywords):
                    entries.append({
                        'title': title,
                        'summary': summary,
                        'link': link,
                        'published': entry.get('published', ''),
                    })
            else:
                entries.append({
                    'title': title,
                    'summary': summary,
                    'link': link,
                    'published': entry.get('published', ''),
                })
        
        print(f"✅ Found {len(entries)} matching entries")
        return entries
    
    except Exception as e:
        print(f"❌ Error listening to RSS: {str(e)}")
        return []


@mcp.tool()
async def extract_ogp_capabilities(url: str) -> Dict[str, Any]:
    """
    Extract Open Graph Protocol metadata from a URL to identify capabilities.
    
    Args:
        url: URL to extract OGP metadata from
    
    Returns:
        Dictionary containing OGP metadata and extracted capabilities
    """
    print(f"🔍 Extracting OGP capabilities from: {url}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract OGP metadata
        ogp_data = {}
        for tag in soup.find_all('meta', property=lambda x: x and x.startswith('og:')):
            property_name = tag.get('property', '').replace('og:', '')
            content = tag.get('content', '')
            if property_name and content:
                ogp_data[property_name] = content
        
        # Extract capabilities from description and title
        title = ogp_data.get('title', '')
        description = ogp_data.get('description', '')
        
        capabilities = {
            'url': url,
            'title': title,
            'description': description,
            'image': ogp_data.get('image', ''),
            'type': ogp_data.get('type', ''),
            'site_name': ogp_data.get('site_name', ''),
            'extracted_at': datetime.now().isoformat(),
        }
        
        print(f"✅ Extracted capabilities: {title}")
        return capabilities
    
    except Exception as e:
        print(f"❌ Error extracting OGP: {str(e)}")
        return {'url': url, 'error': str(e)}


@mcp.tool()
async def search_internal_db(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search internal knowledge base for relevant information.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
    
    Returns:
        List of search results
    """
    print(f"🔍 Searching internal DB: {query}")
    
    # For now, return blueprints that match the query
    blueprints = blueprint_vault.load_all_blueprints()
    matching = []
    
    query_lower = query.lower()
    for bp in blueprints:
        if (query_lower in bp.get('name', '').lower() or 
            query_lower in bp.get('description', '').lower()):
            matching.append(bp)
    
    results = matching[:limit]
    print(f"✅ Found {len(results)} matching results")
    return results


@mcp.tool()
async def calculate_competitive_delta(
    current_capability: Dict[str, Any],
    benchmark: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculate competitive advantage delta between current and benchmark capabilities.
    
    Args:
        current_capability: Current capability metrics
        benchmark: Benchmark capability metrics
    
    Returns:
        Delta analysis with urgency score
    """
    print(f"📊 Calculating competitive delta")
    
    # Simple scoring based on keyword presence and recency
    delta = {
        'current': current_capability.get('title', 'Unknown'),
        'benchmark': benchmark.get('title', 'Unknown'),
        'timestamp': datetime.now().isoformat(),
    }
    
    # Calculate urgency score (0-100)
    urgency_keywords = ['breakthrough', 'revolutionary', 'first', 'launch', 'announce', 'new']
    urgency_score = 0
    
    text = f"{current_capability.get('title', '')} {current_capability.get('description', '')}".lower()
    for keyword in urgency_keywords:
        if keyword in text:
            urgency_score += 20
    
    delta['urgency_score'] = min(urgency_score, 100)
    delta['is_urgent'] = urgency_score >= 60
    
    print(f"✅ Urgency score: {delta['urgency_score']}")
    return delta


@mcp.tool()
async def send_alert(
    message: str,
    channel: str = "console",
    priority: str = "normal"
) -> Dict[str, Any]:
    """
    Send alert to specified channel.
    
    Args:
        message: Alert message
        channel: Destination channel (console, slack, email)
        priority: Priority level (low, normal, high, urgent)
    
    Returns:
        Alert delivery status
    """
    print(f"🚨 ALERT [{priority.upper()}]: {message}")
    
    # For now, just log to console
    # In production, integrate with Slack/email
    return {
        'status': 'sent',
        'message': message,
        'channel': channel,
        'priority': priority,
        'timestamp': datetime.now().isoformat(),
    }


# ============================================================================
# EVOLUTIONARY ENGINE - Self-improvement core
# ============================================================================

async def propose_and_test_workflow(
    objective: str,
    context: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Generate and test a new workflow hypothesis using LLM.
    
    This is the core self-evolution mechanism:
    1. LLM generates workflow hypothesis
    2. SimulationLab tests it in isolation
    3. If score >= 85, auto-deploy to BlueprintVault
    
    Args:
        objective: The goal to achieve
        context: Relevant context information
    
    Returns:
        Deployed blueprint if successful, None otherwise
    """
    print(f"🧪 Proposing workflow for: {objective}")
    
    try:
        # Generate hypothesis using LLM
        hypotheses = await llm_client.generate_hypotheses(objective, context)
        
        if not hypotheses:
            print("❌ No hypotheses generated")
            return None
        
        # Test each hypothesis
        for hypothesis in hypotheses:
            print(f"🧪 Testing hypothesis: {hypothesis.get('name', 'Unnamed')}")
            
            test = HypothesisTest(
                name=hypothesis.get('name', 'Unnamed Workflow'),
                description=hypothesis.get('description', ''),
                tool_sequence=hypothesis.get('tool_sequence', []),
                expected_outcome=hypothesis.get('expected_outcome', ''),
            )
            
            # Execute in simulation lab
            result = await simulation_lab.test_hypothesis(test, context)
            
            print(f"📊 Score: {result.score}/100 (threshold: 85)")
            
            # Auto-deploy if score >= 85
            if result.score >= 85:
                blueprint = {
                    'name': test.name,
                    'description': test.description,
                    'tool_sequence': test.tool_sequence,
                    'score': result.score,
                    'created_at': datetime.now().isoformat(),
                    'success_count': 0,
                    'total_runs': 0,
                }
                
                blueprint_vault.store_blueprint(test.name, blueprint)
                print(f"✅ DEPLOYED: {test.name} (score: {result.score})")
                return blueprint
        
        print("❌ No hypothesis met deployment threshold")
        return None
    
    except Exception as e:
        print(f"❌ Error in workflow evolution: {str(e)}")
        return None


# ============================================================================
# DYNAMIC COMPOSITE TOOL LOADER
# ============================================================================

def load_composite_tools():
    """
    Load composite tools from BlueprintVault and register them dynamically.
    This enables hot-reload of evolved workflows.
    """
    print("🔄 Loading composite tools from Blueprint Vault...")
    
    blueprints = blueprint_vault.load_all_blueprints()
    print(f"✅ Loaded {len(blueprints)} blueprints")
    
    # In production, dynamically register blueprints as MCP tools
    # For now, they're available via execute_blueprint()
    return blueprints


@mcp.tool()
async def execute_blueprint(
    blueprint_name: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute a deployed blueprint workflow.
    
    Args:
        blueprint_name: Name of the blueprint to execute
        context: Execution context
    
    Returns:
        Execution result
    """
    print(f"🚀 Executing blueprint: {blueprint_name}")
    
    blueprint = blueprint_vault.get_blueprint(blueprint_name)
    if not blueprint:
        return {'error': f'Blueprint not found: {blueprint_name}'}
    
    try:
        # Execute tool sequence
        results = []
        for tool_call in blueprint['tool_sequence']:
            tool_name = tool_call.get('tool', '')
            params = tool_call.get('params', {})
            
            # Execute tool (simplified - in production, use proper tool registry)
            print(f"  ⚙️  Executing: {tool_name}")
            results.append({'tool': tool_name, 'status': 'executed'})
        
        # Update blueprint stats
        blueprint['success_count'] = blueprint.get('success_count', 0) + 1
        blueprint['total_runs'] = blueprint.get('total_runs', 0) + 1
        blueprint_vault.store_blueprint(blueprint_name, blueprint)
        
        print(f"✅ Blueprint executed successfully")
        return {
            'status': 'success',
            'blueprint': blueprint_name,
            'results': results,
        }
    
    except Exception as e:
        print(f"❌ Blueprint execution failed: {str(e)}")
        blueprint['total_runs'] = blueprint.get('total_runs', 0) + 1
        blueprint_vault.store_blueprint(blueprint_name, blueprint)
        return {'error': str(e)}


# ============================================================================
# MAIN QUERY HANDLER
# ============================================================================

@mcp.tool()
async def process_query(query: str) -> Dict[str, Any]:
    """
    Main entry point - routes query and potentially evolves new workflows.
    
    Args:
        query: User query or objective
    
    Returns:
        Processing result with potential new workflow deployment
    """
    print(f"🧠 Processing query: {query}")
    
    # Route query to determine intent
    routing = route_query(query)
    print(f"📍 Routing: {routing.intent} (confidence: {routing.confidence})")
    
    # Check if existing blueprint can handle this
    matching_blueprints = await search_internal_db(query, limit=3)
    
    if matching_blueprints:
        print(f"✅ Found {len(matching_blueprints)} matching blueprints")
        # Execute best matching blueprint
        best = matching_blueprints[0]
        return await execute_blueprint(best['name'], {'query': query})
    
    # No existing blueprint - evolve new workflow
    print("🧪 No matching blueprint - evolving new workflow...")
    new_blueprint = await propose_and_test_workflow(
        objective=query,
        context={'routing': routing.__dict__}
    )
    
    if new_blueprint:
        return {
            'status': 'evolved',
            'blueprint': new_blueprint,
            'message': f"Created and deployed new workflow: {new_blueprint['name']}"
        }
    
    return {
        'status': 'failed',
        'message': 'Could not create workflow for this query'
    }


# ============================================================================
# SERVER INITIALIZATION
# ============================================================================

if __name__ == "__main__":
    print("🧠 intelligentOne MCP Server started")
    print("=" * 50)
    print("Self-evolving autonomous intelligence platform")
    print("Atomic Tools: listen_to_rss, extract_ogp_capabilities, search_internal_db")
    print("              calculate_competitive_delta, send_alert")
    print("Composite Tools: execute_blueprint, process_query")
    print("Evolutionary: propose_and_test_workflow")
    print("=" * 50)
    
    # Load existing blueprints
    load_composite_tools()
    
    # Run server (fastmcp handles this in production)
    print("✅ Server ready for MCP connections")
