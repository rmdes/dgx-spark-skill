#!/usr/bin/env bash
# ABOUTME: Opens or updates one tracking issue per maintenance check; closes it when the check comes back clean.
# ABOUTME: Usage: upsert-issue.sh "<title>" <report.md> <findings>   (needs GH_TOKEN and issues: write)
set -euo pipefail
title="$1"; report="$2"; findings="$3"
label="kb-maintenance"

gh label create "$label" --color BFD4F2 --description "Scheduled knowledge-base maintenance report" --force >/dev/null

number=$(gh issue list --state open --label "$label" --search "\"$title\" in:title" --json number,title \
  --jq "map(select(.title == \"$title\")) | .[0].number // empty")

if [ "$findings" -gt 0 ]; then
  if [ -n "$number" ]; then
    gh issue edit "$number" --body-file "$report"
    echo "Updated issue #$number"
  else
    gh issue create --title "$title" --label "$label" --body-file "$report"
  fi
elif [ -n "$number" ]; then
  gh issue close "$number" --comment "The latest scheduled check found nothing to do."
  echo "Closed issue #$number"
else
  echo "Clean, no open issue."
fi
