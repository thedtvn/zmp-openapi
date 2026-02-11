"""
Low-level API functions for Zalo Mini App Open API.

This module provides direct function-based API calls for Zalo Mini App management.
For object-oriented interface with better abstraction, use OpenAPIClient or AsyncOpenAPIClient instead.

Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/
"""

import aiohttp
import requests
from typing import Any, Dict, Optional
from .constants import APPS, DOMAIN_PROD, PUBLISH, REQUEST_PUBLISH, UPLOAD, VERSIONS


def _parse_response(response: requests.Response) -> Any:
    """Parse synchronous HTTP response and handle errors."""
    response.raise_for_status()
    try:
        payload = response.json()
    except ValueError:
        payload = response.text
    return payload


def create_app(data: Dict[str, Any], domain: str = DOMAIN_PROD) -> Any:
    """
    Create a new Mini App (low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/create-mini-app/

    Args:
        data: Mini App information dictionary containing appName, appDescription, appCategory, etc.
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, appId, and appName

    Raises:
        requests.HTTPError: If the API request fails
    """
    response = requests.post(f"{domain}{APPS}", json=data)
    return _parse_response(response)


def get_apps(offset: int, limit: int, domain: str = DOMAIN_PROD) -> Any:
    """
    Get a list of Mini Apps (low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-mini-apps/

    Args:
        offset: Starting position for pagination
        limit: Number of items to retrieve (maximum 20)
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, total count, and apps list

    Raises:
        requests.HTTPError: If the API request fails
    """
    response = requests.get(
        f"{domain}{APPS}",
        params={"offset": offset, "limit": limit},
    )
    return _parse_response(response)


def deploy_app(
    mini_app_id: str,
    data: Dict[str, Any],
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Deploy a new version of a Mini App (low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/deploy-mini-app/

    Args:
        mini_app_id: ID of the Mini App
        data: Deployment data dictionary containing file, name, and description
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, versionId, and entrypoint

    Raises:
        requests.HTTPError: If the API request fails
    """
    response = requests.post(
        f"{domain}{APPS}/{mini_app_id}{UPLOAD}",
        json=data,
    )
    return _parse_response(response)


def get_versions_app(
    mini_app_id: str,
    offset: int,
    limit: int,
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Get a list of versions for a Mini App (low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-versions/

    Args:
        mini_app_id: ID of the Mini App
        offset: Starting position for pagination
        limit: Number of items to retrieve
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, total count, and versions list

    Raises:
        requests.HTTPError: If the API request fails
    """
    response = requests.get(
        f"{domain}{APPS}/{mini_app_id}{VERSIONS}",
        params={"offset": offset, "limit": limit},
    )
    return _parse_response(response)


def request_publish(
    mini_app_id: str,
    version_id: int,
    description: Optional[str] = None,
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Request to publish a Mini App version for review (low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

    Args:
        mini_app_id: ID of the Mini App
        version_id: ID of the version to request for publishing
        description: Optional description for the publish request
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code and message

    Raises:
        requests.HTTPError: If the API request fails
    """
    payload: Dict[str, Any] = {"versionId": version_id}
    if description is not None:
        payload["description"] = description
    response = requests.post(
        f"{domain}{APPS}/{mini_app_id}{REQUEST_PUBLISH}",
        json=payload,
    )
    return _parse_response(response)


def publish(
    mini_app_id: str,
    version_id: int,
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Publish a Mini App version to users (low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

    Args:
        mini_app_id: ID of the Mini App
        version_id: ID of the version to publish
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code and message

    Raises:
        requests.HTTPError: If the API request fails
    """
    response = requests.post(
        f"{domain}{APPS}/{mini_app_id}{PUBLISH}",
        json={"versionId": version_id},
    )
    return _parse_response(response)


async def async_create_app(data: Dict[str, Any], domain: str = DOMAIN_PROD) -> Any:
    """
    Create a new Mini App (async low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/create-mini-app/

    Args:
        data: Mini App information dictionary containing appName, appDescription, appCategory, etc.
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, appId, and appName

    Raises:
        aiohttp.ClientError: If the API request fails
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{domain}{APPS}", json=data) as response:
            return await _parse_async_response(response)


async def async_get_apps(offset: int, limit: int, domain: str = DOMAIN_PROD) -> Any:
    """
    Get a list of Mini Apps (async low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-mini-apps/

    Args:
        offset: Starting position for pagination
        limit: Number of items to retrieve (maximum 20)
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, total count, and apps list

    Raises:
        aiohttp.ClientError: If the API request fails
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{domain}{APPS}",
            params={"offset": offset, "limit": limit},
        ) as response:
            return await _parse_async_response(response)


async def async_deploy_app(
    mini_app_id: str,
    data: Dict[str, Any],
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Deploy a new version of a Mini App (async low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/deploy-mini-app/

    Args:
        mini_app_id: ID of the Mini App
        data: Deployment data dictionary containing file, name, and description
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, versionId, and entrypoint

    Raises:
        aiohttp.ClientError: If the API request fails
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{domain}{APPS}/{mini_app_id}{UPLOAD}",
            json=data,
        ) as response:
            return await _parse_async_response(response)


async def async_get_versions_app(
    mini_app_id: str,
    offset: int,
    limit: int,
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Get a list of versions for a Mini App (async low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-versions/

    Args:
        mini_app_id: ID of the Mini App
        offset: Starting position for pagination
        limit: Number of items to retrieve
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code, message, total count, and versions list

    Raises:
        aiohttp.ClientError: If the API request fails
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{domain}{APPS}/{mini_app_id}{VERSIONS}",
            params={"offset": offset, "limit": limit},
        ) as response:
            return await _parse_async_response(response)


async def async_request_publish(
    mini_app_id: str,
    version_id: int,
    description: Optional[str] = None,
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Request to publish a Mini App version for review (async low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

    Args:
        mini_app_id: ID of the Mini App
        version_id: ID of the version to request for publishing
        description: Optional description for the publish request
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code and message

    Raises:
        aiohttp.ClientError: If the API request fails
    """
    payload: Dict[str, Any] = {"versionId": version_id}
    if description is not None:
        payload["description"] = description
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{domain}{APPS}/{mini_app_id}{REQUEST_PUBLISH}",
            json=payload,
        ) as response:
            return await _parse_async_response(response)


async def async_publish(
    mini_app_id: str,
    version_id: int,
    domain: str = DOMAIN_PROD,
) -> Any:
    """
    Publish a Mini App version to users (async low-level function).

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

    Args:
        mini_app_id: ID of the Mini App
        version_id: ID of the version to publish
        domain: API domain URL (defaults to production)

    Returns:
        dict: Response containing error code and message

    Raises:
        aiohttp.ClientError: If the API request fails
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{domain}{APPS}/{mini_app_id}{PUBLISH}",
            json={"versionId": version_id},
        ) as response:
            return await _parse_async_response(response)


async def _parse_async_response(response: aiohttp.ClientResponse) -> Any:
    """Parse asynchronous HTTP response and handle errors."""
    response.raise_for_status()
    try:
        payload = await response.json()
    except aiohttp.ContentTypeError:
        payload = await response.text()
    return payload
