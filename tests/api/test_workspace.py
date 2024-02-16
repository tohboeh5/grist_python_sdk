import pytest
from grist_python_sdk.api.workspace import (
    change_users_of_workspace,
    create_workspace,
    delete_workspace,
    describe_workspace,
    list_users_of_workspace,
    list_workspaces_info,
    rename_workspace,
)
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_list_workspaces_info(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    org_id = "your_org_id"
    requests_mock.get(
        f"{mock_root_url}/api/orgs/{org_id}/workspaces",
        status_code=200,
        json=[
            {
                "id": 97,
                "name": "Secret Plans",
                "access": "owners",
                "docs": [
                    {
                        "id": 145,
                        "name": "Project Lollipop",
                        "access": "owners",
                        "isPinned": True,
                        "urlId": None,
                    }
                ],
                "orgDomain": "gristlabs",
            }
        ],
    )
    workspaces_info = list_workspaces_info(grist_client, org_id)
    assert workspaces_info[0]["id"] == 97
    assert workspaces_info[0]["name"] == "Secret Plans"


def test_describe_workspace(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    workspace_id = 97
    requests_mock.get(
        f"{mock_root_url}/api/workspaces/{workspace_id}",
        status_code=200,
        json={
            "id": 97,
            "name": "Secret Plans",
            "access": "owners",
            "docs": [
                {
                    "id": 145,
                    "name": "Project Lollipop",
                    "access": "owners",
                    "isPinned": True,
                    "urlId": None,
                }
            ],
            "org": {
                "id": 42,
                "name": "Grist Labs",
                "domain": "gristlabs",
                "owner": {"id": 101, "name": "Helga Hufflepuff", "picture": None},
                "access": "owners",
                "createdAt": "2019-09-13T15:42:35.000Z",
                "updatedAt": "2019-09-13T15:42:35.000Z",
            },
        },
    )
    workspace_info = describe_workspace(grist_client, workspace_id)
    assert workspace_info["id"] == 97
    assert workspace_info["name"] == "Secret Plans"


def test_list_users_of_workspace(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    workspace_id = 97
    requests_mock.get(
        f"{mock_root_url}/api/workspaces/{workspace_id}/access",
        status_code=200,
        json={
            "maxInheritedRole": "owners",
            "users": [
                {
                    "id": 1,
                    "name": "Andrea",
                    "email": "andrea@getgrist.com",
                    "access": "owners",
                    "parentAccess": "owners",
                }
            ],
        },
    )
    users_info = list_users_of_workspace(grist_client, workspace_id)
    assert users_info[0]["id"] == 1
    assert users_info[0]["name"] == "Andrea"


def test_change_users_of_workspace(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    workspace_id = 97
    users_info = [{"foo@getgrist.com": "owners", "bar@getgrist.com": None}]
    requests_mock.patch(
        f"{mock_root_url}/api/workspaces/{workspace_id}/access",
        status_code=200,
        json={
            "maxInheritedRole": "owners",
            "users": [
                {
                    "id": 1,
                    "name": "Andrea",
                    "email": "andrea@getgrist.com",
                    "access": "owners",
                    "parentAccess": "owners",
                }
            ],
        },
    )
    updated_users_info = change_users_of_workspace(
        grist_client, workspace_id, users_info
    )
    assert updated_users_info[0]["id"] == 1
    assert updated_users_info[0]["name"] == "Andrea"


def test_delete_workspace(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    workspace_id = 97
    requests_mock.delete(
        f"{mock_root_url}/api/workspaces/{workspace_id}", status_code=200, json={}
    )
    delete_workspace(grist_client, workspace_id)


def test_rename_workspace(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    workspace_id = 97
    new_name = "New Plans"
    requests_mock.patch(
        f"{mock_root_url}/api/workspaces/{workspace_id}",
        status_code=200,
        json={
            "id": 97,
            "name": new_name,
            "access": "owners",
            "docs": [
                {
                    "id": 145,
                    "name": "Project Lollipop",
                    "access": "owners",
                    "isPinned": True,
                    "urlId": None,
                }
            ],
            "org": {
                "id": 42,
                "name": "Grist Labs",
                "domain": "gristlabs",
                "owner": {"id": 101, "name": "Helga Hufflepuff", "picture": None},
                "access": "owners",
                "createdAt": "2019-09-13T15:42:35.000Z",
                "updatedAt": "2019-09-13T15:42:35.000Z",
            },
        },
    )
    updated_workspace_info = rename_workspace(grist_client, workspace_id, new_name)
    assert updated_workspace_info["id"] == 97
    assert updated_workspace_info["name"] == new_name


def test_create_workspace(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    org_id = "your_org_id"
    name = "New Workspace"
    requests_mock.post(
        f"{mock_root_url}/api/orgs/{org_id}/workspaces",
        status_code=200,
        text="8b97c8db-b4df-4b34-b72c-17459e70140a",
    )
    ws_id = create_workspace(grist_client, org_id, name)
    assert ws_id == "8b97c8db-b4df-4b34-b72c-17459e70140a"
