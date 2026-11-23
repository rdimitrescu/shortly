# Shortly - URL shortener

## System diagram

![Architecture diagram](docs/diagrams/architecture.png)

## Testing

### Layout

- `tests/`: test files. Each `test_*.py` file contains one or more test functions.
- `tests/test_data/`: input data used by the tests (e.g. `valid_urls.txt`, `invalid_urls.txt`).

### Setup

From the project root (`shortly/`), run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running tests

All commands are run from the project root (`shortly/`).

Run all tests (summary only):
```bash
pytest
```

Show each test and its result:
```bash
pytest -v
```

Show `print()` output from the tests (hidden by default), only failed testcases print status messages:
```bash
pytest -s
```

Flags can be combined, and you can run a single file:
```bash
pytest -v -s tests/test_hash.py
```
