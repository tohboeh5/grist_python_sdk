from datetime import datetime
from typing import Any, Dict, List

import pytest
from grist_python_sdk.client.organazation import GristOrganizationClient
from grist_python_sdk.typing.orgs import OrganizationInfo
from requests_mock import Mocker


def test_init_with_no_organizations(
    requests_mock: Mocker,
) -> None:
    root_url = "https://example.com"
    api_key = "your_api_key"

    # Mock the orgs endpoint to return an empty list
    requests_mock.get(f"{root_url}/api/orgs", json=[], status_code=200)
    # Test that ValueError is raised when there are no organizations available
    with pytest.raises(ValueError, match="No organizations available."):
        GristOrganizationClient(root_url, api_key)


def test_init_with_no_org_info(
    requests_mock: Mocker,
) -> None:
    root_url = "https://example.com"
    api_key = "your_api_key"

    # Mock the orgs endpoint to include at least one organization
    orgs_response = [
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
    requests_mock.get(f"{root_url}/api/orgs", json=orgs_response, status_code=200)

    grist_client_with_no_org_info = GristOrganizationClient(root_url, api_key)
    # Mock the orgs endpoint to include at least one organization
    orgs_response = [{"id": 1, "name": "Example Org"}]
    requests_mock.get(
        "https://example.com/api/orgs", json=orgs_response, status_code=200
    )

    # Test that the selected_org_id is set to the first organization in the list
    assert grist_client_with_no_org_info.selected_org_id is None


@pytest.fixture
def grist_client_with_selected_org(requests_mock: Mocker) -> GristOrganizationClient:
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

    return GristOrganizationClient(root_url, api_key, org_info)


def test_select_organization_with_valid_org_name(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    grist_client_with_selected_org.select_organization("Example Org")
    assert grist_client_with_selected_org.selected_org_id == 1


def test_select_organization_with_valid_org_id(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    grist_client_with_selected_org.select_organization(1)
    assert grist_client_with_selected_org.selected_org_id == 1


def test_select_organization_with_invalid_org_info(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    with pytest.raises(
        ValueError, match="Organization with ID or name 'Nonexistent Org' not found"
    ):
        grist_client_with_selected_org.select_organization("Nonexistent Org")


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
    # Reset the selected_org_id to None
    grist_client_with_selected_org.selected_org_id = None

    # Test that ValueError is raised when describe_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client_with_selected_org.describe_organization()


def test_list_orgs_endpoint(
    requests_mock: Mocker, grist_client_with_selected_org: GristOrganizationClient
) -> None:
    orgs_response: List[
        OrganizationInfo
    ] = grist_client_with_selected_org.list_organizations()

    assert orgs_response[0]["id"] == 1
    assert orgs_response[0]["name"] == "Example Org"
    assert orgs_response[0]["domain"] == "example-domain"
    assert orgs_response[0]["access"] == "owners"
    assert orgs_response[0]["createdAt"] == datetime.strptime(
        "2019-09-13T15:42:35.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert orgs_response[0]["updatedAt"] == datetime.strptime(
        "2019-09-13T15:42:35.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    )


def test_rename_organization_endpoint(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    org_id = 1
    new_name = "New Org Name"
    expected_url = f"https://example.com/api/orgs/{org_id}"
    expected_response: Dict[str, Any] = {
        "id": 1,
        "name": new_name,
        "domain": "example-domain",
        "owner": {"id": 1, "name": "Owner Name"},
        "access": "owners",
        "createdAt": "2019-09-13T15:42:35.000Z",
        "updatedAt": "2024-02-04T12:30:00.000Z",
    }
    requests_mock.patch(expected_url, json=expected_response, status_code=200)

    # Test the rename_organization method
    modified_org: OrganizationInfo = grist_client_with_selected_org.rename_organization(
        new_name=new_name
    )

    assert modified_org["id"] == expected_response["id"]
    assert modified_org["name"] == expected_response["name"]
    assert modified_org["domain"] == expected_response["domain"]
    assert modified_org["access"] == expected_response["access"]
    assert modified_org["createdAt"] == datetime.strptime(
        expected_response["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert modified_org["updatedAt"] == datetime.strptime(
        expected_response["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )


def test_rename_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Reset the selected_org_id to None
    grist_client_with_selected_org.selected_org_id = None

    # Test that ValueError is raised when rename_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client_with_selected_org.rename_organization(new_name="New Org Name")


def test_list_users_of_organization(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    users = grist_client_with_selected_org.list_users_of_organization()
    assert users[0]["id"] == 1
    assert users[0]["name"] == "you@example.com"


def test_list_users_of_organization_without_selecting_org(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Reset the selected_org_id to None
    grist_client_with_selected_org.selected_org_id = None

    # Test that ValueError is raised when list_users_of_organization is called without selecting an org first
    with pytest.raises(ValueError, match="Select org first."):
        grist_client_with_selected_org.list_users_of_organization()
