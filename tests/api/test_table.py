from typing import List

import pytest
from grist_python_sdk.api.table import (
    TableWithColumnsInfo,
    add_tables,
    list_tables_info,
    modify_tables,
)
from grist_python_sdk.api.typing import TableInfo
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_list_tables(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"

    expected_tables = [
        {"id": "People", "fields": {"tableRef": 1, "onDemand": True}},
        {"id": "Places", "fields": {"tableRef": 2, "onDemand": False}},
    ]

    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/tables",
        status_code=200,
        json={"tables": expected_tables},
    )

    tables = list_tables_info(grist_client, doc_id)
    assert tables == expected_tables


def test_add_tables(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"

    tables_to_add: List[TableWithColumnsInfo] = [
        {
            "id": "People",
            "columns": [
                {"id": "pet", "fields": {"label": "Pet"}},
                {"id": "popularity", "fields": {"label": "Popularity ❤"}},
            ],
        }
    ]

    expected_response = {"tables": [{"id": "People"}]}

    requests_mock.post(
        f"{mock_root_url}/api/docs/{doc_id}/tables",
        status_code=200,
        json=expected_response,
    )

    response = add_tables(grist_client, doc_id, tables_to_add)
    assert response == ["People"]


def test_modify_tables(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"

    tables_to_modify: List[TableInfo] = [
        {"id": "People", "fields": {"tableRef": 1, "onDemand": True}},
        {"id": "Places", "fields": {"tableRef": 2, "onDemand": False}},
    ]

    requests_mock.patch(
        f"{mock_root_url}/api/docs/{doc_id}/tables",
        status_code=200,
    )

    modify_tables(grist_client, doc_id, tables_to_modify)
