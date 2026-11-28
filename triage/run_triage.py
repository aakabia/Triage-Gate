import json
from pathlib import Path

from ai_triage import triage

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TICKETS_FILE = PROJECT_ROOT / "evidence" / "tickets.json"
RESULTS_FILE = PROJECT_ROOT / "evidence" / "ai_triage.json"


def main():
    # don't overwrite existing evidence
    if RESULTS_FILE.exists():
        print("ai_triage.json already exists. Delete it first if you want to rerun.")
        return

    # load existing tickets 
    tickets = json.loads(TICKETS_FILE.read_text(encoding="utf-8"))

    # initalize empty dict to store each ai decision: "summary", "severity", "verdict", "reasoning", "fix_code" with the hashed ticket id as the key.
    results = {}
    for ticket in tickets:
        result = triage(ticket)
        results[ticket["id"]] = result
        print(ticket["id"], result["verdict"], result["severity"])

    RESULTS_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Saved {len(results)} results")


if __name__ == "__main__":
    main()