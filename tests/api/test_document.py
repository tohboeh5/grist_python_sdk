from typing import Dict, List

import pytest
from grist_python_sdk.api.document import (
    change_doc_pinned_state,
    change_users_of_doc,
    create_doc,
    delete_doc,
    describe_doc,
    list_users_of_doc,
    rename_doc,
)
from grist_python_sdk.api.typing import Access
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_create_doc(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    ws_id = 97
    doc_name = "New Document"
    doc_id = "8b97c8db-b4df-4b34-b72c-17459e70140a"

    requests_mock.post(
        f"{mock_root_url}/api/workspaces/{ws_id}/docs",
        status_code=200,
        text=doc_id,
    )

    created_doc_id = create_doc(grist_client, ws_id, doc_name)
    assert created_doc_id == doc_id


def test_describe_doc(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}",
        status_code=200,
        text="""{
  "id": 145,
  "name": "Project Lollipop",
  "access": "owners",
  "isPinned": true,
  "urlId": null,
  "workspace": {
    "id": 97,
    "name": "Secret Plans",
    "access": "owners",
    "org": {
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
  }
}""",
    )

    doc_info = describe_doc(grist_client, doc_id)
    assert doc_info["id"] == "145"
    assert doc_info["name"] == "Project Lollipop"


def test_rename_doc(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    new_name = "Competitive Analysis"
    requests_mock.patch(
        f"{mock_root_url}/api/docs/{doc_id}",
        status_code=200,
        json={"name": new_name},
    )

    rename_doc(grist_client, doc_id, new_name)


def test_change_doc_pinned_state(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    doc_id = "145"
    is_pinned = False
    requests_mock.patch(
        f"{mock_root_url}/api/docs/{doc_id}",
        status_code=200,
        json={"isPinned": is_pinned},
    )

    change_doc_pinned_state(grist_client, doc_id, is_pinned)


def test_delete_doc(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    print(f"{mock_root_url}/api/docs/{doc_id}")
    requests_mock.delete(f"{mock_root_url}/api/docs/{doc_id}", status_code=200, json={})

    delete_doc(grist_client, doc_id)


def test_list_users_of_doc(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/access",
        status_code=200,
        text='{"maxInheritedRole": "owners", "users": [{"id": 1, "name": "Andrea", "email": "andrea@getgrist.com", "access": "owners", "parentAccess": "owners"}]}',
    )

    users = list_users_of_doc(grist_client, doc_id)
    assert len(users) == 1
    assert users[0]["id"] == 1
    assert users[0]["name"] == "Andrea"


def test_change_users_of_doc(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    doc_id = "145"
    users_info: List[Dict[str, Access]] = [
        {"foo@getgrist.com": "owners", "bar@getgrist.com": None}
    ]
    requests_mock.patch(
        f"{mock_root_url}/api/docs/{doc_id}/access",
        status_code=200,
        text='{"maxInheritedRole": "owners", "users": [{"id": 1, "name": "Andrea", "email": "andrea@getgrist.com", "access": "owners", "parentAccess": "owners"}]}',
    )

    changed_users = change_users_of_doc(grist_client, doc_id, users_info)
    assert len(changed_users) == 1
    assert changed_users[0]["id"] == 1
    assert changed_users[0]["name"] == "Andrea"
