from datetime import datetime
from typing import List, Literal, Optional, TypedDict

Access = Literal["owners", "editors", "viewers", "members", None]


class UserInfoRequired(TypedDict):
    id: int
    name: str


class UserInfo(UserInfoRequired, total=False):
    email: Optional[str]
    access: Optional[Access]


class OrganizationInfo(TypedDict):
    id: int | str
    name: str
    domain: Optional[str]
    owner: UserInfo
    access: Access
    createdAt: datetime
    updatedAt: datetime


class DocumentInfoRequired(TypedDict):
    id: str
    name: str
    access: Access
    isPinned: bool


class DocumentInfo(DocumentInfoRequired, total=False):
    urlId: Optional[str]


class WorkspaceInfoRequired(TypedDict):
    id: int
    name: str
    owner: UserInfo
    access: Access
    docs: List[DocumentInfo]


class WorkspaceInfo(WorkspaceInfoRequired, total=False):
    orgDomain: Optional[str]


class TableFieldsInfo(TypedDict):
    tableRef: int
    onDemand: bool


class TableInfo(TypedDict):
    id: str
    fields: TableFieldsInfo
