# PyInstaller Spec File Template

Guide for writing spec files for complex build configurations.

## Basic Template

```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],                    # Entry point
    pathex=[],                      # Additional search paths
    binaries=[],                    # Binary files
    datas=[                         # Data files (src, dst)
        ('data', 'data'),
        ('config.json', '.'),
    ],
    hiddenimports=[                 # Hidden imports
        'module_name',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],                    # Modules to exclude
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyApp',                   # Output file name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                       # UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                   # Console mode
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',                # Icon (optional)
)
```

## Multi-file Build (onedir)

```python
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MyApp',
    debug=False,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='MyApp',
)
```

## Adding Version Info

`version_info.txt`:

```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
  ),
  kids=[
    StringFileInfo([
      StringTable('040904B0', [
        StringStruct('CompanyName', 'My Company'),
        StringStruct('FileDescription', 'My Application'),
        StringStruct('FileVersion', '1.0.0'),
        StringStruct('ProductName', 'MyApp'),
        StringStruct('ProductVersion', '1.0.0'),
      ])
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

Usage in spec:

```python
exe = EXE(
    ...
    version='version_info.txt',
    ...
)
```

## Excluding Unnecessary Modules (reduce file size)

```python
a = Analysis(
    ...
    excludes=[
        'tkinter',
        'unittest',
        'email',
        'html',
        'http',
        'xml',
        'pydoc',
    ],
    ...
)
```

## Runtime Hooks

Code to run at app startup:

`runtime_hook.py`:
```python
import os
import sys

# Set environment variables
os.environ['MY_VAR'] = 'value'
```

In spec:
```python
a = Analysis(
    ...
    runtime_hooks=['runtime_hook.py'],
    ...
)
```
