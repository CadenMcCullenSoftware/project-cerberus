# [CERBERUS A-F correction workflow]

## [Exact task question]
Implement this specification in CERBERUS

## [Request and source context]
Source: user-supplied A–F Artificial Intelligence Assistant Specification — Formalized, November 4, 2026. Repository inspected: CadenMcCullenSoftware/project-cerberus, baseline deec42a0176884b6192fa044bc1c3052ac8f2f3e. Supporting project document: CERBERUS AI System Specification.pdf, sections 6–8 and 14.

## [Goals and requirements]
Preserve Select → Apply → Configure → Structure → Generate. Preserve fixed meanings: A terminology adjustment; B tagging/assignment; C content correction; D definitional correction; E historical information inclusion; F responsible, supportive formatting. Produce Type 1 followed by Type 2. Retain source text and source-relative spans. Preserve review as the selected term and Task presented as the applied wording in the supplied example. Repeated letters retain their category meanings; correction IDs distinguish individual changes.

## [Scope and category tags]
This first implementation is an importable Python module and command-line entry point. Existing HTTP service and database behavior are unchanged. Input explicitly supplies corrections, category names, definitions, and any final sentence restructuring. The implementation does not infer corrections, verify category registration against a central taxonomy, or establish semantic correctness. Categories A–F are the supplied correction taxonomy, not replacements for other project taxonomies.

## [Research questions and methodology]
1. Identify the repository and default branch through GitHub.
2. Inspect repository root and minimal_service directory.
3. Consult project files for ordering, terminology, review, and attribution constraints.
4. Read minimal_service/service.py to identify existing integration boundaries.
5. Implement the standalone module and regression tests without altering existing endpoints.
6. Execute local tests against the prepared module; request exact-content authorization before repository write.
Tools: GitHub connector, Project Files exploration, Python execution. AI assistance: source review, implementation drafting, and local test execution.

## [Findings and answer]
The existing service uses Python standard-library HTTP and SQLite components. The new module also uses only the standard library. process(data) returns source, specification version, type_1, and type_2. render(result) emits both response types in order. Span validation rejects mismatched originals and overlapping edits. Explicit structured_text is recorded as a whole-sentence restructuring with a required structure_note; it is not represented as a set of verified token-level changes.

## [Implementation and use]
From repository root:

```sh
python -m minimal_service.af_workflow < correction-request.json
python -m unittest discover -s tests -p 'test_af_workflow.py' -v
```

Input example:

```json
{"source":"material","corrections":[{"id":"C-01","letter":"C","start":0,"end":8,"original":"material","replacement":"content"}]}
```

Python integration:

```python
from minimal_service.af_workflow import process, render
result = process(request_data)
response_text = render(result)
```

Each correction requires id, letter, start, end, original, replacement. Offsets use Python string indices and reference the unchanged source. selected_term, category, definition are optional except B requires category and D requires definition. Optional structured_text requires structure_note. Preserve letters as category identifiers rather than incrementing them as entry numbers.

## [Verification and derivation]
Local execution: 4 test methods passed, including 8 invalid-request subcases. Tests cover the exact supplied Type 1 sentence, fixed stage order, review versus Task presented, repeated A category, unchanged content, invalid spans, overlaps, unknown letters, absent B category, duplicate IDs, absent restructuring note, boolean offsets, and absent D definition. These results apply only to this module in the execution environment; full repository tests, HTTP integration, deployment, and semantic validation were not performed.

## [Options and action plan]
Current implementation supports CLI use or explicit Python import. Repository commit requires approval of exact contents. HTTP routing, automated terminology selection, and persistent correction storage are not included in this change.

## [Uncertainty and review]
Human review of the patch remains pending. Supplied terms and final example are preserved as project-specific instructions, not universal terminology equivalences. No automatic transformation of unrelated uses of scope, objective, traceability, or evidence occurs. No confidentiality or compliance certification is asserted. No external processing is added by this module.

## [Editorial record and attribution]
Type 2 uses bracketed headings, fixed step names, A–F category labels, correction IDs, and structured entry details. Requested attribution: Nicholas M. Grossi and Caden H. McCullen. No additional authorship or ownership determination is made.

## [Disposition and change history]
Version CERBERUS-AF-1.0, November 4, 2026. Prepared and locally tested; repository write awaiting explicit authorization. No production deployment or full-specification completion is claimed.
