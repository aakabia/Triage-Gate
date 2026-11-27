import json
from datetime import datetime, timezone
from pathlib import Path

from code_context import get_code
from finding_id import make_id
from parse_findings import parse_data

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TICKETS_FILE = PROJECT_ROOT / "evidence" / "tickets.json"


# use all our helper functions to build tickets that include the code, a hashed id, and the normalized data
# Build one ticket per finding: the parsed data plus a stable ID, OPEN status, and detection time
def build_tickets():
    # One timestamp for the whole scan, so every ticket shares the same detected time
    detected_at = datetime.now(timezone.utc).isoformat()

    tickets = []
    for finding in parse_data():
        code = get_code(finding)

        ticket = dict(finding)  # copy, so the original finding isn't changed
        ticket["id"] = make_id(finding, code)
        ticket["status"] = "OPEN"
        ticket["detected_at"] = detected_at
        tickets.append(ticket)

    return tickets


def save_tickets(tickets):
    # Never overwrite: re-running would reset detected_at and ruin MTTR
    if TICKETS_FILE.exists():
        print(f"{TICKETS_FILE} already exists, not overwriting.")
        return

    with open(TICKETS_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2) # using dump because its a dict to json 
    print(f"Saved {len(tickets)} tickets")


if __name__ == "__main__":
    save_tickets(build_tickets())