from copy import deepcopy
from datetime import datetime
from typing import List

import pytest
from grist_python_sdk.client.organazation import GristOrganizationClient
from grist_python_sdk.typing.orgs import OrganizationInfo
from requests_mock import Mocker
from utils import (
    mock_org_dict,
    mock_org_dict2,
    mock_org_dict3,
    mock_root_url,
    mock_user_dict,
)


def test_init_with_no_organizations(
    requests_mock: Mocker,
) -> None:
    api_key = "your_api_key"

    # Mock the orgs endpoint to return an empty list
    requests_mock.get(f"{mock_root_url}/api/orgs", json=[], status_code=200)
    # Test that ValueError is raised when there are no organizations available
    with pytest.raises(ValueError, match="No organizations available."):
        GristOrganizationClient(mock_root_url, api_key)


def test_init_with_no_org_info(
    requests_mock: Mocker,
) -> None:
    api_key = "your_api_key"

    # Mock the orgs endpoint to include at least one organization
    requests_mock.get(
        f"{mock_root_url}/api/orgs", json=[mock_org_dict], status_code=200
    )

    grist_client_with_no_org_info = GristOrganizationClient(mock_root_url, api_key)
    # Mock the orgs endpoint to include at least one organization

    # Test that the _selected_org_id is set to the first organization in the list
    assert grist_client_with_no_org_info._selected_org_id is None


@pytest.fixture
def grist_client_with_selected_org(requests_mock: Mocker) -> GristOrganizationClient:
    api_key = "your_api_key"
    org_info = "Example Org"

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

    return GristOrganizationClient(mock_root_url, api_key, org_info)


def test_select_organization_with_valid_org_name(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    grist_client_with_selected_org.select_organization("Example Org")
    assert grist_client_with_selected_org._selected_org_id == 1


def test_select_organization_with_valid_org_id(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    grist_client_with_selected_org.select_organization(1)
    assert grist_client_with_selected_org._selected_org_id == 1


def test_select_organization_with_invalid_org_info(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    with pytest.raises(
        ValueError, match="Organization with ID or name 'Nonexistent Org' not found"
    ):
        grist_client_with_selected_org.select_organization("Nonexistent Org")


def test_select_organization_with_duplicate_name(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    with pytest.raises(
        ValueError,
        match="Organizations with ID or name 'Example Org 2' found 2 or more.",
    ):
        grist_client_with_selected_org.select_organization("Example Org 2")


def test_describe_organization(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    org_details = grist_client_with_selected_org.describe_organization()
    assert org_details is not None
    assert org_details["id"] == 1


def test_describe_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Reset the _selected_org_id to None
    grist_client_with_selected_org._selected_org_id = None

    # Test that ValueError is raised when describe_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client_with_selected_org.describe_organization()


def test_list_orgs_endpoint(
    requests_mock: Mocker, grist_client_with_selected_org: GristOrganizationClient
) -> None:
    orgs_response: List[
        OrganizationInfo
    ] = grist_client_with_selected_org.list_organizations()

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


def test_rename_organization_endpoint(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
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
    modified_org: OrganizationInfo = grist_client_with_selected_org.rename_organization(
        new_name=new_name
    )

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
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Reset the _selected_org_id to None
    grist_client_with_selected_org._selected_org_id = None

    # Test that ValueError is raised when rename_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client_with_selected_org.rename_organization(new_name="New Org Name")


def test_list_users_of_organization(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_client_with_selected_org.list_users_of_organization()
    assert users[0]["id"] == mock_user_dict["id"]
    assert users[0]["name"] == mock_user_dict["name"]


def test_list_users_of_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Reset the _selected_org_id to None
    grist_client_with_selected_org._selected_org_id = None

    # Test that ValueError is raised when list_users_of_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client_with_selected_org.list_users_of_organization()
