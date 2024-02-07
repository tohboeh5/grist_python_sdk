from copy import deepcopy

import pytest
from grist_python_sdk.client.workspace import WorkspaceClient
from requests_mock import Mocker
from utils import (
    mock_org_dict,
    mock_root_url,
    mock_user_dict,
    mock_ws_dict,
    mock_ws_dict2,
    mock_ws_dict3,
    mock_ws_new_dict,
)


@pytest.fixture
def grist_client(requests_mock: Mocker) -> WorkspaceClient:
    api_key = "your_api_key"
    ws_id = 1
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
    requests_mock.patch(
        f"{mock_root_url}/api/workspaces/1", json=mock_ws_new_dict, status_code=200
    )

    return WorkspaceClient(mock_root_url, api_key, ws_id=ws_id)


def test_describe_workspace(grist_client: WorkspaceClient) -> None:
    ws_details = grist_client.describe_workspace()
    assert ws_details is not None
    assert ws_details["id"] == 1


def test_rename_workspace_endpoint(grist_client: WorkspaceClient) -> None:
    # Mocking the request function to simulate a successful modification
    new_name = "New Ws"

    mock_org_dict_new = deepcopy(mock_org_dict)
    mock_org_dict_new["name"] = new_name  # type:ignore

    # Test the rename_organization method
    modified_ws = grist_client.rename_workspace(new_name=new_name)

    assert modified_ws["id"] == mock_ws_new_dict["id"]
    assert modified_ws["name"] == mock_ws_new_dict["name"]
    assert modified_ws["docs"] == []


def test_list_users_of_workspace(grist_client: WorkspaceClient) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_client.list_users_of_workspace()
    assert users[0]["id"] == mock_user_dict["id"]
    assert users[0]["name"] == mock_user_dict["name"]


def test_delete_workspace(grist_client: WorkspaceClient) -> None:
    grist_client.delete_workspace()
