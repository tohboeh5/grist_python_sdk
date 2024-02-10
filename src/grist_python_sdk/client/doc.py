from typing import Any, Dict, List

from grist_python_sdk.typing.orgs import UserInfo
from grist_python_sdk.typing.workspaces import DocumentInfo, TableInfo

from .base import BaseGristAPIClient
from .table import TableClient
from .utils import parse_document_info, parse_table_info


class DocumentClient(BaseGristAPIClient):
    _selected_doc_id: str

    def __init__(self, root_url: str, api_key: str, doc_id: str) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self._selected_doc_id = doc_id

    @property
    def selected_doc_id(self) -> str:
        return self._selected_doc_id

    def describe_doc(self) -> DocumentInfo:
        doc_parsed: Dict[str, Any] = self.request(
            method="get",
            path=f"docs/{self.selected_doc_id}",
        )
        return parse_document_info(doc_parsed)

    def rename_doc(self, new_name: str) -> DocumentInfo:
        changes = {"name": new_name}
        doc_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"docs/{self.selected_doc_id}",
            json=changes,
        )
        return parse_document_info(doc_parsed)

    def list_users_of_doc(self) -> List[UserInfo]:
        users: List[UserInfo] = self.request(
            method="get",
            path=f"docs/{self.selected_doc_id}/access",
        )["users"]
        return users

    def delete_doc(self) -> None:
        self.request(
            method="delete",
            path=f"docs/{self.selected_doc_id}",
        )
        return None

    def create_table(self, name: str) -> TableClient:
        table_id: str = self.request(
            method="post",
            path=f"docs/{self.selected_doc_id}/tables",
            json={"name": name},
        )
        return TableClient(self.root_url, self.api_key, table_id)

    def list_tables_info(self) -> List[TableInfo]:
        tables_info: List[Dict[str, Any]] = self.request(
            method="get",
            path=f"docs/{self.selected_doc_id}/tables",
        )["tables"]
        return [parse_table_info(table_info) for table_info in tables_info]

    def get_table(self, table_id: str) -> TableClient:
        tables = self.list_tables_info()
        if table_id not in [table["id"] for table in tables]:
            raise ValueError(f"Table with id '{table_id}' not found")
        return TableClient(self.root_url, self.api_key, table_id)
