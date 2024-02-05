from typing import Any, Dict, List

from grist_python_sdk.client.organazation import OrganizationClient
from grist_python_sdk.typing.orgs import UserInfo
from grist_python_sdk.typing.workspaces import DocumentInfo, WorkspaceInfo


class WorkspaceClient(OrganizationClient):
    _selected_ws_id: int

    def __init__(self, root_url: str, api_key: str, ws_id: int) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self._selected_ws_id = ws_id

    @property
    def selected_ws_id(self) -> int:
        return self._selected_ws_id

    @staticmethod
    def parse_workspace_info(ws_dict: Dict[str, Any]) -> WorkspaceInfo:
        docs: List[DocumentInfo] = []
        for ws_dict_doc in ws_dict["docs"]:
            doc: DocumentInfo = {
                "id": str(ws_dict_doc["id"]),
                "name": str(ws_dict_doc["name"]),
                "access": str(ws_dict_doc["access"]),  # type:ignore
                "isPinned": bool(ws_dict_doc["isPinned"]),
            }
            if "isPinned" in ws_dict_doc.keys():
                doc["urlId"] = str(ws_dict_doc["isPinned"])
            docs.append(doc)
        ws: WorkspaceInfo = {
            "id": int(ws_dict["id"]),
            "name": str(ws_dict["name"]),
            "owner": str(ws_dict["owner"]),  # type:ignore
            "access": str(ws_dict["access"]),  # type:ignore
            "docs": docs,
        }
        if "orgDomain" in ws_dict.keys():
            ws["orgDomain"] = str(ws_dict["orgDomain"])
        return ws

    def describe_workspace(self) -> WorkspaceInfo:
        ws_parsed: Dict[str, Any] = self.request(
            method="get",
            path=f"workspaces/{self.selected_ws_id}",
        )
        return WorkspaceClient.parse_workspace_info(ws_parsed)

    def rename_workspace(self, new_name: str) -> WorkspaceInfo:
        changes = {"name": new_name}
        ws_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"workspaces/{self.selected_ws_id}",
            json=changes,
        )
        return WorkspaceClient.parse_workspace_info(ws_parsed)

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
