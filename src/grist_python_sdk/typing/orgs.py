from datetime import datetime
from typing import Literal, Optional, TypedDict

Access = Literal["owners", "editors", "viewers"]


class UserRequired(TypedDict):
    id: str
    name: str


class User(UserRequired, total=False):
    email: Optional[str]
    access: Optional[Access]


class Organization(TypedDict):
    id: str
    name: str
    domain: Optional[str]
    owner: User
    access: Access
    createdAt: datetime
    updatedAt: datetime
