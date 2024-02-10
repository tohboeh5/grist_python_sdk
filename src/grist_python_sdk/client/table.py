from typing import Any, Dict, List, Optional

from grist_python_sdk.typing.orgs import UserInfo
from grist_python_sdk.typing.workspaces import TableInfo

from .base import BaseGristAPIClient

# from .doc import DocumentClient
from .utils import parse_table_info


class TableClient(BaseGristAPIClient):
    _selected_table_id: str

    def __init__(self, root_url: str, api_key: str, doc_id: str, table_id: str) -> None:
        self.root_url = root_url
        self.api_key = api_key
        self._selected_doc_id = doc_id
        self._selected_table_id = table_id

    @property
    def selected_table_id(self) -> str:
        return self._selected_table_id

    @property
    def selected_doc_id(self) -> str:
        return self._selected_doc_id

    def describe_table(self) -> TableInfo:
        raise NotImplementedError

    def modify_table(
        self, tableRef: Optional[str], onDemand: Optional[bool]
    ) -> TableInfo:
        new_fields: Dict[str, Any] = {}
        if tableRef is not None:
            new_fields["tableRef"] = tableRef
        if onDemand is not None:
            new_fields["onDemand"] = onDemand
        table_parsed: Dict[str, Any] = self.request(
            method="patch",
            path=f"docs/{self.selected_doc_id}/tables",
            json={
                "tables": [
                    {
                        "id": self.selected_table_id,
                        "fields": new_fields,
                    }
                ]
            },
        )
        return parse_table_info(table_parsed)

    def list_users_of_table(self) -> List[UserInfo]:
        users: List[UserInfo] = self.request(
            method="get",
            path=f"tables/{self.selected_table_id}/access",
        )["users"]
        return users

    def delete_table(self) -> None:
        self.request(
            method="delete",
            path=f"tables/{self.selected_table_id}",
        )
        return None

    # def get_parent_doc(self) -> DocumentClient:
    #     return DocumentClient(self.root_url, self.api_key, self._selected_doc_id)
