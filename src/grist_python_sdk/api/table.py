from typing import Any, Dict, List, Optional

from grist_python_sdk.client import GristAPIClient

from .typing import TableInfo
from .utils import parse_table_info


def list_tables_info(client: GristAPIClient, doc_id: str) -> List[TableInfo]:
    tables_info: List[Dict[str, Any]] = client.request(
        method="get", path=f"docs/{doc_id}/tables"
    )["tables"]
    return [parse_table_info(table_info) for table_info in tables_info]


def modify_table(
    client: GristAPIClient,
    doc_id: str,
    table_id: str,
    tableRef: Optional[str],
    onDemand: Optional[bool],
) -> TableInfo:
    new_fields: Dict[str, Any] = {}
    if tableRef is not None:
        new_fields["tableRef"] = tableRef
    if onDemand is not None:
        new_fields["onDemand"] = onDemand
    table_parsed: Dict[str, Any] = client.request(
        method="patch",
        path=f"docs/{doc_id}/tables",
        json={
            "tables": [
                {
                    "id": table_id,
                    "fields": new_fields,
                }
            ]
        },
    )
    return parse_table_info(table_parsed)
