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
    assert grist_client_with_no_org_info.selected_org_id == 1


@pytest.fixture
def grist_client_with_selected_org(requests_mock: Mocker) -> GristOrganizationClient:
    root_url = "https://example.com"
    api_key = "your_api_key"
    org_info = "Example Org"

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

    return GristOrganizationClient(root_url, api_key, org_info)


def test_get_organization_id_with_valid_org_name(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    selected_org_id = grist_client_with_selected_org.get_organization_id("Example Org")
    assert selected_org_id == 1


def test_get_organization_id_with_valid_org_id(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    selected_org_id = grist_client_with_selected_org.get_organization_id(1)
    assert selected_org_id == 1


def test_get_organization_id_with_invalid_org_info(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    with pytest.raises(
        ValueError, match="Organization with ID or name 'Nonexistent Org' not found"
    ):
        grist_client_with_selected_org.get_organization_id("Nonexistent Org")


def test_describe_organization(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    org_details = grist_client_with_selected_org.describe_organization(1)
    assert org_details is not None
    assert org_details["id"] == 1


def test_describe_organization_with_invalid_org_info(
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    with pytest.raises(
        ValueError, match="Organization with ID or name 'Nonexistent Org' not found"
    ):
        grist_client_with_selected_org.describe_organization("Nonexistent Org")


def test_base_grist_client_request_with_incorrect_api_key(
    requests_mock: Mocker,
    grist_client_with_selected_org: GristOrganizationClient,
) -> None:
    # Mocking the request function to simulate an incorrect API key error
    requests_mock.request(
        method="get",
        url="https://example.com/api/path",
        headers=grist_client_with_selected_org.headers_with_auth,
        status_code=401,  # Unauthorized
        reason="Unauthorized",
    )

    # Test the request method with an incorrect API key
    with pytest.raises(Exception, match="Unauthorized"):
        grist_client_with_selected_org.request("get", "path")


def test_list_orgs_endpoint(
    requests_mock: Mocker, grist_client_with_selected_org: GristOrganizationClient
) -> None:
    expected_url = "https://example.com/api/orgs"
    expected_response: List[Dict[str, Any]] = [
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
    requests_mock.get(expected_url, json=expected_response, status_code=200)

    orgs_response: List[
        OrganizationInfo
    ] = grist_client_with_selected_org.list_organizations()

    assert orgs_response[0]["id"] == expected_response[0]["id"]
    assert orgs_response[0]["name"] == expected_response[0]["name"]
    assert orgs_response[0]["domain"] == expected_response[0]["domain"]
    assert orgs_response[0]["access"] == expected_response[0]["access"]
    assert orgs_response[0]["createdAt"] == datetime.strptime(
        expected_response[0]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    assert orgs_response[0]["updatedAt"] == datetime.strptime(
        expected_response[0]["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
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
        org_id=org_id, new_name=new_name
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
