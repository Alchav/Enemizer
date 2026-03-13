from __future__ import annotations

import json
from pathlib import Path

from enemizer_py.cli import main


def _write(path: Path, content: bytes) -> None:
    path.write_bytes(content)


def test_json_mode_writes_merged_patch(tmp_path: Path) -> None:
    rom = tmp_path / "base.sfc"
    enemizer = tmp_path / "enemizerOptions.json"
    base_patch = tmp_path / "base2patched.json"
    randomizer_patch = tmp_path / "randomizerPatch.json"
    output = tmp_path / "output.json"

    _write(rom, b"\x00" * 10)
    enemizer.write_text("{}", encoding="utf-8")
    base_patch.write_text('[{"16":[1,2]}]', encoding="utf-8")
    randomizer_patch.write_text('[{"18":[3,4]}]', encoding="utf-8")

    code = main([
        "--rom", str(rom),
        "--enemizer", str(enemizer),
        "--base", str(base_patch),
        "--randomizer", str(randomizer_patch),
        "--output", str(output),
    ])

    assert code == 0
    assert json.loads(output.read_text(encoding="utf-8")) == [{"16": [1, 2]}, {"18": [3, 4]}]


def test_binary_mode_writes_expanded_rom(tmp_path: Path) -> None:
    rom = tmp_path / "base.sfc"
    enemizer = tmp_path / "enemizerOptions.json"
    output = tmp_path / "output.sfc"

    _write(rom, b"\xAA" * 1024)
    enemizer.write_text("{}", encoding="utf-8")

    code = main([
        "--rom", str(rom),
        "--enemizer", str(enemizer),
        "--binary",
        "--output", str(output),
    ])

    assert code == 0
    out = output.read_bytes()
    assert len(out) == 2 * 1024 * 1024
    assert out[:4] == b"\xAA\xAA\xAA\xAA"


def test_json_mode_requires_base_and_randomizer(tmp_path: Path) -> None:
    rom = tmp_path / "base.sfc"
    enemizer = tmp_path / "enemizerOptions.json"
    output = tmp_path / "output.json"

    _write(rom, b"\x00" * 10)
    enemizer.write_text("{}", encoding="utf-8")

    code = main([
        "--rom", str(rom),
        "--enemizer", str(enemizer),
        "--output", str(output),
    ])

    assert code == 1
    assert not output.exists()
