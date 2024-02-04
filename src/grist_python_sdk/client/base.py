from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from urllib.parse import urljoin

from grist_python_sdk.typing.orgs import Organization
from requests import request


class BaseGristClient:
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

    def get_orgs(self) -> List[Organization]:
        orgs_parsed: List[Dict[str, Any]] = self.request(
            method="get", path="orgs", params={}
        )
        orgs: List[Organization] = []
        for org_parsed in orgs_parsed:
            orgs.append(
                {
                    "id": org_parsed["id"],
                    "name": org_parsed["name"],
                    "domain": org_parsed["domain"],
                    "owner": org_parsed["owner"],
                    "access": org_parsed["access"],
                    "createdAt": datetime.strptime(
                        org_parsed["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    "updatedAt": datetime.strptime(
                        org_parsed["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                }
            )
        return orgs

    def request(
        self,
        method: Literal["get", "post", "put", "delete"],
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
