from typing import Any, Dict, List

from grist_python_sdk.typing.orgs import UserInfo
from grist_python_sdk.typing.workspaces import WorkspaceInfo

from .base import BaseGristAPIClient
from .utils import parse_workspace_info


class WorkspaceClient(BaseGristAPIClient):
    _selected_ws_id: int

    def __init__(self, root_url: str, api_key: str, ws_id: int) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self._selected_ws_id = ws_id

    @property
    def selected_ws_id(self) -> int:
        return self._selected_ws_id

    def describe_workspace(self) -> WorkspaceInfo:
        ws_parsed: Dict[str, Any] = self.request(
            method="get",
            path=f"workspaces/{self.selected_ws_id}",
        )
        return parse_workspace_info(ws_parsed)

    def rename_workspace(self, new_name: str) -> WorkspaceInfo:
        changes = {"name": new_name}
        ws_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"workspaces/{self.selected_ws_id}",
            json=changes,
        )
        return parse_workspace_info(ws_parsed)

    def list_users_of_workspace(self) -> List[UserInfo]:
        users: List[UserInfo] = self.request(
            method="get",
            path=f"workspaces/{self.selected_ws_id}/access",
        )["users"]
        return users

    def delete_workspace(self) -> None:
        self.request(
            method="delete",
            path=f"workspaces/{self.selected_ws_id}",
        )
        return None
