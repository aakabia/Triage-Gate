from pathlib import Path

# get the path to our root directory for this project (Triage-Gate)
PROJECT_ROOT = Path(__file__).resolve().parent.parent 


# takes a finding and scans our app.py for the line numbers for that finding
def get_code(finding):

    # concat or root to the path of our finding
    file_path = PROJECT_ROOT / finding["path"]

    # Path objects have read_text(): opens, reads, and closes the file in one call

    lines = file_path.read_text(encoding="utf-8").splitlines()
    
    # get our start and end lines for this finding 
    start = finding["start_line"]
    end = finding["end_line"]

    # lists are index by zero so we list slice start -1 to the end not including the end index, covering entire segment where code is.
    return "\n".join(lines[start - 1:end])


if __name__ == "__main__":
    from parse_findings import parse_data

    findings = parse_data()
    print(get_code(findings[0]))