from typing import Any, Dict, Optional

import aiohttp

from .client import OpenAPIClient
from .constants import APPS, PUBLISH, REQUEST_PUBLISH, UPLOAD, VERSIONS
from .models import AppInfo, AppSlice, DeployApp, PublishApp, Proxy
from .models import model_to_payload, encode_deploy_file


def _build_proxy_url(proxy: Optional[Proxy]) -> Optional[str]:
    if not proxy:
        return None
    return f"http://{proxy.host}:{proxy.port}"


async def _parse_response(response: aiohttp.ClientResponse) -> Any:
    response.raise_for_status()
    try:
        payload = await response.json()
    except aiohttp.ContentTypeError:
        payload = await response.text()
    return payload


class AsyncOpenAPIClient(OpenAPIClient):
    def __init__(self, api_key: str, zalo_app_id: str, proxy: Optional[Proxy] = None) -> None:
        super().__init__(api_key=api_key, zalo_app_id=zalo_app_id, proxy=proxy)

    async def create_mini_app(self, app_info: AppInfo | Dict[str, Any]) -> Any:
        payload = model_to_payload(app_info)
        proxy_url = _build_proxy_url(self.proxy) if self.is_use_proxy else None
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.DOMAIN}{APPS}",
                json=payload,
                headers=self.headers,
                proxy=proxy_url,
            ) as response:
                return await _parse_response(response)

    async def get_mini_apps(self, app_slice: AppSlice | Dict[str, Any]) -> Any:
        params = model_to_payload(app_slice)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.DOMAIN}{APPS}",
                params=params,
                headers=self.headers,
            ) as response:
                return await _parse_response(response)

    async def deploy_mini_app(self, deploy_app: DeployApp | Dict[str, Any]) -> Any:
        payload = encode_deploy_file(model_to_payload(deploy_app))
        mini_app_id = payload.get("miniAppId")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.DOMAIN}{APPS}/{mini_app_id}{UPLOAD}",
                json=payload,
                headers=self.headers,
            ) as response:
                return await _parse_response(response)

    async def get_versions_mini_app(self, app_slice: AppSlice | Dict[str, Any]) -> Any:
        params = model_to_payload(app_slice)
        mini_app_id = params.get("miniAppId")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.DOMAIN}{APPS}/{mini_app_id}{VERSIONS}",
                params=params,
                headers=self.headers,
            ) as response:
                return await _parse_response(response)

    async def request_publish_mini_app(self, publish_app: PublishApp | Dict[str, Any]) -> Any:
        """
        Request to publish a Mini App version for review (async version).

        This method submits a version for review before it can be published to users.
        The Mini App will need to pass the review process before it can go to production.

        Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

        Args:
            publish_app: Publish request information (PublishApp model or dict) containing:
                - miniAppId (long): ID of the corresponding Mini App
                - versionId (int): ID of the version to request for publishing

        Returns:
            dict: Response containing:
                - error (int): Error code, 0 if request succeeds
                - message (str): Detailed message corresponding to error code

        Raises:
            aiohttp.ClientError: If the API request fails

        Example:
            >>> from zmp_openapi.models import PublishApp
            >>> publish_app = PublishApp(miniAppId=123456, versionId=789)
            >>> response = await client.request_publish_mini_app(publish_app)
            >>> if response['error'] == 0:
            ...     print("Publish request submitted for review")
        """
        payload = model_to_payload(publish_app)
        mini_app_id = payload.get("miniAppId")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.DOMAIN}{APPS}/{mini_app_id}{REQUEST_PUBLISH}",
                json=payload,
                headers=self.headers,
            ) as response:
                return await _parse_response(response)

    async def publish_mini_app(self, publish_app: PublishApp | Dict[str, Any]) -> Any:
        """
        Publish a Mini App version to users (async version).

        This method directly publishes a version to production, making it available to all users.
        The version must have passed the review process (status: READY_TO_PRODUCTION) before it can be published.

        Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

        Args:
            publish_app: Publish information (PublishApp model or dict) containing:
                - miniAppId (long): ID of the corresponding Mini App
                - versionId (int): ID of the version to publish

        Returns:
            dict: Response containing:
                - error (int): Error code, 0 if request succeeds
                - message (str): Detailed message corresponding to error code

        Raises:
            aiohttp.ClientError: If the API request fails

        Example:
            >>> from zmp_openapi.models import PublishApp
            >>> publish_app = PublishApp(miniAppId=123456, versionId=789)
            >>> response = await client.publish_mini_app(publish_app)
            >>> if response['error'] == 0:
            ...     print("Mini App published successfully")
        """
        payload = model_to_payload(publish_app)
        mini_app_id = payload.get("miniAppId")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.DOMAIN}{APPS}/{mini_app_id}{PUBLISH}",
                json=payload,
                headers=self.headers,
            ) as response:
                return await _parse_response(response)
