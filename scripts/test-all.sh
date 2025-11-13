#!/usr/bin/env bash
#
# Comprehensive test script to validate everything before PR
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================="
echo "  Comprehensive Testing Suite"
echo "========================================="
echo ""

# Track test results
PASSED=0
FAILED=0

run_test() {
    local test_name="$1"
    local test_command="$2"

    echo -n "Testing: $test_name... "

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

# Test 1: Python syntax
echo "=== Python Syntax Tests ==="
run_test "Python syntax validation" "python3 -m py_compile cli/bp"

# Test 2: CLI functionality
echo ""
echo "=== CLI Tests ==="
run_test "CLI version" "./cli/bp --version"
run_test "CLI list command" "./cli/bp list | head -1"
run_test "CLI cache stats" "./cli/bp cache stats"

# Test 3: Search performance
echo ""
echo "=== Performance Tests ==="
echo -n "Testing: Search performance... "
SEARCH_TIME=$(python3 -c "
from cli.utils.search import search_docs
import time
start = time.time()
search_docs('kubernetes', limit=5)
elapsed = (time.time() - start) * 1000
print(f'{elapsed:.2f}')
")

if (( $(echo "$SEARCH_TIME < 100" | bc -l) )); then
    echo -e "${GREEN}PASS${NC} (${SEARCH_TIME}ms < 100ms)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (${SEARCH_TIME}ms >= 100ms)"
    ((FAILED++))
fi

echo -n "Testing: Index build... "
INDEX_TIME=$(python3 -c "
from cli.utils.search import build_search_index
import time
start = time.time()
build_search_index()
elapsed = (time.time() - start) * 1000
print(f'{elapsed:.2f}')
")

if (( $(echo "$INDEX_TIME < 1000" | bc -l) )); then
    echo -e "${GREEN}PASS${NC} (${INDEX_TIME}ms < 1000ms)"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} (${INDEX_TIME}ms >= 1000ms)"
    ((FAILED++))
fi

# Test 4: Documentation
echo ""
echo "=== Documentation Tests ==="
run_test "Documentation files exist" "test -d docs && test -f mkdocs.yml"
run_test "README exists" "test -f README.md"
run_test "CONTRIBUTING exists" "test -f CONTRIBUTING.md"

# Test 5: Snippets
echo ""
echo "=== Snippet Tests ==="
run_test "Snippets directory exists" "test -d snippets"
run_test "Snippet loading" "python3 -c 'from cli.utils.snippets import load_snippets; snippets = load_snippets(); exit(0 if len(snippets) > 0 else 1)'"

# Test 6: File structure
echo ""
echo "=== Structure Tests ==="
run_test "CLI directory exists" "test -d cli"
run_test "bp executable" "test -x cli/bp"
run_test "Scripts directory exists" "test -d scripts"
run_test "Install script exists" "test -f scripts/install-bp.sh"

# Test 7: No cache files
echo ""
echo "=== Cleanup Tests ==="
CACHE_COUNT=$(find . -name "__pycache__" -o -name "*.pyc" 2>/dev/null | wc -l)
echo -n "Testing: No Python cache files... "
if [ "$CACHE_COUNT" -eq 0 ]; then
    echo -e "${GREEN}PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}FAIL${NC} ($CACHE_COUNT cache files found)"
    ((FAILED++))
fi

# Test 8: GitHub Actions
echo ""
echo "=== GitHub Actions Tests ==="
run_test "Test workflow exists" "test -f .github/workflows/test.yml"
run_test "Docs workflow exists" "test -f .github/workflows/docs.yml"
run_test "PR workflow exists" "test -f .github/workflows/pr.yml"
run_test "Release workflow exists" "test -f .github/workflows/release.yml"
run_test "Labeler config exists" "test -f .github/labeler.yml"

# Summary
echo ""
echo "========================================="
echo "  Test Summary"
echo "========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo "Ready to create PR"
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    echo "Please fix issues before creating PR"
    exit 1
fi
