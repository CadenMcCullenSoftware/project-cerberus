#!/usr/bin/env bash
set -euo pipefail

die() { printf 'Error: %s\n' "$*" >&2; exit 1; }
usage() {
  cat <<'EOF'
Usage: bash setup-cerberus.sh [directory] [--publish OWNER/REPO]
Run from a committed CERBERUS clone.
Requires Bash, Git 2.28+, and tar. Publication requires authenticated gh.
Creates a separate repository; publication is public and GitHub.com-only.
EOF
}
TARGET=project-cerberus
REMOTE_REPO=
POSITIONAL_SET=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --publish)
      [[ $# -ge 2 ]] || die '--publish requires OWNER/REPO.'
      REMOTE_REPO=$2; shift 2 ;;
    -*) die "Unknown option: $1" ;;
    *)
      [[ $POSITIONAL_SET -eq 0 ]] || die 'Only one directory is allowed.'
      TARGET=$1; POSITIONAL_SET=1; shift ;;
  esac
done
command -v git >/dev/null || die 'Git is required.'
command -v tar >/dev/null || die 'tar is required.'
SOURCE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
git -C "$SOURCE" rev-parse --verify HEAD >/dev/null 2>&1 || die 'Use a committed clone.'
if [[ -n $REMOTE_REPO ]]; then
  [[ $REMOTE_REPO =~ ^[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9._-]+$ ]] || die 'Use OWNER/REPO format.'
  command -v gh >/dev/null || die 'GitHub CLI is required.'
  gh auth status --hostname github.com >/dev/null 2>&1 || die 'Run gh auth login --hostname github.com.'
fi
if [[ -e $TARGET ]]; then
  [[ -d $TARGET ]] || die 'Target is not a directory.'
else
  mkdir -p -- "$TARGET"
fi
TARGET=$(cd -- "$TARGET" && pwd)
CONTENTS=$(find "$TARGET" -mindepth 1 -maxdepth 1 -print -quit) || die 'Cannot inspect target.'
[[ -z $CONTENTS ]] || die 'Target must be empty; no files overwritten.'
if git -C "$TARGET" rev-parse --show-toplevel >/dev/null 2>&1; then
  die 'Target must be outside an existing Git working tree.'
fi
inputs=(README.md CONTRIBUTING.md SECURITY.md .gitignore docs templates scripts .github setup-cerberus.sh research/.gitkeep reports/.gitkeep)
for file in LICENSE LICENSE.md LICENSE.txt NOTICE; do
  if git -C "$SOURCE" cat-file -e "HEAD:$file" 2>/dev/null; then inputs+=("$file"); fi
done
for file in "${inputs[@]}"; do
  git -C "$SOURCE" cat-file -e "HEAD:$file" || die "Missing committed input: $file"
done
git -C "$SOURCE" archive HEAD -- "${inputs[@]}" | tar -xf - -C "$TARGET"
cd -- "$TARGET"
git init -q -b main
git add -- "${inputs[@]}"
if [[ -n $(git config user.name || true) && -n $(git config user.email || true) ]]; then
  git commit -m 'chore: initialize CERBERUS framework and templates'
else
  printf 'Files staged. Configure local Git user.name and user.email, then commit.\n'
fi
printf 'Local repository ready: %s\n' "$PWD"
if [[ -n $REMOTE_REPO ]]; then
  git rev-parse --verify HEAD >/dev/null 2>&1 || die 'Commit before publication.'
  printf 'PUBLIC destination: https://github.com/%s\n' "$REMOTE_REPO"
  git log -1 --oneline
  git ls-files
  printf 'Commit identity is published metadata. Review contents before proceeding.\n'
  printf 'Type "publish %s" to confirm: ' "$REMOTE_REPO"
  CONFIRMATION=
  read -r CONFIRMATION || die 'No confirmation; nothing published.'
  if [[ $CONFIRMATION != "publish $REMOTE_REPO" ]]; then
    printf 'Publication cancelled; local repository retained.\n'; exit 0
  fi
  if ! GH_HOST=github.com gh repo create "$REMOTE_REPO" --public --source=. --remote=origin --description 'Actionable research framework with usable instructions.' --push; then
    die 'Publication failed. Inspect remote and local state before retrying; partial creation is possible.'
  fi
fi
