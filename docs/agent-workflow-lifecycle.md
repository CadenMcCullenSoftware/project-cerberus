# CERBERUS Agent Workflow Lifecycle

## [Document Status]
Status: Proposed. Review date: 2026-10-28.
This documentation defines a proposed engineering lifecycle. It does not install runtime controls, authorize execution, certify compliance, or establish application readiness.

## [Exact Review Question]
Review it against the repository's existing implementation

## [Direct Answer]
CERBERUS implements a documentation-first research framework, templates, setup tooling, structural validation, and CI/release automation. The proposed agent lifecycle extends beyond those delivered capabilities. Documentation archive publication is not application deployment.

## [Repository Baseline]
Repository: CadenMcCullenSoftware/project-cerberus.
Inspected main revision: 96b70e40a5c7c954a8a2e9e0cad2c727e912403a.

- scripts/validate.py checks required files, template headings, evidence CSV structure, and private-workspace tracking and ignore rules. It does not establish source credibility or comprehensive security assurance.
- .github/workflows/cerberus-ci.yml invokes structural validation, Bash syntax checks, setup integration tests, and whitespace checks. Source inspection does not establish successful execution.
- .github/workflows/release.yml responds to version tags, validates structure and Bash syntax, checks tag format and main-branch ancestry, packages documentation/templates, generates checksums, and creates a GitHub release.
- The inspected publishing job has no explicit human-approval step and does not run the setup integration suite. Repository-level approval and protection settings were not verified. Main-branch ancestry alone does not establish successful CI for the tagged commit.

## [Step 1: Clarify Requirements and Research]
1. Preserve the exact question, goals, category tags, scope, constraints, audience, deliverables, and acceptance criteria.
2. Establish source-selection criteria before design.
3. Record source provenance, relevant passages, applicability, limitations, and discrepancies in the evidence record.
4. Separate user requirements, source material, assumptions, and synthesized conclusions.

Proposed gate: design requires reviewed research or an explicitly authorized exemption. Source counts and retrieval records do not establish correctness.

## [Step 2: Design Architecture and Structure]
1. Define directory layout, components, interfaces, dependencies, and versioned schemas.
2. Define states, authorized transitions, failure states, and gate owners.
3. Specify data minimization, permissions, retention, deletion, redaction, and audit requirements.
4. Record alternatives, rationale, limitations, and migration decisions.

Proposed gate: review architecture and data handling before implementation.

## [Step 3: Build and Configure]
1. Implement approved configuration, modules, templates, and schemas.
2. Link artifacts to requirements and exact revisions.
3. Enforce transitions at execution boundaries rather than only in saved records.
4. Define transaction boundaries, bounded retries, idempotency, and recovery for applicable persistent or external actions.
5. Keep direct source material distinct from generated outputs.

Proposed gate: implementation remains within approved scope; material scope changes require renewed authorization where applicable.

## [Step 4: Security and Safety Review]
1. Review relevant threats, privacy, accessibility, stakeholder impacts, and residual risks.
2. Test input handling, access controls, and approval-denial paths.
3. Run applicable dependency, secret, and vulnerability checks; record scope and limitations.
4. Validate schemas and cross-field invariants.
5. Link findings, mitigations, dispositions, and reviewer decisions to the exact revision.

Proposed gate: unresolved blocking findings prevent release. A caller-supplied completion flag does not demonstrate a completed audit.

## [Step 5: Test, Document, and Release]
1. Execute normal-path and failure-mode tests, including malformed records, invalid timestamps, missing references, unauthorized transitions, revision mismatch, and approval-service failure where applicable.
2. Test concurrent writes, interrupted transactions, retries, restoration, and recovery where applicable.
3. Record environment, commands, revision, results, and limitations.
4. Complete user guidance, technical documentation, examples, and release notes.
5. Verify applicable CI results for the exact release commit, including setup integration tests.
6. Obtain authenticated human approval bound to the exact revision, artifact, and release scope. Changed revisions require new approval.
7. Verify approval at publication time and deny release when required checks or authorization are unavailable or invalid.
8. Record publication outcome and recovery instructions; do not represent partial failure as success.

## [Required Artifacts]
Requirements record; research record; design decision; revision-linked build record; security review; test results; authenticated revision-bound approval; release outcome and recovery record. Each record identifies its scope, owner role, applicable revision, and unresolved limitations.

## [Compatibility]
The CERBERUS research pipeline remains the method for preparing research deliveries. These five phases describe agent engineering and do not silently replace that pipeline.

Separate supplementary project files define eight ordered stages: scope -> clarification -> research -> design -> safety_review -> draft -> human_review -> release. The five phases are engineering groupings, not a replacement five-entry schema. The reference model has no dedicated build/testing stage and places safety review before drafting. Post-build review needs explicit artifact linkage or a versioned schema change. Those reference artifacts are not established as this repository's agent runtime.

## [Implementation Options]
1. Documentation-first: use this lifecycle as a manual checklist without claiming automated enforcement.
2. Validation-first: add versioned contracts, procedural validation, examples, and failure-mode tests. Keep record validation separate from authorization.
3. Runtime-governed: implement trusted approval verification, execution-boundary checks, transactional persistence, and tested recovery after deployment requirements are approved.

## [Research Methodology]
1. Inspect repository roots and record revisions.
2. Read governance and CERBERUS status statements and requirements.
3. Inspect structural validation, CI, and release source files.
4. Compare supplementary schemas, validator, example, and tests.
5. Map proposed phases to existing documentation, source checks, and implementation gaps.

This was a read-only implementation comparison, not an independently completed systematic academic literature review. Tests were not executed. CI outcomes and repository protection settings were not verified.

## [Supporting Source Locations]
- README.md, scripts/validate.py, .github/workflows/cerberus-ci.yml, and .github/workflows/release.yml at CERBERUS revision 96b70e40a5c7c954a8a2e9e0cad2c727e912403a.
- Related ai-assistant-governance-workflow README.md and INFORMATION_ONLY_REQUIREMENTS.md at ba6af7b02f9e85d23d4226b4b63c65d872aaf8d1.
- Separate project reference artifacts: workflow.schema.json, validate_workflow.py, test_workflow.py, example_workflow.json, and WORKFLOW_DOCUMENTATION.md.

## [Acceptance Checklist]
- [ ] Research reviewed or exemption authorized.
- [ ] Architecture and data handling reviewed.
- [ ] Build, audit, test, and approval records identify the intended revision.
- [ ] Applicable security and failure-mode tests have recorded results.
- [ ] Approval is authenticated, valid, scoped, and revision-bound.
- [ ] Publishing verifies required CI results and approval.
- [ ] Publication outcome and recovery instructions are recorded.

## [Statement]
This AI supports the temple's operations.
