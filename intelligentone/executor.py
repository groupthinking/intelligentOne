"""
Capability Executor - Executes discovered capabilities
"""

from typing import Dict, Any, Optional
import json


class CapabilityExecutor:
    """
    Executes capabilities discovered from the web
    
    This executor:
    - Manages capability lifecycle
    - Handles parameter marshalling
    - Performs actual HTTP requests
    - Transforms results
    - Handles errors and retries
    """
    
    def __init__(self):
        self.capabilities = {}
        self.execution_history = []
        
    def register(self, capability):
        """Register a capability for execution"""
        self.capabilities[capability.name] = capability
        
    def unregister(self, name: str):
        """Unregister a capability"""
        if name in self.capabilities:
            del self.capabilities[name]
    
    def execute(self, capability_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a capability with given parameters
        
        Args:
            capability_name: Name of the capability to execute
            params: Parameters to pass to the capability
            
        Returns:
            Result of the execution
        """
        if capability_name not in self.capabilities:
            raise ValueError(f"Capability '{capability_name}' not registered")
        
        capability = self.capabilities[capability_name]
        params = params or {}
        
        # Validate parameters
        self._validate_parameters(capability, params)
        
        # Execute the capability
        result = self._execute_capability(capability, params)
        
        # Record execution
        self.execution_history.append({
            "capability": capability_name,
            "params": params,
            "result": result
        })
        
        return result
    
    def _validate_parameters(self, capability, params: Dict[str, Any]):
        """Validate parameters against capability specification"""
        required_params = [
            name for name, spec in capability.parameters.items()
            if isinstance(spec, dict) and spec.get("required", False)
        ]
        
        for req_param in required_params:
            if req_param not in params:
                raise ValueError(f"Required parameter '{req_param}' missing for capability '{capability.name}'")
    
    def _execute_capability(self, capability, params: Dict[str, Any]) -> Any:
        """
        Execute the actual capability
        
        In a full implementation, this would:
        1. Prepare the HTTP request based on capability.method and capability.endpoint
        2. Marshal parameters into request (query params, body, headers, etc.)
        3. Execute the request
        4. Handle response and errors
        5. Transform result according to capability.returns
        
        For this demonstration, we'll simulate execution
        """
        # Simulate execution based on capability type
        execution_type = capability.metadata.get("source", "rest")
        
        if execution_type == "rest":
            return self._execute_rest(capability, params)
        elif execution_type == "openapi":
            return self._execute_rest(capability, params)
        elif execution_type == "graphql":
            return self._execute_graphql(capability, params)
        elif execution_type == "html":
            return self._execute_html(capability, params)
        else:
            raise ValueError(f"Unknown execution type: {execution_type}")
    
    def _execute_rest(self, capability, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a REST API capability"""
        # In production, this would use requests library to make actual HTTP calls
        # For demonstration, return simulated response
        
        return {
            "status": "success",
            "capability": capability.name,
            "endpoint": capability.endpoint,
            "method": capability.method,
            "params": params,
            "result": {
                "message": f"Successfully executed {capability.name}",
                "data": self._generate_mock_response(capability, params)
            }
        }
    
    def _execute_graphql(self, capability, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a GraphQL capability"""
        query_type = capability.metadata.get("type", "query")
        
        return {
            "status": "success",
            "capability": capability.name,
            "type": query_type,
            "data": self._generate_mock_response(capability, params)
        }
    
    def _execute_html(self, capability, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an HTML interaction capability"""
        return {
            "status": "success",
            "capability": capability.name,
            "action": "form_submitted",
            "result": self._generate_mock_response(capability, params)
        }
    
    def _generate_mock_response(self, capability, params: Dict[str, Any]) -> Any:
        """Generate a mock response based on capability and params"""
        # This simulates what a real API would return
        
        if "user" in capability.name.lower():
            return {
                "id": "12345",
                "name": params.get("name", "John Doe"),
                "email": params.get("email", "john@example.com"),
                "created_at": "2025-12-22T22:56:50Z"
            }
        elif "weather" in capability.name.lower():
            return {
                "location": params.get("location", "Unknown"),
                "temperature": 72,
                "conditions": "Sunny",
                "forecast": ["Sunny", "Partly Cloudy", "Cloudy"]
            }
        else:
            return {"result": "Success", "params": params}
    
    def get_execution_history(self) -> list:
        """Get the history of capability executions"""
        return self.execution_history
    
    def clear_history(self):
        """Clear execution history"""
        self.execution_history = []
