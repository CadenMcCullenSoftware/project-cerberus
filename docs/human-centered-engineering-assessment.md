# Human-Centered Engineering and Its Relationship to Axiom Hive

## 1. Purpose and scope

This assessment examines two documents as described in the supplied material:

1. A human-centered engineering specification for an order-management service.
2. A research report discussing human-centered engineering across technology and industry.

The engineering specification defines expected development behavior, architectural boundaries, business rules, testing expectations, and human decision authority. The research report provides broader context and discusses potential benefits and limitations.

This assessment is based on descriptions in the user-supplied `pasted_text_1793534424.txt`. The original two documents were not independently inspected for this assessment. References to implementation behavior, coverage, CI configuration, and deployment artifacts require confirmation against those documents and their corresponding repository. The uploaded source is not included in this commit.

This document is an assessment, not a replacement for authoritative project requirements or authorization to change them.

## 2. Executive assessment

The engineering specification connects software requirements with accountability for affected people. Its stated priorities include preserving foundational requirements, separating business rules from technical interfaces, evaluating human consequences, and distinguishing evidence from assumptions.

The research report broadens that discussion to industrial and technological applications. Its examples and conclusions require stronger source traceability and clearer separation between intended benefits, provider claims, and measured outcomes.

Together, the documents describe an engineering approach. They do not, by themselves, demonstrate a completed platform, enforceable governance controls, successful deployment, or measured human benefit.

## 3. Engineering requirements and human authority

The specification is described as requiring engineers to:

- Preserve foundational requirements unless an authorized person approves a change.
- Keep business rules distinct from interface and infrastructure concerns.
- Support implementation and deployment claims with identifiable evidence.
- Evaluate effects on direct users and other affected people.
- Distinguish observations, assumptions, interpretations, and uncertainty.
- Present proposed changes for human review rather than treating suggestions as authorization.

These are requirements for engineering conduct. Their enforcement must be assessed separately. An instruction to obtain approval is not, on its own, an implemented authorization control.

The governing document should identify decision authority, decisions requiring approval, the applicable foundational-principles version, and the scope of any delegated authority.

## 4. Architecture and dependency boundaries

The described order-management scaffold uses four responsibility areas:

| Layer | Intended responsibility |
| --- | --- |
| Domain | Business entities, value objects, state transitions, and invariants. |
| Application | Use cases and interfaces through which required capabilities are accessed. |
| Infrastructure | Storage implementations, configuration, and technical adapters. |
| Presentation | HTTP and command-line interfaces translating external input into application operations. |

The intention is to keep business behavior independent of particular interfaces and storage technologies. Replacing an in-memory repository should not require moving database-specific behavior into order rules.

This remains an architectural intention until code demonstrates appropriate dependency boundaries. Layer names and directory structure alone do not establish that separation. The reference order service must not be conflated with the CERBERUS implementation.

## 5. Domain rules and unresolved decisions

The supplied assessment attributes these requirements to the order-service specification:

- Orders begin as empty drafts; only drafts can be edited.
- Placement requires at least one order line.
- Canceled orders cannot be edited or placed; repeated cancellation is rejected.
- Order-line currencies must match the order currency.
- Quantities must be positive integers, excluding Boolean values.
- Money uses decimal arithmetic; values must be finite and exactly representable at the specified two-decimal-place precision.
- External interfaces represent monetary amounts as decimal strings.

These are stated requirements, not verified implementation results. Three decisions require explicit treatment:

1. Unit-price positivity: decide whether it is a business invariant or an HTTP-specific restriction. A business invariant belongs at the relevant domain boundary; a general-purpose money object need not reject every negative amount.
2. Currency validation: distinguish a three-uppercase-letter format check from validation against assigned ISO 4217 codes. SIX maintains the ISO 4217 currency-code lists [S1].
3. Monetary precision: preserve the stated distinction between `1.230`, which is exactly representable to two decimal places, and `1.005`, which is not. Do not introduce silent rounding without an approved requirement.

The two-decimal-place rule is a project rule, not evidence of complete support for all currencies.

## 6. Interfaces, error handling, and deployment boundaries

| Described feature or artifact | What it does not establish |
| --- | --- |
| Custom domain-error handling | A uniform response format for every framework, validation, or infrastructure error. |
| A liveness endpoint | Readiness of external dependencies. |
| A multi-stage Dockerfile with a non-root runtime | A successful build, passing smoke test, or secure deployment. |
| A Compose configuration | Production suitability. |
| A Kubernetes reference manifest with placeholders | A deployment-ready cluster configuration. |
| An in-memory repository | Durable persistence or recovery after process termination. |

The supplied assessment distinguishes framework request-validation errors from handled domain errors. Preserve that distinction until code and tests establish a broader contract. Authentication, authorization, payments, inventory, and fulfillment must not be described as included without separately identified and verified implementations.

## 7. Testing and verification evidence

The described testing strategy separates domain and use-case tests from adapter and interface tests. References to a 90% coverage threshold, artifact builds, container smoke tests, and security workflows remain reported characteristics, not verified results of this assessment.

Verification records should distinguish:

1. Test code exists.
2. Tests executed against an identified revision.
3. Assertions passed.
4. Coverage met its defined threshold.
5. Artifacts built successfully.
6. A deployed system passed relevant operational checks.

