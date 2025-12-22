# Quick Start Guide

Get started with intelligentOne in 5 minutes.

## Installation

```bash
# Clone the repository
git clone https://github.com/groupthinking/intelligentOne.git
cd intelligentOne

# No dependencies required for core functionality
# Optional: Install full dependencies
pip install -r requirements.txt
```

## Your First Program

Create a file called `my_first_capability.py`:

```python
import sys
sys.path.insert(0, '.')

from intelligentone import IntelligentOne

# Initialize the OS
os = IntelligentOne()

# Discover capabilities from an API
capabilities = os.discover("https://api.example.com", "rest")

print(f"Discovered {len(capabilities)} capabilities:")
for cap in capabilities:
    print(f"  - {cap.name}")

# Execute a capability
result = os.execute("api.get", {})
print(f"\nResult: {result['result']['message']}")
```

Run it:
```bash
python my_first_capability.py
```

## Core Concepts in 2 Minutes

### 1. Discovery
Find capabilities from web resources:

```python
from intelligentone import IntelligentOne

os = IntelligentOne()

# From REST API
os.discover("https://api.example.com", "rest")

# From OpenAPI spec
os.discover("https://api.example.com/swagger.json", "openapi")

# From GraphQL
os.discover("https://api.example.com/graphql", "graphql")
```

### 2. Execution
Execute discovered capabilities:

```python
# Simple execution
result = os.execute("api.get", {})

# With parameters
result = os.execute("users.create", {
    "name": "Alice",
    "email": "alice@example.com"
})
```

### 3. Composition
Chain capabilities together:

```python
pipeline = os.pipeline([
    ("step1", {"param": "value"}),
    ("step2", lambda prev: {"input": prev["output"]}),
    ("step3", lambda prev: {"data": prev["result"]})
])

result = pipeline.execute()
```

## Run Examples

The repository includes several examples:

```bash
# Basic usage
python examples/basic_usage.py

# OpenAPI discovery
python examples/openapi_discovery.py

# Pipeline composition
python examples/capability_pipeline.py

# OS abstractions
python examples/os_abstractions.py

# Complete demo
python demo.py
```

## Run Tests

```bash
python run_tests.py
```

All 27 tests should pass.

## Next Steps

1. **Read the README**: Understand the vision and philosophy
2. **Check ARCHITECTURE.md**: Deep dive into the design
3. **Explore examples/**: See real usage patterns
4. **Build something**: Create your own capability-driven application

## Common Patterns

### Pattern 1: API Wrapper
```python
class WeatherOS:
    def __init__(self):
        self.os = IntelligentOne()
        self.os.discover("https://api.weather.com/swagger.json", "openapi")
    
    def get_forecast(self, location, days=7):
        return self.os.execute("weather.forecast", {
            "location": location,
            "days": days
        })

weather = WeatherOS()
forecast = weather.get_forecast("San Francisco")
```

### Pattern 2: Multi-API Workflow
```python
os = IntelligentOne()

# Discover multiple APIs
os.discover("https://api.geocoding.com", "rest")
os.discover("https://api.weather.com", "rest")
os.discover("https://api.email.com", "rest")

# Create workflow
pipeline = os.pipeline([
    ("geocode.lookup", {"address": "123 Main St"}),
    ("weather.forecast", lambda p: {"coords": p["coords"]}),
    ("email.send", lambda p: {"body": p["forecast"]})
])

pipeline.execute()
```

### Pattern 3: Capability Registry
```python
from intelligentone import Capability

# Register custom capability
custom = Capability(
    name="my.custom.capability",
    description="My custom capability",
    endpoint="https://myapi.com/endpoint",
    method="POST",
    parameters={"param1": {"type": "string", "required": True}}
)

os.register_capability(custom)
result = os.execute("my.custom.capability", {"param1": "value"})
```

## Troubleshooting

### ModuleNotFoundError: No module named 'intelligentone'

Add the project root to Python path:
```python
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
```

### Capability not found

Make sure to discover or register the capability first:
```python
# Discover
os.discover("https://api.example.com", "rest")

# Or register manually
from intelligentone import Capability
cap = Capability(name="my.cap", ...)
os.register_capability(cap)
```

## Philosophy

Remember the core principle:

> **Traditional systems retrieve information.**  
> **intelligentOne retrieves capabilities.**

Instead of getting data and figuring out what to do with it, you get executable functions that you can invoke directly.

## Get Help

- **Documentation**: Read README.md and ARCHITECTURE.md
- **Examples**: Check the examples/ directory
- **Tests**: See tests/ for usage patterns

## Contributing

intelligentOne is about expanding the universe of executable web capabilities. Contributions welcome!

---

**Welcome to the executable web. 🚀**
