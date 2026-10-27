#!/usr/bin/env python3
"""Structural checks only; not factual or comprehensive security verification."""
import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS = []
REQUIRED = [
    'README.md', 'CONTRIBUTING.md', 'SECURITY.md', '.gitignore',
    'setup-cerberus.sh', 'docs/methodology.md', 'docs/product-requirements.md',
    'templates/request.md', 'templates/evidence-matrix.csv',
    'templates/approach.md', 'templates/delivery.md', 'templates/qa-checklist.md',
    '.github/ISSUE_TEMPLATE/research-request.md', '.github/pull_request_template.md',
    '.github/workflows/cerberus-ci.yml', '.github/workflows/release.yml',
]
SECTIONS = {
    'templates/request.md': ['Exact Question', 'Intended Outcome',
        'Project Goals and Requirements', 'Category Tags', 'Constraints',
        'Audience', 'Requested Presentation Order', 'Delivery Format', 'Acceptance Criteria'],
    'templates/approach.md': ['Purpose', 'Suitable When', 'Prerequisites',
        'Instructions', 'Expected Outcome', 'Verify the Result', 'Evidence'],
    'templates/delivery.md': ['Exact Question', 'Direct Answer', 'Credible Approaches',
        'Step-by-Step Instructions', 'Supporting Findings', 'Research Methodology',
        'Material Limitations', 'Optional Technical Detail', 'Research Record'],
}
HEADER = ('claim_id,claim,category_tags,source_title,source_author_or_organization,'
          'source_reference,source_date_or_version,accessed_date,'
          'supporting_passage_or_result,applicability,limitations_or_conflicts,'
          'verification_status,practical_implication').split(',')

for name in REQUIRED:
    path = ROOT / name
    if not path.is_file() or not path.read_bytes().strip():
        ERRORS.append(f'Missing or empty required file: {name}')

for name, headings in SECTIONS.items():
    path = ROOT / name
    if not path.is_file():
        continue
    try:
        lines = path.read_text(encoding='utf-8').splitlines()
    except UnicodeError as exc:
        ERRORS.append(f'{name}: {exc}')
        continue
    positions = []
    for title in headings:
        heading = '## ' + title
        if heading not in lines:
            ERRORS.append(f'{name}: missing {heading}')
        else:
            positions.append(lines.index(heading))
    if name == 'templates/delivery.md' and positions != sorted(positions):
        ERRORS.append('Delivery template canonical default order is invalid.')

matrix = ROOT / 'templates/evidence-matrix.csv'
if matrix.is_file():
    try:
        with matrix.open(encoding='utf-8', newline='') as handle:
            reader = csv.reader(handle, strict=True)
            if next(reader, None) != HEADER:
                ERRORS.append('Evidence matrix schema is invalid.')
            for row in reader:
                if row and len(row) != len(HEADER):
                    ERRORS.append(f'CSV field count at line {reader.line_num}')
    except (UnicodeError, csv.Error) as exc:
        ERRORS.append(str(exc))

try:
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z'], cwd=ROOT
    ).decode('utf-8').split('\0')
    for name in tracked:
        if name.startswith(('research/', 'reports/')) and name not in {
            'research/.gitkeep', 'reports/.gitkeep'
        }:
            ERRORS.append(f'Private workspace file is tracked: {name}')
    for name in ['research/private-probe.txt', 'reports/private-probe.txt']:
        result = subprocess.run(
            ['git', 'check-ignore', '--quiet', '--', name], cwd=ROOT, check=False
        )
        if result.returncode != 0:
            ERRORS.append(f'Private workspace is not ignored: {name}')
except (OSError, subprocess.CalledProcessError) as exc:
    ERRORS.append(f'Git checks failed: {exc}')

if ERRORS:
    raise SystemExit('\n'.join(ERRORS))
print('CERBERUS structural validation passed; content review remains required.')
