from datetime import datetime
from typing import Literal, Optional, TypedDict

Access = Literal["owners", "editors", "viewers"]


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
