from datetime import datetime
from typing import Any, Dict, List

import pytest
from grist_python_sdk.client.base import BaseGristClient
from grist_python_sdk.typing.orgs import Organization
from requests_mock import Mocker


@pytest.fixture
def grist_client() -> BaseGristClient:
    root_url = "https://example.com"
    api_key = "your_api_key"
    return BaseGristClient(root_url, api_key)


def test_base_grist_client_request_with_incorrect_api_key(
    requests_mock: Mocker,
    grist_client: BaseGristClient,
) -> None:
    # Mocking the request function to simulate an incorrect API key error
    requests_mock.request(
        method="get",
        url="https://example.com/api/path",
        headers=grist_client.headers_with_auth,
        status_code=401,  # Unauthorized
        reason="Unauthorized",
    )

    # Test the request method with an incorrect API key
    with pytest.raises(Exception, match="Unauthorized"):
        grist_client.request("get", "path")


def test_list_orgs_endpoint(
    requests_mock: Mocker, grist_client: BaseGristClient
) -> None:
    expected_url = "https://example.com/api/orgs"
    expected_response: List[Dict[str, Any]] = [
        {
            "id": 1,
            "name": "Example Org",
            "domain": "example-domain",
            "owner": {"id": 123, "name": "Owner Name"},
            "access": "owners",
            "createdAt": "2019-09-13T15:42:35.000Z",
            "updatedAt": "2019-09-13T15:42:35.000Z",
        },
    ]
    requests_mock.get(expected_url, json=expected_response, status_code=200)

    orgs_response: List[Organization] = grist_client.get_orgs()

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


def test_modify_org_name_endpoint(
    requests_mock: Mocker,
    grist_client: BaseGristClient,
) -> None:
    # Mocking the request function to simulate a successful modification
    org_id = "12345"
    new_name = "New Org Name"
    expected_url = f"https://example.com/api/orgs/{org_id}"
    expected_response: Dict[str, Any] = {
        "id": 12345,
        "name": new_name,
        "domain": "example-domain",
        "owner": {"id": 123, "name": "Owner Name"},
        "access": "owners",
        "createdAt": "2019-09-13T15:42:35.000Z",
        "updatedAt": "2024-02-04T12:30:00.000Z",
    }
    requests_mock.patch(expected_url, json=expected_response, status_code=200)

    # Test the modify_org_name method
    modified_org: Organization = grist_client.modify_org_name(
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


def test_base_grist_client_request(
    requests_mock: Mocker,
    grist_client: BaseGristClient,
) -> None:
    # Mocking the request function
    input_params = {"param": "value"}
    expected_url = "https://example.com/api/path"
    expected_return_value = {"abc": "value"}
    requests_mock.request(
        method="get",
        url=expected_url,
        # params=input_params,
        headers=grist_client.headers_with_auth,
        json=expected_return_value,
        status_code=200,
    )

    # Test the request method with params as a dictionary
    result: Any = grist_client.request(
        "get", "path", params=input_params, json={"key": "value"}
    )

    assert result == expected_return_value


def test_base_grist_client_headers_with_auth(grist_client: BaseGristClient) -> None:
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {grist_client.api_key}",
    }
    headers = grist_client.headers_with_auth
    assert headers == expected_headers


def test_base_grist_client_get_url(grist_client: BaseGristClient) -> None:
    path = "path"
    expected_url = "https://example.com/api/path"
    result: str = grist_client.get_url(path)
    assert result == expected_url
