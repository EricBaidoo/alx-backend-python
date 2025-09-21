# 0x03-Unittests_and_integration_tests

This project demonstrates the difference between unit and integration tests in Python, using the `unittest` framework, `parameterized`, and `unittest.mock` for mocking and parameterization.

## Project Structure
- `utils.py`: Utility functions for nested map access, HTTP JSON retrieval, and memoization.
- `client.py`: Client class for integration testing (to be extended as needed).
- `fixtures.py`: Fixtures for integration and unit tests.
- `test_utils.py`: Unit tests for utility functions.
- `test_client.py`: Unit and integration tests for the client.

## How to Run Tests

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```

## Requirements
- Python 3.7+
- `parameterized` package
- `requests` package

## Learning Objectives
- Understand the difference between unit and integration tests.
- Use mocking, parameterization, and fixtures in Python tests.

---

All files are executable and follow PEP8/pycodestyle guidelines.
