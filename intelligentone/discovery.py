"""
Capability Discovery Engine - Discovers executable capabilities from web resources
"""

from typing import List, Dict, Any
import json
import re
from .models import Capability


class CapabilityDiscovery:
    """
    Discovers capabilities from various web sources:
    - OpenAPI/Swagger specifications
    - GraphQL schemas
    - REST API endpoints
    - HTML pages with interactive elements
    """
    
    def __init__(self):
        self.adapters = {
            "rest": self._discover_rest,
            "openapi": self._discover_openapi,
            "graphql": self._discover_graphql,
            "html": self._discover_html
        }
    
    def discover(self, url: str, capability_type: str = "rest") -> List[Capability]:
        """
        Discover capabilities from a URL
        
        Args:
            url: URL to discover capabilities from
            capability_type: Type of discovery to perform
            
        Returns:
            List of discovered Capability objects
        """
        if capability_type not in self.adapters:
            raise ValueError(f"Unknown capability type: {capability_type}")
        
        return self.adapters[capability_type](url)
    
    def _discover_rest(self, url: str) -> List[Capability]:
        """Discover REST API capabilities"""
        # In a real implementation, this would probe the API
        # For now, return example capabilities
        base_url = url.rstrip('/')
        
        return [
            Capability(
                name=f"api.get",
                description=f"GET request to {url}",
                endpoint=url,
                method="GET",
                parameters={},
                metadata={"source": "rest", "base_url": base_url}
            ),
            Capability(
                name=f"api.post",
                description=f"POST request to {url}",
                endpoint=url,
                method="POST",
                parameters={"body": {"type": "object"}},
                metadata={"source": "rest", "base_url": base_url}
            )
        ]
    
    def _discover_openapi(self, url: str) -> List[Capability]:
        """
        Discover capabilities from OpenAPI/Swagger specification
        
        In a full implementation, this would:
        1. Fetch the OpenAPI spec from the URL
        2. Parse paths and operations
        3. Extract parameters and schemas
        4. Create Capability objects for each operation
        """
        capabilities = []
        
        # Example OpenAPI discovery
        # This would parse actual OpenAPI JSON/YAML in production
        example_paths = {
            "/users": {
                "get": {
                    "description": "List all users",
                    "parameters": [
                        {"name": "limit", "type": "integer", "default": 10}
                    ]
                },
                "post": {
                    "description": "Create a new user",
                    "parameters": [
                        {"name": "name", "type": "string", "required": True},
                        {"name": "email", "type": "string", "required": True}
                    ]
                }
            },
            "/users/{id}": {
                "get": {
                    "description": "Get user by ID",
                    "parameters": [
                        {"name": "id", "type": "string", "required": True}
                    ]
                }
            }
        }
        
        base_url = url.replace("/swagger.json", "").replace("/openapi.json", "")
        
        for path, methods in example_paths.items():
            for method, spec in methods.items():
                cap_name = self._generate_capability_name(path, method)
                
                params = {}
                for param in spec.get("parameters", []):
                    params[param["name"]] = {
                        "type": param.get("type", "string"),
                        "required": param.get("required", False)
                    }
                
                capabilities.append(Capability(
                    name=cap_name,
                    description=spec.get("description", ""),
                    endpoint=f"{base_url}{path}",
                    method=method.upper(),
                    parameters=params,
                    metadata={"source": "openapi", "path": path}
                ))
        
        return capabilities
    
    def _discover_graphql(self, url: str) -> List[Capability]:
        """
        Discover capabilities from GraphQL schema
        
        In a full implementation, this would:
        1. Send an introspection query
        2. Parse the schema
        3. Extract queries, mutations, and subscriptions
        4. Create Capability objects for each operation
        """
        capabilities = []
        
        # Example GraphQL capabilities
        capabilities.append(Capability(
            name="graphql.query",
            description="Execute GraphQL query",
            endpoint=url,
            method="POST",
            parameters={
                "query": {"type": "string", "required": True},
                "variables": {"type": "object", "required": False}
            },
            metadata={"source": "graphql", "type": "query"}
        ))
        
        capabilities.append(Capability(
            name="graphql.mutation",
            description="Execute GraphQL mutation",
            endpoint=url,
            method="POST",
            parameters={
                "mutation": {"type": "string", "required": True},
                "variables": {"type": "object", "required": False}
            },
            metadata={"source": "graphql", "type": "mutation"}
        ))
        
        return capabilities
    
    def _discover_html(self, url: str) -> List[Capability]:
        """
        Discover interactive capabilities from HTML pages
        
        In a full implementation, this would:
        1. Fetch and parse the HTML
        2. Identify forms, buttons, and interactive elements
        3. Extract actions and parameters
        4. Create Capability objects for interactions
        """
        capabilities = []
        
        # Example: Form submission capability
        capabilities.append(Capability(
            name="html.submit_form",
            description=f"Submit form on {url}",
            endpoint=url,
            method="POST",
            parameters={"form_data": {"type": "object"}},
            metadata={"source": "html", "type": "form"}
        ))
        
        return capabilities
    
    def _generate_capability_name(self, path: str, method: str) -> str:
        """Generate a capability name from path and method"""
        # Convert /users/{id} to users.get_by_id
        clean_path = re.sub(r'\{[^}]+\}', 'by_id', path)
        clean_path = clean_path.strip('/').replace('/', '.')
        
        method_name = method.lower()
        if method_name == "post":
            method_name = "create"
        elif method_name == "put":
            method_name = "update"
        elif method_name == "delete":
            method_name = "delete"
        elif method_name == "get":
            method_name = "get"
        
        return f"{clean_path}.{method_name}"
