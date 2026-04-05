"""
Download all files from a Google Drive folder to a local directory.
Usage: python download_drive_folder.py <folder_id> <output_dir>
"""
import sys
import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

CREDENTIALS_FILE = Path(__file__).parent.parent.parent / "credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_service():
    creds = service_account.Credentials.from_service_account_file(
        str(CREDENTIALS_FILE), scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)

def list_files(service, folder_id):
    files = []
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, mimeType)",
            pageToken=page_token
        ).execute()
        files.extend(response.get("files", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return files

def download_file(service, file_id, file_name, output_dir):
    dest = Path(output_dir) / file_name
    if dest.exists():
        print(f"  skip (exists): {file_name}")
        return
    request = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    dest.write_bytes(buf.getvalue())
    print(f"  downloaded: {file_name}")

def main(folder_id, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    service = get_service()
    print(f"Listing files in folder {folder_id}...")
    files = list_files(service, folder_id)
    print(f"Found {len(files)} files.")
    for f in files:
        if "google-apps" in f["mimeType"]:
            print(f"  skip (Google Doc): {f['name']}")
            continue
        download_file(service, f["id"], f["name"], output_dir)
    print("Done.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python download_drive_folder.py <folder_id> <output_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
