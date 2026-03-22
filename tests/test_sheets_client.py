import pytest
import json
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_SHEETS_ID", "test-sheet-id")
    monkeypatch.setenv("GOOGLE_CREDENTIALS_PATH", "fake-creds.json")


@pytest.fixture
def mock_worksheet():
    ws = MagicMock()
    ws.get_all_records.return_value = [
        {"id": "P-001", "name": "Test", "status": "in_process", "area_m2": "200"},
        {"id": "P-002", "name": "Other", "status": "built", "area_m2": "300"},
    ]
    ws.row_values.return_value = ["id", "name", "status", "area_m2"]
    return ws


@pytest.fixture
def client(mock_env, mock_worksheet):
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_gc = MagicMock()
    mock_gc.open_by_key.return_value = mock_spreadsheet

    with patch("gspread.authorize", return_value=mock_gc), \
         patch("google.oauth2.service_account.Credentials.from_service_account_file"):
        from scripts.sheets_client import SheetsClient
        return SheetsClient()


def test_read_sheet_returns_list_of_dicts(client, mock_worksheet):
    rows = client.read_sheet("Projects")
    assert isinstance(rows, list)
    assert rows[0]["id"] == "P-001"
    assert rows[1]["status"] == "built"
    mock_worksheet.get_all_records.assert_called_once_with(default_blank="")


def test_append_row_writes_values_in_header_order(client, mock_worksheet):
    from scripts.sheets_client import SHEET_HEADERS
    client.append_row("Leads", {
        "id": "L-001",
        "date": "2026-03-22",
        "client_name": "Ana García",
        "status": "new",
    })
    args = mock_worksheet.append_row.call_args[0][0]
    headers = SHEET_HEADERS["Leads"]
    assert args[headers.index("id")] == "L-001"
    assert args[headers.index("client_name")] == "Ana García"
    assert args[headers.index("status")] == "new"
    # Fields not provided should be empty string
    assert args[headers.index("email")] == ""


def test_update_row_changes_correct_cell(client, mock_worksheet):
    # Mock returns ["id", "name", "status", "area_m2"] — "status" is col 3 (1-based)
    # This test is internally consistent with the mock; the real Projects sheet has
    # "status" at col 18 — the implementation correctly reads live header positions
    client.update_row("Projects", "P-001", {"status": "built"})
    # row P-001 is index 0 in records → row_num = 2; status is col 3 in the mock
    mock_worksheet.update_cell.assert_called_once_with(2, 3, "built")


def test_update_row_raises_if_not_found(client, mock_worksheet):
    with pytest.raises(KeyError, match="not found"):
        client.update_row("Projects", "P-999", {"status": "built"})


def test_upsert_row_appends_when_not_found(client, mock_worksheet):
    from scripts.sheets_client import SHEET_HEADERS
    client.upsert_row("Projects", {"id": "P-003", "name": "New"})
    mock_worksheet.append_row.assert_called_once()


def test_upsert_row_updates_when_found(client, mock_worksheet):
    client.upsert_row("Projects", {"id": "P-001", "status": "built"})
    mock_worksheet.update_cell.assert_called()
    mock_worksheet.append_row.assert_not_called()


def test_missing_sheet_id_raises(monkeypatch):
    monkeypatch.delenv("GOOGLE_SHEETS_ID", raising=False)
    monkeypatch.setenv("GOOGLE_CREDENTIALS_PATH", "fake.json")
    with patch("gspread.authorize"), \
         patch("google.oauth2.service_account.Credentials.from_service_account_file"):
        import importlib
        import scripts.sheets_client as sc
        importlib.reload(sc)
        with pytest.raises(EnvironmentError, match="GOOGLE_SHEETS_ID"):
            sc.SheetsClient()
