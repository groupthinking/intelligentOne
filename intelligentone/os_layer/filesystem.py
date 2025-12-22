"""
File System - Organizes web resources as a file system
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ResourceType(Enum):
    """Types of web resources"""
    CAPABILITY = "capability"
    API = "api"
    SERVICE = "service"
    DATA = "data"


@dataclass
class Resource:
    """Represents a web resource in the file system"""
    path: str
    type: ResourceType
    data: Any
    metadata: Dict[str, Any]


class FileSystem:
    """
    Organizes web resources as a hierarchical file system
    
    This provides familiar file system abstractions:
    - Hierarchical organization (directories and files)
    - Path-based access (/api/weather/forecast)
    - Resource metadata
    - Mount points for external services
    """
    
    def __init__(self):
        self.root: Dict[str, Any] = {}
        self.resources: Dict[str, Resource] = {}
        
    def mount(self, path: str, resource: Resource):
        """
        Mount a resource at a given path
        
        Args:
            path: Path to mount at (e.g., /api/weather)
            resource: Resource to mount
        """
        path = self._normalize_path(path)
        self.resources[path] = resource
        
        # Create directory structure
        parts = path.strip('/').split('/')
        current = self.root
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # Store resource at leaf
        if parts:
            current[parts[-1]] = resource
    
    def get(self, path: str) -> Optional[Resource]:
        """Get a resource by path"""
        path = self._normalize_path(path)
        return self.resources.get(path)
    
    def list(self, path: str = "/") -> List[str]:
        """
        List resources in a directory
        
        Args:
            path: Directory path to list
            
        Returns:
            List of resource names in the directory
        """
        if path == "/" or path == "":
            return list(self.root.keys())
        
        path = self._normalize_path(path)
        
        # Navigate to directory
        parts = path.strip('/').split('/')
        current = self.root
        
        for part in parts:
            if part not in current:
                return []
            current = current[part]
        
        if isinstance(current, dict):
            return list(current.keys())
        
        return []
    
    def unmount(self, path: str):
        """Unmount a resource"""
        path = self._normalize_path(path)
        if path in self.resources:
            del self.resources[path]
    
    def exists(self, path: str) -> bool:
        """Check if a resource exists at path"""
        path = self._normalize_path(path)
        return path in self.resources
    
    def _normalize_path(self, path: str) -> str:
        """Normalize a path"""
        if not path.startswith('/'):
            path = '/' + path
        return path.rstrip('/')
    
    def tree(self, path: str = "/", indent: int = 0) -> str:
        """
        Generate a tree view of the file system
        
        Args:
            path: Starting path
            indent: Indentation level
            
        Returns:
            String representation of the tree
        """
        lines = []
        items = self.list(path)
        
        for item in items:
            item_path = f"{path.rstrip('/')}/{item}"
            prefix = "  " * indent + "├── "
            lines.append(f"{prefix}{item}")
            
            # Recursively add subdirectories
            if self.list(item_path):
                lines.append(self.tree(item_path, indent + 1))
        
        return "\n".join(lines)
