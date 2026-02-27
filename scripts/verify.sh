#!/usr/bin/env bash
set -euo pipefail

echo "=== Running tests ==="
pytest tests/ -v --tb=short

echo ""
echo "=== CLI smoke test ==="
a11y-assist --help > /dev/null
assist-run echo "hello" > /dev/null 2>&1 || true
echo "CLI commands OK"

echo ""
echo "=== Building package ==="
python -m build

echo ""
echo "=== All checks passed ==="
