from typing import Any

import pytest
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    root_url = "https://example.com"
    api_key = "your_api_key"

    return GristAPIClient(root_url, api_key)


def test_base_grist_client_request(
    requests_mock: Mocker,
    grist_client: GristAPIClient,
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


def test_base_grist_client_request_with_incorrect_api_key(
    requests_mock: Mocker,
    grist_client: GristAPIClient,
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


def test_base_grist_client_headers_with_auth(
    grist_client: GristAPIClient,
) -> None:
    expected_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {grist_client.api_key}",
    }
    headers = grist_client.headers_with_auth
    assert headers == expected_headers


def test_base_grist_client_get_url(
    grist_client: GristAPIClient,
) -> None:
    path = "path"
    expected_url = "https://example.com/api/path"
    result: str = grist_client.get_url(path)
    assert result == expected_url
