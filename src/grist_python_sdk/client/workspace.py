from typing import Any, Dict, List, Literal, Optional

from grist_python_sdk.client.organazation import GristOrganizationClient
from grist_python_sdk.typing.orgs import UserInfo
from grist_python_sdk.typing.workspaces import WorkspaceInfo


class GristWorkspaceClient(GristOrganizationClient):
    selected_ws_id: Optional[int] = None

    def __init__(
        self,
        root_url: str,
        api_key: str,
        org_info: Optional[int | str] = None,
        org_info_key: Optional[Literal["id", "name"]] = None,
        ws_info: Optional[int] = None,
        ws_info_key: Optional[Literal["id", "name"]] = None,
    ) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self.select_organization(org_info=org_info, org_info_key=org_info_key)
        self.select_workspace(ws_info=ws_info, ws_info_key=ws_info_key)

    @staticmethod
    def parse_workspace_info(ws_dict: Dict[str, Any]) -> WorkspaceInfo:
        ws_dict["id"] = int(ws_dict["id"])
        ws_dict["name"] = str(ws_dict["name"])
        for doc in ws_dict["docs"]:
            doc["id"] = str(doc["id"])
            doc["name"] = str(doc["name"])
            doc["isPinned"] = str(doc["isPinned"])

        return ws_dict  # type:ignore

    def select_workspace(
        self,
        ws_info: Optional[int],
        ws_info_key: Optional[Literal["id", "name"]] = None,
    ) -> None:
        orgs = self.list_workspaces()

        if not orgs:
            raise ValueError("No Workspaces available.")

        if ws_info is not None:
            ws_info_keys = [ws_info_key] if ws_info_key else ["id", "name"]

            # If ws_info is provided, confirm it is in the available Workspaces
            for org in orgs:
                if (
                    sum([org[ws_info_key_] == ws_info for ws_info_key_ in ws_info_keys])
                    > 0
                ):
                    self.selected_ws_id = org["id"]
                    return

            # If the Workspace is not found, you can raise an exception or handle as needed
            raise ValueError(f"Workspace with ID or name '{ws_info}' not found")

    def list_workspaces(self, all_organization: bool = False) -> List[WorkspaceInfo]:
        wss: List[WorkspaceInfo] = []
        if not all_organization:
            if self.selected_ws_id is None:
                raise ValueError("Select organization first.")
            wss_parsed: List[Dict[str, Any]] = self.request(
                method="get", path=f"orgs/{self.selected_org_id}/workspaces", params={}
            )
            for ws_parsed in wss_parsed:
                wss.append(GristWorkspaceClient.parse_workspace_info(ws_parsed))
        else:
            orgs = self.list_organizations()
            for org in orgs:
                wss_parsed_now: List[Dict[str, Any]] = self.request(
                    method="get",
                    path=f"orgs/{self.selected_org_id}/workspaces",
                    params={},
                )
                for ws_parsed in wss_parsed_now:
                    wss.append(GristWorkspaceClient.parse_workspace_info(ws_parsed))
        return wss

    def describe_workspace(self) -> WorkspaceInfo:
        if self.selected_ws_id is None:
            raise ValueError("Select workspace first.")
        ws_parsed: Dict[str, Any] = self.request(
            method="get",
            path=f"workspaces/{self.selected_ws_id}",
        )
        return GristWorkspaceClient.parse_workspace_info(ws_parsed)

    def rename_workspace(
        self,
        new_name: str,
    ) -> WorkspaceInfo:
        if self.selected_ws_id is None:
            raise ValueError("Select workspace first.")
        changes = {"name": new_name}
        ws_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"workspaces/{self.selected_ws_id}",
            json=changes,
        )
        return GristWorkspaceClient.parse_workspace_info(ws_parsed)

    def list_users_of_workspace(self) -> List[UserInfo]:
        if self.selected_ws_id is None:
            raise ValueError("Select workspace first.")
        users: List[UserInfo] = self.request(
            method="get",
            path=f"workspaces/{self.selected_ws_id}/access",
        )["users"]
        return users
