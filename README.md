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

### Status vocabulary

| Term | Meaning |
| --- | --- |
| Implemented | Code exists on main at a named commit. |
| Tested | Test cases exist for the named conditions. |
| CI verified | An Actions run on that exact SHA passed; record the event and tested scope. |
| Unverified | No independent verification record is available for the stated assessment. |
| Not established | The function cannot be claimed from the inspected material. |

Proposed mappings and unrun tests do not establish implementation.
Test-case presence and test execution are separate records.

### Function-level assessment

Assessment date: November 1, 2026. Inspected implementation baseline:
`f3471215eef2ee824633264a66b99934420ea61f`.

| Function | Status | Tested | CI verified |
| --- | --- | --- | --- |
| Request authentication, validation, storage, source queueing | Implemented | | |
| Query classification | Not established | | |
| Structural evidence-reference validation | Implemented | | |
| Semantic source-support checking | Not established | | |
| Executable synthesis and recommendation | Not established | | |

Blank Tested and CI verified cells mean those statuses have not been
established by this assessment. The relevant test contents and a
successful exact-SHA run must be inspected before filling them in.

Implementation locations in `minimal_service/service.py`:

- `Handler.handle_request()` checks bearer-token authentication.
- `submit()` validates and stores the question and queues supplied
  source URLs; it does not classify queries.
- `product()` validates claim structure and checks that referenced
  evidence belongs to the same request. It does not determine whether
  source content supports a claim.

### Conceptual three-head model

The three-head model is a conceptual grouping, not three established
executable components. The implemented service and the documented
five-stage research methodology must remain distinct.

| Conceptual head | Description and boundary |
| --- | --- |
| Head 1: Perception | Request authentication, validation, storage, and source queueing. Query classification is not established. |
| Head 2: Verification | Structural evidence-reference validation. Semantic source-support checking is not established. |
| Head 3: Guidance | Documented AI-assisted synthesis and recommendations. Executable synthesis and recommendation are not established. |

### CI provenance

CI status for `f3471215eef2ee824633264a66b99934420ea61f`:
Unverified as of November 1, 2026.

Run `41333988500` remains unconfirmed. Its head SHA, conclusion,
event, and tested scope were not retrieved in this assessment.
Unsuccessful retrieval is not an empty run list or a failed CI run.
No claim of independent retrieval or successful execution is made.

Before assigning CI verified, record together:

1. The full assessed commit SHA.
2. The run URL and successful conclusion.
3. The event type and checkout target.
4. The workflow, jobs, and commands actually executed.
5. The assessment date.

A matching `headSha` alone is insufficient. A successful workflow
verifies only its recorded scope, not every function in this table.

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
AI-assisted synthesis and cross-verification are documented research
activities, not an implemented semantic verification engine.

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
- SHA-256 digests support source-integrity checks. They do not
  establish source accuracy or authenticity. Assurance depends on
  protecting the reference digest.
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

These are documented commands, not execution results from this
assessment. The service tests are described as using temporary
databases and injected source bytes rather than external retrieval.
Their contents were not inspected for the function-level assessment
above, so no Tested status is assigned there.

### Historical service-test record

The previous README attributed an isolated execution to
[pull request #2](https://github.com/CadenMcCullenSoftware/project-cerberus/pull/2)
against:

```text
ffff487093c7bdfcfec0cd5ff09c9b028ec48bd9
```

| Item | Previously recorded value |
| --- | --- |
| Python | 3.12.8 |
| SQLite | 3.46.1 |
| Tests | 4 passed |
| Failures, errors, skipped | 0 |
| External retrieval | Not performed |
| HTTP server or persistent worker startup | Not performed |

This historical record was not independently reverified in the
November 1, 2026 assessment. It does not establish Tested or CI
verified status for `f3471215eef2ee824633264a66b99934420ea61f`
or for the README update commit.

### GitHub Actions scope

The previous README described the
[repository CI workflow](.github/workflows/cerberus-ci.yml) at
`5435c08a5e771ada1865021bfb8eec3a9fca3b97` as running framework
validation, Bash syntax checks, setup integration tests, and
whitespace checks, without explicitly running
`minimal_service.test_service`. That is a historical scope
description, not a verified account of the pinned revision's run.

The earlier recorded successful `validate` check was not
independently reverified in this assessment and does not establish
execution of service tests. Inspect the actual workflow and run
steps before assigning a tested scope or deciding which CI changes
remain necessary.

Consult [GitHub Actions](https://github.com/CadenMcCullenSoftware/project-cerberus/actions)
for the result and tested commit of each actual workflow run.
Workflow presence alone does not establish successful execution.
The exact-SHA provenance gap is recorded under Implementation Status.

### Remaining validation

Further integration testing is required for:

- HTTP authentication and routing.
- Actual HTTPS retrieval and network rejection behavior.
- Slow clients and complete request deadlines.
- Concurrent operations.
- Worker interruption, lease expiry, and restart recovery.
- Deployment-specific access controls.

Tests cover the listed conditions. They do not establish comprehensive
coverage, security assurance, or production readiness. Structural
checks and unit-test results do not establish factual accuracy or
regulatory compliance.

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

SHA-256 digests support source-integrity checks. They do not establish
source accuracy or authenticity. Assurance depends on protecting the
reference digest. Checksums do not establish software security.

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
