from typing import Any, Dict, Optional

import requests

from .constants import APPS, DOMAIN_PROD, PUBLISH, REQUEST_PUBLISH, UPLOAD, VERSIONS
from .models import DeployApp, model_to_payload, encode_deploy_file
from .models import AppInfo, AppSlice, PublishApp, Proxy
from .version import __version__


def _build_proxy(proxy: Optional[Proxy]) -> Optional[Dict[str, str]]:
    if not proxy:
        return None
    proxy_url = f"http://{proxy.host}:{proxy.port}"
    return {"http": proxy_url, "https": proxy_url}


def _parse_response(response: requests.Response) -> Any:
    response.raise_for_status()
    try:
        payload = response.json()
    except ValueError:
        payload = response.text
    return payload


class OpenAPIClient:
    """
    Zalo Mini App Open API Client for Partner Integration.

    This client provides server-to-server API integration for automating
    Mini App management and development. This feature is only available for
    Zalo Mini App solution partners.

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/

    Args:
        api_key: API Key provided by Zalo Mini App
        zalo_app_id: Your Zalo App ID
        proxy: Optional proxy configuration

    Raises:
        ValueError: If api_key or zalo_app_id is invalid

    Example:
        >>> client = OpenAPIClient(api_key="your_api_key", zalo_app_id="your_app_id")
    """
    DOMAIN = DOMAIN_PROD
    SDK_VERSION = __version__
    SDK_NAME = "Python"

    def __init__(self, api_key: str, zalo_app_id: str, proxy: Optional[Proxy] = None) -> None:
        if not api_key or not zalo_app_id:
            raise ValueError("Invalid init value")
        self.api_key = api_key
        self.zalo_app_id = zalo_app_id
        self.is_use_proxy = False
        self.proxy = None
        if proxy:
            if not proxy.host or not proxy.port:
                raise ValueError("Invalid proxy value")
            self.proxy = proxy
            self.is_use_proxy = True
        self.headers = {
            "X-Api-Key": self.api_key,
            "X-Zalo-AppID": self.zalo_app_id,
            "X-Sdk-Version": self.SDK_VERSION,
            "X-Sdk-Name": self.SDK_NAME,
        }

    def set_proxy(self, proxy: Proxy) -> None:
        """
        Configure proxy settings for API requests.

        Args:
            proxy: Proxy configuration with host and port

        Example:
            >>> from zmp_openapi.models import Proxy
            >>> client.set_proxy(Proxy(host="proxy.example.com", port=8080))
        """
        self.proxy = proxy
        self.is_use_proxy = True

    def cancel_proxy(self) -> None:
        """
        Disable proxy settings and use direct connection.

        Example:
            >>> client.cancel_proxy()
        """
        self.proxy = None
        self.is_use_proxy = False

    def create_mini_app(self, app_info: AppInfo | Dict[str, Any]) -> Any:
        """
        Create a new Mini App for your Zalo App.

        By default, the owner of the Mini App will be set to the owner of your Zalo App.

        Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/create-mini-app/

        Args:
            app_info: Mini App information (AppInfo model or dict) containing:
                - appName (str): Name of the Mini App (3-50 characters, no sensitive keywords or duplicates)
                - appDescription (str): Description of the Mini App (20-500 characters, no sensitive keywords)
                - appCategory (str): App category
                - appSubCategory (str): App sub-category
                - appLogoUrl (str): URL of the app logo image
                - browsable (bool): Allow public display on Zalo and Mini App Store
                - zaloAppId (str, optional): Create Mini App from provided Zalo App. If not provided, a new Zalo App will be created

        Returns:
            dict: Response containing:
                - error (int): Error code, 0 if request succeeds
                - message (str): Detailed message corresponding to error code
                - appId (str): ID of the newly created Mini App
                - appName (str): Name of the newly created Mini App

        Raises:
            requests.HTTPError: If the API request fails

        Example:
            >>> from zmp_openapi.models import AppInfo
            >>> app_info = AppInfo(
            ...     appName="My Mini App",
            ...     appDescription="A description of my mini app",
            ...     appCategory="shopping",
            ...     appSubCategory="fashion",
            ...     appLogoUrl="https://example.com/logo.png",
            ...     browsable=True
            ... )
            >>> response = client.create_mini_app(app_info)
            >>> print(response['appId'])
        """
        payload = model_to_payload(app_info)
        response = requests.post(
            f"{self.DOMAIN}{APPS}",
            json=payload,
            headers=self.headers,
            proxies=_build_proxy(self.proxy) if self.is_use_proxy else None,
        )
        return _parse_response(response)

    def get_mini_apps(self, app_slice: AppSlice | Dict[str, Any]) -> Any:
        """
        Get a list of Mini Apps from your Zalo App.

        Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-mini-apps/

        Args:
            app_slice: Pagination parameters (AppSlice model or dict) containing:
                - offset (int): Starting position
                - limit (int): Number of items to retrieve (maximum 20)

        Returns:
            dict: Response containing:
                - error (int): Error code, 0 if request succeeds
                - message (str): Detailed message corresponding to error code
                - total (int): Total number of Mini Apps in your Zalo App
                - apps (List[AppInfo]): List of Mini Apps corresponding to offset and limit, each containing:
                    - appId (str): Mini App ID
                    - appName (str): Mini App name
                    - appCategory (str): Mini App category
                    - appSubCategory (str): Mini App sub-category
                    - appLogoUrl (str): URL to the Mini App logo
                    - appStatus (str): Current status of the Mini App (ENABLE, DISABLE)

        Raises:
            requests.HTTPError: If the API request fails

        Example:
            >>> from zmp_openapi.models import AppSlice
            >>> app_slice = AppSlice(offset=0, limit=10)
            >>> response = client.get_mini_apps(app_slice)
            >>> print(f"Total apps: {response['total']}")
            >>> for app in response['apps']:
            ...     print(f"App: {app['appName']} (ID: {app['appId']})")
        """
        params = model_to_payload(app_slice)
        response = requests.get(
            f"{self.DOMAIN}{APPS}",
            params=params,
            headers=self.headers,
        )
        return _parse_response(response)

    def deploy_mini_app(self, deploy_app: DeployApp | Dict[str, Any]) -> Any:
        """
        Deploy a new version of your Mini App to the system.

        Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/deploy-mini-app/

        Args:
            deploy_app: Deployment information (DeployApp model or dict) containing:
                - miniAppId (long): ID of the corresponding Mini App
                - file (File): Your Mini App build file in zip format
                - name (str, optional): Version name
                - description (str, optional): Description of the uploaded version

        Returns:
            dict: Response containing:
                - error (int): Error code, 0 if request succeeds
                - message (str): Detailed message corresponding to error code
                - versionId (int): ID of the successfully deployed version
                - entrypoint (str): URL to open the deployed version on Zalo

        Raises:
            requests.HTTPError: If the API request fails

        Example:
            >>> from zmp_openapi.models import DeployApp
            >>> deploy_app = DeployApp(
            ...     miniAppId=123456,
            ...     file=open('miniapp.zip', 'rb'),
            ...     name="v1.0.0",
            ...     description="Initial release"
            ... )
            >>> response = client.deploy_mini_app(deploy_app)
            >>> print(f"Version ID: {response['versionId']}")
            >>> print(f"Entrypoint: {response['entrypoint']}")
        """
        payload = encode_deploy_file(model_to_payload(deploy_app))
        mini_app_id = payload.get("miniAppId")
        response = requests.post(
            f"{self.DOMAIN}{APPS}/{mini_app_id}{UPLOAD}",
            json=payload,
            headers=self.headers,
        )
        return _parse_response(response)

    def get_versions_mini_app(self, app_slice: AppSlice | Dict[str, Any]) -> Any:
        """
        Get a list of versions for a specific Mini App.

        Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-versions/

        Args:
            app_slice: Pagination parameters (AppSlice model or dict) containing:
                - miniAppId (long): ID of the corresponding Mini App
                - offset (int): Starting position
                - limit (int): Number of items to retrieve

        Returns:
            dict: Response containing:
                - error (int): Error code, 0 if request succeeds
                - message (str): Detailed message corresponding to error code
                - total (int): Total number of versions for the Mini App
                - versions (List[AppVersion]): List of versions corresponding to offset and limit, each containing:
                    - versionId (int): Version ID
                    - name (str): Version name
                    - description (str): Version description
                    - lastUpdated (int): Last update timestamp
                    - size (int): Size of the Mini App at this version
                    - entrypoint (str): URL to open this version on Zalo
                    - status (str): Version status (DEVELOPMENT, TESTING, WAITING_APPROVAL, REJECTED, READY_TO_PRODUCTION, PRODUCTION)

        Raises:
            requests.HTTPError: If the API request fails

        Example:
            >>> from zmp_openapi.models import AppSlice
            >>> app_slice = AppSlice(miniAppId=123456, offset=0, limit=10)
            >>> response = client.get_versions_mini_app(app_slice)
            >>> print(f"Total versions: {response['total']}")
            >>> for version in response['versions']:
            ...     print(f"Version: {version['name']} - Status: {version['status']}")
        """
        params = model_to_payload(app_slice)
        mini_app_id = params.get("miniAppId")
        response = requests.get(
            f"{self.DOMAIN}{APPS}/{mini_app_id}{VERSIONS}",
            params=params,
            headers=self.headers,
        )
        return _parse_response(response)

    def request_publish_mini_app(self, publish_app: PublishApp | Dict[str, Any]) -> Any:
        """
        Request to publish a Mini App version for review.

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
            requests.HTTPError: If the API request fails

        Example:
            >>> from zmp_openapi.models import PublishApp
            >>> publish_app = PublishApp(miniAppId=123456, versionId=789)
            >>> response = client.request_publish_mini_app(publish_app)
            >>> if response['error'] == 0:
            ...     print("Publish request submitted for review")
        """
        payload = model_to_payload(publish_app)
        mini_app_id = payload.get("miniAppId")
        response = requests.post(
            f"{self.DOMAIN}{APPS}/{mini_app_id}{REQUEST_PUBLISH}",
            json=payload,
            headers=self.headers,
        )
        return _parse_response(response)

    def publish_mini_app(self, publish_app: PublishApp | Dict[str, Any]) -> Any:
        """
        Publish a Mini App version to users.

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
            requests.HTTPError: If the API request fails

        Example:
            >>> from zmp_openapi.models import PublishApp
            >>> publish_app = PublishApp(miniAppId=123456, versionId=789)
            >>> response = client.publish_mini_app(publish_app)
            >>> if response['error'] == 0:
            ...     print("Mini App published successfully")
        """
        payload = model_to_payload(publish_app)
        mini_app_id = payload.get("miniAppId")
        response = requests.post(
            f"{self.DOMAIN}{APPS}/{mini_app_id}{PUBLISH}",
            json=payload,
            headers=self.headers,
        )
        return _parse_response(response)
