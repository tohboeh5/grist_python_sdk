from typing import List, Optional

from grist_python_sdk.client import GristAPIClient

from .typing import ColumnInfo


def list_columns(
    client: GristAPIClient, doc_id: str, table_id: str, hidden: Optional[bool] = None
) -> List[ColumnInfo]:
    path = f"docs/{doc_id}/tables/{table_id}/columns"
    params = {"hidden": hidden} if hidden is not None else None
    columns_parsed = client.request(method="get", path=path, params=params)["columns"]
    columns: List[ColumnInfo] = [
        {"id": column_parsed["id"], "fields": column_parsed["fields"]}
        for column_parsed in columns_parsed
    ]
    return columns


def add_columns(
    client: GristAPIClient, doc_id: str, table_id: str, columns: List[ColumnInfo]
) -> List[str]:
    path = f"docs/{doc_id}/tables/{table_id}/columns"
    payload = {"columns": columns}
    response = client.request(method="post", path=path, json=payload)["columns"]
    return [col["id"] for col in response]


def patch_columns(
    client: GristAPIClient, doc_id: str, table_id: str, columns: List[ColumnInfo]
) -> None:
    path = f"docs/{doc_id}/tables/{table_id}/columns"
    payload = {"columns": columns}
    client.request(method="patch", path=path, json=payload, return_type="text")


def put_columns(
    client: GristAPIClient,
    doc_id: str,
    table_id: str,
    columns: List[ColumnInfo],
    noadd: Optional[bool] = None,
    noupdate: Optional[bool] = None,
    replaceall: Optional[bool] = None,
) -> None:
    path = f"docs/{doc_id}/tables/{table_id}/columns"
    params = {"noadd": noadd, "noupdate": noupdate, "replaceall": replaceall}
    payload = {"columns": columns}
    client.request(
        method="put", path=path, params=params, json=payload, return_type="text"
    )


def delete_column(
    client: GristAPIClient, doc_id: str, table_id: str, col_id: str
) -> None:
    path = f"docs/{doc_id}/tables/{table_id}/columns/{col_id}"
    client.request(method="delete", path=path, return_type="text")
