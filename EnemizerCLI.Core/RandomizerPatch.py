from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class PatchObject:
    address: int
    patchData: list[int] = field(default_factory=list)


class RandomizerPatch:
    def __init__(self, base_patch_json: str, patch_json: str):
        self.Patches: list[PatchObject] = []
        self._convert_patch(json.loads(base_patch_json))
        self._convert_patch(json.loads(patch_json))

    def _convert_patch(self, patch_base: object) -> None:
        if not isinstance(patch_base, list):
            raise ValueError("patch json must be a JSON array")

        for patch_entry in patch_base:
            if not isinstance(patch_entry, dict):
                raise ValueError(f"invalid patch property: {patch_entry}")
            for key, val in patch_entry.items():
                if not isinstance(val, list):
                    raise ValueError(f"invalid patch property value: {val}")
                try:
                    address = int(key)
                except ValueError as exc:
                    raise ValueError(f"invalid address: {key}") from exc
                self.Patches.append(PatchObject(address=address, patchData=[int(x) & 0xFF for x in val]))

    def PatchRom(self, rom: bytearray) -> None:
        for patch in self.Patches:
            rom[patch.address : patch.address + len(patch.patchData)] = bytes(patch.patchData)
