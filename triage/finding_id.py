import hashlib


def make_id(finding, code):
    # Collapse all whitespace so formatting changes don't change the ID
    normalized_code = " ".join(code.split())

    # "|" separates the parts so they can't blur together
    raw = "|".join([finding["rule_id"], finding["path"], normalized_code])

    # Hash the text and keep the first 10 characters as a short ID
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:10]


if __name__ == "__main__":
    from parse_findings import parse_data
    from code_context import get_code

    for finding in parse_data()[:3]:
        print(make_id(finding, get_code(finding)), finding["rule_id"])