from typing import Any, Dict, List, Optional

from grist_python_sdk.client import GristAPIClient

from .typing import RecordInfo


def fetch_records(
    client: GristAPIClient,
    doc_id: str,
    table_id: str,
    filterstring: Optional[str] = None,
    sortstring: Optional[str] = None,
    limitnumber: Optional[int] = None,
    hidden: Optional[bool] = None,
) -> List[RecordInfo]:
    path = f"docs/{doc_id}/tables/{table_id}/records"
    params = {
        "filterstring": filterstring,
        "sortstring": sortstring,
        "limitnumber": limitnumber,
        "hidden": hidden,
    }
    records_parsed = client.request(method="get", path=path, params=params)["records"]
    records: List[RecordInfo] = [
        {"id": int(record_parsed["id"]), "fields": record_parsed["fields"]}
        for record_parsed in records_parsed
    ]
    return records


def add_records(
    client: GristAPIClient,
    doc_id: str,
    table_id: str,
    records: List[Dict[str, Any]],
    noparse: Optional[bool] = None,
) -> List[int]:
    path = f"docs/{doc_id}/tables/{table_id}/records"
    params = {"noparse": noparse} if noparse is not None else None
    payload = {"records": records}
    response = client.request(method="post", path=path, params=params, json=payload)
    return [int(record["id"]) for record in response["records"]]


def patch_records(
    client: GristAPIClient,
    doc_id: str,
    table_id: str,
    records: List[Dict[str, Any]],
    noparse: Optional[bool] = None,
) -> None:
    path = f"docs/{doc_id}/tables/{table_id}/records"
    params = {"noparse": noparse} if noparse is not None else None
    payload = {"records": records}
    client.request(
        method="patch", path=path, params=params, json=payload, return_type="text"
    )


def put_records(
    client: GristAPIClient,
    doc_id: str,
    table_id: str,
    records: List[Dict[str, Any]],
    noparse: Optional[bool] = None,
    onmany: Optional[str] = None,
    noadd: Optional[bool] = None,
    noupdate: Optional[bool] = None,
    allow_empty_require: Optional[bool] = None,
) -> None:
    path = f"docs/{doc_id}/tables/{table_id}/records"
    params = {
        "noparse": noparse,
        "onmany": onmany,
        "noadd": noadd,
        "noupdate": noupdate,
        "allow_empty_require": allow_empty_require,
    }
    payload = {"records": records}
    client.request(
        method="put", path=path, params=params, json=payload, return_type="text"
    )
