from typing import Any, Dict, List

import pytest
from grist_python_sdk.client.workspace import GristWorkspaceClient
from grist_python_sdk.typing.workspaces import WorkspaceInfo
from requests_mock import Mocker
from utils import mock_org_dict, mock_root_url, mock_user_dict, mock_ws_dict


@pytest.fixture
def grist_workspace_client_with_selected_ws(
    requests_mock: Mocker,
) -> GristWorkspaceClient:
    api_key = "your_api_key"
    requests_mock.get(
        f"{mock_root_url}/api/orgs", json=[mock_org_dict], status_code=200
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
        json=[mock_ws_dict],
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

    return GristWorkspaceClient(
        mock_root_url,
        api_key,
        org_info=str(mock_org_dict["name"]),
        ws_info="Workspace 1",
    )


@pytest.fixture
def grist_workspace_client_without_selected_ws(
    requests_mock: Mocker,
) -> GristWorkspaceClient:
    api_key = "your_api_key"
    requests_mock.get(
        f"{mock_root_url}/api/orgs", json=[mock_org_dict], status_code=200
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
        json=[mock_ws_dict],
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

    return GristWorkspaceClient(
        mock_root_url,
        api_key,
        org_info=str(mock_org_dict["name"]),
    )


def test_init_with_no_workspaces(
    requests_mock: Mocker,
) -> None:
    api_key = "your_api_key"
    requests_mock.get(
        f"{mock_root_url}/api/orgs", json=[mock_org_dict], status_code=200
    )

    # Mock the workspaces endpoint to return an empty list
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1/workspaces",
        json=[],
        status_code=200,
    )

    # Test that ValueError is raised when there are no workspaces available
    with pytest.raises(ValueError, match="No Workspaces available."):
        GristWorkspaceClient(mock_root_url, api_key, org_info=1)


def test_init_with_no_org_info(
    requests_mock: Mocker,
) -> None:
    root_url = "https://example.com"
    api_key = "your_api_key"
    requests_mock.get(
        f"{mock_root_url}/api/orgs", json=[mock_org_dict], status_code=200
    )

    # Mock the workspaces endpoint to include at least one workspace
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1/workspaces",
        json=[mock_ws_dict],
        status_code=200,
    )

    grist_client_with_no_ws_info = GristWorkspaceClient(root_url, api_key)
    # Test that the selected_ws_id is set to the first workspace in the list
    assert grist_client_with_no_ws_info.selected_org_id is None
    assert grist_client_with_no_ws_info.selected_ws_id is None


def test_init_with_no_ws_info(
    requests_mock: Mocker,
    grist_workspace_client_without_selected_ws: GristWorkspaceClient,
) -> None:
    # Test that the selected_ws_id is set to the first workspace in the list
    assert grist_workspace_client_without_selected_ws.selected_ws_id is None


def test_select_workspace_with_valid_ws_name(
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    grist_workspace_client_with_selected_ws.select_workspace("Workspace 1")
    assert grist_workspace_client_with_selected_ws.selected_ws_id == 1


def test_select_workspace_with_valid_ws_id(
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    grist_workspace_client_with_selected_ws.select_workspace(1)
    assert grist_workspace_client_with_selected_ws.selected_ws_id == 1


def test_select_workspace_with_invalid_ws_info(
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    with pytest.raises(
        ValueError, match="Workspace with ID or name 'Nonexistent Workspace' not found"
    ):
        grist_workspace_client_with_selected_ws.select_workspace(
            "Nonexistent Workspace"
        )


def test_list_workspaces_endpoint(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    ws_response: List[
        WorkspaceInfo
    ] = grist_workspace_client_with_selected_ws.list_workspaces()

    assert ws_response[0]["id"] == mock_ws_dict["id"]
    assert ws_response[0]["name"] == mock_ws_dict["name"]
    assert ws_response[0]["docs"] == mock_ws_dict["docs"]


def test_describe_workspace(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    ws_details = grist_workspace_client_with_selected_ws.describe_workspace()
    assert ws_details is not None
    assert ws_details["id"] == 1


def test_describe_workspace_without_selecting_ws(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.selected_ws_id = None

    # Test that ValueError is raised when describe_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.describe_workspace()


def test_rename_workspace_endpoint(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
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
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.selected_ws_id = None

    # Test that ValueError is raised when rename_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.rename_workspace(
            new_name="New Workspace Name"
        )


def test_list_users_of_workspace(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_workspace_client_with_selected_ws.list_users_of_workspace()
    assert users[0]["id"] == mock_user_dict["id"]
    assert users[0]["name"] == mock_user_dict["name"]


def test_list_users_of_workspace_without_selecting_ws(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.selected_ws_id = None

    # Test that ValueError is raised when list_users_of_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.list_users_of_workspace()
