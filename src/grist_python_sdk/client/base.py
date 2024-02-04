from typing import Any, Dict, Literal, Optional
from urllib.parse import urljoin

from requests import request


class GristBaseClient:
    def __init__(self, root_url: str, api_key: str) -> None:
        self.root_url = root_url
        self.api_key = api_key

    @property
    def headers_with_auth(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def get_url(self, path: str) -> str:
        api_url = urljoin(self.root_url, "/api/")
        return urljoin(api_url, path)

    def request(
        self,
        method: Literal["get", "post", "put", "delete", "patch"],
        path: str,
        params: Optional[Dict[str, str]] = None,
        json: Any = None,
    ) -> Any:
        response = request(
            method=method,
            url=self.get_url(path),
            params=params,
            headers=self.headers_with_auth,
            json=json,
        )
        response.raise_for_status()
        return response.json()
