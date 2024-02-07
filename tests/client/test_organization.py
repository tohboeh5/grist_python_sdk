from copy import deepcopy
from datetime import datetime

import pytest
from grist_python_sdk.client.organazation import OrganizationClient
from grist_python_sdk.typing.orgs import OrganizationInfo
from requests_mock import Mocker
from utils import (
    mock_org_dict,
    mock_org_dict2,
    mock_org_dict3,
    mock_org_dict_new,
    mock_root_url,
    mock_user_dict,
    mock_ws_dict,
    mock_ws_dict2,
    mock_ws_dict3,
)


@pytest.fixture
def grist_client(requests_mock: Mocker) -> OrganizationClient:
    api_key = "your_api_key"
    org_id = 1

    requests_mock.get(
        f"{mock_root_url}/api/orgs",
        json=[mock_org_dict, mock_org_dict2, mock_org_dict3],
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
    requests_mock.patch(
        f"{mock_root_url}/api/orgs/{mock_org_dict['id']}",
        json=mock_org_dict_new,
        status_code=200,
    )
    requests_mock.post(
        f"{mock_root_url}/api/orgs/1/workspaces",
        text="2",
        status_code=200,
    )
    requests_mock.get(
        f"{mock_root_url}/api/orgs/1/workspaces",
        json=[mock_ws_dict, mock_ws_dict2, mock_ws_dict3],
        status_code=200,
    )

    return OrganizationClient(mock_root_url, api_key, org_id)


def test_describe_organization(grist_client: OrganizationClient) -> None:
    org_details = grist_client.describe_organization()
    assert org_details is not None
    assert org_details["id"] == 1


def test_rename_organization_endpoint(grist_client: OrganizationClient) -> None:
    # Mocking the request function to simulate a successful modification
    new_name = "New Org"

    mock_org_dict_new = deepcopy(mock_org_dict)
    mock_org_dict_new["name"] = new_name  # type:ignore

    # Test the rename_organization method
    modified_org: OrganizationInfo = grist_client.rename_organization(new_name=new_name)

    assert modified_org["id"] == mock_org_dict["id"]
    assert modified_org["name"] == new_name
    assert modified_org["domain"] == mock_org_dict["domain"]
    assert modified_org["access"] == mock_org_dict["access"]
    assert modified_org["createdAt"] == datetime.strptime(
        str(mock_org_dict["createdAt"]), "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert modified_org["updatedAt"] == datetime.strptime(
        str(mock_org_dict["updatedAt"]), "%Y-%m-%dT%H:%M:%S.%fZ"
    )


def test_list_users_of_organization(grist_client: OrganizationClient) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_client.list_users_of_organization()
    assert users[0]["id"] == mock_user_dict["id"]
    assert users[0]["name"] == mock_user_dict["name"]


def test_create_workspace(grist_client: OrganizationClient) -> None:
    ws = grist_client.create_workspace("New Workspace Name")
    assert ws._selected_ws_id == 2


def test_list_workspaces_info(grist_client: OrganizationClient) -> None:
    ws_response = grist_client.list_workspaces_info()

    assert ws_response[0]["id"] == mock_ws_dict["id"]
    assert ws_response[0]["name"] == mock_ws_dict["name"]
    assert ws_response[0]["docs"] == mock_ws_dict["docs"]
