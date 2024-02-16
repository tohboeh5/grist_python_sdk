from typing import List

import pytest
from grist_python_sdk.api.column import (
    add_columns,
    delete_column,
    list_columns,
    patch_columns,
    put_columns,
)
from grist_python_sdk.api.typing import ColumnInfo
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_list_columns(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"
    hidden = True

    expected_columns = [
        {"id": "pet", "fields": {"label": "Pet"}},
        {"id": "popularity", "fields": {"label": "Popularity ❤", "type": "Int"}},
    ]

    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/columns",
        status_code=200,
        json={"columns": expected_columns},
    )

    columns = list_columns(grist_client, doc_id, table_id, hidden=hidden)
    assert columns == expected_columns


def test_add_columns(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"

    columns_to_add: List[ColumnInfo] = [
        {"id": "pet", "fields": {"label": "Pet"}},
        {"id": "popularity", "fields": {"label": "Popularity ❤", "type": "Int"}},
        {"id": "Order", "fields": {"type": "Ref:Orders", "visibleCol": 2}},
        {
            "id": "Formula",
            "fields": {"type": "Int", "formula": "$A + $B", "isFormula": True},
        },
    ]

    expected_response = {"columns": [{"id": "pet"}, {"id": "popularity"}]}

    requests_mock.post(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/columns",
        status_code=200,
        json=expected_response,
    )

    response = add_columns(grist_client, doc_id, table_id, columns_to_add)
    assert response == ["pet", "popularity"]


def test_patch_columns(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"

    columns_to_patch: List[ColumnInfo] = [
        {"id": "pet", "fields": {"label": "Pet"}},
        {"id": "popularity", "fields": {"label": "Popularity ❤", "type": "Int"}},
    ]

    requests_mock.patch(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/columns",
        status_code=200,
    )

    patch_columns(grist_client, doc_id, table_id, columns_to_patch)


def test_put_columns(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"

    columns_to_put: List[ColumnInfo] = [
        {"id": "pet", "fields": {"label": "Pet"}},
        {"id": "popularity", "fields": {"label": "Popularity ❤", "type": "Int"}},
    ]

    requests_mock.put(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/columns",
        status_code=200,
    )

    put_columns(grist_client, doc_id, table_id, columns_to_put)


def test_delete_column(grist_client: GristAPIClient, requests_mock: Mocker) -> None:
    doc_id = "145"
    table_id = "exampleTable"
    col_id = "pet"

    requests_mock.delete(
        f"{mock_root_url}/api/docs/{doc_id}/tables/{table_id}/columns/{col_id}",
        status_code=200,
    )

    delete_column(grist_client, doc_id, table_id, col_id)
