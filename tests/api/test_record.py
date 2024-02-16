import pytest
from grist_python_sdk.api.record import (
    add_records,
    fetch_records,
    patch_records,
    put_records,
)
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_fetch_records(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"
    filterstring = '{"pet": ["cat", "dog"]}'
    sortstring = "pet,-age"
    limitnumber = 5
    hidden = True

    expected_records = [
        {"id": 1, "fields": {"pet": "cat", "popularity": 67}},
        {"id": 2, "fields": {"pet": "dog", "popularity": 95}},
    ]

    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/records",
        status_code=200,
        json={"records": expected_records},
    )

    records = fetch_records(
        grist_client,
        doc_id,
        table_id,
        filterstring=filterstring,
        sortstring=sortstring,
        limitnumber=limitnumber,
        hidden=hidden,
    )

    assert records == expected_records


def test_add_records(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"

    records_to_add = [
        {"fields": {"pet": "cat", "popularity": 67}},
        {"fields": {"pet": "dog", "popularity": 95}},
    ]

    expected_response = {"records": [{"id": 1}, {"id": 2}]}

    requests_mock.post(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/records",
        status_code=200,
        json=expected_response,
    )

    response = add_records(grist_client, doc_id, table_id, records_to_add)
    assert response == [1, 2]


def test_patch_records(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"

    records_to_patch = [
        {"id": 1, "fields": {"pet": "cat", "popularity": 67}},
        {"id": 2, "fields": {"pet": "dog", "popularity": 95}},
    ]
    requests_mock.patch(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/records",
        status_code=200,
    )

    patch_records(grist_client, doc_id, table_id, records_to_patch)


def test_put_records(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"

    records_to_put = [
        {"require": {"pet": "cat"}, "fields": {"popularity": 67}},
        {"require": {"pet": "dog"}, "fields": {"popularity": 95}},
    ]

    requests_mock.put(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/records",
        status_code=200,
    )

    put_records(grist_client, doc_id, table_id, records_to_put)
