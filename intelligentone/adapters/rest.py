"""
REST API Adapter - Translates REST APIs to OS-level capabilities
"""


class RESTAdapter:
    """
    Adapts REST APIs to intelligentOne capabilities
    
    This adapter handles:
    - HTTP method mapping
    - URL parameter binding
    - Request/response transformation
    - Authentication handling
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        
    def build_request(self, capability, params):
        """
        Build an HTTP request from capability and parameters
        
        Returns:
            dict with request details (url, method, headers, body)
        """
        url = self._build_url(capability.endpoint, params)
        method = capability.method
        headers = self._build_headers(params)
        body = self._build_body(capability, params)
        
        return {
            "url": url,
            "method": method,
            "headers": headers,
            "body": body
        }
    
    def _build_url(self, endpoint, params):
        """Build URL with path and query parameters"""
        # In production, handle path params and query strings
        return endpoint
    
    def _build_headers(self, params):
        """Build request headers"""
        headers = {"Content-Type": "application/json"}
        
        # Handle authentication if provided
        if "auth_token" in params:
            headers["Authorization"] = f"Bearer {params['auth_token']}"
        
        return headers
    
    def _build_body(self, capability, params):
        """Build request body for POST/PUT requests"""
        if capability.method in ["POST", "PUT", "PATCH"]:
            # Filter out special params like auth_token
            body_params = {
                k: v for k, v in params.items()
                if k not in ["auth_token"]
            }
            return body_params
        return None
    
    def parse_response(self, response):
        """Parse HTTP response into capability result"""
        # In production, handle various response types
        return response
