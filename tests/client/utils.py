mock_root_url = "https://example.com"

mock_org_dict = {
    "id": 1,
    "name": "Example Org",
    "domain": "example-domain",
    "owner": {"id": 1, "name": "Owner Name"},
    "access": "owners",
    "createdAt": "2019-09-13T15:42:35.000Z",
    "updatedAt": "2019-09-13T15:42:35.000Z",
}

mock_user_dict = {
    "id": 1,
    "email": "you@example.com",
    "name": "you@example.com",
    "access": "owners",
    "isMember": True,
}

mock_ws_dict = {
    "id": 1,
    "name": "Workspace 1",
    "access": "owners",
    "owner": {"id": 1, "name": "Owner Name"},
    "docs": [{"id": "doc1", "name": "doc1", "access": "owners", "isPinned": True}],
}
