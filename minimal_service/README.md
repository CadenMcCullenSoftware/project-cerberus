# CERBERUS Minimal Research Service

## [Status and Purpose]
First local implementation slice: authenticated request intake, a separate URL-retrieval worker, persisted source bytes and hashes, work-product validation, and deletion denial. Source code and tests are supplied; no passing execution result or deployment is claimed.

No existing framework files are replaced. Python standard library only. No model, crawler, automatic synthesis, or publication endpoint is included.

## [Supported Audience]
Developers and researchers evaluating a local single-operator research pipeline. Not a multi-tenant or public-facing service.

## [Local Configuration]
Use Python 3.11 or later. CERBERUS_DB must identify a new database file in an existing private directory outside the repository. Protect that directory with operating-system permissions. Set CERBERUS_TOKEN to a high-entropy secret of at least 32 characters. Do not commit secrets or collected evidence.

After separate execution authorization, run the server and worker as two processes from the repository root:

```sh
python3 -m minimal_service.service server
python3 -m minimal_service.service worker
```

The server binds only to 127.0.0.1:8765. All implemented routes require Authorization: Bearer followed by CERBERUS_TOKEN. POST bodies require application/json and Content-Length. No services are started by committing these files.

## [API]
- POST /requests: {"question":"Compare a technical option","sources":["https://example.org/"]}. Returns request_id and queues only supplied URLs.
- GET /requests/{request_id}: returns request, job states, and evidence IDs, URLs, retrieval times, hashes, and media types. Raw source bodies remain in the database and are not rendered as HTML.
- POST /products: {"request_id":"returned-id","text":"Draft","claims":[{"statement":"A statement","evidence_ids":["returned-evidence-id"]}]}. Returns 201 for structurally accepted records or 422 for recorded validation rejection. Accepted does not mean approved for publication, factually verified, or human-authorized.
- DELETE: denied; no deletion API is provided. Unsupported methods are not implemented.

## [Worker and Persistence]
The worker allows HTTPS on port 443, resolves only public IP addresses, pins the connection to the checked address with hostname certificate verification, does not follow redirects, and accepts only bounded uncompressed text/plain, text/html, or application/json responses. Maximum source and API body size: 262144 bytes. Do not submit private, credential-bearing, or otherwise sensitive URLs. Retrieval is not exhaustive research or semantic verification.

SQLite persists requests, jobs, immutable evidence, work products, and events. Queue claims use write transactions and 120-second leases; expired claims can be reclaimed. Completion is token-checked. Source-fetch failures are recorded as failed, without automatic retry. A crashed worker can recover an expired running claim. Network timeouts are per socket operation, not a complete wall-clock deadline. A slow source may therefore exceed a lease; stale completion is discarded.

Database triggers deny DELETE on service tables and UPDATE on research records; queue status updates remain permitted. This is application-level protection, not protection against an administrator who can modify the database file, schema, or service code. No authenticated reviewer service, operating-system hardening, or tamper-proof storage is claimed. Schema initialization is additive and intended only for a new dedicated database.

## [Validation and Tests]
Validation checks nonblank product text, claim structure, and evidence existence within the same research request. It does not discover undeclared claims or judge whether sources support them. Rejected products with a valid request and top-level structure are retained with reasons; malformed API inputs are rejected without storing their submitted content.

After separate test authorization:

```sh
python3 -m unittest minimal_service.test_service -v
```

Tests use temporary databases and injected source bytes, not external network access. They cover intake-to-evidence-to-product flow, recorded rejection, deletion/update denial, and invalid-source rejection. HTTP authentication, actual HTTPS retrieval, process interruption, and adversarial cases require additional integration tests before broader use. Tests clean up only their newly created temporary fixtures.

## [Design Basis]
This slice implements the requested intake, evidence, validation, and deletion controls alongside the existing CERBERUS research framework. It is not the full eight-stage governance contract or a Time Thread PostgreSQL deployment. Original source bytes are preserved separately from submitted synthesis. Nothing is automatically released. Corrections require new records rather than overwriting evidence.

This AI supports the temple's operations.
