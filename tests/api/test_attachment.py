import tempfile

import pytest
from grist_python_sdk.api.attachment import (
    download_attachment_contents,
    get_attachment_metadata,
    list_attachments_metadata,
    upload_attachments,
)
from grist_python_sdk.client import GristAPIClient
from requests_mock import Mocker

api_key = "your_api_key"
mock_root_url = "https://example.com"


@pytest.fixture
def grist_client(requests_mock: Mocker) -> GristAPIClient:
    return GristAPIClient(mock_root_url, api_key)


def test_list_attachments_metadata(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    doc_id = "145"
    filter_ = '{"pet": ["cat", "dog"]}'
    sort = "pet,-age"
    limit = 5

    expected_attachments = [
        {
            "id": 1,
            "fields": {
                "fileName": "logo.png",
                "fileSize": 12345,
                "timeUploaded": "2020-02-13T12:17:19.000Z",
            },
        },
    ]

    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/attachments",
        status_code=200,
        json={"records": expected_attachments},
    )

    attachments = list_attachments_metadata(grist_client, doc_id, filter_, sort, limit)
    assert attachments == expected_attachments


def test_upload_attachments(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    doc_id = "145"
    file1_contents = b"file1_contents"
    with tempfile.NamedTemporaryFile() as f:
        f.write(file1_contents)

        expected_response = [101]

        requests_mock.post(
            f"{mock_root_url}/api/docs/{doc_id}/attachments",
            status_code=200,
            json=expected_response,
        )

        response = upload_attachments(grist_client, doc_id, [f.name])
        assert response == expected_response


def test_get_attachment_metadata(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    doc_id = "145"
    attachment_id = 1

    expected_metadata = {
        "fileName": "logo.png",
        "fileSize": 12345,
        "timeUploaded": "2020-02-13T12:17:19.000Z",
    }

    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/attachments/{attachment_id}",
        status_code=200,
        json=expected_metadata,
    )

    metadata = get_attachment_metadata(grist_client, doc_id, attachment_id)
    assert metadata == expected_metadata


def test_download_attachment_contents(
    grist_client: GristAPIClient, requests_mock: Mocker
) -> None:
    doc_id = "145"
    attachment_id = 1
    expected_contents = b"attachment_contents"

    requests_mock.get(
        f"{mock_root_url}/api/docs/{doc_id}/attachments/{attachment_id}/download",
        status_code=200,
        content=expected_contents,
    )

    contents = download_attachment_contents(grist_client, doc_id, attachment_id)
    assert contents == expected_contents
