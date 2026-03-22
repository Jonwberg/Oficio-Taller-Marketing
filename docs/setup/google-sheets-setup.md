# Google Sheets Setup Guide

Follow these steps **in order** before running any scripts.

## Step 1: Create a Google Cloud project

1. Go to https://console.cloud.google.com
2. Click "New Project" → name it `oficio-taller-studio` → Create

## Step 2: Enable APIs

1. In the left menu → APIs & Services → Library
2. Search "Google Sheets API" → Enable
3. Search "Google Drive API" → Enable

## Step 3: Create a service account

1. APIs & Services → Credentials → Create Credentials → Service Account
2. Name: `studio-sync` → Create and continue → Done
3. Click the service account → Keys tab → Add Key → JSON
4. Download the file → rename it `credentials.json` → place at project root

## Step 4: Note the service account email

On the service account page, copy the email address.
It looks like: `studio-sync@oficio-taller-studio.iam.gserviceaccount.com`

## Step 5: Create the spreadsheet

1. Go to https://sheets.google.com
2. Create a new blank spreadsheet
3. Rename it: **Oficio Taller — Studio Data**

## Step 6: Share the spreadsheet with the service account

1. Click Share (top right)
2. Paste the service account email
3. Set role to **Editor**
4. Uncheck "Notify people" → Share

## Step 7: Get the spreadsheet ID

From the URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
Copy the `SPREADSHEET_ID` part.

## Step 8: Create .env file

Create `.env` at the project root:

```
GOOGLE_SHEETS_ID=your_spreadsheet_id_here
GOOGLE_CREDENTIALS_PATH=credentials.json
```

## Step 9: Run setup script

```bash
python scripts/setup_sheets.py
```

Expected output:
```
→ Creating sheets...
→ Projects: created with 22 columns
→ Milestones: created with 9 columns
→ Leads: created with 11 columns
→ Invoices: created with 8 columns
→ Bank: created with 7 columns
→ Campaigns: created with 9 columns
→ Assets: created with 7 columns
→ Seeding Projects: 34 rows written
→ Seeding Milestones: 136 rows written
Setup complete.
```

## Step 10: Verify sync

```bash
python scripts/sheets_sync.py
```

Expected: both JSON files written, no errors.

## Troubleshooting

- `SpreadsheetNotFound`: `GOOGLE_SHEETS_ID` is wrong — re-copy from the URL between `/d/` and `/edit`
- `APIError 403`: service account does not have Editor access — re-share the spreadsheet with the service account email
- `FileNotFoundError` on `credentials.json`: `GOOGLE_CREDENTIALS_PATH` points to wrong location — check `.env`
- `EnvironmentError: GOOGLE_SHEETS_ID not set`: `.env` not loaded — confirm `.env` exists at project root
