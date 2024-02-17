from datetime import datetime
from typing import Any, Dict, List

from .typing import DocumentInfo, OrganizationInfo, TableInfo, WorkspaceInfo


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
    if ws_dict["docs"]:
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
        "access": str(ws_dict["access"]),  # type:ignore
        "docs": docs,
    }
    if "orgDomain" in ws_dict.keys():
        ws["orgDomain"] = str(ws_dict["orgDomain"])
    return ws


def parse_document_info(doc_dict: Dict[str, Any]) -> DocumentInfo:
    doc: DocumentInfo = {
        "id": str(doc_dict["id"]),
        "name": str(doc_dict["name"]),
        "access": str(doc_dict["access"]),  # type:ignore
        "isPinned": bool(doc_dict["isPinned"]),
    }
    if "urlId" in doc_dict.keys():
        doc["urlId"] = str(doc_dict["urlId"])
    return doc


def parse_table_info(table: Dict[str, Any]) -> TableInfo:
    doc: TableInfo = {
        "id": str(table["id"]),
        "fields": {
            "tableRef": int(table["fields"]["tableRef"]),
            "onDemand": bool(table["fields"]["onDemand"]),
        },
    }
    return doc
