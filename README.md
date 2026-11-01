<div align="center">

# CERBERUS

### Research that leads to action.

A canonical research framework and initial local research service for
turning complex questions into evidence-supported answers, practical
options, and instructions people can use.

Created by Nicholas M. Grossi, Caden H. McCullen, Alexis M. Adam’s,
Hannah E. Dolch, and Tyler R. White.

Repository owner: [Caden McCullen](https://github.com/CadenMcCullenSoftware)

[Start here](#start-here) ·
[Methodology](docs/methodology.md) ·
[Requirements](docs/product-requirements.md) ·
[Local research service](minimal_service/README.md) ·
[Validation](#validation-and-automation)

</div>

---

## Purpose

CERBERUS researches the user's exact request to meet project goals,
objectives, and requirements. Appropriate tools support the research;
the finished delivery provides credible approaches, clear answers,
and instructions the user can follow.

The outcome is actionability. A PDF, README, or application screen is
a delivery format, not the underlying objective.

## Implementation Status

The repository contains two cooperating components:

| Component | Current scope |
| --- | --- |
| Research framework | A five-stage methodology, research templates, evidence matrix, delivery structure, and quality checklist. |
| Minimal research service | A local HTTP API and separate retrieval worker for authenticated request intake, source preservation, and structural work-product validation. |

The service is an initial executable implementation, not a production
or multi-tenant application.

It does not include a model, automatic synthesis, authenticated human
release approval, or a publication endpoint. Structural acceptance of
a work product does not establish factual accuracy, source support,
or permission to publish.

## What a Delivery Contains

| Element | What the user receives |
| --- | --- |
| Exact question | The original request, preserved rather than silently rewritten. |
| Direct answer | A practical explanation in plain language. |
| Credible approaches | Supported ways to accomplish the task and when each applies. |
| Usable instructions | Prerequisites, ordered actions, expected results, and checks. |
| Supporting findings | Evidence relevant to the question and category goals. |
| Research methodology | How the information was gathered and checked, in execution order. |
| Optional technical detail | Deeper information after the practical answer. |

Follow the user's requested presentation order when supplied.
Keep essential qualifications beside affected instructions and
optional technical depth afterward.

## Choose How to Use CERBERUS

| Your goal | Starting point | What to expect |
| --- | --- | --- |
| Conduct a research task | Follow “Start Here” and copy the templates into a private task workspace. | A structured process for preparing evidence-supported answers and usable instructions. |
| Evaluate the local service | Read `minimal_service/README.md`. | Authenticated intake, retrieval of explicitly supplied sources, preservation of evidence, and structural product validation. |
| Create a separate project repository | Follow “Set Up a Separate Project” from a committed clone. | A new local repository containing the committed framework files selected by the setup script. |
| Download the research documents and templates | Use a published release, when available. | Documentation and template archives under the current release workflow; clone the repository for the executable service. |

## Start Here

1. Copy [the request template](templates/request.md) into a private
   task workspace.
2. Record the exact question, goals, category tags, constraints,
   and acceptance criteria.
3. Gather relevant evidence with
   [the evidence matrix](templates/evidence-matrix.csv).
4. Compare supported options using
   [the approach template](templates/approach.md).
5. Prepare the result with
   [the delivery template](templates/delivery.md).
6. Complete [the QA checklist](templates/qa-checklist.md).

Keep private working material in `research/` and `reports/`.
These workspaces are ignored except for their `.gitkeep` files.

Review all tracked content before publication. Ignore rules do not
remove files already tracked by Git or guarantee privacy.

## Canonical Research Pipeline

| Stage | Purpose |
| --- | --- |
| 1. Scope definition and parameter alignment | Preserve the question and establish goals, boundaries, and completion criteria. |
| 2. Multi-source information gathering | Collect relevant evidence and record its origin. |
| 3. AI-assisted synthesis and cross-verification | Compare findings, check material claims, and identify uncertainty. |
| 4. Goal-aligned technical structuring | Turn findings into accessible approaches and usable instructions. |
| 5. Quality assurance and formatting | Review support, relevance, usability, and requested order. |

The pipeline defines research execution order. It does not require
the reader to encounter methodology before the answer.

The local service supports selected intake, evidence, and validation
operations. It does not automatically execute the complete pipeline.

See [the full methodology](docs/methodology.md) and
[product requirements](docs/product-requirements.md).

## Research Toolkit

| Resource | Use |
| --- | --- |
| [Request template](templates/request.md) | Define the task without losing its original wording. |
| [Evidence matrix](templates/evidence-matrix.csv) | Connect claims to sources, applicability, and verification status. |
| [Approach template](templates/approach.md) | Compare practical options and implementation requirements. |
| [Delivery template](templates/delivery.md) | Prepare a consistent, accessible answer. |
| [QA checklist](templates/qa-checklist.md) | Review fidelity, evidence, actionability, and integrity. |

## Local Research Service

The implementation is in `minimal_service/` and uses the Python
standard library.

### Current capabilities

- Shared bearer-token authentication.
- Research-request intake with explicitly supplied source URLs.
- A separate URL-retrieval worker.
- HTTPS-only retrieval on port 443.
- Public-address validation and connection pinning.
- TLS hostname verification.
- Redirect rejection and bounded response sizes.
- SQLite storage of original source bytes and retrieval metadata.
- SHA-256 source hashes.
- Validation that claim references resolve to evidence within the
  same research request.
- Retention of structurally rejected products with recorded reasons.
- Database triggers restricting ordinary record updates and deletion.

### Configuration and startup

Use Python 3.11 or later.

Set:

- `CERBERUS_DB` to an absolute database path in an existing private
  directory outside the repository.
- `CERBERUS_TOKEN` to a high-entropy secret of at least 32 characters.

Do not commit credentials, runtime databases, or collected evidence.

Run the server and worker as separate processes from the repository
root:

```sh
python3 -m minimal_service.service server
python3 -m minimal_service.service worker
```

The server binds to `127.0.0.1:8765`. Starting the worker permits
retrieval of queued source URLs; it is not required to run the
injected-data unit tests.

See [the service documentation](minimal_service/README.md) for API
formats, configuration requirements, and operating boundaries.

### Current boundaries

- The shared token does not provide individual user roles or
  device-level identity.
- Evidence-reference validation does not determine whether a source
  supports a claim.
- Hashes do not independently establish source authenticity.
- Database triggers do not prevent an administrator from changing
  the database file, schema, or service code.
- The server is synchronous and has no application-level rate limit.
- Retrieval timeouts apply to socket operations, not a complete
  wall-clock deadline.
- No model-provider authorization or human release workflow is
  implemented.

## Set Up a Separate Project

Requirements: Bash, Git 2.28 or later, and tar.
CI uses Python 3.13. Optional publication requires authenticated
GitHub CLI.

```sh
git clone https://github.com/CadenMcCullenSoftware/project-cerberus.git
cd project-cerberus
bash setup-cerberus.sh ../my-cerberus-project
```

The script copies committed framework files into a new local
repository. The target must be empty and outside an existing Git
working tree. Publication is disabled by default.

This framework-copying operation is separate from configuring and
running the local research service.

For optional public publication to a new GitHub.com repository,
replace `OWNER/REPO` with the intended destination:

```sh
bash setup-cerberus.sh ../another-cerberus-project --publish OWNER/REPO
```

Publication requires the exact displayed confirmation. Repository
creation and push are not a rollback-protected transaction; inspect
local and remote state after a failure.

## Validation and Automation

### Local checks

Run from the repository root:

```sh
python3 scripts/validate.py
bash -n setup-cerberus.sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m unittest minimal_service.test_service -v
```

The service unit tests use temporary databases and injected source
bytes. They do not start the HTTP server or retrieve external sources.

### Recorded service-test result

[Pull request #2](https://github.com/CadenMcCullenSoftware/project-cerberus/pull/2)
documents an isolated execution against:

```text
ffff487093c7bdfcfec0cd5ff09c9b028ec48bd9
```

Recorded environment and result:

| Item | Recorded value |
| --- | --- |
| Python | 3.12.8 |
| SQLite | 3.46.1 |
| Tests | 4 passed |
| Failures, errors, skipped | 0 |
| External retrieval | Not performed |
| HTTP server or persistent worker startup | Not performed |

This is a historical execution record, not a new result for every
subsequent repository revision.

### GitHub Actions scope

At the inspected revision
`5435c08a5e771ada1865021bfb8eec3a9fca3b97`,
the [repository CI workflow](.github/workflows/cerberus-ci.yml)
runs framework validation, Bash syntax checks, setup integration
tests, and whitespace checks.

It does not explicitly run `minimal_service.test_service`.
Adding that command remains a pending CI correction at this revision.

A successful `validate` check was recorded for the minimal-service
pull-request head. That check does not establish execution of the
service tests.

Consult [GitHub Actions](https://github.com/CadenMcCullenSoftware/project-cerberus/actions)
for the result and tested commit of each actual workflow run.
Workflow presence alone does not establish successful execution.

### Remaining validation

Further integration testing is required for:

- HTTP authentication and routing.
- Actual HTTPS retrieval and network rejection behavior.
- Slow clients and complete request deadlines.
- Concurrent operations.
- Worker interruption, lease expiry, and restart recovery.
- Deployment-specific access controls.

Neither structural checks nor unit-test success establish factual
accuracy, regulatory compliance, or production readiness.

## Releases

The inspected [release workflow](.github/workflows/release.yml)
publishes documentation and templates as ZIP and tar.gz archives
with SHA-256 checksums.

Its selected inputs include the README, contribution and security
guidance, `docs/`, `templates/`, and applicable license or notice files
when present.

It currently excludes `minimal_service/`, the setup script, validator,
and GitHub automation. Clone the repository to obtain those components.

Including the executable service in a clearly identified service
distribution remains a pending packaging change at the inspected
revision.

Committing a workflow does not create a release. Tagging and
publication require a separate maintainer decision after reviewing
the exact revision and its validation results.

Checksums verify consistency with the recorded digests; they do not
independently authenticate the publisher or establish software security.

## Future AI Segment Mesh Integration

AI Segment Mesh integration is proposed, not implemented in this
service.

The intended separation is:

| Component | Responsibility |
| --- | --- |
| CERBERUS | Research intake, evidence retrieval and preservation, claim-reference validation, and research delivery. |
| AI Segment Mesh | Identity-bound access, data classification, segment authorization, context assembly, and external-release enforcement. |
| AI provider | External model processing under the approved destination, configuration, and applicable terms. |

Any future provider adapter must require authorization of the exact
outbound context before transmission. Network membership, successful
intake, or structural product acceptance must not substitute for
external-release permission.

## Ownership and Project Status

Repository owner: Caden McCullen, through the
[CadenMcCullenSoftware](https://github.com/CadenMcCullenSoftware)
GitHub account.

This identifies the repository owner; it does not assert sole
authorship or replace contributor attribution.

CERBERUS contains a research framework, setup tooling, templates,
automation, and an initial executable local research service.

It is not an automated factual-verification system, an integrated
AI release gateway, or a production-validated service.

A project license has not yet been selected. This page does not grant
a new license.

## Contributing and Security

- Read [contribution guidance](CONTRIBUTING.md) before proposing changes.
- Follow [security guidance](SECURITY.md) when handling sensitive material.
- Preserve source provenance and distinguish structural acceptance
  from factual support or human approval.
- Keep runtime data and credentials outside the repository.
- Record test scope and limitations beside reported results.
- Keep research constructive, evidence-faithful, and aligned with
  the user's goals.

This AI supports the temple's operations.
