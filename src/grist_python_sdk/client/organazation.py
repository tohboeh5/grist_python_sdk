from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from grist_python_sdk.client.base import GristBaseClient
from grist_python_sdk.typing.orgs import OrganizationInfo, UserInfo


class GristOrganizationClient(GristBaseClient):
    selected_org_id: Optional[int | str] = None

    def __init__(
        self,
        root_url: str,
        api_key: str,
        org_info: Optional[int | str] = None,
        org_info_key: Optional[Literal["id", "name"]] = None,
    ) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self.select_organization(org_info=org_info, org_info_key=org_info_key)

    @staticmethod
    def parse_organization_info(org_dict: Dict[str, Any]) -> OrganizationInfo:
        return {
            "id": org_dict["id"],
            "name": str(org_dict["name"]),
            "domain": org_dict["domain"],
            "owner": org_dict["owner"],
            "access": org_dict["access"],
            "createdAt": datetime.strptime(
                org_dict["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "updatedAt": datetime.strptime(
                org_dict["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
        }

    def select_organization(
        self,
        org_info: Optional[int | str],
        org_info_key: Optional[Literal["id", "name"]] = None,
    ) -> None:
        orgs = self.list_organizations()

        if not orgs:
            raise ValueError("No organizations available.")

        if org_info is not None:
            org_info_keys = [org_info_key] if org_info_key else ["id", "name"]

            # If org_info is provided, confirm it is in the available organizations
            for org in orgs:
                if (
                    sum(
                        [
                            org[org_info_key_] == org_info
                            for org_info_key_ in org_info_keys
                        ]
                    )
                    > 0
                ):
                    self.selected_org_id = org["id"]
                    return

            # If the organization is not found, you can raise an exception or handle as needed
            raise ValueError(f"Organization with ID or name '{org_info}' not found")

    def list_organizations(self) -> List[OrganizationInfo]:
        orgs_parsed: List[Dict[str, Any]] = self.request(
            method="get", path="orgs", params={}
        )
        orgs: List[OrganizationInfo] = []
        for org_parsed in orgs_parsed:
            orgs.append(GristOrganizationClient.parse_organization_info(org_parsed))
        return orgs

    def describe_organization(self) -> OrganizationInfo:
        if self.selected_org_id is None:
            raise ValueError("Select org first.")
        org_parsed: Dict[str, Any] = self.request(
            method="get",
            path=f"orgs/{self.selected_org_id}",
        )
        return GristOrganizationClient.parse_organization_info(org_parsed)

    def rename_organization(
        self,
        new_name: str,
    ) -> OrganizationInfo:
        if self.selected_org_id is None:
            raise ValueError("Select org first.")
        changes = {"name": new_name}
        org_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"orgs/{self.selected_org_id}",
            json=changes,
        )
        return GristOrganizationClient.parse_organization_info(org_parsed)

    def list_users_for_organization(self) -> List[UserInfo]:
        if self.selected_org_id is None:
            raise ValueError("Select org first.")
        users: List[UserInfo] = self.request(
            method="get",
            path=f"orgs/{self.selected_org_id}/access",
        )["users"]
        return users
