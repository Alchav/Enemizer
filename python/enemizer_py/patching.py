from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Iterable


@dataclass
class PatchObject:
    address: int
    patch_data: list[int] = field(default_factory=list)


class RandomizerPatch:
    """Python port of EnemizerCLI.RandomizerPatch."""

    def __init__(self, base_patch_json: str, randomizer_patch_json: str) -> None:
        self.patches: list[PatchObject] = []
        self._convert_patch(json.loads(base_patch_json))
        self._convert_patch(json.loads(randomizer_patch_json))

    def _convert_patch(self, raw_patch: object) -> None:
        if not isinstance(raw_patch, list):
            raise ValueError("patch JSON must be an array")

        for entry in raw_patch:
            if not isinstance(entry, dict):
                raise ValueError(f"invalid patch property: {entry!r}")

            for key, value in entry.items():
                if not isinstance(value, list):
                    raise ValueError(f"invalid patch property value: {value!r}")
                try:
                    address = int(key)
                except ValueError as exc:
                    raise ValueError(f"invalid address: {key}") from exc
                self.patches.append(PatchObject(address=address, patch_data=[int(x) & 0xFF for x in value]))

    def patch_rom(self, rom: bytearray) -> None:
        for patch in self.patches:
            end = patch.address + len(patch.patch_data)
            rom[patch.address:end] = bytes(patch.patch_data)


def apply_patches(rom_bytes: bytes, patches: Iterable[PatchObject]) -> bytes:
    rom = bytearray(rom_bytes)
    for patch in patches:
        end = patch.address + len(patch.patch_data)
        rom[patch.address:end] = bytes(patch.patch_data)
    return bytes(rom)
