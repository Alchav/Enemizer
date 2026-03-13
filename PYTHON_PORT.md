# Python Port Status

This repository has been migrated away from C# source files.

## Current state

- C# source files have been replaced with Python modules.
- Core functionality has started being ported with real implementations in:
  - `EnemizerCLI.Core/Program.py`
  - `EnemizerCLI.Core/RandomizerPatch.py`
  - `EnemizerLibrary/OptionFlags.py`
  - `EnemizerLibrary/RomData.py`
- Unit tests cover CLI patch flow, option flag serialization, and ROM metadata handling.

## Still in progress

- Large portions of `EnemizerLibrary` subsystems (boss/enemy randomization, graph logic, GUI parity) still need full behavior parity beyond placeholder modules.

## Validation

```bash
pytest -q
rg --files -g '*.cs' | wc -l
```
