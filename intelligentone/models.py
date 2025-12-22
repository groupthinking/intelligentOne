"""
Data models for intelligentOne
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Capability:
    """Represents an executable capability discovered from the web"""
    
    name: str
    description: str
    endpoint: str
    method: str = "GET"
    parameters: Dict[str, Any] = field(default_factory=dict)
    returns: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        return f"Capability(name={self.name}, endpoint={self.endpoint}, method={self.method})"
