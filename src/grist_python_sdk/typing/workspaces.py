from typing import List, Literal, Optional, TypedDict

from grist_python_sdk.typing.orgs import UserInfo

Access = Literal["owners", "editors", "viewers"]


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
