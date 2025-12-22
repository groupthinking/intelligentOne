"""
Security Manager - Handles authentication and authorization
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class PermissionLevel(Enum):
    """Permission levels for capabilities"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


@dataclass
class Credential:
    """Represents authentication credentials"""
    type: str  # bearer, api_key, oauth, etc.
    value: str
    metadata: Dict[str, Any]


@dataclass
class Permission:
    """Represents a permission grant"""
    capability: str
    level: PermissionLevel
    granted_by: str


class SecurityManager:
    """
    Manages security for web capabilities
    
    Provides:
    - Authentication management
    - Authorization checks
    - Credential storage
    - Permission management
    """
    
    def __init__(self):
        self.credentials: Dict[str, Credential] = {}
        self.permissions: Dict[str, List[Permission]] = {}
        
    def store_credential(self, name: str, credential: Credential):
        """
        Store authentication credentials
        
        Args:
            name: Credential identifier
            credential: Credential object
        """
        self.credentials[name] = credential
    
    def get_credential(self, name: str) -> Optional[Credential]:
        """Get stored credentials by name"""
        return self.credentials.get(name)
    
    def grant_permission(self, user: str, capability: str, level: PermissionLevel):
        """
        Grant permission to a user for a capability
        
        Args:
            user: User identifier
            capability: Capability name
            level: Permission level
        """
        if user not in self.permissions:
            self.permissions[user] = []
        
        permission = Permission(
            capability=capability,
            level=level,
            granted_by="system"
        )
        
        self.permissions[user].append(permission)
    
    def check_permission(self, user: str, capability: str, level: PermissionLevel) -> bool:
        """
        Check if user has permission for capability
        
        Args:
            user: User identifier
            capability: Capability name
            level: Required permission level
            
        Returns:
            True if user has permission, False otherwise
        """
        if user not in self.permissions:
            return False
        
        user_permissions = self.permissions[user]
        
        for perm in user_permissions:
            if perm.capability == capability or perm.capability == "*":
                # Check if permission level is sufficient
                if perm.level == PermissionLevel.ADMIN:
                    return True
                if perm.level == level:
                    return True
        
        return False
    
    def revoke_permission(self, user: str, capability: str):
        """Revoke permission from user"""
        if user in self.permissions:
            self.permissions[user] = [
                p for p in self.permissions[user]
                if p.capability != capability
            ]
    
    def list_permissions(self, user: str) -> List[Permission]:
        """List all permissions for a user"""
        return self.permissions.get(user, [])
    
    def authenticate(self, credential_name: str) -> bool:
        """
        Authenticate using stored credentials
        
        In production, this would validate credentials against the service
        """
        return credential_name in self.credentials
    
    def rotate_credential(self, name: str, new_credential: Credential):
        """Rotate/update a credential"""
        if name in self.credentials:
            old_credential = self.credentials[name]
            self.credentials[name] = new_credential
            # In production, invalidate old credential
            return True
        return False
