import json 




def as_list(value):
    """cwe and owasp are a list in some findings, a plain string in others,
    and missing in some. Always return a list."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return value



def parse_data():

    # use with open to safely open and load our json file using json.load 
    with open("../evidence/scan_before.json", "r", encoding= "utf-8") as f:
        data = json.load(f)

    # extract the result key for easier parsing 
    vuls_Data= data["results"]

    # initalize an empty array for our findings
    findings= []

    for item in vuls_Data:

        # parse the extra key to return a dict 
        extra = item["extra"]

        # metadata is parased from the extra key within the loaded json and if no data it defaults to empty dict. 
        metadata = extra.get("metadata", {})

        # append our data to findings list in order to normalize 
        findings.append({
            "rule_id": item["check_id"],
            "path": item["path"],
            "start_line": item["start"]["line"],
            "end_line": item["end"]["line"],
            "severity": extra["severity"],
            "message": extra["message"].strip(),
            "cwe": as_list(metadata.get("cwe")),
            "owasp": as_list(metadata.get("owasp")),
        })
    return findings
   
if __name__ == "__main__":
    findings = parse_data()
    print(len(findings))
    print(findings[0])