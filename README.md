# Zalo Mini App Open API SDK for Python

A Python SDK for server-to-server integration with Zalo Mini App Open API.

## What is this SDK?

This SDK provides automated management and development tools for Zalo Mini Apps through server-to-server API integration.
It is designed for Zalo Mini App solution partners.

With this SDK, you can create, deploy, publish, and manage Mini Apps programmatically without manual intervention through the web console.

## Requirements

- Python 3.10 or higher
- API Key from Zalo Mini App
- Zalo App ID

## Install

```bash
pip install zmp_openapi
```

### Development version

```bash
pip install git+https://github.com/thedtvn/zmp-openapi.git
```

## Sync client

```python
from zmp_openapi import OpenAPIClient

client = OpenAPIClient(api_key="YOUR_API_KEY", zalo_app_id="YOUR_APP_ID")
apps = client.get_mini_apps({"offset": 0, "limit": 10})
print(apps)
```

## Async client

```python
import asyncio

from zmp_openapi import AsyncOpenAPIClient


async def main() -> None:
    client = AsyncOpenAPIClient(api_key="YOUR_API_KEY", zalo_app_id="YOUR_APP_ID")
    apps = await client.get_mini_apps({"offset": 0, "limit": 10})
    print(apps)


asyncio.run(main())
```

## Module-level helpers

```python
from zmp_openapi import openapi

apps = openapi.get_apps(offset=0, limit=10)
```

## Documentation

- Local docs landing page: `docs/templates/preload/index.html`

## FAQ

**What can this SDK do?**
It can create Mini Apps, deploy new versions, publish apps to production, list apps and versions, and verify webhook signatures. All operations are automated through server-to-server API calls.

**Is this SDK official?**
This SDK is built based on the official Zalo Mini App Open API documentation available at https://miniapp.zaloplatforms.com/documents/open-apis/partner/.

**Can I use this for both sync and async operations?**
Yes. The SDK provides both `OpenAPIClient` for synchronous operations and `AsyncOpenAPIClient` for asynchronous operations using aiohttp.

## Notes

- Responses return raw JSON or raw text when JSON is not available.
- HTTP errors raise exceptions (requests or aiohttp) on non-2xx responses.
