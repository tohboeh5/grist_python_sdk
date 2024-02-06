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
    mock_root_url,
    mock_user_dict,
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

    return OrganizationClient(mock_root_url, api_key, org_id)


def test_describe_organization(
    grist_client: OrganizationClient,
) -> None:
    org_details = grist_client.describe_organization()
    assert org_details is not None
    assert org_details["id"] == 1


def test_describe_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client: OrganizationClient,
) -> None:
    # Reset the selected_org_id to None
    grist_client.select_org_by_id(None)

    # Test that ValueError is raised when describe_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client.describe_organization()


def test_rename_organization_endpoint(
    requests_mock: Mocker,
    grist_client: OrganizationClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    new_name = "New Org Name"

    mock_org_dict_new = deepcopy(mock_org_dict)
    mock_org_dict_new["name"] = new_name  # type:ignore
    requests_mock.patch(
        f"{mock_root_url}/api/orgs/{mock_org_dict['id']}",
        json=mock_org_dict_new,
        status_code=200,
    )

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


def test_rename_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client: OrganizationClient,
) -> None:
    # Reset the selected_org_id to None
    grist_client.select_org_by_id(None)

    # Test that ValueError is raised when rename_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client.rename_organization(new_name="New Org Name")


def test_list_users_of_organization(
    requests_mock: Mocker,
    grist_client: OrganizationClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_client.list_users_of_organization()
    assert users[0]["id"] == mock_user_dict["id"]
    assert users[0]["name"] == mock_user_dict["name"]


def test_list_users_of_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client: OrganizationClient,
) -> None:
    # Reset the selected_org_id to None
    grist_client.select_org_by_id(None)

    # Test that ValueError is raised when list_users_of_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client.list_users_of_organization()
