"""
Example: OpenAPI capability discovery

This example demonstrates discovering capabilities from an OpenAPI/Swagger specification
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone import IntelligentOne


def main():
    print("=== OpenAPI Capability Discovery ===\n")
    
    # Initialize the OS
    os = IntelligentOne()
    
    # Discover from OpenAPI specification
    print("Discovering capabilities from OpenAPI spec...")
    capabilities = os.discover("https://api.example.com/swagger.json", "openapi")
    
    print(f"\n✓ Discovered {len(capabilities)} capabilities:\n")
    
    # Display each capability in detail
    for cap in capabilities:
        print(f"Capability: {cap.name}")
        print(f"  Description: {cap.description}")
        print(f"  Endpoint: {cap.endpoint}")
        print(f"  Method: {cap.method}")
        print(f"  Parameters:")
        
        for param_name, param_spec in cap.parameters.items():
            required = param_spec.get('required', False)
            param_type = param_spec.get('type', 'string')
            req_marker = "*" if required else " "
            print(f"    {req_marker} {param_name} ({param_type})")
        
        print()
    
    # Execute a discovered capability
    print("\nExecuting capability: users.get...")
    result = os.execute("users.get", {"limit": 5})
    print(f"Result: {result['result']['message']}")
    
    print("\nExecuting capability: users.create...")
    result = os.execute("users.create", {
        "name": "Alice Smith",
        "email": "alice@example.com"
    })
    print(f"Result: {result['result']['data']}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
