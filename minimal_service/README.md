# CERBERUS

## Purpose
CERBERUS is a research and delivery framework for turning ambiguous questions into evidence-backed work products that include practical instructions, supporting findings, and clear decisions.

The repository includes both a research methodology and a minimal local service for authenticated intake, evidence capture, and structural validation.

## Repository structure
- `docs/` contains methodology, requirements, and research-process reference material.
- `templates/` contains reusable request, evidence, approach, delivery, and QA templates.
- `minimal_service/` contains the local research service and its focused test coverage.
- `tests/` contains the framework and setup validation suite.
- `web/` contains the static browser prototype.

## Local validation
Run from the repository root:

```sh
python3 scripts/validate.py
bash -n setup-cerberus.sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m unittest minimal_service.test_service -v
python3 -m unittest minimal_service.test_http_timeout -v
```

The HTTP timeout suite covers idle client disconnects, incomplete request framing, authenticated timeout behavior, and recovery after a stalled request. The service tests cover intake, evidence capture, product validation, and database integrity protections.

## Documentation map
- `docs/methodology.md` — the canonical research process
- `docs/product-requirements.md` — product and evidence requirements
- `minimal_service/README.md` — API and service behavior
- `web/README.md` — browser prototype scope and verification status
- `CONTRIBUTING.md` — contribution guidance
- `SECURITY.md` — security expectations

## Status
This repository is a framework and working implementation, not a complete multi-user production system. Documentation and tests help preserve explicit limits, operational boundaries, and verification scope.
