from typing import Any, Dict, List

from grist_python_sdk.client import GristAPIClient

from .typing import Access, DocumentInfo, UserInfo
from .utils import parse_document_info


def create_doc(
    client: GristAPIClient, ws_id: int, name: str, pinned: bool = False
) -> str:
    doc_id: str = client.request(
        method="post",
        path=f"workspaces/{ws_id}/docs",
        json={"name": name, "isPinned": pinned},
        return_text=True,
    )
    return doc_id


def describe_doc(client: GristAPIClient, doc_id: str) -> DocumentInfo:
    doc_parsed: Dict[str, Any] = client.request(method="get", path=f"docs/{doc_id}")
    return parse_document_info(doc_parsed)


def rename_doc(client: GristAPIClient, doc_id: str, new_name: str) -> None:
    changes = {"name": new_name}
    client.request(method="patch", path=f"docs/{doc_id}", json=changes)


def change_doc_pinned_state(
    client: GristAPIClient, doc_id: str, is_pinned: bool
) -> None:
    changes = {"isPinned": is_pinned}
    client.request(method="patch", path=f"docs/{doc_id}", json=changes)


def delete_doc(client: GristAPIClient, doc_id: str) -> None:
    client.request(method="delete", path=f"docs/{doc_id}")


def list_users_of_doc(client: GristAPIClient, doc_id: str) -> List[UserInfo]:
    users: List[UserInfo] = client.request(method="get", path=f"docs/{doc_id}/access")[
        "users"
    ]
    return users


def change_users_of_doc(
    client: GristAPIClient, doc_id: str, users_info: List[Dict[str, Access]]
) -> List[UserInfo]:
    delta_info: Dict[str, Any] = {"delta": {"users": users_info}}
    users: List[UserInfo] = client.request(
        method="patch", path=f"docs/{doc_id}/access", json=delta_info
    )["users"]
    return users
