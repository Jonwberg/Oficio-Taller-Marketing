#!/usr/bin/env python3
"""
Check payment gate before starting a project phase.
Sends a WhatsApp payment reminder if payment is due within 3 days and still pending.

Usage:
    python check-payment-gate.py <project-id> <fase>

    fase: fase_01 | fase_02 | fase_03

Examples:
    python check-payment-gate.py casa-surf-2026-03-15 fase_01
    python check-payment-gate.py casa-surf-2026-03-15 fase_02

Exit codes:
    0 — Payment confirmed, phase can begin
    1 — Payment pending, phase blocked
    2 — Contract not signed, phase blocked
"""

import sys
import json
import subprocess
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGNS_DIR = ROOT / "campaigns"
LEADS_DIR = ROOT / "leads"


def find_project_status(project_id: str) -> tuple[Path, dict]:
    """Find project-status.json for a given project id."""
    for status_dir in ("pending", "approved", "published"):
        candidate = CAMPAIGNS_DIR / status_dir / project_id / "project-status.json"
        if candidate.exists():
            data = json.loads(candidate.read_text(encoding="utf-8"))
            return candidate, data

    raise FileNotFoundError(
        f"project-status.json not found for project '{project_id}'.\n"
        f"Expected at: campaigns/<status>/{project_id}/project-status.json"
    )


def check_gate(project_id: str, fase: str):
    try:
        status_path, status = find_project_status(project_id)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    client_name = status.get("client_name", project_id)
    project_name = status.get("project_name", project_id)

    # ── Check contract ────────────────────────────────────────────────────────
    contract = status.get("contract", {})
    if not contract.get("signed"):
        print("BLOCKED — Contract not signed.")
        print(f"  Project: {project_name}")
        print(f"  Client:  {client_name}")
        print(f"\nAction required: Send contract to client and obtain signature before proceeding.")
        sys.exit(2)

    print(f"✓ Contract signed ({contract.get('signed_date', 'date not recorded')})")

    # ── Check payment for requested fase ─────────────────────────────────────
    payments = status.get("payments", {})
    payment = payments.get(fase, {})

    if not payment:
        print(f"ERROR: No payment entry found for '{fase}' in project-status.json")
        sys.exit(1)

    payment_status = payment.get("status", "pending")
    amount = payment.get("amount_mxn", 0)
    due_date_str = payment.get("due_date", "")

    if payment_status == "received":
        received_date = payment.get("received_date", "date not recorded")
        print(f"✓ Payment for {fase} confirmed ({received_date}) — ${amount:,.0f} MXN")
        print(f"\n✓ GATE CLEAR — {fase} may begin.")
        sys.exit(0)

    # Payment is pending — check how close the due date is
    print(f"✗ Payment for {fase} is PENDING — ${amount:,.0f} MXN")

    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            days_until_due = (due_date - date.today()).days

            if days_until_due < 0:
                print(f"  OVERDUE by {abs(days_until_due)} day(s) — due {due_date_str}")
                urgency = "overdue"
            elif days_until_due <= 3:
                print(f"  Due in {days_until_due} day(s) — {due_date_str}")
                urgency = "due_soon"
            else:
                print(f"  Due {due_date_str} ({days_until_due} days away)")
                urgency = "upcoming"

            # Send WhatsApp reminder if overdue or due within 3 days
            if urgency in ("overdue", "due_soon"):
                print(f"\nSending WhatsApp payment reminder...")
                send_payment_reminder(project_id, project_name, client_name, fase, amount, due_date_str, urgency)

        except ValueError:
            print(f"  Due date format invalid: {due_date_str} (expected YYYY-MM-DD)")

    print(f"\nBLOCKED — {fase} cannot begin until payment is confirmed.")
    print(f"Action: Mark payment as received in project-status.json once transfer is confirmed.")
    sys.exit(1)


def send_payment_reminder(project_id, project_name, client_name, fase, amount, due_date, urgency):
    """Send a WhatsApp reminder to the client about upcoming/overdue payment."""

    fase_display = fase.replace("_", " ").title()

    if urgency == "overdue":
        message = (
            f"Hola {client_name},\n\n"
            f"Te escribimos sobre el proyecto *{project_name}*.\n\n"
            f"El pago correspondiente al inicio de la {fase_display} "
            f"(${amount:,.0f} MXN) venció el {due_date}.\n\n"
            f"Para continuar con el proceso de diseño sin interrupciones, "
            f"te pedimos confirmar el pago a tu conveniencia.\n\n"
            f"Cualquier duda, con gusto te atendemos."
        )
    else:
        message = (
            f"Hola {client_name},\n\n"
            f"Te recordamos que el pago para el inicio de la {fase_display} "
            f"del proyecto *{project_name}* "
            f"(${amount:,.0f} MXN) vence el {due_date}.\n\n"
            f"Una vez confirmado el pago, comenzamos de inmediato.\n\n"
            f"¡Gracias y seguimos en contacto!"
        )

    # Write message to a temp file for the WhatsApp script to pick up
    # (Reuses the existing send-whatsapp infrastructure with a direct message mode)
    reminder_file = ROOT / "publisher" / f".reminder-{project_id}-{fase}.txt"
    reminder_file.write_text(message, encoding="utf-8")

    print(f"  Reminder message saved: {reminder_file.name}")
    print(f"  To send manually, use send-whatsapp.py with the client's phone number.")
    print(f"\n--- Message preview ---")
    print(message)
    print("----------------------")


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    project_id = sys.argv[1]
    fase = sys.argv[2]

    valid_fases = ("fase_01", "fase_02", "fase_03")
    if fase not in valid_fases:
        print(f"ERROR: fase must be one of: {', '.join(valid_fases)}")
        sys.exit(1)

    check_gate(project_id, fase)
