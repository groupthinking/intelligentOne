"""
intelligentOne - Transform the web into an executable operating system

While traditional systems retrieve information, intelligentOne retrieves capabilities.
"""

from .models import Capability
from .core import IntelligentOne
from .discovery import CapabilityDiscovery
from .executor import CapabilityExecutor

__version__ = "0.1.0"
__all__ = ["IntelligentOne", "Capability", "CapabilityDiscovery", "CapabilityExecutor"]
