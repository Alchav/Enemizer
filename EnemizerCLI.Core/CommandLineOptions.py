from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CommandLineOptions:
    BaseRomFilename: str
    SeedNumber: str = ""
    BasePatchJsonFilename: str | None = None
    RandomizerPatchJsonFilename: str | None = None
    EnemizerOptionsJsonFilename: str = ""
    OutputFilePath: str = ""
    BinaryMode: bool = False
