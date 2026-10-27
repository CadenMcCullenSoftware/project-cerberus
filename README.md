<div align="center">

# CERBERUS

### Research that leads to action.

A canonical research framework for turning complex questions into
credible options, clear answers, and instructions people can use.

Repository owner: [Caden McCullen](https://github.com/CadenMcCullenSoftware)

[Start here](#start-here) · [Methodology](docs/methodology.md) · [Requirements](docs/product-requirements.md) · [Research templates](#research-toolkit)

</div>

---

## Purpose

CERBERUS researches the user's exact request to meet project goals, objectives, and requirements. Appropriate tools improve the research; the finished delivery provides a few credible ways to accomplish the job with instructions the user can actually follow.

The outcome is actionability. A PDF, README, or app screen is a delivery format, not the objective.

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

Follow the user's requested presentation order when supplied. Keep essential qualifications beside affected instructions and optional technical depth afterward.

## Start Here

1. Copy [the request template](templates/request.md) into a private task workspace.
2. Record the exact question, goals, category tags, constraints, and acceptance criteria.
3. Gather relevant evidence with [the evidence matrix](templates/evidence-matrix.csv).
4. Compare supported options using [the approach template](templates/approach.md).
5. Prepare the result with [the delivery template](templates/delivery.md).
6. Complete [the QA checklist](templates/qa-checklist.md).

Keep private working material in research/ and reports/. These workspaces are ignored except for their .gitkeep files. Review all tracked content before publication; ignore rules do not guarantee privacy.

## Canonical Research Pipeline

| Stage | Purpose |
| --- | --- |
| 1. Scope definition and parameter alignment | Preserve the question and establish goals, boundaries, and completion criteria. |
| 2. Multi-source information gathering | Collect relevant evidence and record its origin. |
| 3. AI-assisted synthesis and cross-verification | Compare findings, check material claims, and identify uncertainty. |
| 4. Goal-aligned technical structuring | Turn findings into accessible approaches and usable instructions. |
| 5. Quality assurance and formatting | Review accuracy of support, relevance, usability, and requested order. |

The pipeline defines research execution order, not an obligation to read methodology before reaching the answer. See [the full methodology](docs/methodology.md) and [product requirements](docs/product-requirements.md).

## Research Toolkit

| Resource | Use |
| --- | --- |
| [Request template](templates/request.md) | Define the task without losing its original wording. |
| [Evidence matrix](templates/evidence-matrix.csv) | Connect claims to sources, applicability, and verification status. |
| [Approach template](templates/approach.md) | Compare practical options and implementation requirements. |
| [Delivery template](templates/delivery.md) | Prepare a consistent, accessible answer. |
| [QA checklist](templates/qa-checklist.md) | Review fidelity, evidence, actionability, and integrity. |

## Set Up a Separate Project

Requirements: Bash, Git 2.28 or later, and tar. CI uses Python 3.13. Optional publication requires authenticated GitHub CLI.

```bash
git clone https://github.com/CadenMcCullenSoftware/project-cerberus.git
cd project-cerberus
bash setup-cerberus.sh ../my-cerberus-project
```

The script copies committed framework files into a new local repository. The target must be empty and outside an existing Git working tree. Publication is disabled by default.

For optional public publication to a new GitHub.com repository, replace OWNER/REPO with your actual destination:

```bash
bash setup-cerberus.sh ../another-cerberus-project --publish OWNER/REPO
```

Publication requires the exact displayed confirmation. Repository creation and push are not a rollback-protected transaction; inspect local and remote state after a failure.

## Validation and Automation

```bash
python3 scripts/validate.py
bash -n setup-cerberus.sh
```

[Repository checks](.github/workflows/cerberus-ci.yml) validate required files, template sections, CSV structure, private-workspace exclusions, and Bash syntax. These structural checks do not establish factual accuracy, source credibility, or absence of secrets.

[View GitHub Actions](https://github.com/CadenMcCullenSoftware/project-cerberus/actions) for actual workflow results; the presence of a workflow does not imply it has passed.

## Releases

After the reviewed main commit passes CI:

```bash
git tag -a v0.1.0 -m 'CERBERUS initial framework release'
git push origin v0.1.0
```

The [release workflow](.github/workflows/release.yml) publishes documentation and templates as ZIP and tar.gz archives with SHA-256 checksums. Tags such as v0.1.0-rc.1 are prereleases. Committing the workflow does not create a release.

## Ownership and Project Status

Repository owner: Caden McCullen, through the [CadenMcCullenSoftware](https://github.com/CadenMcCullenSoftware) GitHub account.

This identifies the repository owner; it does not assert sole authorship or replace contributor attribution.

CERBERUS currently contains the initial documentation-first framework, setup tooling, research templates, and automation. It is not yet an implemented application or automated factual-verification system.

A project license has not yet been selected. This page does not grant a new license.

## Contributing and Security

- Read [contribution guidance](CONTRIBUTING.md) before proposing a change.
- Follow [security guidance](SECURITY.md) when handling sensitive material.
- Keep research constructive, evidence-faithful, and aligned with the user's goals.
