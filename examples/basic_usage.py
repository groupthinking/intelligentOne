"""
Example: Basic usage of intelligentOne

This example demonstrates:
1. Initializing the intelligentOne OS
2. Discovering capabilities from an API
3. Executing a capability
4. Viewing execution results
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone import IntelligentOne


def main():
    print("=== intelligentOne Basic Example ===\n")
    
    # Initialize the OS
    print("1. Initializing intelligentOne OS...")
    os = IntelligentOne()
    print("   ✓ OS initialized\n")
    
    # Discover capabilities from a REST API
    print("2. Discovering capabilities from example API...")
    capabilities = os.discover("https://api.example.com", "rest")
    print(f"   ✓ Discovered {len(capabilities)} capabilities")
    
    for cap in capabilities:
        print(f"     - {cap.name}: {cap.description}")
    print()
    
    # List all registered capabilities
    print("3. Listing all registered capabilities...")
    all_caps = os.list_capabilities()
    print(f"   ✓ Total capabilities: {len(all_caps)}\n")
    
    # Execute a capability
    print("4. Executing capability: api.get")
    result = os.execute("api.get", {})
    print("   ✓ Execution result:")
    print(f"     Status: {result['status']}")
    print(f"     Message: {result['result']['message']}")
    print()
    
    # Execute with parameters
    print("5. Executing capability with parameters: api.post")
    result = os.execute("api.post", {
        "name": "John Doe",
        "email": "john@example.com"
    })
    print("   ✓ Execution result:")
    print(f"     Status: {result['status']}")
    print(f"     Data: {result['result']['data']}")
    print()
    
    print("=== Example Complete ===")


if __name__ == "__main__":
    main()
