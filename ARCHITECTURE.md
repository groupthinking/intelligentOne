# intelligentOne Architecture

## Vision: Capabilities over Information

Traditional web systems retrieve **information** - static data that must be parsed, understood, and processed by the user or application.

intelligentOne retrieves **capabilities** - executable functions that can be invoked directly, composed together, and managed as OS-level resources.

## Core Philosophy

```
Traditional Web:                intelligentOne:
──────────────────            ──────────────────

Request → Information         Request → Capability
Parse → Process → Act         Execute → Result

Information is passive        Capabilities are active
Data is retrieved             Functions are invoked
Manual integration            Dynamic discovery
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  (User Code, Scripts, Agents, Automation)                   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              intelligentOne Core Engine                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │ Capability Discovery │  │ Capability Executor  │        │
│  ├──────────────────────┤  ├──────────────────────┤        │
│  │ • API Detection      │  │ • Invocation         │        │
│  │ • Schema Extraction  │  │ • Param Marshalling  │        │
│  │ • Signature Mapping  │  │ • Result Transform   │        │
│  │ • Dynamic Registry   │  │ • Error Handling     │        │
│  └──────────────────────┘  └──────────────────────┘        │
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │  Pipeline Composer   │  │  Web Adapters        │        │
│  ├──────────────────────┤  ├──────────────────────┤        │
│  │ • Capability Chain   │  │ • REST               │        │
│  │ • Data Flow          │  │ • GraphQL            │        │
│  │ • Composition        │  │ • WebSocket          │        │
│  └──────────────────────┘  │ • HTML/Browser       │        │
│                             └──────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              OS Abstraction Layer                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐        │
│  │  Process Manager     │  │  File System         │        │
│  ├──────────────────────┤  ├──────────────────────┤        │
│  │ • Spawn              │  │ • Mount              │        │
│  │ • Lifecycle          │  │ • Hierarchy          │        │
│  │ • State Management   │  │ • Resource Access    │        │
│  └──────────────────────┘  └──────────────────────┘        │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │         Security Manager                      │          │
│  ├──────────────────────────────────────────────┤          │
│  │ • Authentication  • Authorization             │          │
│  │ • Credentials     • Permissions               │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    The Web as OS                             │
│  APIs • Services • GraphQL • REST • WebSockets • HTML       │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Capability Discovery Engine

**Purpose:** Discovers executable capabilities from web resources

**Inputs:**
- API endpoints (REST, GraphQL)
- API specifications (OpenAPI/Swagger)
- Web pages (HTML with interactive elements)

**Outputs:**
- Capability objects with:
  - Name and description
  - Endpoint and method
  - Parameter schemas
  - Metadata

**Process:**
1. Probe or fetch specification
2. Extract operation definitions
3. Map to capability model
4. Register in capability registry

### 2. Capability Executor

**Purpose:** Executes discovered capabilities

**Features:**
- Parameter validation against schemas
- Dynamic HTTP request construction
- Response parsing and transformation
- Error handling and retries
- Execution history tracking

**Flow:**
```
Capability + Parameters
        ↓
  Validate params
        ↓
  Build request (URL, method, body, headers)
        ↓
  Execute HTTP request
        ↓
  Parse response
        ↓
  Transform result
        ↓
  Return structured data
```

### 3. Pipeline Composer

**Purpose:** Chains multiple capabilities into workflows

**Features:**
- Sequential execution
- Data flow between steps
- Lambda-based parameter binding
- Result aggregation

**Example:**
```python
pipeline = os.pipeline([
    ("geocode", {"address": "..."}),
    ("weather", lambda prev: {"lat": prev["lat"], "lon": prev["lon"]}),
    ("notify", lambda prev: {"message": prev["forecast"]})
])
result = pipeline.execute()
```

### 4. Web Adapters

**Purpose:** Translate web protocols to intelligentOne abstractions

**REST Adapter:**
- URL construction with path/query params
- Method mapping (GET, POST, PUT, DELETE)
- Header management
- Body serialization

**GraphQL Adapter:**
- Query/mutation construction
- Variable binding
- Schema introspection
- Fragment support

### 5. OS Abstraction Layer

#### Process Manager
Treats capability executions as OS processes:
- PID allocation
- State tracking (ready, running, waiting, terminated)
- Lifecycle management

#### File System
Organizes web resources hierarchically:
- Mount points for APIs and services
- Path-based access
- Directory listing
- Resource metadata

#### Security Manager
Handles authentication and authorization:
- Credential storage (API keys, tokens)
- Permission grants
- Authorization checks
- Credential rotation

## Data Flow Example

### Discovering and Executing a Weather API

```
1. Discovery Phase:
   User: os.discover("https://api.weather.com/swagger.json", "openapi")
   ↓
   Discovery Engine:
     - Fetch OpenAPI spec
     - Parse operations
     - Extract: GET /forecast, params: {location, days}
   ↓
   Capability Registry:
     - Register: "weather.forecast"
     - Store: endpoint, params, metadata

