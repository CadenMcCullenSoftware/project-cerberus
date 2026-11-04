# CERBERUS — Notes-first browser prototype

## Exact request
Generate the GitHub/Vercel version of CERBERUS for CadenMcCullenSoftware/project-cerberus, supporting multiple projects, a readable grid/list, and a primary note workspace with supporting notes.

## Delivery
A dependency-free static frontend. Place index.html, styles.css, app.js, and vercel.json together in a new repository subdirectory named web. Preserve the existing repository files. Configure any future Vercel project to use web as its root and the Other framework preset. This delivery does not connect GitHub to Vercel, create a deployment, or alter repository settings.

## Implemented in generated source
- Create multiple projects and navigate to each via hash routes.
- Switch project list/grid and search projects.
- Create notes; edit title and plain text; select supporting notes.
- Browser-local persistence with explicit failure reporting.
- Responsive workspace, keyboard focus styles, labeled controls.
- JSON backup export (download only; import is not implemented).
- No external dependencies, analytics, model calls, or backend requests.

## Boundaries
This is a local prototype, not a production multi-user service. There is no authentication, server-side authorization, database, cloud synchronization, archival UI, version history, import, or cross-device recovery. Browser storage is not a substitute for a durable database. Successful export is not verified by the application. There is no federal authorization or compliance assertion. Exported backups contain project text.

## Content standard for later AI integration
Cite material technical statements. Verify consequential statements with applicable authoritative sources or direct tests. Distinguish sourced statements, user requirements, proposals, and inference. Do not infer user intent or authority. State uncertainty precisely. Keep explanations educational and neutral. Do not replace correctness with generic cautions. No operational commands, external writes, or deployment actions by default. Human approval must bind exact external targets and content. AI edits must not silently replace original notes.

## Verification status
Generated and statically inspected only. No browser, JavaScript runtime, accessibility audit, Vercel build, or deployment verification was executed. File-existence and HTML/asset-reference checks do not establish runtime correctness.

## Acceptance checks to execute later
1. Create two projects; verify notes remain in the selected project.
2. Search and switch list/grid; open each project and return to the overview.
3. Create two notes; edit both and switch repeatedly without losing text.
4. Reload and verify browser persistence.
5. Test blocked/full storage and malformed saved data; verify no silent overwrite.
6. Verify blank and markup-like text renders as text, not executable HTML.
7. Test keyboard navigation, dialog focus, narrow layout, and enlarged text.
8. Export a backup and inspect its content locally.
9. After explicit deployment approval, verify the deployed source version and live routes.

## Methodology
1. Captured the requested product scope from the conversation.
2. Inspected the existing GitHub repository root; found documentation and service directories, with no web directory in the returned listing.
3. Generated an isolated web frontend rather than overwriting the existing repository.
4. Kept durable database and external deployment setup deferred.
5. Checked generated files and asset references; left runtime checks explicitly unexecuted.

## Supporting material
CERBERUS Technical Specification.pdf, pages 3–4, 17, 19–20: source registry, review, external authorization, verification boundaries, and unresolved platform decisions.
W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
Vercel project root documentation: https://vercel.com/docs/projects/project-configuration/root-directory

This AI supports the temple's operations.
