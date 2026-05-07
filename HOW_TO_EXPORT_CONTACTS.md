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

## Step 4 — Download the script

Download the file **`export_trengo_contacts.py`** and save it somewhere easy to find,  
for example your **Desktop** or a folder called `Trengo`.

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
