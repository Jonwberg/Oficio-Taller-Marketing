"""
Gmail API wrapper for Oficio Taller production agents.

Handles all email operations: Marcela review gates and client-facing communications.
Reads GMAIL_CREDENTIALS_PATH from environment.

First-run OAuth: will open browser for consent. Session saved to token.json beside credentials.
IMPORTANT: token.json (written beside credentials) contains a live OAuth token — never commit it.

Usage from agent bash call:
    python entrega/gmail_client.py send_review_request <to> <subject> <body>
    python entrega/gmail_client.py read_latest_reply <thread_id>
    python entrega/gmail_client.py send_client_email <to> <subject> <body>
    python entrega/gmail_client.py read_client_reply <thread_id>
"""

import os
import sys
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SENDER = "me"


def _get_service():
    """Build and return authenticated Gmail service. Handles OAuth flow."""
    creds_path = os.environ.get("GMAIL_CREDENTIALS_PATH")
    if not creds_path:
        raise EnvironmentError("GMAIL_CREDENTIALS_PATH environment variable not set")

    creds_file = Path(creds_path)
    token_file = creds_file.parent / "token.json"

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _build_message(to: str, subject: str, body: str, thread_id: str = None) -> dict:
    """Build a Gmail API message dict."""
    msg = MIMEMultipart("alternative")
    msg["To"] = to
    msg["From"] = SENDER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = {"raw": raw}
    if thread_id:
        result["threadId"] = thread_id
    return result


def _decode_body(payload: dict) -> str:
    """Extract plain text body from a Gmail message payload."""
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"] + "==").decode("utf-8")

    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data + "==").decode("utf-8")
    return ""


def send_review_request(to: str, subject: str, body: str) -> str:
    """Send a new review request email to Marcela. Returns Gmail thread_id."""
    service = _get_service()
    message = _build_message(to, subject, body)
    result = service.users().messages().send(userId=SENDER, body=message).execute()
    return result["threadId"]


def read_latest_reply(thread_id: str) -> str | None:
    """
    Return the text of the latest reply in a thread, or None if no reply yet.

    Returns None when the thread has 0 or 1 messages (the original review request).
    A reply exists only when len(messages) >= 2.
    """
    service = _get_service()
    thread = service.users().threads().get(
        userId=SENDER, id=thread_id, format="full"
    ).execute()

    messages = thread.get("messages", [])
    if len(messages) < 2:
        return None

    # Latest message is last in the thread's message list
    latest_msg = messages[-1]
    return _decode_body(latest_msg["payload"]) or None


def send_reminder(thread_id: str, to: str, body: str) -> None:
    """Reply on the same thread at 24h with a reminder."""
    service = _get_service()
    subject = "Re: [Recordatorio] Revisión pendiente"
    message = _build_message(to, subject, body, thread_id=thread_id)
    service.users().messages().send(userId=SENDER, body=message).execute()


def send_escalation(thread_id: str, to: str, body: str) -> None:
    """Reply on the same thread at 48h with an escalation to Marcela."""
    service = _get_service()
    subject = "Re: [URGENTE] Revisión pendiente — 48h sin respuesta"
    message = _build_message(to, subject, body, thread_id=thread_id)
    service.users().messages().send(userId=SENDER, body=message).execute()


def send_client_email(to: str, subject: str, body: str) -> str:
    """Send a client-facing email (questionnaire, proposal, doc request). Returns thread_id."""
    service = _get_service()
    message = _build_message(to, subject, body)
    result = service.users().messages().send(userId=SENDER, body=message).execute()
    return result["threadId"]


def read_client_reply(thread_id: str) -> str | None:
    """Return latest client reply text, or None if no reply yet."""
    return read_latest_reply(thread_id)


# ── CLI interface for agents calling via Bash ────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == "send_review_request":
        to, subject, body = sys.argv[2], sys.argv[3], sys.argv[4]
        thread_id = send_review_request(to, subject, body)
        print(thread_id)

    elif cmd == "read_latest_reply":
        thread_id = sys.argv[2]
        text = read_latest_reply(thread_id)
        print(text if text else "NO_REPLY")

    elif cmd == "send_reminder":
        thread_id, to, body = sys.argv[2], sys.argv[3], sys.argv[4]
        send_reminder(thread_id, to, body)
        print("ok")

    elif cmd == "send_escalation":
        thread_id, to, body = sys.argv[2], sys.argv[3], sys.argv[4]
        send_escalation(thread_id, to, body)
        print("ok")

    elif cmd == "send_client_email":
        to, subject, body = sys.argv[2], sys.argv[3], sys.argv[4]
        thread_id = send_client_email(to, subject, body)
        print(thread_id)

    elif cmd == "read_client_reply":
        thread_id = sys.argv[2]
        text = read_client_reply(thread_id)
        print(text if text else "NO_REPLY")

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
