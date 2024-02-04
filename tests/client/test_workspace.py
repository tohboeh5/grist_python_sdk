from typing import Any, Dict, List

import pytest
from grist_python_sdk.client.organazation import GristOrganizationClient
from grist_python_sdk.client.workspace import GristWorkspaceClient
from grist_python_sdk.typing.workspaces import WorkspaceInfo
from requests_mock import Mocker


@pytest.fixture
def grist_workspace_client_with_selected_ws(
    requests_mock: Mocker,
) -> GristWorkspaceClient:
    root_url = "https://example.com"
    api_key = "your_api_key"
    org_info = "Example Org"

    orgs_response_list = [
        {
            "id": 1,
            "name": "Example Org",
            "domain": "example-domain",
            "owner": {"id": 1, "name": "Owner Name"},
            "access": "owners",
            "createdAt": "2019-09-13T15:42:35.000Z",
            "updatedAt": "2019-09-13T15:42:35.000Z",
        },
    ]
    requests_mock.get(f"{root_url}/api/orgs", json=orgs_response_list, status_code=200)

    orgs_response_describe: Dict[str, Any] = {
        "id": 1,
        "name": "Example Org",
        "domain": "example-domain",
        "owner": {"id": 1, "name": "Owner Name"},
        "access": "owners",
        "createdAt": "2019-09-13T15:42:35.000Z",
        "updatedAt": "2019-09-13T15:42:35.000Z",
    }
    requests_mock.get(
        f"{root_url}/api/orgs/1", json=orgs_response_describe, status_code=200
    )

    expected_url_list_users = "https://example.com/api/orgs/1/access"
    expected_response_list_users: Dict[str, Any] = {
        "users": [
            {
                "id": 1,
                "email": "you@example.com",
                "name": "you@example.com",
                "access": "owners",
                "isMember": True,
            }
        ]
    }
    requests_mock.get(
        expected_url_list_users, json=expected_response_list_users, status_code=200
    )

    expected_response_ws_list = [
        {
            "id": 1,
            "name": "Workspace 1",
            "access": "owners",
            "owner": {"id": 1, "name": "Owner Name"},
            "docs": [
                {"id": "doc1", "name": "doc1", "access": "owners", "isPinned": True}
            ],
        },
        {
            "id": 2,
            "name": "Workspace 2",
            "access": "owners",
            "owner": {"id": 1, "name": "Owner Name"},
            "docs": [
                {"id": "doc2", "name": "doc2", "access": "owners", "isPinned": True}
            ],
        },
    ]
    requests_mock.get(
        f"{root_url}/api/orgs/1/workspaces",
        json=expected_response_ws_list,
        status_code=200,
    )

    return GristWorkspaceClient(
        root_url, api_key, org_info=org_info, ws_info="Workspace 1"
    )


def test_init_with_no_workspaces(
    requests_mock: Mocker,
) -> None:
    root_url = "https://example.com"
    api_key = "your_api_key"
    org_info = "Example Org"

    # Mock the workspaces endpoint to return an empty list
    requests_mock.get(
        f"{root_url}/api/orgs/1/workspaces",
        json=[],
        status_code=200,
    )

    # Test that ValueError is raised when there are no workspaces available
    with pytest.raises(ValueError, match="No Workspaces available."):
        GristWorkspaceClient(root_url, api_key, org_info)


def test_init_with_no_ws_info(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristOrganizationClient,
) -> None:
    root_url = "https://example.com"
    api_key = "your_api_key"
    org_info = "Example Org"

    # Mock the workspaces endpoint to include at least one workspace
    ws_response = [
        {
            "id": 1,
            "name": "Example Workspace",
            "docs": [],
        },
    ]
    requests_mock.get(
        f"{root_url}/api/orgs/{grist_workspace_client_with_selected_ws.selected_org_id}/workspaces",
        json=ws_response,
        status_code=200,
    )

    grist_client_with_no_ws_info = GristWorkspaceClient(
        root_url, api_key, org_info=org_info
    )
    # Test that the selected_ws_id is set to the first workspace in the list
    assert grist_client_with_no_ws_info.selected_ws_id == 1


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

    assert ws_response[0]["id"] == 1
    assert ws_response[0]["name"] == "Example Workspace"
    assert ws_response[0]["docs"] == []


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
    assert users[0]["id"] == 1
    assert users[0]["name"] == "you@example.com"


def test_list_users_of_workspace_without_selecting_ws(
    requests_mock: Mocker,
    grist_workspace_client_with_selected_ws: GristWorkspaceClient,
) -> None:
    # Reset the selected_ws_id to None
    grist_workspace_client_with_selected_ws.selected_ws_id = None

    # Test that ValueError is raised when list_users_of_workspace is called without selecting a workspace first
    with pytest.raises(ValueError, match="Select workspace first."):
        grist_workspace_client_with_selected_ws.list_users_of_workspace()
