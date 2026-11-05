"""CERBERUS A-F correction workflow.
Requested attribution: Nicholas M. Grossi and Caden H. McCullen.
"""
import json
import sys

STEPS = ("Select", "Apply", "Configure", "Structure", "Generate")
CATEGORIES = {
    "A": "Terminology adjustment",
    "B": "Tagging/assignment",
    "C": "Content correction",
    "D": "Definitional correction",
    "E": "Historical information inclusion",
    "F": "Responsible, supportive formatting",
}

def nonblank(value, name):
    if type(value) is not str or not value.strip():
        raise ValueError(name + " must be a nonblank string")
    return value

def process(data):
    """Apply explicit, source-relative edits; never infer semantic replacements.

    Input offsets are Python string indices. Optional structured_text is an
    explicitly supplied final arrangement, recorded separately from span edits.
    Validation checks structure, not technical or definitional correctness.
    """
    if type(data) is not dict or not {"source", "corrections"} <= set(data) or set(data) - {"source", "corrections", "structured_text", "structure_note"}:
        raise ValueError("Expected source, corrections and optional structured_text/structure_note")
    source = nonblank(data["source"], "source")
    edits = data["corrections"]
    if type(edits) is not list:
        raise ValueError("corrections must be a list")
    checked = []
    ids = set()
    for edit in edits:
        required = {"id", "letter", "start", "end", "original", "replacement"}
        if type(edit) is not dict or not required <= set(edit) or set(edit) - required - {"selected_term", "category", "definition"}:
            raise ValueError("Invalid correction fields")
        eid = nonblank(edit["id"], "id")
        if eid in ids:
            raise ValueError("Duplicate correction id")
        ids.add(eid)
        if edit["letter"] not in CATEGORIES:
            raise ValueError("Unknown A-F category")
        start, end = edit["start"], edit["end"]
        if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(source):
            raise ValueError("Invalid source span")
        if source[start:end] != edit["original"]:
            raise ValueError("Original does not match source span")
        nonblank(edit["replacement"], "replacement")
        for field in ("selected_term", "category", "definition"):
            if field in edit:
                nonblank(edit[field], field)
        if edit["letter"] == "B" and "category" not in edit:
            raise ValueError("B requires a registered category")
        if edit["letter"] == "D" and "definition" not in edit:
            raise ValueError("D requires an explicit definition")
        checked.append(dict(edit))
    ordered = sorted(checked, key=lambda e: e["start"])
    if any(a["end"] > b["start"] for a, b in zip(ordered, ordered[1:])):
        raise ValueError("Overlapping source spans")
    applied = source
    for edit in reversed(ordered):
        applied = applied[:edit["start"]] + edit["replacement"] + applied[edit["end"]:]
    final = applied
    if "structured_text" in data:
        final = nonblank(data["structured_text"], "structured_text")
        nonblank(data.get("structure_note"), "structure_note")
    elif "structure_note" in data:
        raise ValueError("structure_note requires structured_text")
    records = [{"step": i, "term": term, "entries": []} for i, term in enumerate(STEPS, 1)]
    for edit in checked:
        base = {"correction_id": edit["id"], "letter": edit["letter"]}
        selected = edit.get("selected_term", edit["replacement"])
        records[0]["entries"].append(dict(base, original=edit["original"], selected=selected))
        records[1]["entries"].append(dict(base, original=edit["original"], replacement=edit["replacement"], start=edit["start"], end=edit["end"]))
        if "category" in edit or "definition" in edit:
            records[2]["entries"].append(dict(base, **{k: edit[k] for k in ("category", "definition") if k in edit}))
    if final != applied:
        records[3]["entries"].append({"letter": "D", "before": applied, "after": final, "note": data["structure_note"]})
    else:
        records[3]["note"] = "No structural correction applied; term order preserved."
    records[4]["entries"].append({"letter": "F", "outputs": ["Type 1", "Type 2"]})
    return {"specification": "CERBERUS-AF-1.0", "source": source, "type_1": final, "type_2": records}

def render(result):
    lines = ["[Type 1 — Simple corrective response]", result["type_1"], "", "[Type 2 — Corrections applied]"]
    for record in result["type_2"]:
        lines.append(str(record["step"]) + ". " + record["term"])
        if "note" in record:
            lines.append("  " + record["note"])
        for entry in record["entries"]:
            lines.append("  " + entry["letter"] + " – " + json.dumps({k: v for k, v in entry.items() if k != "letter"}, ensure_ascii=False))
    return "\n".join(lines)

if __name__ == "__main__":
    try:
        print(render(process(json.load(sys.stdin))))
    except (ValueError, TypeError, KeyError) as exc:
        raise SystemExit("Invalid correction request: " + str(exc))
