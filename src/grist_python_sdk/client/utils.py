from datetime import datetime
from typing import Any, Dict, List

from grist_python_sdk.typing.orgs import OrganizationInfo
from grist_python_sdk.typing.workspaces import DocumentInfo, WorkspaceInfo


def parse_organization_info(org_dict: Dict[str, Any]) -> OrganizationInfo:
    return {
        "id": org_dict["id"],
        "name": str(org_dict["name"]),
        "domain": org_dict["domain"],
        "owner": org_dict["owner"],
        "access": org_dict["access"],
        "createdAt": datetime.strptime(org_dict["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        "updatedAt": datetime.strptime(org_dict["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"),
    }


def parse_workspace_info(ws_dict: Dict[str, Any]) -> WorkspaceInfo:
    docs: List[DocumentInfo] = []
    for ws_dict_doc in ws_dict["docs"]:
        doc: DocumentInfo = {
            "id": str(ws_dict_doc["id"]),
            "name": str(ws_dict_doc["name"]),
            "access": str(ws_dict_doc["access"]),  # type:ignore
            "isPinned": bool(ws_dict_doc["isPinned"]),
        }
        if "urlId" in ws_dict_doc.keys():
            doc["urlId"] = str(ws_dict_doc["urlId"])
        docs.append(doc)
    ws: WorkspaceInfo = {
        "id": int(ws_dict["id"]),
        "name": str(ws_dict["name"]),
        "owner": str(ws_dict["owner"]),  # type:ignore
        "access": str(ws_dict["access"]),  # type:ignore
        "docs": docs,
    }
    if "orgDomain" in ws_dict.keys():
        ws["orgDomain"] = str(ws_dict["orgDomain"])
    return ws
