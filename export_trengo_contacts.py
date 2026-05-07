"""
Trengo Contact Group CSV Exporter
----------------------------------
Usage:
  1. Set your API token in the TRENGO_API_TOKEN variable below (or pass it as an env var).
  2. Run:  python export_trengo_contacts.py
  3. The script will list all contact groups, let you pick one, and save a CSV.

Requirements:  pip install requests
"""

import csv
import os
import time

import requests

# ── Configuration ─────────────────────────────────────────────────────────────
TRENGO_API_TOKEN = os.getenv("TRENGO_API_TOKEN", "PASTE_YOUR_TOKEN_HERE")
# ──────────────────────────────────────────────────────────────────────────────

BASE_URL = "https://app.trengo.com/api/v2"


def headers():
    return {"Authorization": f"Bearer {TRENGO_API_TOKEN}", "Accept": "application/json"}


def get_contact_groups():
    resp = requests.get(f"{BASE_URL}/contact_groups", headers=headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_contacts_in_group(group_id):
    contacts, page = [], 1
    while True:
        resp = requests.get(
            f"{BASE_URL}/contacts",
            headers=headers(),
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


def save_csv(contacts, filename):
    fields = ["id", "name", "email", "phone", "formatted_phone", "created_at", "updated_at"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for c in contacts:
            writer.writerow({
                "id": c.get("id", ""),
                "name": c.get("name") or c.get("full_name") or "",
                "email": c.get("email") or "",
                "phone": c.get("phone") or "",
                "formatted_phone": c.get("formatted_phone") or "",
                "created_at": c.get("created_at") or "",
                "updated_at": c.get("updated_at") or "",
            })


def main():
    if TRENGO_API_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        print("ERROR: Please set your API token in the script or via the TRENGO_API_TOKEN env var.")
        return

    print("Fetching contact groups...\n")
    groups = get_contact_groups()

    if not groups:
        print("No contact groups found.")
        return

    print(f"{'#':<4} {'ID':<10} {'Name':<35} Contacts")
    print("-" * 60)
    for i, g in enumerate(groups):
        print(f"{i+1:<4} {g['id']:<10} {g['name']:<35} {g.get('contacts_count', '?')}")

    print()
    choice = input("Enter the number of the group to export (or press Enter to export all): ").strip()

    if choice == "":
        selected = groups
    else:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(groups):
            print("Invalid selection.")
            return
        selected = [groups[idx]]

    for group in selected:
        print(f"\nFetching contacts for '{group['name']}'...")
        contacts = get_contacts_in_group(group["id"])
        safe_name = group["name"].lower().replace(" ", "_").replace("/", "-")
        filename = f"{safe_name}_contacts.csv"
        save_csv(contacts, filename)
        print(f"  Saved {len(contacts)} contact(s) to {filename}")

    print("\nDone.")


if __name__ == "__main__":
    main()
