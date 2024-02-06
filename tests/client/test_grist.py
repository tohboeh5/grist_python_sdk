from datetime import datetime

import pytest
from grist_python_sdk.client.grist import GristAPIClient
from requests_mock import Mocker
from utils import (
    mock_org_dict,
    mock_org_dict2,
    mock_org_dict3,
    mock_root_url,
    mock_ws_dict,
    mock_ws_dict2,
    mock_ws_dict3,
    mock_ws_dict4,
    mock_ws_dict5,
)


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    api_key = "your_api_key"

    requests_mock.get(
        f"{mock_root_url}/api/orgs",
        json=[mock_org_dict, mock_org_dict2, mock_org_dict3],
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1", json=mock_org_dict, status_code=200
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1/workspaces",
        json=[mock_ws_dict, mock_ws_dict2, mock_ws_dict3],
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/2/workspaces",
        json=[mock_ws_dict4],
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/3/workspaces",
        json=[mock_ws_dict5],
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/workspaces/1",
        json=mock_ws_dict,
        status_code=200,
    )
    return GristAPIClient(mock_root_url, api_key)


def test_get_organization(grist_client: GristAPIClient) -> None:
    organization = grist_client.get_organization(1)
    assert organization._selected_org_id == 1


def test_get_organization_with_invalid_id(grist_client: GristAPIClient) -> None:
    with pytest.raises(ValueError, match="not found"):
        grist_client.get_organization(100)


def test_find_organization(grist_client: GristAPIClient) -> None:
    organization = grist_client.find_organization("Example Org")
    assert organization._selected_org_id == 1


def test_find_organization_with_invalid_name(grist_client: GristAPIClient) -> None:
    with pytest.raises(ValueError, match="not found"):
        grist_client.find_organization("Nonexistent Org")


def test_find_organization_with_duplicate_name(grist_client: GristAPIClient) -> None:
    with pytest.raises(ValueError, match="found 2 or more."):
        grist_client.find_organization("Example Org 2")


def test_list_organizations_info(grist_client: GristAPIClient) -> None:
    orgs_response = grist_client.list_organizations_info()

    assert orgs_response[0]["id"] == mock_org_dict["id"]
    assert orgs_response[0]["name"] == mock_org_dict["name"]
    assert orgs_response[0]["domain"] == mock_org_dict["domain"]
    assert orgs_response[0]["access"] == mock_org_dict["access"]
    assert orgs_response[0]["createdAt"] == datetime.strptime(
        str(mock_org_dict["createdAt"]),
        "%Y-%m-%dT%H:%M:%S.%fZ",
    )
    assert orgs_response[0]["updatedAt"] == datetime.strptime(
        str(mock_org_dict["updatedAt"]), "%Y-%m-%dT%H:%M:%S.%fZ"
    )


def test_get_workspace(grist_client: GristAPIClient) -> None:
    workspace = grist_client.get_workspace(1)
    assert workspace._selected_ws_id == 1


def test_get_workspace_with_invalid_id(grist_client: GristAPIClient) -> None:
    with pytest.raises(ValueError, match="not found"):
        grist_client.get_workspace(100)


def test_find_workspace(grist_client: GristAPIClient) -> None:
    workspace = grist_client.find_workspace("Workspace 1")
    assert workspace.selected_ws_id == 1


def test_find_workspace_with_invalid_name(grist_client: GristAPIClient) -> None:
    with pytest.raises(ValueError, match="not found"):
        grist_client.find_workspace("Nonexistent Ws")


def test_find_workspace_with_duplicate_name(grist_client: GristAPIClient) -> None:
    with pytest.raises(ValueError, match="found 2 or more."):
        grist_client.find_workspace("Workspace 2")


def test_list_workspaces_info(grist_client: GristAPIClient) -> None:
    ws_response = grist_client.list_workspaces_info()

    assert ws_response[0]["id"] == mock_ws_dict["id"]
    assert ws_response[0]["name"] == mock_ws_dict["name"]
    assert ws_response[0]["docs"] == mock_ws_dict["docs"]
