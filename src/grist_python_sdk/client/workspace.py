from typing import Any, Dict, List

from grist_python_sdk.typing.orgs import UserInfo
from grist_python_sdk.typing.workspaces import DocumentInfo, WorkspaceInfo

from .base import BaseGristAPIClient
from .doc import DocumentClient
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

    def create_doc(self, name: str) -> DocumentClient:
        doc_id: str = self.request(
            method="post",
            path=f"workspaces/{self.selected_ws_id}/docs",
            json={"name": name},
        )
        return DocumentClient(self.root_url, self.api_key, doc_id)

    def list_docs_info(self) -> List[DocumentInfo]:
        docs_info = self.describe_workspace()["docs"]
        return docs_info

    def get_doc(self, doc_id: str) -> DocumentClient:
        docs = self.list_docs_info()
        if doc_id not in [doc["id"] for doc in docs]:
            raise ValueError(f"Doc with id '{doc_id}' not found")
        return DocumentClient(self.root_url, self.api_key, doc_id)

    def find_doc(self, doc_name: str) -> DocumentClient:
        docs = self.list_docs_info()
        selected_docs_ids = [doc["id"] for doc in docs if doc["name"] == doc_name]

        if len(selected_docs_ids) == 1:
            return DocumentClient(self.root_url, self.api_key, selected_docs_ids[0])
        elif len(selected_docs_ids) == 0:
            # If the Doc is not found, you can raise an exception or handle as needed
            raise ValueError(f"Doc with name '{doc_name}' not found")
        else:
            raise ValueError(f"Docs with name '{doc_name}' found 2 or more.")