Tests exercising HTTP behavior through an in-process ASGI application establish behavior within that boundary, not network, proxy, container, orchestration, or deployed-environment behavior. Link requirements to test identifiers and execution evidence. The presence of tests does not prove test-driven development or complete correctness.

## 8. Human-impact assessment

Make the human-impact requirement repeatable through a proposed assessment record:

| Field | Required information |
| --- | --- |
| Human need | The problem and people experiencing it. |
| Affected groups | Direct users and others experiencing consequences. |
| Intended benefit | The improvement expected from the change. |
| Baseline | Conditions before the change. |
| Risks and burdens | Potential harm, exclusion, accessibility barriers, and operational burdens. |
| Evaluation method | How benefits and harms will be assessed. |
| Evidence | Observations, test results, and source material. |
| Limitations | Uncertainty and unevaluated populations or conditions. |
| Human decision | Reviewer, decision, scope, date, and applicable requirements version. |

This is a proposed operational improvement, not an existing implemented control. Intended benefit and demonstrated benefit must remain distinct.

## 9. Research quality and external context

State the research question before drawing conclusions. If the original question was unspecified, disclose that prominently: an exploratory overview is not a direct evaluation of the order-service specification.

Classify evidence as original empirical studies, research reviews, standards and policy publications, provider-authored descriptions, or testimonials and commentary. Do not label all these categories as primary data.

The European Commission describes Industry 5.0 as a forward-looking vision centered on human-centricity, sustainability, and resilience, not a specific legal directive [S2].

ISO 9241-210:2019 provides requirements and recommendations for human-centred design principles and activities throughout the lifecycle of computer-based interactive systems. Its relevance does not establish project conformity; its scope does not provide detailed coverage of all health and safety concerns [S3].

Human-centered engineering has recognized standards and policy foundations. Benefits of a particular implementation still require context-specific evaluation. Those foundations do not establish that this project has achieved measurable financial, safety, or usability improvements.

## 10. Research examples requiring verification

The supplied assessment names consultancy examples, Lotwork, and purported research reviews. It includes author-year references, publication counts, and a September 2026 review claim without sufficient bibliographic detail to verify them.

Until original references are supplied:

- Do not present the examples as independently verified.
- Do not replace a possibly mismatched citation with a similar paper without establishing identity.
- Do not retain precise publication counts without traceable sources.
- Label provider performance statements as provider claims.
- Record author, title, publication venue, date, identifier, and the finding used.

The inconsistent terms `Kensei Engineering` and `Canto Engineering` remain flagged for source confirmation. Do not silently substitute an assumed research field.

## 11. Relationship to CERBERUS and Axiom Hive

The supplied assessment proposes this conceptual separation:

| Component | Proposed responsibility |
| --- | --- |
| Human-centered engineering specification | Requirements, practices, and decision boundaries. |
| Research methodology | Evidence gathering, evaluation, and synthesis. |
| CERBERUS | Research organization, source preservation, and claim-to-evidence traceability. |
| AI segment mesh | A proposed information-release boundary for external AI services. |
| Human authorization | Approval of consequential actions within an explicitly defined scope. |

This is a conceptual mapping, not evidence of integration or enforced controls.

- Source existence does not establish claim support.
- Claim support does not authorize disclosure.
- Permission to disclose does not establish factual accuracy.
- Structural validation does not constitute human approval.
- Human approval does not substitute for technical verification.

The report's six ergonomic considerations and Axiom Hive's six constitutional pillars remain separate frameworks; this assessment does not establish equivalence.

## 12. Recommended next steps and status

1. Identify the authoritative foundational-principles document and version.
2. Resolve unit-price positivity and currency-validation requirements.
3. Normalize headings and numbering.
4. Link requirements to tests and recorded results.
5. Adopt a repeatable human-impact assessment record.
6. Define rollback expectations and verification evidence.
7. Complete the research bibliography and remove unsupported precision.
8. Keep the order-service reference architecture distinct from CERBERUS.

The supplied material establishes a stated approach and useful requirements and review questions. It does not establish verified code behavior, passing CI, successful deployment, standards conformance, integrated authorization enforcement, or measured human outcomes.

## 13. Editorial corrections and source provenance

- Replaced the corrupted phrase `Python 3.1 toll-free API` with `Python-based order-management API`; the intended Python version remains unconfirmed.
- Corrected `ISO 42117` to `ISO 4217` [S1].
- Corrected `ISO 9241-2110:2019` to `ISO 9241-210:2019` [S3].
- Replaced damaged headings and separated artifact descriptions from unsupported conclusions.
- Consolidated duplicated introductions and supplied an explicit status statement in place of the unfinished ending.
- Reclassified unsupported independent-verification claims and left uncertain research terms unresolved.

Source material: user-supplied `pasted_text_1793534424.txt`. This assessment is not a reproduction or independent audit of its two underlying documents. External references support only their associated factual statements, not project compliance or implementation claims.

### External references

- [S1] SIX, Global Financial Data Standards: https://www.six-group.com/en/products-services/financial-information/market-reference-data/data-standards.html
- [S2] European Commission, Industry 5.0: https://research-and-innovation.ec.europa.eu/research-area/industrial-research-and-innovation/industry-50_en
- [S3] ISO, ISO 9241-210:2019: https://www.iso.org/es/contents/data/standard/07/75/77520.html
