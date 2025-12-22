"""
Core IntelligentOne engine - The heart of the web operating system
"""

from typing import Dict, List, Any, Optional, Callable
from .models import Capability
from .discovery import CapabilityDiscovery
from .executor import CapabilityExecutor


class CapabilityPipeline:
    """Chains multiple capabilities together for composition"""
    
    def __init__(self, steps: List[tuple]):
        self.steps = steps
        self.executor = None
    
    def set_executor(self, executor: CapabilityExecutor):
        self.executor = executor
        
    def execute(self, initial_input: Optional[Dict[str, Any]] = None) -> Any:
        """Execute the pipeline, passing results between steps"""
        result = initial_input or {}
        
        for capability_name, params in self.steps:
            # If params is a function, call it with previous result
            if callable(params):
                actual_params = params(result)
            else:
                actual_params = params
            
            # Execute the capability
            result = self.executor.execute(capability_name, actual_params)
        
        return result


class IntelligentOne:
    """
    Main IntelligentOne engine - Transforms the web into an executable OS
    
    This class provides the primary interface for:
    - Discovering capabilities from web resources
    - Executing discovered capabilities
    - Managing capability lifecycle
    - Composing capabilities into pipelines
    """
    
    def __init__(self):
        self.discovery = CapabilityDiscovery()
        self.executor = CapabilityExecutor()
        self.capabilities: Dict[str, Capability] = {}
        
    def discover(self, url: str, capability_type: str = "rest") -> List[Capability]:
        """
        Discover capabilities from a web resource
        
        Args:
            url: URL of the API or service to discover
            capability_type: Type of capability (rest, graphql, openapi, etc.)
            
        Returns:
            List of discovered capabilities
        """
        capabilities = self.discovery.discover(url, capability_type)
        
        # Register discovered capabilities
        for cap in capabilities:
            self.register_capability(cap)
            
        return capabilities
    
    def register_capability(self, capability: Capability):
        """Register a capability for later execution"""
        self.capabilities[capability.name] = capability
        self.executor.register(capability)
        
    def execute(self, capability_name: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Execute a registered capability
        
        Args:
            capability_name: Name of the capability to execute
            params: Parameters to pass to the capability
            
        Returns:
            Result of capability execution
        """
        if capability_name not in self.capabilities:
            raise ValueError(f"Capability '{capability_name}' not found. Did you discover it first?")
        
        return self.executor.execute(capability_name, params or {})
    
    def list_capabilities(self) -> List[Capability]:
        """List all registered capabilities"""
        return list(self.capabilities.values())
    
    def pipeline(self, steps: List[tuple]) -> CapabilityPipeline:
        """
        Create a capability pipeline for composition
        
        Args:
            steps: List of (capability_name, params) tuples
            
        Returns:
            CapabilityPipeline object
        """
        pipeline = CapabilityPipeline(steps)
        pipeline.set_executor(self.executor)
        return pipeline
    
    def get_capability(self, name: str) -> Optional[Capability]:
        """Get a capability by name"""
        return self.capabilities.get(name)
    
    def unregister_capability(self, name: str):
        """Unregister a capability"""
        if name in self.capabilities:
            del self.capabilities[name]
            self.executor.unregister(name)
