from typing import Any, Dict, List

from grist_python_sdk.client import GristAPIClient

from .typing import Access, UserInfo, WorkspaceInfo
from .utils import parse_workspace_info


def list_workspaces_info(
    client: GristAPIClient, org_id: str | int
) -> List[WorkspaceInfo]:
    wss: List[WorkspaceInfo] = []
    wss_parsed: List[Dict[str, Any]] = client.request(
        method="get", path=f"orgs/{org_id}/workspaces", params={}
    )
    for ws_parsed in wss_parsed:
        wss.append(parse_workspace_info(ws_parsed))
    return wss


def describe_workspace(client: GristAPIClient, ws_id: int) -> WorkspaceInfo:
    ws_parsed: Dict[str, Any] = client.request(method="get", path=f"workspaces/{ws_id}")
    return parse_workspace_info(ws_parsed)


def list_users_of_workspace(client: GristAPIClient, ws_id: int) -> List[UserInfo]:
    users: List[UserInfo] = client.request(
        method="get", path=f"workspaces/{ws_id}/access"
    )["users"]
    return users


def change_users_of_workspace(
    client: GristAPIClient, ws_id: int, users_info: List[Dict[str, Access]]
) -> List[UserInfo]:
    delta_info: Dict[str, Any] = {"delta": {"users": users_info}}
    users: List[UserInfo] = client.request(
        method="patch", path=f"workspaces/{ws_id}/access", json=delta_info
    )["users"]
    return users


def delete_workspace(client: GristAPIClient, ws_id: int) -> None:
    client.request(method="delete", path=f"workspaces/{ws_id}")


def rename_workspace(
    client: GristAPIClient, ws_id: int, new_name: str
) -> WorkspaceInfo:
    changes = {"name": new_name}
    ws_parsed: Dict[str, Any] = client.request(
        method="patch", path=f"workspaces/{ws_id}", json=changes
    )
    return parse_workspace_info(ws_parsed)


def create_workspace(client: GristAPIClient, org_id: str | int, name: str) -> str:
    ws_id: str = client.request(
        method="post",
        path=f"orgs/{org_id}/workspaces",
        params={"name": name},
        return_text=True,
    )
    return ws_id
