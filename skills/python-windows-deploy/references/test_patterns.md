# Pre-Deploy Test Patterns

Guide for writing tests to verify before building.

## Test Structure

```
project/
├── src/
│   └── core.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── conftest.py      # pytest config
└── main.py
```

## pytest Basic Patterns

### Function Tests

```python
# tests/test_core.py
import pytest
from src.core import process_data, validate_input

def test_process_data_success():
    result = process_data("valid input")
    assert result is not None
    assert result["status"] == "success"

def test_process_data_empty():
    with pytest.raises(ValueError):
        process_data("")

def test_validate_input():
    assert validate_input("test") == True
    assert validate_input("") == False
```

### Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value", "items": [1, 2, 3]}

@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("test content")
    return file

# tests/test_core.py
def test_with_sample_data(sample_data):
    assert "key" in sample_data

def test_file_processing(temp_file):
    content = temp_file.read_text()
    assert content == "test content"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("test", "TEST"),
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

## CLI Application Tests

### Command-line Argument Tests

```python
import subprocess
import sys

def test_cli_help():
    result = subprocess.run(
        [sys.executable, "main.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()

def test_cli_version():
    result = subprocess.run(
        [sys.executable, "main.py", "--version"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_cli_process():
    result = subprocess.run(
        [sys.executable, "main.py", "input.txt"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
```

### Direct argparse Module Tests

```python
from main import parse_args, main

def test_parse_args_default():
    args = parse_args([])
    assert args.verbose == False

def test_parse_args_verbose():
    args = parse_args(["-v"])
    assert args.verbose == True

def test_main_with_args(capsys):
    main(["--test"])
    captured = capsys.readouterr()
    assert "Test mode" in captured.out
```

## File I/O Tests

```python
def test_read_config(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text('{"setting": "value"}')

    from src.core import read_config
    config = read_config(str(config_file))
    assert config["setting"] == "value"

def test_write_output(tmp_path):
    output_file = tmp_path / "output.txt"

    from src.core import write_output
    write_output(str(output_file), "test content")

    assert output_file.exists()
    assert output_file.read_text() == "test content"
```

## Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific file
python -m pytest tests/test_core.py -v

# Specific function
python -m pytest tests/test_core.py::test_process_data_success -v

# With coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Stop on first failure
python -m pytest tests/ -x

# Show output
python -m pytest tests/ -v -s
```

## Post-Build Tests

Basic verification after exe build:

```python
# tests/test_exe.py
import subprocess
import os

EXE_PATH = "dist/myapp.exe"

def test_exe_exists():
    assert os.path.exists(EXE_PATH)

def test_exe_runs():
    result = subprocess.run(
        [EXE_PATH, "--help"],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0

def test_exe_basic_function():
    result = subprocess.run(
        [EXE_PATH, "test_input"],
        capture_output=True,
        text=True,
        timeout=60
    )
    assert result.returncode == 0
    assert "expected output" in result.stdout
```
