"""
API endpoint constants for Zalo Mini App Open API.

This module contains domain URLs and API path constants used throughout the SDK.

Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/
"""

# API Domain URLs
DOMAIN_PROD = "https://openapi.mini.zalo.me"  # Production API endpoint
DOMAIN_DEV = "http://10.30.80.237:9065"  # Development API endpoint (internal)
DOMAIN = DOMAIN_PROD  # Default domain

# API Path Constants
APPS = "/apps"  # Mini Apps endpoint
UPLOAD = "/upload"  # Upload/deploy version endpoint
VERSIONS = "/versions"  # Versions listing endpoint
REQUEST_PUBLISH = "/request-publish"  # Request publish for review endpoint
PUBLISH = "/publish"  # Direct publish endpoint
