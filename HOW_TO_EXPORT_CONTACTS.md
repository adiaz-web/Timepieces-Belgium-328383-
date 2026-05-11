# How to export your Trengo contacts to a CSV file

This guide walks you through exporting contacts from a Trengo contact group — step by step.  
No technical experience needed. You only need your **Trengo API token** and about 10 minutes.

---

## Step 1 — Install Python

Python is the free program that runs the export script.

1. Go to **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python"** button
3. Open the downloaded file and follow the installer
   - **Important:** on the first screen, tick the box that says **"Add Python to PATH"** before clicking Install

To check it worked, open a terminal (see Step 2) and type:
```
python --version
```
You should see something like `Python 3.12.0`. Any version 3.8 or higher is fine.

---

## Step 2 — Open a terminal

A terminal is a text window where you type commands.

- **Windows:** press `Windows key + R`, type `cmd`, press Enter
- **Mac:** press `Cmd + Space`, type `Terminal`, press Enter

---

## Step 3 — Install the required library

In the terminal, copy and paste this line, then press Enter:

```
pip install requests
```

Wait for it to finish. You will see some text scroll by — that is normal.

---

## Step 4 — Create the script file

1. Open **Notepad** (Windows) or **TextEdit** (Mac)
2. Copy **everything** in the grey box below and paste it in:

```python
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
        contacts = get_contacts_in_group(TOKEN, group["id"])
        safe_name = group["name"].lower().replace(" ", "_").replace("/", "-")
        filename = f"{safe_name}_contacts.csv"
        save_csv(contacts, filename)
        print(f"  Saved {len(contacts)} contact(s) to {filename}")

    print("\nDone.")


if __name__ == "__main__":
    main()
```

3. In Notepad/TextEdit, click **File → Save As**
4. Name the file exactly: **`export_trengo_contacts.py`**  
   - **Windows:** in the "Save as type" dropdown, choose **All Files (\*.\*)** — otherwise it saves as `.txt`
   - **Mac:** uncheck "If no extension is provided, use .txt"
5. Save it on your **Desktop** or in a folder called `Trengo`

---

## Step 5 — Add your API token to the script

1. Open the file `export_trengo_contacts.py` with a text editor  
   (right-click the file → **Open with** → Notepad on Windows, TextEdit on Mac)
2. Find this line near the top:
   ```
   TRENGO_API_TOKEN = "PASTE_YOUR_TOKEN_HERE"
   ```
3. Replace `PASTE_YOUR_TOKEN_HERE` with your actual API token, keeping the quotes.  
   It should look like this:
   ```
   TRENGO_API_TOKEN = "eyJ0eXAiOiJKV1Qi..."
   ```
4. Save the file (`Ctrl + S` on Windows, `Cmd + S` on Mac)

---

## Step 6 — Run the script

In the terminal, navigate to the folder where you saved the script.  
For example, if you saved it on your Desktop:

- **Windows:**
  ```
  cd Desktop
  ```
- **Mac:**
  ```
  cd ~/Desktop
  ```

Then run the script:
```
python export_trengo_contacts.py
```

---

## Step 7 — Pick your contact group

The script will show you a list of all your contact groups, like this:

```
Fetching contact groups...

#    ID         Name                    Contacts
------------------------------------------------
1    469885     Groep 1: interesse      28
2    469886     Groep 2: geen interesse  2
3    442814     Kirsten test            24
...

Enter the number of the group to export (or press Enter to export all):
```

- Type the **number** next to the group you want and press Enter
- Or just press **Enter** without typing anything to export **all groups at once**

---

## Step 8 — Find your CSV file

The script saves the CSV file in the same folder as the script.  
The file is named after the group, for example:

```
kirsten_test_contacts.csv
```

You can open it directly in **Excel** or **Google Sheets**.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `python` is not recognized | Make sure you ticked "Add Python to PATH" during installation. Reinstall Python if needed. |
| `pip` is not recognized | Try `python -m pip install requests` instead |
| `401 Unauthorized` error | Your API token is incorrect — double-check it in the script |
| The CSV is empty | The contact group exists but has no contacts in Trengo |

---

If anything goes wrong, take a screenshot of the error message and send it over — we'll help you sort it out.
