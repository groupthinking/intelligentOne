"""
💾 Blueprint Vault - Persistent recipe storage
Stores and manages workflow blueprints (evolved recipes)
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class BlueprintVault:
    """
    Manages persistent storage of workflow blueprints.
    
    Blueprints are stored as JSON files in the ./blueprints/ directory.
    Each blueprint represents a tested and approved workflow recipe.
    """
    
    def __init__(self, storage_path: str = "./blueprints"):
        """
        Initialize the Blueprint Vault.
        
        Args:
            storage_path: Directory path for storing blueprints
        """
        self.storage_path = storage_path
        self._ensure_storage_exists()
        print(f"💾 Blueprint Vault initialized: {self.storage_path}")
    
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
            print(f"📁 Created blueprint storage: {self.storage_path}")
    
    def _get_blueprint_path(self, name: str) -> str:
        """
        Get the file path for a blueprint.
        
        Args:
            name: Blueprint name
        
        Returns:
            Full file path
        """
        # Sanitize name for filesystem
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        return os.path.join(self.storage_path, f"{safe_name}.json")
    
    def store_blueprint(self, name: str, blueprint: Dict[str, Any]) -> bool:
        """
        Store a blueprint to persistent storage.
        
        Args:
            name: Unique name for the blueprint
            blueprint: Blueprint data to store
        
        Returns:
            True if successfully stored, False otherwise
        """
        try:
            filepath = self._get_blueprint_path(name)
            
            # Add metadata
            blueprint['name'] = name
            blueprint['updated_at'] = datetime.now().isoformat()
            
            if not blueprint.get('created_at'):
                blueprint['created_at'] = datetime.now().isoformat()
            
            # Write to file
            with open(filepath, 'w') as f:
                json.dump(blueprint, f, indent=2)
            
            print(f"💾 Stored blueprint: {name}")
            return True
        
        except Exception as e:
            print(f"❌ Error storing blueprint: {str(e)}")
            return False
    
    def load_all_blueprints(self) -> List[Dict[str, Any]]:
        """
        Load all blueprints from storage.
        
        Returns:
            List of all stored blueprints
        """
        blueprints = []
        
        try:
            if not os.path.exists(self.storage_path):
                return blueprints
            
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.storage_path, filename)
                    try:
                        with open(filepath, 'r') as f:
                            blueprint = json.load(f)
                            blueprints.append(blueprint)
                    except Exception as e:
                        print(f"⚠️  Error loading {filename}: {str(e)}")
            
            print(f"💾 Loaded {len(blueprints)} blueprints")
            return blueprints
        
        except Exception as e:
            print(f"❌ Error loading blueprints: {str(e)}")
            return []
    
    def get_blueprint(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific blueprint by name.
        
        Args:
            name: Name of the blueprint to retrieve
        
        Returns:
            Blueprint data if found, None otherwise
        """
        try:
            filepath = self._get_blueprint_path(name)
            
            if not os.path.exists(filepath):
                print(f"⚠️  Blueprint not found: {name}")
                return None
            
            with open(filepath, 'r') as f:
                blueprint = json.load(f)
            
            print(f"💾 Retrieved blueprint: {name}")
            return blueprint
        
        except Exception as e:
            print(f"❌ Error retrieving blueprint: {str(e)}")
            return None
    
    def delete_blueprint(self, name: str) -> bool:
        """
        Delete a blueprint from storage.
        
        Args:
            name: Name of the blueprint to delete
        
        Returns:
            True if successfully deleted, False otherwise
        """
        try:
            filepath = self._get_blueprint_path(name)
            
            if not os.path.exists(filepath):
                print(f"⚠️  Blueprint not found: {name}")
                return False
            
            os.remove(filepath)
            print(f"🗑️  Deleted blueprint: {name}")
            return True
        
        except Exception as e:
            print(f"❌ Error deleting blueprint: {str(e)}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored blueprints.
        
        Returns:
            Statistics dictionary
        """
        blueprints = self.load_all_blueprints()
        
        total = len(blueprints)
        total_runs = sum(bp.get('total_runs', 0) for bp in blueprints)
        total_successes = sum(bp.get('success_count', 0) for bp in blueprints)
        
        success_rate = (total_successes / total_runs * 100) if total_runs > 0 else 0
        
        # Count recent deployments (today)
        today = datetime.now().date().isoformat()
        deployed_today = sum(
            1 for bp in blueprints
            if bp.get('created_at', '').startswith(today)
        )
        
        return {
            'total_blueprints': total,
            'deployed_today': deployed_today,
            'total_runs': total_runs,
            'total_successes': total_successes,
            'success_rate': round(success_rate, 1),
        }
