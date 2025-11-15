# GiftScout Agent - Test Suite Documentation

## Overview

The test suite provides comprehensive coverage of the LangGraph agent functionality including:
- **Unit Tests**: Individual tool and component testing
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Speed and efficiency validation
- **Error Handling Tests**: Exception and edge case handling

---

## Quick Start

### Running Quick Tests (No Dependencies)
```bash
# Run quick validation without pytest
cd agent
python quick_test.py
```

Expected output:
```
✓ PASS: Module Imports
✓ PASS: Redis Connection
✓ PASS: State Creation
✓ PASS: Tool Structure
✓ PASS: Graph Compilation
✓ PASS: JSON Serialization
✓ PASS: Performance Baseline
```

### Running Full Test Suite
```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Run all tests
npm run test:agent:all

# Or directly with pytest
cd agent && pytest test_agent.py -v
```

---

## Available Test Commands

### Quick Validation
```bash
npm run test:agent
```
Runs the quick test suite with colored output. No pytest required.

### Unit Tests Only
```bash
npm run test:agent:unit
```
Tests individual components in isolation.

### Integration Tests
```bash
npm run test:agent:integration
```
Tests complete workflows and component interactions.

### All Tests with Full Output
```bash
npm run test:agent:all
```
Runs complete test suite with verbose output.

### Coverage Report
```bash
npm run test:agent:coverage
```
Generates HTML coverage report in `htmlcov/index.html`.

---

## Test Structure

### 1. **Module Import Tests**
Validates that all required dependencies are available:
- LangChain modules
- LangGraph modules  
- Agent module
- External libraries (Redis, Tavily)

```bash
pytest agent/test_agent.py::TestImports -v
```

### 2. **Tool Tests**

#### Search Social Trends
```python
# Tests trending topic discovery
def test_search_social_trends_success()
def test_search_social_trends_no_results()
def test_search_social_trends_api_error()
def test_search_social_trends_missing_api_key()
```

#### Search Products by Budget
```python
# Tests product search functionality
def test_search_products_success()
def test_search_products_empty_results()
def test_search_products_api_error()
```

#### Filter Recommendations
```python
# Tests product filtering and ranking
def test_filter_recommendations_success()
def test_filter_recommendations_limits_to_5()
def test_filter_recommendations_empty_input()
```

### 3. **Redis Integration Tests**
Validates caching and state persistence:
```python
def test_save_to_redis()
def test_get_from_redis_existing()
def test_get_from_redis_nonexistent()
def test_redis_connection_error()
```

### 4. **State Management Tests**
Tests the GiftScoutState data structure:
```python
def test_state_initialization()
def test_state_update()
```

### 5. **Workflow Tests**
Tests async agent operations:
```python
async def test_chat_node_creates_command()
async def test_chat_node_error_handling()
```

### 6. **Integration Tests**
Tests complete workflows:
```python
def test_complete_gift_search_workflow()
```

### 7. **Performance Tests**
Validates response times and efficiency:
```python
def test_search_response_time()
def test_filter_performance_with_large_dataset()
```

### 8. **Error Handling Tests**
Tests edge cases and error conditions:
```python
def test_malformed_json_input()
def test_invalid_budget_values()
def test_unicode_persona_handling()
```

---

## Running Specific Tests

### Test a single class
```bash
cd agent && pytest test_agent.py::TestSearchSocialTrends -v
```

### Test a single function
```bash
cd agent && pytest test_agent.py::TestSearchSocialTrends::test_search_social_trends_success -v
```

### Test with specific markers
```bash
cd agent && pytest test_agent.py -m asyncio -v
cd agent && pytest test_agent.py -m integration -v
cd agent && pytest test_agent.py -m performance -v
```

### Run with output capture disabled (for debugging)
```bash
cd agent && pytest test_agent.py -s -v
```

---

## Mock Objects Used

### Mock Redis
```python
@pytest.fixture
def mock_redis():
    """Mock Redis client for testing without actual Redis."""
    with patch('agent.redis_client') as mock:
        mock.ping = Mock(return_value=True)
        mock.set = Mock()
        mock.get = Mock()
        mock.expire = Mock()
        yield mock
```

### Mock Tavily
```python
@pytest.fixture
def mock_tavily():
    """Mock Tavily client for testing without API calls."""
    with patch('agent.tavily_client') as mock:
        yield mock
```

### Mock GiftScout State
```python
@pytest.fixture
def gift_scout_state():
    """Create a test GiftScout state."""
    return GiftScoutState(
        messages=[],
        persona_description="20-year-old tech enthusiast",
        budget=100.0,
        search_session_id="test-session-123",
        ...
    )
```

---

## Test Results Examples

### Successful Test Run
```
======================== test session starts =========================
collected 45 items

agent/test_agent.py::TestSearchSocialTrends::test_search_social_trends_success PASSED
agent/test_agent.py::TestSearchSocialTrends::test_search_social_trends_no_results PASSED
agent/test_agent.py::TestSearchSocialTrends::test_search_social_trends_api_error PASSED
agent/test_agent.py::TestSearchProductsByBudget::test_search_products_success PASSED
...

======================= 45 passed in 0.82s ==========================
```

