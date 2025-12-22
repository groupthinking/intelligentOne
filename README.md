# intelligentOne

**Transform the web into an executable operating system**

## Overview

intelligentOne is a revolutionary system that transforms the web from a passive information repository into an active, executable operating system. While traditional systems simply retrieve *information* from the web, intelligentOne retrieves *capabilities* - actionable functions that can be discovered, composed, and executed.

## Core Concept

The web contains billions of APIs, services, and interactive elements. intelligentOne treats these as executable capabilities rather than static content, creating a dynamic operating system where:

- **Web services become system calls** - APIs and endpoints are treated as OS-level capabilities
- **Websites become executable resources** - Interactive elements are discoverable and executable
- **Capabilities are composable** - Web functions can be chained and orchestrated
- **Dynamic discovery** - Capabilities are discovered and registered at runtime

## Architecture

```
┌─────────────────────────────────────────────────┐
│          intelligentOne Core Engine             │
├─────────────────────────────────────────────────┤
│  Capability Discovery  │  Capability Executor   │
│  ───────────────────── │  ──────────────────── │
│  • API Detection       │  • Function Execution  │
│  • Service Mapping     │  • Parameter Binding   │
│  • Schema Extraction   │  • Result Handling     │
└────────────┬────────────────────────┬───────────┘
             │                        │
    ┌────────▼────────┐      ┌───────▼────────┐
    │  Web Interface  │      │  OS Abstraction │
    │    Adapter      │      │     Layer       │
    └─────────────────┘      └────────────────┘
             │                        │
    ┌────────▼────────────────────────▼───────────┐
    │           The Web as an OS                   │
    │  APIs • Services • Interactive Elements      │
    └──────────────────────────────────────────────┘
```

## Key Components

### 1. Capability Discovery Engine
Discovers executable capabilities from web resources:
- API endpoint detection
- Function signature extraction
- Service capability mapping
- Real-time capability registration

### 2. Capability Executor
Executes discovered capabilities:
- Dynamic invocation
- Parameter marshalling
- Error handling and retry logic
- Result transformation

### 3. Web Interface Adapter
Adapts web resources to OS-level abstractions:
- HTTP to system call translation
- WebSocket to process streams
- REST/GraphQL to function calls

### 4. OS Abstraction Layer
Provides familiar OS primitives:
- Process management (web service lifecycle)
- File system (web resource organization)
- Networking (capability communication)
- Security (authentication and authorization)

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from intelligentone import IntelligentOne

# Initialize the OS
os = IntelligentOne()

# Discover capabilities from a service
capabilities = os.discover("https://api.example.com")

# Execute a capability
result = os.execute("weather.get_forecast", {
    "location": "San Francisco",
    "days": 7
})

print(result)
```

### Discovering Capabilities

```python
# Discover from OpenAPI/Swagger
capabilities = os.discover("https://api.example.com/swagger.json")

# Discover from GraphQL
capabilities = os.discover("https://api.example.com/graphql", type="graphql")

# List available capabilities
for cap in os.list_capabilities():
    print(f"{cap.name}: {cap.description}")
```

### Composing Capabilities

```python
# Chain multiple capabilities
pipeline = os.pipeline([
    ("geocode.address_to_coords", {"address": "123 Main St"}),
    ("weather.get_forecast", lambda prev: {"lat": prev["lat"], "lon": prev["lon"]}),
    ("notifications.send_email", lambda prev: {"body": prev["summary"]})
])

result = pipeline.execute()
```

## Examples

See the `examples/` directory for complete examples:
- `weather_service.py` - Weather API capability discovery
- `github_api.py` - GitHub API as OS capabilities
- `web_automation.py` - Browser automation as capabilities
- `capability_chain.py` - Composing multiple capabilities

## Philosophy

intelligentOne reimagines the web as a distributed, executable operating system:

1. **Everything is a capability** - APIs, services, and interactive elements are treated as executable functions
2. **Discovery over configuration** - Capabilities are discovered dynamically rather than hardcoded
3. **Composition is key** - Simple capabilities combine to create complex behaviors
4. **The web is the kernel** - The internet itself becomes the OS kernel, managing distributed capabilities

## Use Cases

- **Automated Workflows**: Compose web services into automated business processes
- **Distributed Computing**: Treat web APIs as distributed system calls
- **Intelligent Agents**: Agents that discover and execute capabilities autonomously
- **API Orchestration**: Dynamic service composition without hardcoded integrations
- **Web Automation**: Treat websites as executable programs

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Project Structure

```
intelligentone/
├── __init__.py           # Main module exports
├── core.py               # Core IntelligentOne engine
├── discovery.py          # Capability discovery engine
├── executor.py           # Capability execution engine
├── adapters/             # Web interface adapters
│   ├── rest.py          # REST API adapter
│   ├── graphql.py       # GraphQL adapter
│   └── browser.py       # Browser automation adapter
└── os_layer/            # OS abstraction layer
    ├── process.py       # Process management
    ├── filesystem.py    # Resource organization
    └── security.py      # Auth and security
```

## Contributing

Contributions are welcome! intelligentOne is about expanding the universe of executable web capabilities.

## License

MIT License - See LICENSE file for details

## Vision

intelligentOne represents a paradigm shift in how we interact with the web. Instead of navigating to websites and manually clicking buttons, we discover capabilities and execute them programmatically. The web becomes less like a library and more like a distributed operating system where every service is a potential system call waiting to be invoked.

Welcome to the executable web.