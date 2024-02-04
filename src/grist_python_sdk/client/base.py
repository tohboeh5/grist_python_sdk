from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from urllib.parse import urljoin

from grist_python_sdk.typing.orgs import Organization
from requests import request


class BaseGristClient:
    def __init__(
        self, root_url: str, api_key: str, org_info: Optional[int | str] = None
    ) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self.selected_org_id = self.get_organization_id(org_info)

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

    def get_organization_id(self, org_info: Optional[int | str]) -> int | str:
        orgs = self.list_organization()

        if not orgs:
            raise ValueError("No organizations available.")

        if org_info is not None:
            # If org_info is provided, confirm it is in the available organizations
            for org in orgs:
                if org["id"] == org_info or org["name"] == org_info:
                    return org["id"]

            # If the organization is not found, raise an error
            raise ValueError(f"Organization with ID or name '{org_info}' not found")
        else:
            # If org_info is not provided, let the client select one organization (you can implement your logic here)
            # For now, just select the first organization
            return orgs[0]["id"]

    def list_organization(self) -> List[Organization]:
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

    def describe_organization(self, org_info: int | str) -> Organization:
        orgs = self.list_organization()
        for org in orgs:
            if org["id"] == org_info or org["name"] == org_info:
                return org

        # If the organization is not found, you can raise an exception or handle as needed
        raise ValueError(f"Organization with ID or name '{org_info}' not found")

    def rename_organization(
        self,
        org_id: int | str,
        new_name: str,
    ) -> Organization:
        changes = {"name": new_name}
        org_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"orgs/{org_id}",
            json=changes,
        )
        return {
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
