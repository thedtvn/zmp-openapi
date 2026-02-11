"""
Data models for Zalo Mini App Open API.

This module contains Pydantic models for API requests and helper functions
for payload conversion and file encoding.

Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/
"""

import base64
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Proxy(BaseModel):
    """
    Proxy configuration for API requests.

    Attributes:
        host: Proxy server hostname or IP address
        port: Proxy server port number
    """
    host: str
    port: int


class AppInfo(BaseModel):
    """
    Mini App information for creation.

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/create-mini-app/

    Attributes:
        app_name: Name of the Mini App (3-50 characters)
        app_description: Description of the Mini App (20-500 characters)
        app_category: App category
        app_logo_url: URL of the app logo image
        browsable: Allow public display on Zalo and Mini App Store
    """
    model_config = ConfigDict(populate_by_name=True)

    app_name: str = Field(alias="appName")
    app_description: str = Field(alias="appDescription")
    app_category: str = Field(alias="appCategory")
    app_logo_url: str = Field(alias="appLogoUrl")
    browsable: bool


class AppSlice(BaseModel):
    """
    Pagination parameters for listing Mini Apps or versions.

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/list-mini-apps/

    Attributes:
        mini_app_id: Optional Mini App ID for version listing
        offset: Starting position for pagination
        limit: Number of items to retrieve (maximum 20 for apps)
    """
    model_config = ConfigDict(populate_by_name=True)

    mini_app_id: Optional[str] = Field(default=None, alias="miniAppId")
    offset: int
    limit: int


class DeployApp(BaseModel):
    """
    Deployment information for uploading a Mini App version.

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/deploy-mini-app/

    Attributes:
        mini_app_id: ID of the Mini App
        file: Mini App build file in zip format (str path, bytes, or Path)
        name: Version name
        description: Version description
    """
    model_config = ConfigDict(populate_by_name=True)

    mini_app_id: str = Field(alias="miniAppId")
    file: Union[str, bytes, Path]
    name: str
    description: str


class PublishApp(BaseModel):
    """
    Publish request information for a Mini App version.

    Reference: https://miniapp.zaloplatforms.com/documents/open-apis/partner/publish-mini-app/

    Attributes:
        mini_app_id: ID of the Mini App
        version_id: ID of the version to publish
        description: Optional description for the publish request
    """
    model_config = ConfigDict(populate_by_name=True)

    mini_app_id: str = Field(alias="miniAppId")
    version_id: int = Field(alias="versionId")
    description: Optional[str] = None


def model_to_payload(value: Any) -> Dict[str, Any]:
    """
    Convert a Pydantic model or dict to API payload format.

    Args:
        value: Pydantic model instance or dictionary

    Returns:
        Dictionary with camelCase keys suitable for API requests

    Raises:
        TypeError: If value is neither a BaseModel nor a dict
    """
    if isinstance(value, BaseModel):
        return value.model_dump(by_alias=True, exclude_none=True)
    if isinstance(value, dict):
        return value
    raise TypeError("Payload must be a dict or pydantic model")


def encode_deploy_file(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Encode file content to base64 for deployment.

    Converts file paths, Path objects, or bytes to base64-encoded strings
    for upload to the Zalo Mini App API.

    Args:
        payload: Deployment payload dictionary containing 'file' field

    Returns:
        Payload with 'file' field encoded as base64 string
    """
    if "file" not in payload:
        return payload

    file_value = payload["file"]
    if isinstance(file_value, Path):
        file_bytes = file_value.read_bytes()
        payload["file"] = base64.b64encode(file_bytes).decode("ascii")
        return payload

    if isinstance(file_value, bytes):
        payload["file"] = base64.b64encode(file_value).decode("ascii")
        return payload

    if isinstance(file_value, str):
        path = Path(file_value)
        if path.is_file():
            payload["file"] = base64.b64encode(path.read_bytes()).decode("ascii")
        return payload

    return payload
