#!/usr/bin/env bash
# find-polluter.sh — Runs test files one-by-one to identify which test creates
# an unwanted file, directory, or state pollution.

set -euo pipefail

if [[ "${1:-}" == "--help" || $# -lt 2 ]]; then
  echo "Usage: bash scripts/find-polluter.sh <file_or_dir_to_check> <test_file_glob> [test_command]"
  echo "Example: bash scripts/find-polluter.sh '.git' 'src/**/*.test.ts' 'npx vitest run'"
  exit 0
fi

POLLUTION_TARGET="$1"
TEST_PATTERN="$2"
TEST_RUNNER="${3:-npm test}"

echo "Searching for test that creates: $POLLUTION_TARGET"
echo "Pattern: $TEST_PATTERN"

for test_file in $TEST_PATTERN; do
  if [[ -e "$POLLUTION_TARGET" ]]; then
    echo "Warning: $POLLUTION_TARGET already exists before running $test_file"
    exit 1
  fi

  echo "Testing: $test_file"
  $TEST_RUNNER "$test_file" > /dev/null 2>&1 || true

  if [[ -e "$POLLUTION_TARGET" ]]; then
    echo "FOUND POLLUTER: $test_file created $POLLUTION_TARGET"
    exit 0
  fi
done

echo "No polluter found across matching test files."
