from typing import Any, Dict, List, Optional

from grist_python_sdk.client import GristAPIClient

from .typing import AttachmentMetadataFieldsInfo, AttachmentMetadataInfo


def parse_attachment_fields_info(data: Dict[Any, Any]) -> AttachmentMetadataFieldsInfo:
    return {
        "fileName": str(data["fileName"]),
        "fileSize": int(data["fileSize"]),
        "timeUploaded": str(data["timeUploaded"]),
    }


def list_attachments_metadata(
    client: GristAPIClient,
    doc_id: str,
    filter_: Optional[str] = None,
    sort: Optional[str] = None,
    limit: Optional[int] = None,
) -> List[AttachmentMetadataInfo]:
    path = f"docs/{doc_id}/attachments"
    params = {"filter": filter_, "sort": sort, "limit": limit}
    response: Dict[Any, Any] = client.request(method="get", path=path, params=params)

    return [
        {
            "id": int(record["id"]),
            "fields": parse_attachment_fields_info(record["fields"]),
        }
        for record in response["records"]
    ]


def upload_attachments(
    client: GristAPIClient,
    doc_id: str,
    filenames: List[str],
) -> List[int]:
    path = f"docs/{doc_id}/attachments"
    response: List[Any] = client.request(method="post", path=path, filenames=filenames)
    print(response)
    return [int(id) for id in response]


def get_attachment_metadata(
    client: GristAPIClient,
    doc_id: str,
    attachment_id: int,
) -> AttachmentMetadataFieldsInfo:
    path = f"docs/{doc_id}/attachments/{attachment_id}"
    response = client.request(method="get", path=path)
    return parse_attachment_fields_info(response)


def download_attachment_contents(
    client: GristAPIClient,
    doc_id: str,
    attachment_id: int,
) -> bytes:
    path = f"docs/{doc_id}/attachments/{attachment_id}/download"
    response: bytes = client.request(method="get", path=path, return_type="content")
    return response
