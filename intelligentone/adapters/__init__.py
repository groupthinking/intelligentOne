"""Web interface adapters for intelligentOne"""

from .rest import RESTAdapter
from .graphql import GraphQLAdapter

__all__ = ["RESTAdapter", "GraphQLAdapter"]
