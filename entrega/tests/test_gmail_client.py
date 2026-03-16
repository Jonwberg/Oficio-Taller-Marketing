import base64
import pytest
from unittest.mock import patch, MagicMock, call
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import gmail_client as gmail


@pytest.fixture(autouse=True)
def set_env(monkeypatch, tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text('{"installed": {"client_id": "test"}}')
    monkeypatch.setenv("GMAIL_CREDENTIALS_PATH", str(creds_file))


def make_mock_service(thread_id="thread_abc", message_text="Approve"):
    """Build a mock Gmail service that returns predictable data."""
    service = MagicMock()

    # send returns a message with threadId
    service.users().messages().send().execute.return_value = {
        "id": "msg_001",
        "threadId": thread_id
    }

    # threads().get() returns thread with messages list
    encoded = base64.urlsafe_b64encode(message_text.encode()).decode()
    service.users().threads().get().execute.return_value = {
        "id": thread_id,
        "messages": [
            {"id": "msg_001", "threadId": thread_id, "payload": {"body": {"data": ""}}},
            {"id": "msg_002", "threadId": thread_id, "payload": {"body": {"data": encoded}}}
        ]
    }
    return service


# ── send_review_request ──────────────────────────────────────────────────────

def test_send_review_request_returns_thread_id():
    mock_service = make_mock_service(thread_id="thread_review_001")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        thread_id = gmail.send_review_request(
            to="marcela@oficiotaller.com",
            subject="DG-01: Lead Review — Casa Torres",
            body="Please approve or reject this lead."
        )
    assert thread_id == "thread_review_001"

def test_send_review_request_sends_to_correct_recipient():
    mock_service = make_mock_service()
    with patch.object(gmail, "_get_service", return_value=mock_service):
        gmail.send_review_request("marcela@oficiotaller.com", "Subject", "Body")
    call_args = mock_service.users().messages().send.call_args
    raw = base64.urlsafe_b64decode(call_args[1]["body"]["raw"] + "==").decode()
    assert "marcela@oficiotaller.com" in raw

# ── read_latest_reply ────────────────────────────────────────────────────────

def test_read_latest_reply_returns_message_text():
    mock_service = make_mock_service(message_text="Approve — looks good")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_latest_reply("thread_abc")
    assert text == "Approve — looks good"

def test_read_latest_reply_returns_none_when_no_messages():
    mock_service = make_mock_service()
    mock_service.users().threads().get().execute.return_value = {"id": "thread_empty", "messages": []}
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_latest_reply("thread_empty")
    assert text is None

def test_read_latest_reply_returns_none_when_only_original_message():
    """1 message = only the original send, no reply yet — should return None."""
    mock_service = make_mock_service()
    mock_service.users().threads().get().execute.return_value = {
        "id": "thread_abc",
        "messages": [{"id": "msg_001", "threadId": "thread_abc", "payload": {"body": {"data": ""}}}]
    }
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_latest_reply("thread_abc")
    assert text is None

# ── send_reminder ────────────────────────────────────────────────────────────

def test_send_reminder_replies_on_same_thread():
    mock_service = make_mock_service(thread_id="thread_abc")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        gmail.send_reminder("thread_abc", "marcela@oficiotaller.com", "24h reminder.")
    call_args = mock_service.users().messages().send.call_args
    body_dict = call_args[1]["body"]
    # Thread binding: message body must include threadId to reply on same thread
    assert body_dict.get("threadId") == "thread_abc"

# ── send_escalation ──────────────────────────────────────────────────────────

def test_send_escalation_sends_email():
    mock_service = make_mock_service()
    with patch.object(gmail, "_get_service", return_value=mock_service):
        gmail.send_escalation("thread_abc", "marcela@oficiotaller.com", "48h escalation.")
    assert mock_service.users().messages().send().execute.called

# ── send_client_email ────────────────────────────────────────────────────────

def test_send_client_email_returns_thread_id():
    mock_service = make_mock_service(thread_id="thread_client_001")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        thread_id = gmail.send_client_email(
            to="cliente@example.com",
            subject="Cuestionario de Descubrimiento",
            body="Buenos días, le enviamos el cuestionario."
        )
    assert thread_id == "thread_client_001"

# ── read_client_reply ────────────────────────────────────────────────────────

def test_read_client_reply_returns_text():
    mock_service = make_mock_service(message_text="Hola, adjunto los documentos.")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_client_reply("thread_client_001")
    assert text == "Hola, adjunto los documentos."
