from typing import Any, Dict, List

import pytest
from grist_python_sdk.client.workspace import WorkspaceClient
from grist_python_sdk.typing.workspaces import WorkspaceInfo
from requests_mock import Mocker
from utils import (
    mock_org_dict,
    mock_root_url,
    mock_user_dict,
    mock_ws_dict,
    mock_ws_dict2,
    mock_ws_dict3,
)


@pytest.fixture
def grist_workspace_client_with_selected_ws(
    requests_mock: Mocker,
) -> WorkspaceClient:
    api_key = "your_api_key"
    requests_mock.get(
        f"{mock_root_url}/api/orgs",
        json=[mock_org_dict],
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1", json=mock_org_dict, status_code=200
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1/access",
        json={"users": [mock_user_dict]},
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1/workspaces",
        json=[mock_ws_dict, mock_ws_dict2, mock_ws_dict3],
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/workspaces/1",
        json=mock_ws_dict,
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/workspaces/1/access",
        json={"users": [mock_user_dict]},
        status_code=200,
    )
    requests_mock.post(
        f"{mock_root_url}/api/orgs/1/workspaces",
        text="2",
        status_code=200,
    )
    requests_mock.delete(
        f"{mock_root_url}/api/workspaces/1",
        json={},
        status_code=200,
    )

    return WorkspaceClient(
        mock_root_url,
        api_key,
        org_info=str(mock_org_dict["name"]),
        ws_info="Workspace 1",
    )


def test_list_workspaces_endpoint(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    ws_response: List[
        WorkspaceInfo
    ] = grist_workspace_client_with_selected_ws.list_workspaces()

    assert ws_response[0]["id"] == mock_ws_dict["id"]
    assert ws_response[0]["name"] == mock_ws_dict["name"]
    assert ws_response[0]["docs"] == mock_ws_dict["docs"]


def test_list_workspaces_without_select_org(
    requests_mock: Mocker,
    grist_workspace_client_without_selected_org: WorkspaceClient,
) -> None:
    with pytest.raises(ValueError, match="Select organization first."):
        grist_workspace_client_without_selected_org.list_workspaces()


def test_list_for_all_organization_workspaces_endpoint(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    ws_response: List[
        WorkspaceInfo
    ] = grist_workspace_client_with_selected_ws.list_workspaces(True)

    assert ws_response[0]["id"] == mock_ws_dict["id"]
    assert ws_response[0]["name"] == mock_ws_dict["name"]
    assert ws_response[0]["docs"] == mock_ws_dict["docs"]


def test_describe_workspace(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    ws_details = grist_workspace_client_with_selected_ws.describe_workspace()
    assert ws_details is not None
    assert ws_details["id"] == 1


def test_describe_workspace_without_selecting_ws(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.select_ws_by_id(None)

    # Test that ValueError is raised when describe_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.describe_workspace()


def test_rename_workspace_endpoint(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    ws_id = 1
    new_name = "New Workspace Name"
    expected_url = f"https://example.com/api/workspaces/{ws_id}"
    expected_response: Dict[str, Any] = {
        "id": ws_id,
        "name": new_name,
        "docs": [],
    }
    requests_mock.patch(expected_url, json=expected_response, status_code=200)

    # Test the rename_workspace method
    modified_ws: WorkspaceInfo = (
        grist_workspace_client_with_selected_ws.rename_workspace(new_name=new_name)
    )

    assert modified_ws["id"] == expected_response["id"]
    assert modified_ws["name"] == expected_response["name"]
    assert modified_ws["docs"] == []


def test_rename_workspace_without_selecting_ws(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.select_ws_by_id(None)

    # Test that ValueError is raised when rename_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.rename_workspace(
            new_name="New Workspace Name"
        )


def test_list_users_of_workspace(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_workspace_client_with_selected_ws.list_users_of_workspace()
    assert users[0]["id"] == mock_user_dict["id"]
    assert users[0]["name"] == mock_user_dict["name"]


def test_list_users_of_workspace_without_selecting_ws(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.select_ws_by_id(None)

    # Test that ValueError is raised when list_users_of_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.list_users_of_workspace()


def test_create_worlspace(
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    grist_workspace_client_with_selected_ws.create_workspace("New Workspace Name")
    assert grist_workspace_client_with_selected_ws.selected_ws_id == 2


def test_delete_worlspace(
    grist_workspace_client_with_selected_ws: WorkspaceClient,
) -> None:
    grist_workspace_client_with_selected_ws.delete_workspace()
    assert grist_workspace_client_with_selected_ws.selected_ws_id is None
