from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from grist_python_sdk.client.base import BaseGristClient
from grist_python_sdk.typing.orgs import OrganizationInfo


class GristOrganizationClient(BaseGristClient):
    selected_org_id: int | str

    def __init__(
        self,
        root_url: str,
        api_key: str,
        org_info: Optional[int | str] = None,
        org_info_key: Optional[Literal["id", "name"]] = None,
    ) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self.selected_org_id = self.get_organization_id(
            org_info=org_info, org_info_key=org_info_key
        )

    def get_organization_id(
        self,
        org_info: Optional[int | str],
        org_info_key: Optional[Literal["id", "name"]] = None,
    ) -> int | str:
        orgs = self.list_organizations()

        if not orgs:
            raise ValueError("No organizations available.")

        if org_info is not None:
            org = self.describe_organization(
                org_info=org_info, org_info_key=org_info_key
            )
            return org["id"]
        else:
            # If org_info is not provided, let the client select one organization (you can implement your logic here)
            # For now, just select the first organization
            return orgs[0]["id"]

    def list_organizations(self) -> List[OrganizationInfo]:
        orgs_parsed: List[Dict[str, Any]] = self.request(
            method="get", path="orgs", params={}
        )
        orgs: List[OrganizationInfo] = []
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

    def describe_organization(
        self,
        org_info: int | str,
        org_info_key: Optional[Literal["id", "name"]] = None,
    ) -> OrganizationInfo:
        orgs = self.list_organizations()
        org_info_keys = [org_info_key] if org_info_key else ["id", "name"]

        # If org_info is provided, confirm it is in the available organizations
        for org in orgs:
            if (
                sum([org[org_info_key_] == org_info for org_info_key_ in org_info_keys])
                > 0
            ):
                return org

        # If the organization is not found, you can raise an exception or handle as needed
        raise ValueError(f"Organization with ID or name '{org_info}' not found")

    def rename_organization(
        self,
        org_id: int | str,
        new_name: str,
    ) -> OrganizationInfo:
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
