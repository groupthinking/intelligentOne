"""
GraphQL Adapter - Translates GraphQL APIs to OS-level capabilities
"""


class GraphQLAdapter:
    """
    Adapts GraphQL APIs to intelligentOne capabilities
    
    This adapter handles:
    - Query/mutation construction
    - Variable binding
    - Schema introspection
    - Subscription management
    """
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        
    def build_query(self, operation, variables=None):
        """
        Build a GraphQL query/mutation
        
        Args:
            operation: GraphQL query or mutation string
            variables: Variables to bind to the operation
            
        Returns:
            dict with GraphQL request payload
        """
        return {
            "query": operation,
            "variables": variables or {}
        }
    
    def introspect_schema(self):
        """
        Introspect GraphQL schema to discover capabilities
        
        Returns introspection query result
        """
        introspection_query = """
        query IntrospectionQuery {
            __schema {
                queryType { name }
                mutationType { name }
                subscriptionType { name }
                types {
                    ...FullType
                }
            }
        }
        fragment FullType on __Type {
            kind
            name
            description
            fields(includeDeprecated: true) {
                name
                description
                args {
                    name
                    description
                    type { ...TypeRef }
                }
                type { ...TypeRef }
            }
        }
        fragment TypeRef on __Type {
            kind
            name
            ofType {
                kind
                name
            }
        }
        """
        return self.build_query(introspection_query)
    
    def parse_response(self, response):
        """Parse GraphQL response"""
        # In production, handle errors and extract data
        if "data" in response:
            return response["data"]
        elif "errors" in response:
            raise Exception(f"GraphQL errors: {response['errors']}")
        return response
