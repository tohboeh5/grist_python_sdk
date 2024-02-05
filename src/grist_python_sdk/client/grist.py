from typing import Any, Dict, List

from grist_python_sdk.client.organazation import OrganizationClient
from grist_python_sdk.client.workspace import WorkspaceClient
from grist_python_sdk.typing.orgs import OrganizationInfo
from grist_python_sdk.typing.workspaces import WorkspaceInfo

from .base import BaseGristAPIClient


class GristAPIClient(BaseGristAPIClient):
    def get_organization(self, org_id: int | str) -> OrganizationClient:
        orgs = self.list_organizations_info()
        if org_id not in [org["id"] for org in orgs]:
            raise ValueError(f"Organization with id '{org_id}' not found")
        return OrganizationClient(self.root_url, self.api_key, org_id)

    def find_organization(self, org_name: str) -> OrganizationClient:
        orgs = self.list_organizations_info()
        selected_org_ids = [org["id"] for org in orgs if org["name"] == org_name]

        if len(selected_org_ids) == 1:
            return OrganizationClient(self.root_url, self.api_key, selected_org_ids[0])
        elif len(selected_org_ids) == 0:
            # If the organization is not found, you can raise an exception or handle as needed
            raise ValueError(f"Organization with name '{org_name}' not found")
        else:
            raise ValueError(f"Organizations with name '{org_name}' found 2 or more.")

    def get_workspace(self, ws_id: int) -> WorkspaceClient:
        wss = self.list_workspaces_info()
        if ws_id not in [ws["id"] for ws in wss]:
            raise ValueError(f"Workspace with id '{ws_id}' not found")
        return WorkspaceClient(self.root_url, self.api_key, ws_id)

    def find_workspace(self, ws_name: str) -> WorkspaceClient:
        wss = self.list_workspaces_info()
        selected_wss_ids = [ws["id"] for ws in wss if ws["name"] == ws_name]

        if len(selected_wss_ids) == 1:
            return WorkspaceClient(self.root_url, self.api_key, selected_wss_ids[0])
        elif len(selected_wss_ids) == 0:
            # If the workspace is not found, you can raise an exception or handle as needed
            raise ValueError(f"Workspace with name '{ws_name}' not found")
        else:
            raise ValueError(f"Workspaces with name '{ws_name}' found 2 or more.")

    def list_organizations_info(self) -> List[OrganizationInfo]:
        orgs_parsed: List[Dict[str, Any]] = self.request(
            method="get", path="orgs", params={}
        )
        orgs: List[OrganizationInfo] = []
        for org_parsed in orgs_parsed:
            orgs.append(OrganizationClient.parse_organization_info(org_parsed))
        return orgs

    def list_workspaces_info(self) -> List[WorkspaceInfo]:
        wss: List[WorkspaceInfo] = []
        orgs = self.list_organizations_info()
        for org in orgs:
            wss_parsed_now: List[Dict[str, Any]] = self.request(
                method="get",
                path=f"orgs/{org['id']}/workspaces",
                params={},
            )
            for ws_parsed in wss_parsed_now:
                wss.append(WorkspaceClient.parse_workspace_info(ws_parsed))
        return wss
