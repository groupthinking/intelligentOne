"""
Example: Capability composition with pipelines

This example demonstrates composing multiple capabilities into a pipeline
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from intelligentone import IntelligentOne


def main():
    print("=== Capability Pipeline Example ===\n")
    
    # Initialize the OS
    os = IntelligentOne()
    
    # Discover some capabilities
    print("1. Discovering capabilities...")
    os.discover("https://api.geocoding.com", "rest")
    os.discover("https://api.weather.com", "rest")
    os.discover("https://api.notifications.com", "rest")
    
    # Register some mock capabilities for demonstration
    from intelligentone.core import Capability
    
    # Geocoding capability
    geocode_cap = Capability(
        name="geocode.lookup",
        description="Convert address to coordinates",
        endpoint="https://api.geocoding.com/lookup",
        method="GET",
        parameters={"address": {"type": "string", "required": True}},
        metadata={"source": "rest"}
    )
    os.register_capability(geocode_cap)
    
    # Weather capability
    weather_cap = Capability(
        name="weather.forecast",
        description="Get weather forecast",
        endpoint="https://api.weather.com/forecast",
        method="GET",
        parameters={
            "lat": {"type": "number", "required": True},
            "lon": {"type": "number", "required": True}
        },
        metadata={"source": "rest"}
    )
    os.register_capability(weather_cap)
    
    # Notification capability
    notify_cap = Capability(
        name="notify.email",
        description="Send email notification",
        endpoint="https://api.notifications.com/email",
        method="POST",
        parameters={
            "to": {"type": "string", "required": True},
            "subject": {"type": "string", "required": True},
            "body": {"type": "string", "required": True}
        },
        metadata={"source": "rest"}
    )
    os.register_capability(notify_cap)
    
    print(f"✓ Registered {len(os.list_capabilities())} capabilities\n")
    
    # Create a pipeline
    print("2. Creating capability pipeline...")
    print("   Pipeline: address → coords → weather → email\n")
    
    pipeline = os.pipeline([
        # Step 1: Convert address to coordinates
        ("geocode.lookup", {"address": "123 Main St, San Francisco, CA"}),
        
        # Step 2: Get weather for those coordinates
        ("weather.forecast", lambda prev: {
            "lat": 37.7749,  # In real implementation, extract from prev
            "lon": -122.4194
        }),
        
        # Step 3: Send email notification with weather
        ("notify.email", lambda prev: {
            "to": "user@example.com",
            "subject": "Your Weather Forecast",
            "body": f"Weather: {prev['result']['data']['conditions']}"
        })
    ])
    
    # Execute the pipeline
    print("3. Executing pipeline...")
    result = pipeline.execute()
    
    print("\n✓ Pipeline execution complete!")
    print(f"   Final result: {result['result']['message']}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
