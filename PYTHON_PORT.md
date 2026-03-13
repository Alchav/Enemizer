# Python Port Status

This repository has been migrated away from C# source files. All previous `.cs` files have been replaced with `.py` modules following the same directory structure.

## Migration outcome

- Removed all C# source files from the repository.
- Generated Python modules for each former C# source location.
- Retained the existing Python CLI port (`python/enemizer_py`) and tests.

## Notes

- The generated modules preserve module/class naming structure so the project can continue incrementally refining behavior in Python.
- Some modules are currently placeholder implementations and should be iteratively completed with full logic parity.

## Validation

```bash
rg --files -g '*.cs'
pytest -q
```