### Quick Test Output
```
GiftScout Agent - Quick Test Suite
============================================================

============================================================
TEST: Module Imports
============================================================
ℹ INFO: Importing langchain modules...
✓ PASS: LangChain imports successful
ℹ INFO: Importing langgraph modules...
✓ PASS: LangGraph imports successful
ℹ INFO: Importing agent module...
✓ PASS: Agent module imported successfully

============================================================
TEST SUMMARY
============================================================

Results: 7/7 tests passed

  ✓ PASS - imports
  ✓ PASS - redis
  ✓ PASS - state
  ✓ PASS - tools
  ✓ PASS - graph
  ✓ PASS - json
  ✓ PASS - performance

✓ All tests passed!
```

---

## Debugging Failed Tests

### 1. Check Test Output
```bash
# Run with verbose output
npm run test:agent:all

# Run specific test with full output
cd agent && pytest test_agent.py::TestSearchSocialTrends::test_search_social_trends_success -vv -s
```

### 2. Print Debug Information
```bash
# Add print statements in test
def test_example():
    result = search_social_trends("test")
    print(f"Result: {result}")  # This will show with -s flag
    assert result is not None

# Run with -s to capture prints
cd agent && pytest test_agent.py::test_example -s
```

### 3. Inspect Mock Calls
```python
def test_with_mock_calls(mock_tavily):
    search_social_trends("test")
    
    # Check if mock was called
    assert mock_tavily.search.called
    print(mock_tavily.search.call_args)
    print(mock_tavily.search.call_count)
```

### 4. Check Dependencies
```bash
# Verify pytest is installed
python -c "import pytest; print(pytest.__version__)"

# Verify pytest-asyncio
python -c "import pytest_asyncio; print('OK')"

# Verify test requirements
pip install -r agent/requirements.txt
pip install pytest pytest-asyncio pytest-mock pytest-cov
```

---

## Continuous Integration

### GitHub Actions Example
```yaml
name: Test Agent

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r agent/requirements.txt
          pip install pytest pytest-asyncio pytest-mock
      
      - name: Quick test
        run: npm run test:agent
      
      - name: Full test suite
        run: npm run test:agent:all
```

---

## Coverage Reports

### Generate Coverage
```bash
npm run test:agent:coverage
```

### View Coverage Report
```bash
# HTML report
open htmlcov/index.html

# Terminal report (shown during test run)
# Lines:    95%
# Branches: 87%
# Functions: 92%
```

### Expected Coverage Targets
- **Lines**: >90%
- **Branches**: >80%
- **Functions**: >90%

---

## Troubleshooting

### Import Errors
```
ImportError: No module named 'pytest'
```
**Solution**: Install test dependencies
```bash
pip install pytest pytest-asyncio pytest-mock
```

### Redis Connection Errors
```
ConnectionRefusedError: [Errno 111] Connection refused
```
**Solution**: Start Redis before running tests
```bash
redis-server
# Or skip Redis tests:
cd agent && pytest test_agent.py -m "not redis" -v
```

### Async/Await Issues
```
RuntimeError: Event loop is closed
```
**Solution**: Make sure pytest-asyncio is installed and configured
```bash
pip install pytest-asyncio
# pytest.ini should have: asyncio_mode = auto
```

### Mock Not Working
```
AttributeError: <MagicMock> has no attribute 'search'
```
**Solution**: Verify mock patch path matches module import path
```python
# If agent.py imports: from tavily import TavilyClient
# Mock path should be: patch('agent.tavily_client')
```

---

## Best Practices

### 1. Test Organization
- Group related tests in test classes
- Use descriptive test names
- Follow the arrange-act-assert pattern

### 2. Mocking
- Mock external dependencies (Redis, API calls)
- Use fixtures for reusable mock objects
- Verify mock calls when needed

### 3. Assertions
- Use clear, specific assertions
- Include helpful error messages
- Test both success and failure cases

### 4. Performance
- Set reasonable timeouts
- Test with realistic data sizes
- Monitor memory usage in loops

### 5. Documentation
- Document complex test scenarios
- Include example test data
- Comment on non-obvious mocking

---

## Running Tests in Different Environments

### Local Development
```bash
# Quick tests
npm run test:agent

# Full tests with Redis running
redis-server &
npm run test:agent:all
```

### CI/CD Pipeline
```bash
# No external dependencies
npm run test:agent

# Or with full setup
docker-compose up -d redis
npm run test:agent:all
docker-compose down
```

### Docker
```bash
# Build test image
docker build -t giftscount-test -f Dockerfile.test .

# Run tests
docker run giftscount-test npm run test:agent:all
```

---

## Resources

- **Pytest Documentation**: https://docs.pytest.org/
- **Pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **LangChain Testing**: https://docs.langchain.com/docs/guides/testing
- **LangGraph Testing**: https://langchain-ai.github.io/langgraph/concepts/testing/
- **Python unittest.mock**: https://docs.python.org/3/library/unittest.mock.html

---

## Next Steps

1. **Run quick tests**: `npm run test:agent`
2. **Check coverage**: `npm run test:agent:coverage`
3. **Add new tests** for new features
4. **Monitor performance**: `npm run test:agent:all`
5. **Set up CI/CD**: Configure automated testing
