from typing import Any, Dict, List

from grist_python_sdk.client import GristAPIClient

from .typing import Access, OrganizationInfo, UserInfo
from .utils import parse_organization_info


def list_organizations_info(client: GristAPIClient) -> List[OrganizationInfo]:
    orgs_parsed: List[Dict[str, Any]] = client.request(
        method="get", path="orgs", params={}
    )
    orgs: List[OrganizationInfo] = []
    for org_parsed in orgs_parsed:
        orgs.append(parse_organization_info(org_parsed))
    return orgs


def describe_organization(
    client: GristAPIClient, org_id: int | str
) -> OrganizationInfo:
    org_parsed: Dict[str, Any] = client.request(
        method="get",
        path=f"orgs/{org_id}",
    )
    return parse_organization_info(org_parsed)


def rename_organization(
    client: GristAPIClient, org_id: int | str, name: str
) -> OrganizationInfo:
    changes = {"name": name}
    org_parsed: Dict[str, Any] = client.request(
        method="patch",
        path=f"orgs/{org_id}",
        json=changes,
    )
    return parse_organization_info(org_parsed)


def list_users_of_organization(
    client: GristAPIClient, org_id: int | str
) -> List[UserInfo]:
    users: List[UserInfo] = client.request(
        method="get",
        path=f"orgs/{org_id}/access",
    )["users"]
    return users


def change_users_of_organization(
    client: GristAPIClient, org_id: int | str, users_info: List[Dict[str, Access]]
) -> List[UserInfo]:
    delta_info: Dict[str, Any] = {"delta": {"users": users_info}}
    users: List[UserInfo] = client.request(
        method="patch", path=f"orgs/{org_id}/access", json=delta_info
    )
    return users
