---
name: python-windows-deploy
description: "Build and deploy Python projects as standalone Windows 10/11 console applications (.exe). Generate single executable files that run without Python installed. PyInstaller-based build with automated pre-deploy test verification. Use when converting Python scripts to exe, deploying to Windows without dependencies, or building console applications."
---

# Python Windows Deploy

Workflow for building and deploying Python projects as Windows console executables (.exe).

## Workflow

```
1. Analyze Project → 2. Run Tests → 3. Build → 4. Verify → 5. Package
```

### 1. Analyze Project

Check at project root:
- Entry point file (main.py, app.py, cli.py, etc.)
- requirements.txt or pyproject.toml
- Data files/resources (if any)

```python
# Example project structure
project/
├── main.py          # Entry point
├── src/
│   └── core.py
├── data/            # Data to bundle
├── requirements.txt
└── tests/
    └── test_core.py
```

### 2. Run Tests

Ensure all tests pass before building:

```bash
# pytest (recommended)
python -m pytest tests/ -v

# unittest
python -m unittest discover tests/

# Single test file
python -m pytest tests/test_core.py -v
```

Do not proceed with build if tests fail. Fix issues and retry.

### 3. PyInstaller Build

#### Environment Setup

```bash
# Create and activate virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller
```

#### Basic Build (single file)

```bash
# Single exe build (console mode)
pyinstaller --onefile --console main.py
```

#### Build with Data Files

```bash
# On Windows, --add-data separator is semicolon (;)
pyinstaller --onefile --console \
    --add-data "data;data" \
    --add-data "config.json;." \
    main.py
```

#### Hidden Imports

When using dynamic imports:

```bash
pyinstaller --onefile --console \
    --hidden-import=module_name \
    --hidden-import=another_module \
    main.py
```

#### Using Spec Files (complex builds)

After creating `build.spec`:

```bash
pyinstaller build.spec
```

### 4. Build Verification

Verify in `dist/` folder after build:

```bash
# Run test on Windows
dist\main.exe --help
dist\main.exe [test arguments]
```

Verification checklist:
- Executable runs successfully
- All features work correctly
- No error messages
- Data file access works

### 5. Packaging

Distribution structure:

```
release/
├── app.exe
├── README.txt      # Usage instructions
└── LICENSE.txt     # (optional)
```

## PyInstaller Key Options

| Option | Description |
|--------|-------------|
| `--onefile` | Generate single exe file |
| `--console` | Show console window (required for CLI apps) |
| `--name=NAME` | Set output file name |
| `--icon=FILE.ico` | Set icon |
| `--add-data "src;dst"` | Include data files |
| `--hidden-import=MOD` | Add hidden imports |
| `--collect-all=PKG` | Collect entire package (for large packages like pandas, numpy) |
| `--clean` | Clean previous build cache |

## Data File Access (Runtime)

Accessing bundled data files at runtime:

```python
import sys
import os

def resource_path(relative_path):
    """Return resource path inside PyInstaller bundle"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Usage
config_path = resource_path("config.json")
data_dir = resource_path("data")
```

## Troubleshooting

### ModuleNotFoundError

```bash
pyinstaller --hidden-import=missing_module main.py
```

### Data Files Not Found

Verify `resource_path()` function is used. Check `--add-data` paths.

### Antivirus False Positives

Use `--key` option for encryption, or apply code signing.

### File Size Optimization

```bash
# UPX compression (requires UPX installed)
pyinstaller --onefile --upx-dir=/path/to/upx main.py
```

## References

- Detailed spec file guide: `references/spec_template.md`
- Test pattern examples: `references/test_patterns.md`
