import time
import requests

BASE_URL = "https://app.trengo.com/api/v2"


def _headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Accept": "application/json"}


def get_contact_groups(token: str) -> list[dict]:
    """Return all contact groups."""
    resp = requests.get(
        f"{BASE_URL}/contact_groups",
        headers=_headers(token),
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def get_contacts_in_group(token: str, group_id: int) -> list[dict]:
    """Return all contacts belonging to the given contact group, handling pagination."""
    contacts = []
    page = 1

    while True:
        resp = requests.get(
            f"{BASE_URL}/contacts",
            headers=_headers(token),
            params={"contact_group_ids[]": group_id, "page": page},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()

        contacts.extend(body["data"])

        if not body.get("links", {}).get("next"):
            break

        page += 1
        time.sleep(0.1)

    return contacts
