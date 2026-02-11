"""
Zalo Mini App Open API SDK for Python.

This SDK provides server-to-server API integration for automating Mini App
management and development. It is designed for Zalo Mini App solution partners.

Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/

Main Components:
    - OpenAPIClient: Synchronous client for API operations
    - AsyncOpenAPIClient: Asynchronous client for API operations
    - AppInfo, AppSlice, DeployApp, PublishApp: Data models for API requests
    - VerifySignature: Webhook signature verification utility
    - AppCategory: Predefined app category constants
    - openapi: Low-level API functions
    - constants: API endpoint constants

Quick Start:
    >>> from zmp_openapi import OpenAPIClient, AppInfo
    >>>
    >>> # Initialize client
    >>> client = OpenAPIClient(api_key="your_api_key", zalo_app_id="your_app_id")
    >>>
    >>> # Create a mini app
    >>> app_info = AppInfo(
    ...     appName="My Mini App",
    ...     appDescription="A description of my mini app",
    ...     appCategory="shopping",
    ...     appSubCategory="fashion",
    ...     appLogoUrl="https://example.com/logo.png",
    ...     browsable=True
    ... )
    >>> response = client.create_mini_app(app_info)
    >>> print(f"Created app: {response['appId']}")

For async operations:
    >>> import asyncio
    >>> from zmp_openapi import AsyncOpenAPIClient
    >>>
    >>> async def main():
    ...     client = AsyncOpenAPIClient(api_key="your_api_key", zalo_app_id="your_app_id")
    ...     apps = await client.get_mini_apps({"offset": 0, "limit": 10})
    ...     return apps
    >>>
    >>> asyncio.run(main())
"""

from .app_category import AppCategory
from . import constants
from .client import OpenAPIClient
from .async_client import AsyncOpenAPIClient
from .models import AppInfo, AppSlice, DeployApp, PublishApp, Proxy
from .verify_signature import VerifySignature
from . import openapi
from .version import __version__

__all__ = [
    "AppCategory",
    "AppInfo",
    "AppSlice",
    "AsyncOpenAPIClient",
    "DeployApp",
    "OpenAPIClient",
    "PublishApp",
    "Proxy",
    "VerifySignature",
    "openapi",
    "__version__",
]
