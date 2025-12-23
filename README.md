# 🧠 intelligentOne

**The world's first self-evolving autonomous intelligence platform**

[![MCP Native](https://img.shields.io/badge/MCP-Native-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

> While others build static workflows, intelligentOne evolves them autonomously.

## 🚀 The Billion-Dollar Opportunity

intelligentOne represents a fundamental paradigm shift in how AI systems operate. This isn't another automation tool—it's the first platform that **writes, tests, and deploys its own capabilities autonomously**.

### The Paradigm Shift

| **Traditional Systems** | **intelligentOne** |
|------------------------|-------------------|
| Static, hardcoded workflows | Self-evolving, autonomous workflows |
| Manual tool integration | Dynamic MCP-native tool discovery |
| Human-designed pipelines | LLM-generated & LLM-judged recipes |
| One-size-fits-all solutions | Context-adaptive intelligence |
| Siloed capabilities | Composable atomic tools |
| Degrades over time | Improves continuously |

## 🏗️ Architecture Overview

intelligentOne operates through three revolutionary layers:

### 1. **Hypothesis Engine** 🧪
The creative core that generates workflow ideas using LLM reasoning:
- Analyzes objectives and context
- Generates multiple workflow hypotheses
- Combines atomic tools in novel ways
- Learns from successful patterns

### 2. **Simulation Lab** 🔬
The quality gate that validates workflows before deployment:
- Executes hypotheses in isolation
- LLM-as-Judge scoring (Completeness 30%, Relevance 40%, Actionability 30%)
- Automatic deployment threshold: **85+ score**
- Zero risk to production systems

### 3. **Blueprint Vault** 💾
The memory that stores and evolves successful recipes:
- Persistent JSON storage of proven workflows
- Hot-reload capability for dynamic composition
- Success metrics and performance tracking
- Continuous improvement through execution feedback

```
┌─────────────────────────────────────────────────────────┐
│                    User Query/Objective                  │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────▼──────────┐
         │   Router Agent       │  Intent Classification
         └───────────┬──────────┘
                     │
         ┌───────────▼──────────┐
         │  Blueprint Vault     │  Check for existing
         │   (Search)           │  workflow match
         └───────────┬──────────┘
                     │
              Found? │ Not Found
         ┌───────────▼──────────┐
         │   Execute Blueprint  │
         └──────────────────────┘
                     │ Not Found
         ┌───────────▼──────────────┐
         │  Hypothesis Engine       │  Generate new
         │  (LLM generates ideas)   │  workflow ideas
         └───────────┬──────────────┘
                     │
         ┌───────────▼──────────────┐
         │   Simulation Lab         │  Test & Judge
         │   (LLM-as-Judge)         │  Score: 0-100
         └───────────┬──────────────┘
                     │
              Score >= 85?
         ┌───────────▼──────────────┐
         │   Blueprint Vault        │  Auto-deploy
         │   (Store & Deploy)       │  successful recipes
         └──────────────────────────┘
```

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/groupthinking/intelligentOne.git
cd intelligentOne

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys (OpenAI or Anthropic)
```

### Running with Claude Desktop

Add to your Claude Desktop MCP configuration:

**MacOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "intelligentone": {
      "command": "python",
      "args": ["/absolute/path/to/intelligentOne/intelligentone_server.py"],
      "env": {
        "OPENAI_API_KEY": "your-key-here",
        "ANTHROPIC_API_KEY": "your-key-here"
      }
    }
  }
}
```

Restart Claude Desktop and you'll see intelligentOne tools available.

### First Workflow Test

```python
# In Claude Desktop, try:
"Monitor TechCrunch RSS for AI chip announcements and alert me about urgent ones"

# intelligentOne will:
# 1. Classify the intent (actionable)
# 2. Check for existing blueprints
# 3. Generate a new workflow hypothesis if needed
# 4. Test it in Simulation Lab
# 5. Auto-deploy if score >= 85
# 6. Execute the workflow
```

## 🎯 Use Cases

### 1. **Competitive Intelligence Automation**
```
Query: "Monitor competitor product launches and calculate competitive delta"

intelligentOne creates:
- RSS monitoring workflow
- OGP metadata extraction
- Competitive analysis scoring
- Urgent alert system
```

### 2. **Market Research Pipeline**
```
Query: "Track AI chip industry news and identify breakthrough capabilities"

intelligentOne builds:
- Multi-source RSS aggregation
- Keyword-based filtering
- Capability extraction from articles
- Trend analysis and alerts
```

### 3. **Autonomous Research Assistant**
```
Query: "Find and summarize latest developments in quantum computing"

intelligentOne evolves:
- Information gathering workflow
- Content extraction and analysis
- Summary generation
- Knowledge base updates
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **MCP Server** | FastMCP | Native tool protocol integration |
| **Hypothesis Engine** | GPT-4o / Claude 3.5 | Workflow generation |
| **Simulation Lab** | LLM-as-Judge | Quality assurance |
| **Blueprint Vault** | JSON Storage | Recipe persistence |
| **Web Scraping** | httpx + BeautifulSoup | Content extraction |
| **Feed Monitoring** | feedparser | RSS/Atom parsing |
| **Data Validation** | Pydantic | Type safety |

## 📊 Atomic Tools

intelligentOne provides five core atomic tools that combine into infinite possibilities:

| Tool | Purpose | Example |
|------|---------|---------|
| `listen_to_rss()` | Monitor RSS feeds | Track TechCrunch AI news |
| `extract_ogp_capabilities()` | Extract metadata | Get article details |
| `search_internal_db()` | Query knowledge base | Find existing workflows |
| `calculate_competitive_delta()` | Analyze gaps | Compare capabilities |
| `send_alert()` | Notify users | Urgent updates |

## 🗺️ Roadmap

### Phase 1: Foundation ✅ (Complete)
- ✅ MCP-native architecture
- ✅ Atomic tools implementation
- ✅ Hypothesis Engine with LLM generation
- ✅ Simulation Lab with LLM-as-Judge
- ✅ Blueprint Vault persistence
- ✅ Dynamic composite tool loading

### Phase 2: Intelligence Enhancement (Q1 2025)
- 🔄 Multi-model ensemble judgment
- 🔄 A/B testing of workflow variants
- 🔄 Automatic hyperparameter tuning
- 🔄 Cross-blueprint learning
- 🔄 Failure analysis and self-healing

### Phase 3: Enterprise Scale (Q2 2025)
- 📋 Multi-user Blueprint Vaults
- 📋 Distributed execution engine
- 📋 Advanced security sandboxing
- 📋 Real-time collaboration
- 📋 Enterprise integrations (Slack, Teams, Email)

## 📚 Documentation

- **[Architecture Deep Dive](docs/ARCHITECTURE.md)** - Technical implementation details
- **[Getting Started Guide](docs/GETTING_STARTED.md)** - Step-by-step tutorial
- **[API Reference](docs/API.md)** - Tool and function documentation (coming soon)

## 🔒 Security

- All workflow hypotheses execute in **simulation sandbox** before deployment
- Blueprint Vault uses **JSON file storage** (no SQL injection risk)
- MCP protocol provides **built-in authentication**
- LLM API keys stored in **environment variables** (never committed)
- Optional **approval threshold** configuration

## 🤝 Contributing

We welcome contributions! intelligentOne is about expanding the universe of autonomous intelligence capabilities.

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🌟 Vision

intelligentOne represents the future of AI systems:

**Before**: Humans design workflows, AI executes them  
**After**: AI designs, tests, and deploys workflows autonomously

This is not incremental improvement—it's a fundamental shift in how intelligent systems evolve. While traditional systems degrade over time requiring manual updates, intelligentOne **gets smarter with every query**, building an ever-expanding library of proven capabilities.

The platform that owns this self-evolution loop will dominate the next decade of AI automation.

**Welcome to autonomous intelligence.**

---

Built with ❤️ by the intelligentOne team | [GitHub](https://github.com/groupthinking/intelligentOne) | [Issues](https://github.com/groupthinking/intelligentOne/issues)
