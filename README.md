# Project CERBERUS

Canonical Research Methodology & Execution Framework

## Purpose

Research the user's exact request to meet project goals, objectives, and requirements. Use appropriate tools to improve research and provide a few credible ways to accomplish the job with instructions the user can actually use.

Actionability is the outcome. A PDF, README, or app screen is a format, not the objective.

## Start Here

1. Record the exact question with [the request template](templates/request.md).
2. Define goals, category tags, constraints, and acceptance criteria.
3. Gather relevant evidence using [the evidence matrix](templates/evidence-matrix.csv).
4. Compare supported approaches with [the approach template](templates/approach.md).
5. Write a practical answer with [the delivery template](templates/delivery.md).
6. Complete [the QA checklist](templates/qa-checklist.md).

Keep private working material in research/ and reports/. These workspaces are ignored except for their .gitkeep files. Review all tracked content before publishing; ignore rules do not guarantee privacy.

## Canonical Execution Order

1. Scope definition and parameter alignment.
2. Multi-source information gathering.
3. AI-assisted synthesis and cross-verification.
4. Goal-aligned technical structuring.
5. Quality assurance and formatting.

See [methodology](docs/methodology.md) and [product requirements](docs/product-requirements.md).

## Default Delivery Order

Follow the user's requested order when supplied. Otherwise: exact question; direct answer; credible approaches; step-by-step instructions; supporting findings; research methodology; optional technical detail.

Put usable information first. Keep evidence relevant to category goals. Explain material limitations without unrelated opinions or steering the conclusion.

## Setup

Requirements: Bash, Git 2.28 or later, and tar. Python 3.13 is used by CI. Optional publication requires authenticated GitHub CLI.

From a clone of this repository:

```bash
bash setup-cerberus.sh ../my-cerberus-project
```

The script copies committed framework files into a new, separate local repository. It requires an empty target and does not publish by default.

```bash
bash setup-cerberus.sh ../my-cerberus-project --publish OWNER/REPO
```

Publication is explicitly GitHub.com-only, public, and requires typing the exact displayed destination confirmation. Creation and push are not a rollback-protected transaction; inspect local and remote state after failure.

## Validation

```bash
python3 scripts/validate.py
bash -n setup-cerberus.sh
```

CI checks required files, template sections, evidence CSV structure, private-workspace exclusions, and Bash syntax. These checks do not establish factual accuracy, evidence credibility, or absence of secrets.

## Releases

After the reviewed main commit passes CI:

```bash
git tag -a v0.1.0 -m 'CERBERUS initial framework release'
git push origin v0.1.0
```

A version tag triggers a documentation release with ZIP, tar.gz, and SHA-256 checksums. Tags such as v0.1.0-rc.1 are prereleases. No tag or release is created by committing the workflow.

## Status

This is the complete initial documentation-first framework, not an implemented application or automated factual-verification system. No application stack or license has been selected.

See [contributing](CONTRIBUTING.md) and [security guidance](SECURITY.md).
