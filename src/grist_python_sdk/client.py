from typing import Any, Dict, List, Literal, Optional
from urllib.parse import urljoin

from requests import request


class GristAPIClient:
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
        params: Optional[Dict[str, Any]] = None,
        json: Any = None,
        filenames: Optional[List[str]] = None,
        return_type: Literal["json", "text", "content"] = "json",
    ) -> Any:
        if filenames is not None:
            files = [
                ("upload", (open(filename, "rb").name, open(filename, "rb")))
                for filename in filenames
            ]
            response = request(
                method=method,
                url=self.get_url(path),
                params=params,
                headers=self.headers_with_auth,
                files=files,
                json=json,
            )
        else:
            response = request(
                method=method,
                url=self.get_url(path),
                params=params,
                headers=self.headers_with_auth,
                json=json,
            )
        response.raise_for_status()
        if return_type == "json":
            return response.json()
        elif return_type == "text":
            return response.text
        elif return_type == "content":
            return response.content
