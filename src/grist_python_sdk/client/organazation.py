from datetime import datetime
from typing import Any, Dict, List

from grist_python_sdk.client.base import BaseGristAPIClient
from grist_python_sdk.client.workspace import WorkspaceClient
from grist_python_sdk.typing.orgs import OrganizationInfo, UserInfo
from grist_python_sdk.typing.workspaces import WorkspaceInfo


class OrganizationClient(BaseGristAPIClient):
    _selected_org_id: int | str

    def __init__(
        self,
        root_url: str,
        api_key: str,
        org_id: int | str,
    ) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self._selected_org_id = org_id

    @property
    def selected_org_id(self) -> int | str:
        return self._selected_org_id

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

    def describe_organization(self) -> OrganizationInfo:
        org_parsed: Dict[str, Any] = self.request(
            method="get",
            path=f"orgs/{self.selected_org_id}",
        )
        return OrganizationClient.parse_organization_info(org_parsed)

    def rename_organization(
        self,
        new_name: str,
    ) -> OrganizationInfo:
        changes = {"name": new_name}
        org_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"orgs/{self.selected_org_id}",
            json=changes,
        )
        return OrganizationClient.parse_organization_info(org_parsed)

    def create_workspace(self, name: str) -> WorkspaceClient:
        ws_id: int = self.request(
            method="post",
            path=f"orgs/{self.selected_org_id}/workspaces",
            params={"name": name},
        )
        return WorkspaceClient(self.root_url, self.api_key, ws_id)

    def list_users_of_organization(self) -> List[UserInfo]:
        users: List[UserInfo] = self.request(
            method="get",
            path=f"orgs/{self.selected_org_id}/access",
        )["users"]
        return users

    def list_workspaces_info(self) -> List[WorkspaceInfo]:
        wss: List[WorkspaceInfo] = []
        wss_parsed: List[Dict[str, Any]] = self.request(
            method="get", path=f"orgs/{self.selected_org_id}/workspaces", params={}
        )
        for ws_parsed in wss_parsed:
            wss.append(WorkspaceClient.parse_workspace_info(ws_parsed))
        return wss
