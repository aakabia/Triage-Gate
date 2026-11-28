import json
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from code_context import get_code

load_dotenv()

MODEL = "claude-sonnet-5-5"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "evidence" / "ai_raw"

client = anthropic.Anthropic()

# Forces the model to answer in this JSON shape
TRIAGE_TOOL = {
    "name": "report_triage",
    "description": "Report the triage result for one security finding.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "summary": {"type": "string"},
            "severity": {"type": "string", "enum": ["critical", "high", "medium", "low"]},
            "verdict": {"type": "string", "enum": ["true_positive", "false_positive", "needs_review"]},
            "reasoning": {"type": "string"},
            "fix_code": {"type": "string", "description": "Replacement for exactly the flagged lines"},
        },
        "required": ["summary", "severity", "verdict", "reasoning", "fix_code"],
    },
}


def triage(ticket):

    # get path for the entire code file where this ticket vulnerability is loacted 
    whole_file = (PROJECT_ROOT / ticket["path"]).read_text(encoding="utf-8")


    # create prompt for ai 
    prompt = f"""You are a security engineer triaging a scanner finding.

    Rule: {ticket['rule_id']}
    Message: {ticket['message']}
    Flagged lines {ticket['start_line']}-{ticket['end_line']}:
    {get_code(ticket)}

    Full file for context:
    {whole_file}

    Is this a real vulnerability or a false positive? Your fix_code must replace
    exactly the flagged lines. Report by calling the report_triage tool."""


    # create the response 
    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        tools=[TRIAGE_TOOL],
        tool_choice={"type": "auto"},
        messages=[{"role": "user", "content": prompt}],
    )


    # Save the raw response as evidence
    # Saves each ai triage response with token information in seperate file. 
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{ticket['id']}.json").write_text(response.model_dump_json(indent=2), encoding="utf-8")


    # response.content could contain many blocks so loop and 
    # find the response block that used our tool or throw error.
    # block.input contains only whats in our properties of TRIAGE_TOOL
    # This is done through "additionalProperties": False,  "properties" and "required"
    for block in response.content:
        if block.type == "tool_use":
            return block.input  
    raise ValueError("The AI did not call report_triage")



if __name__ == "__main__":
    # using read text from path to convert our json file to string and load it to dick withs loads
    tickets = json.loads((PROJECT_ROOT / "evidence" / "tickets.json").read_text(encoding="utf-8"))
    print(json.dumps(triage(tickets[0]), indent=2))