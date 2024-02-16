from typing import Any, Dict, List, TypedDict

from grist_python_sdk.client import GristAPIClient

from .typing import ColumnInfo, TableInfo
from .utils import parse_table_info


def list_tables_info(client: GristAPIClient, doc_id: str) -> List[TableInfo]:
    tables_info: List[Dict[str, Any]] = client.request(
        method="get", path=f"docs/{doc_id}/tables"
    )["tables"]
    return [parse_table_info(table_info) for table_info in tables_info]


def modify_tables(
    client: GristAPIClient,
    doc_id: str,
    tables: List[TableInfo],
) -> None:
    path = f"docs/{doc_id}/tables"
    payload = {"tables": tables}
    client.request(method="patch", path=path, json=payload, return_text=True)


class TableWithColumnsInfo(TypedDict):
    id: str
    columns: List[ColumnInfo]


def add_tables(
    client: GristAPIClient,
    doc_id: str,
    tables: List[TableWithColumnsInfo],
) -> List[str]:
    path = f"docs/{doc_id}/tables"
    payload = {"tables": tables}
    response = client.request(method="post", path=path, json=payload)
    return [table["id"] for table in response["tables"]]
