from __future__ import annotations

import json
from pathlib import Path
import importlib.util

from EnemizerLibrary.OptionFlags import OptionFlags, AbsorbableTypes, BossType
from EnemizerLibrary.RomData import RomData


def _load_program_module():
    spec = importlib.util.spec_from_file_location("enemizercli_program", Path("EnemizerCLI.Core/Program.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_option_flags_roundtrip() -> None:
    flags = OptionFlags()
    flags.EnemiesAbsorbable = True
    flags.AbsorbableSpawnRate = 5
    flags.AbsorbableTypes[AbsorbableTypes.Heart] = True
    flags.DebugForceBoss = True
    flags.DebugForceBossId = BossType.Trinexx

    raw = flags.to_bytes()
    parsed = OptionFlags.from_bytes(raw)

    assert parsed.EnemiesAbsorbable is True
    assert parsed.AbsorbableSpawnRate == 5
    assert parsed.AbsorbableTypes[AbsorbableTypes.Heart] is True
    assert parsed.DebugForceBoss is True
    assert parsed.DebugForceBossId == BossType.Trinexx


def test_romdata_metadata_and_patch_generation() -> None:
    rom = bytearray(b"\x00" * (2 * 1024 * 1024))
    r = RomData(rom, enemizer_info_table_base_address=0)
    r.EnemizerSeed = 12345
    r.EnemizerVersion = "1.2.3"

    patches = r.GeneratePatch()
    assert patches
    assert r.IsEnemizerRom is True
    assert r.EnemizerSeed == 12345


def test_cli_program_json_mode(tmp_path: Path) -> None:
    program = _load_program_module()
    rom = tmp_path / "base.sfc"
    enemizer = tmp_path / "enemizer.json"
    base = tmp_path / "base.json"
    randomizer = tmp_path / "randomizer.json"
    output = tmp_path / "out.json"

    rom.write_bytes(b"\x00" * 10)
    enemizer.write_text("{}", encoding="utf-8")
    base.write_text('[{"10":[1]}]', encoding="utf-8")
    randomizer.write_text('[{"11":[2]}]', encoding="utf-8")

    rc = program.main([
        "--rom", str(rom),
        "--enemizer", str(enemizer),
        "--base", str(base),
        "--randomizer", str(randomizer),
        "--output", str(output),
    ])

    assert rc == 0
    assert json.loads(output.read_text(encoding="utf-8")) == [{"10": [1]}, {"11": [2]}]