2. Execution Phase:
   User: os.execute("weather.forecast", {"location": "SF", "days": 7})
   ↓
   Executor:
     - Validate: location ✓, days ✓
     - Build: GET https://api.weather.com/forecast?location=SF&days=7
     - Execute: HTTP request
     - Parse: JSON response
   ↓
   Result: {"temperature": 72, "conditions": "Sunny", ...}
```

## Key Design Principles

### 1. Discovery Over Configuration
- Capabilities are discovered dynamically
- No hardcoded integrations
- Self-describing APIs preferred

### 2. Execution as Primitive
- Capabilities are first-class executables
- Direct invocation model
- Structured results

### 3. Composability
- Simple capabilities combine into complex workflows
- Pipeline model for data flow
- Functional composition

### 4. OS Metaphors
- Familiar abstractions (process, filesystem, security)
- Maps web concepts to OS concepts
- Unified interface

## Use Cases

### 1. API Orchestration
Compose multiple APIs without hardcoded integrations:
```python
result = os.pipeline([
    ("payment.process", {"amount": 100}),
    ("inventory.update", lambda p: {"item": p["item_id"]}),
    ("notification.send", lambda p: {"user": p["user_id"]})
]).execute()
```

### 2. Intelligent Agents
Agents that discover and use capabilities autonomously:
```python
# Agent discovers available capabilities
capabilities = os.discover_all()

# Agent selects and executes relevant capability
result = os.execute("weather.forecast", {"location": agent.location})
```

### 3. Distributed Computing
Treat web APIs as distributed system calls:
```python
# Submit computation
job_id = os.execute("compute.submit", {"task": "train_model"})

# Check status
status = os.execute("compute.status", {"job_id": job_id})
```

### 4. Web Automation
Automate web interactions as capability executions:
```python
# Login, navigate, extract
os.execute("browser.login", {"user": "alice", "pass": "***"})
os.execute("browser.navigate", {"url": "/dashboard"})
data = os.execute("browser.extract", {"selector": ".data-table"})
```

## Comparison: Before and After

### Before intelligentOne (Traditional)

```python
# Hardcoded API integration
import requests

# Must know exact endpoint
response = requests.get("https://api.weather.com/v1/forecast",
                       params={"location": "SF", "days": 7},
                       headers={"X-API-Key": "..."})

# Must parse response
data = response.json()

# Must understand data structure
temp = data["forecasts"][0]["temperature"]["fahrenheit"]
```

### After intelligentOne

```python
from intelligentone import IntelligentOne

os = IntelligentOne()

# Discovery
os.discover("https://api.weather.com")

# Execution
result = os.execute("weather.forecast", {
    "location": "SF",
    "days": 7
})

# Direct access
temp = result["temperature"]
```

## Future Directions

1. **Real HTTP Implementation**: Connect to actual APIs
2. **Advanced Discovery**: AI-powered capability detection
3. **Caching Layer**: Cache capability results
4. **Monitoring**: Track capability health and performance
5. **Marketplace**: Share and discover capabilities
6. **Federation**: Federated capability registries
7. **Versioning**: Capability versioning and compatibility
8. **Streaming**: Support for streaming capabilities

## Conclusion

intelligentOne represents a paradigm shift: the web is no longer a collection of information to be retrieved and parsed, but a distributed operating system where capabilities can be discovered, invoked, and composed.

**The web is executable. Welcome to intelligentOne.**
