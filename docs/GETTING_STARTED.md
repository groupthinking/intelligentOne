# Getting Started with intelligentOne

Welcome to intelligentOne—the world's first self-evolving autonomous intelligence platform! This guide will walk you through installation, configuration, and your first workflow evolution.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** installed
- **pip** package manager
- **Git** for cloning the repository
- **API key** for OpenAI (GPT-4o) or Anthropic (Claude 3.5 Sonnet)
- **Claude Desktop** (optional but recommended for best experience)

## Step 1: Installation

### Clone the Repository

```bash
git clone https://github.com/groupthinking/intelligentOne.git
cd intelligentOne
```

### Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- MCP framework (fastmcp)
- LLM clients (openai, anthropic)
- Web tools (httpx, beautifulsoup4, feedparser)
- Data validation (pydantic)
- Testing tools (pytest)

### Verify Installation

```bash
python -c "import fastmcp; import openai; import anthropic; print('✅ All dependencies installed!')"
```

## Step 2: Configuration

### Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your favorite text editor:
```bash
nano .env  # or vim, code, etc.
```

3. Add at least one API key:
```bash
# LLM API Keys (at least one required)
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Server Configuration
PORT=8080
ENVIRONMENT=development

# Blueprint Storage
BLUEPRINT_STORAGE_PATH=./blueprints

# Optional Integrations
SLACK_WEBHOOK_URL=
DATABASE_URL=
```

### Verify Configuration

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('OpenAI:', '✅' if os.getenv('OPENAI_API_KEY') else '❌'); print('Anthropic:', '✅' if os.getenv('ANTHROPIC_API_KEY') else '❌')"
```

## Step 3: First Workflow Test

### Option A: Run Standalone Server

Start the MCP server:
```bash
python intelligentone_server.py
```

You should see:
```
🧠 intelligentOne MCP Server initializing...
💾 Blueprint Vault initialized: ./blueprints
🤖 OpenAI client initialized (GPT-4o)
🧪 SIMULATION LAB initialized
🧠 intelligentOne MCP Server started
==================================================
Self-evolving autonomous intelligence platform
Atomic Tools: listen_to_rss, extract_ogp_capabilities, search_internal_db
              calculate_competitive_delta, send_alert
Composite Tools: execute_blueprint, process_query
Evolutionary: propose_and_test_workflow
==================================================
✅ Server ready for MCP connections
```

### Option B: Test with Python (Without MCP)

Create a test script `test_workflow.py`:

```python
import asyncio
from intelligentone_server import listen_to_rss, extract_ogp_capabilities

async def test_basic_workflow():
    print("🧪 Testing basic workflow...")
    
    # Test 1: Monitor TechCrunch RSS
    print("\n1️⃣ Testing RSS monitoring...")
    entries = await listen_to_rss(
        "https://techcrunch.com/feed/",
        keywords=["AI", "artificial intelligence"]
    )
    print(f"   Found {len(entries)} AI-related articles")
    
    # Test 2: Extract metadata from first article
    if entries:
        print("\n2️⃣ Testing OGP extraction...")
        first_article = entries[0]['link']
        metadata = await extract_ogp_capabilities(first_article)
        print(f"   Extracted: {metadata.get('title', 'N/A')}")
    
    print("\n✅ Basic workflow test complete!")

if __name__ == "__main__":
    asyncio.run(test_basic_workflow())
