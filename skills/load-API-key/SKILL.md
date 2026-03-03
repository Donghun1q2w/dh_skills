---
name: load-API-key
description: Shared API key loader using settings.ini and .env files from a department server. Use when the user asks to "load API keys", "read API key from server", "set up shared API key", "configure .env loading", "write API key loader code", or when implementing centralized API key management in Python, C#, or VBA projects. Also use when referencing shared server paths for .env files or setting up settings.ini-based configuration.
argument-hint: "[optional: target language (python/csharp/vba) or specific API key name]"
---

# Shared API Key Loader

Standard pattern for loading API keys from a `.env` file on a shared department server.

## Core Structure

```
project/
├── settings.ini              ← Shared server path config (Git-trackable)
├── shared_apikey_loader.py   ← Key loader utility
├── .env                      ← Local fallback (excluded from Git, add to .gitignore)
└── your_app.py               ← Your application
```

## How It Works

1. Read the shared server `.env` path from `settings.ini`
2. Load the `.env` file into environment variables using `python-dotenv`
3. Fall back to a local `.env` if the shared server is unreachable
4. Access individual keys via `os.getenv()`

## settings.ini Format

```ini
[server]
# UNC path or local mount path
env_path = \\192.168.1.100\shared\config\.env

[options]
encoding = utf-8
use_local_fallback = true
local_env_path = .env
```

The shared server path must only be managed in `settings.ini`. Never hard-code paths in source code.

## Usage Patterns

### Python
```python
from shared_apikey_loader import load_shared_keys, get_key

load_shared_keys()
api_key = get_key("OPENAI_API_KEY")
```

### C#
```csharp
var loader = new SharedApiKeyLoader();
loader.LoadSharedKeys();
string apiKey = loader.GetKey("OPENAI_API_KEY");
```

### VBA
```vb
LoadSharedKeys
Dim apiKey As String
apiKey = GetKey("OPENAI_API_KEY")
```

## Coding Guidelines

1. **Never write API keys directly in source code** — always reference via `get_key()`
2. **Manage server paths only in settings.ini** — no code changes needed when the path changes
3. **Always add local .env to .gitignore** — `echo ".env" >> .gitignore`
4. **Mask key values when printing/logging** — `list_keys()` applies automatic masking
5. **Maintain the fallback mechanism** — enable local development when the shared server is unavailable

## Reference Code

See the `references/` directory for full implementations:

### Python
- `references/shared_apikey_loader.py` — Core loader module
- `references/usage_example.py` — Usage example

### C#
- `references/SharedApiKeyLoader.cs` — C# implementation (IniParser-based)

### VBA
- `references/SharedApiKeyLoader.bas` — VBA module (for Excel/Access, etc.)

### Common
- `references/settings.ini` — Configuration file template
- `references/sample.env` — Sample .env file

When adding API key loading to a new project, use the reference files above and customize them to fit your project.

## Security Notes

- Set NTFS permissions on the shared server `.env` file to restrict read access to department members only
- `settings.ini` is safe to include in Git (contains only path info, no keys)
- Never commit `.env` files to Git
- When rotating keys, update only the shared server `.env` — changes propagate to all users automatically
