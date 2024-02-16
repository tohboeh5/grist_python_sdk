from typing import Dict, List

import pytest
from grist_python_sdk.api.organazation import (
    change_users_of_organization,
    describe_organization,
    list_organizations_info,
    list_users_of_organization,
    rename_organization,
)
from grist_python_sdk.api.typing import Access
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_organization_info(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    requests_mock.get(
        f"{mock_root_url}/api/orgs",
        status_code=200,
        text="""[
      {
        "id": 42,
        "name": "Grist Labs",
        "domain": "gristlabs",
        "owner": {
          "id": 101,
          "name": "Helga Hufflepuff",
          "picture": null
        },
        "access": "owners",
        "createdAt": "2019-09-13T15:42:35.000Z",
        "updatedAt": "2019-09-13T15:42:35.000Z"
      }
    ]""",
    )
    organizations_info = list_organizations_info(grist_client)
    assert organizations_info[0]["id"] == 42
    assert organizations_info[0]["name"] == "Grist Labs"


def test_describe_organization(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    requests_mock.get(
        f"{mock_root_url}/api/orgs/42",
        status_code=200,
        text="""{
  "id": 42,
  "name": "Grist Labs",
  "domain": "gristlabs",
  "owner": {
    "id": 101,
    "name": "Helga Hufflepuff",
    "picture": null
  },
  "access": "owners",
  "createdAt": "2019-09-13T15:42:35.000Z",
  "updatedAt": "2019-09-13T15:42:35.000Z"
}""",
    )
    org_info = describe_organization(grist_client, 42)
    assert org_info["id"] == 42
    assert org_info["name"] == "Grist Labs"


def test_rename_organization(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    org_id = 42
    new_name = "New Name"
    requests_mock.patch(
        f"{mock_root_url}/api/orgs/{org_id}",
        status_code=200,
        json={"id": org_id, "name": new_name},
    )
    rename_organization(grist_client, org_id, new_name)


def test_list_users_of_organization(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    org_id = 42
    requests_mock.get(
        f"{mock_root_url}/api/orgs/{org_id}/access",
        status_code=200,
        json={
            "users": [
                {
                    "id": 1,
                    "name": "Andrea",
                    "email": "andrea@getgrist.com",
                    "access": "owners",
                }
            ]
        },
    )
    users = list_users_of_organization(grist_client, org_id)
    assert len(users) == 1
    assert users[0]["id"] == 1
    assert users[0]["name"] == "Andrea"


def test_change_users_of_organization(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    org_id = 42
    users_info: List[Dict[str, Access]] = [
        {"foo@getgrist.com": "owners", "bar@getgrist.com": None}
    ]
    requests_mock.patch(
        f"{mock_root_url}/api/orgs/{org_id}/access",
        status_code=200,
        json={
            "users": [
                {
                    "id": 1,
                    "name": "Andrea",
                    "email": "andrea@getgrist.com",
                    "access": "owners",
                }
            ]
        },
    )
    users = change_users_of_organization(grist_client, org_id, users_info)
    assert len(users) == 1
    if users:  # Check if the list is not empty before accessing its elements
        assert users[0]["id"] == 1