```

Run it:
```bash
python test_workflow.py
```

## Step 4: Connect to Claude Desktop

For the best experience, integrate intelligentOne with Claude Desktop as an MCP server.

### Find Your Configuration File

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Add intelligentOne Server

Edit the configuration file:

```json
{
  "mcpServers": {
    "intelligentone": {
      "command": "python",
      "args": [
        "/absolute/path/to/intelligentOne/intelligentone_server.py"
      ],
      "env": {
        "OPENAI_API_KEY": "your-openai-key-here",
        "ANTHROPIC_API_KEY": "your-anthropic-key-here"
      }
    }
  }
}
```

**Important**: Replace `/absolute/path/to/intelligentOne/` with your actual path!

### Restart Claude Desktop

1. Quit Claude Desktop completely
2. Restart it
3. Look for the 🔌 icon in the bottom right
4. You should see "intelligentone" in the available servers

### Test in Claude Desktop

Try these prompts:

**Test 1: Monitor RSS Feed**
```
Use intelligentOne to monitor the TechCrunch RSS feed for articles about AI chips
```

**Test 2: Extract Metadata**
```
Use intelligentOne to extract metadata from https://techcrunch.com/2024/01/15/openai-announces-gpt-4/
```

**Test 3: Create Autonomous Workflow**
```
Use intelligentOne to create a workflow that monitors AI news and alerts me about breakthroughs
```

## Step 5: Launch Dashboard

The dashboard provides real-time visibility into your Blueprint Vault.

### Start Dashboard Server

```bash
cd dashboard
python server.py
```

You should see:
```
🎨 Dashboard server starting...
📊 Serving on http://localhost:8080
💾 Blueprint Vault: ./blueprints
🔄 Auto-refresh: 30 seconds
```

### Open Dashboard

Visit in your browser:
```
http://localhost:8080
```

You'll see:
- **Total Blueprints**: Number of evolved workflows
- **Deployed Today**: New workflows created today
- **Success Rate**: Percentage of successful executions
- **Average Time**: Mean execution time
- **Blueprint Cards**: Visual representation of each workflow
- **Recent Activity**: Live feed of executions

The dashboard auto-refreshes every 30 seconds.

## Step 6: Your First Autonomous Workflow

Let's evolve a complete workflow from scratch!

### In Claude Desktop

```
I want to monitor TechCrunch for articles about AI chips. 
When you find an article about a breakthrough, 
extract the key details and send me an urgent alert.
```

### What Happens Behind the Scenes

1. **Intent Classification** (Router Agent)
   - Classifies as "actionable" (not just informational)
   - Confidence: ~0.85

2. **Blueprint Search** (Blueprint Vault)
   - Searches for existing workflow
   - No match found (first time)

3. **Hypothesis Generation** (LLM Client)
   - GPT-4o generates workflow hypothesis:
   ```json
   {
     "name": "TechCrunch AI Chip Monitor",
     "description": "Monitor TechCrunch for AI chip breakthroughs",
     "tool_sequence": [
       {"tool": "listen_to_rss", "params": {...}},
       {"tool": "extract_ogp_capabilities", "params": {...}},
       {"tool": "calculate_competitive_delta", "params": {...}},
       {"tool": "send_alert", "params": {...}}
     ]
   }
   ```

4. **Simulation & Testing** (Simulation Lab)
   - Executes workflow in sandbox
   - Each tool runs in isolation
   - No real side effects

5. **LLM Judgment**
   - Completeness: 95/100 (all tools executed)
   - Relevance: 90/100 (addresses objective)
   - Actionability: 85/100 (produces alert)
   - **Overall Score: 90/100** ✅

6. **Auto-Deployment** (Blueprint Vault)
   - Score >= 85 → Auto-deploy!
   - Saves to `./blueprints/TechCrunch_AI_Chip_Monitor.json`
   - Now available for future use

7. **Execution**
   - Runs the workflow live
   - Returns results to you
   - Updates success stats

### Check Dashboard

Refresh your dashboard (or wait 30 seconds) and you'll see:
- **Total Blueprints**: 1
- **Deployed Today**: 1
- **New Card**: "TechCrunch AI Chip Monitor"

## Step 7: Reuse Evolved Workflow

Try the same query again:

```
Monitor TechCrunch for AI chip articles
```

### What's Different This Time

1. **Blueprint Search**: MATCH FOUND! ✅
2. **Execution**: Instant (no generation/testing needed)
3. **Stats Update**: `success_count` incremented
4. **Total Time**: ~2 seconds (vs ~10 seconds first time)

This is **self-evolution in action**—the system gets smarter with use!

## Common Use Cases

### Use Case 1: Competitive Intelligence

```
Create a workflow that:
1. Monitors competitor RSS feeds
2. Extracts product announcements
3. Calculates competitive delta vs our offerings
4. Alerts me if they launch something significant
```

### Use Case 2: Market Research

```
Monitor the top 5 AI news sites for quantum computing breakthroughs.
When you find relevant articles, extract the key capabilities and 
organize them in a report format.
```

### Use Case 3: Trend Detection

```
Track mentions of "transformer models" across tech news.
Analyze the frequency and sentiment over time.
Alert me if there's a spike in coverage.
```

## Troubleshooting

### Issue: "No LLM clients available"

**Solution**: Check your `.env` file has at least one API key set correctly.

```bash
# Verify environment variables are loaded
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
```

### Issue: "ModuleNotFoundError: No module named 'fastmcp'"

**Solution**: Install dependencies in your virtual environment.

```bash
# Ensure venv is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Blueprint not found"

**Solution**: Make sure `./blueprints/` directory exists.

```bash
# Create directory if missing
mkdir -p blueprints
```

### Issue: Dashboard not loading

**Solution**: Check the dashboard server is running and port 8080 is available.

```bash
# Check if port is in use
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Use different port if needed
PORT=8081 python dashboard/server.py
```

## Next Steps

Now that you're up and running:

1. **Explore Atomic Tools**: Try each tool individually to understand capabilities
2. **Review Architecture**: Read [ARCHITECTURE.md](ARCHITECTURE.md) for deep dive
3. **Check Examples**: Look at test files for usage patterns
4. **Monitor Dashboard**: Watch workflows evolve in real-time
5. **Experiment**: Try complex multi-step workflows
6. **Share**: Create blueprints others can use

## Advanced Configuration

### Custom Blueprint Storage

```bash
# Use different directory
BLUEPRINT_STORAGE_PATH=/path/to/custom/blueprints
```

### Adjust Deployment Threshold

Edit `simulation_lab.py`:
```python
# Lower threshold for more aggressive evolution
DEPLOYMENT_THRESHOLD = 80  # default: 85

# Higher threshold for more conservative evolution
DEPLOYMENT_THRESHOLD = 90
```

### Enable Slack Alerts

```bash
# Add to .env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

Update `send_alert()` in `intelligentone_server.py` to use Slack client.

## Getting Help

- **Documentation**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Issues**: [GitHub Issues](https://github.com/groupthinking/intelligentOne/issues)
- **Community**: Join discussions in GitHub
- **Examples**: Check `tests/` directory for working code

## Summary

You've now:
- ✅ Installed intelligentOne
- ✅ Configured LLM API keys
- ✅ Tested basic workflows
- ✅ Connected to Claude Desktop (optional)
- ✅ Launched the dashboard
- ✅ Evolved your first autonomous workflow
- ✅ Experienced self-improvement in action

**Welcome to the future of autonomous intelligence!** 🧠✨

---

[Back to Main README](../README.md) | [Architecture Deep Dive](ARCHITECTURE.md)
