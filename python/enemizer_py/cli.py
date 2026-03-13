from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path

from .patching import RandomizerPatch

ENEMIZER_ROM_SIZE = 2 * 1024 * 1024


def _get_seed(seed_number: str) -> int:
    if not seed_number:
        return random.randint(0, 999_999_999)

    try:
        seed = int(seed_number)
    except ValueError as exc:
        raise ValueError("Invalid Seed Number entered. Please enter an integer value.") from exc

    if seed < 0:
        raise ValueError("Please enter a positive Seed Number.")
    return seed


def _load_json_file(path: str) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _expand_rom(raw_data: bytes) -> bytearray:
    data = bytearray(raw_data)
    if len(data) < ENEMIZER_ROM_SIZE:
        data.extend(b"\x00" * (ENEMIZER_ROM_SIZE - len(data)))
    return data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python port of EnemizerCLI.Core")
    parser.add_argument("--rom", required=True, help="path to the base rom file")
    parser.add_argument("--seed", default="", help="seed number")
    parser.add_argument("--base", help="path to the base2patched.json (not used in binary mode)")
    parser.add_argument("--randomizer", help="path to the randomizerPatch.json (not used in binary mode)")
    parser.add_argument("--enemizer", required=True, help="path to the enemizerOptions.json")
    parser.add_argument("--output", required=True, help="path to the intended output file")
    parser.add_argument(
        "--binary",
        action="store_true",
        help=(
            "operate in binary mode (takes already randomized SFC and "
            "applies enemizer directly to ROM)"
        ),
    )
    return parser


def _require_json_patch_inputs(options: argparse.Namespace) -> None:
    if not options.base:
        raise ValueError("--base is required unless --binary is used")
    if not options.randomizer:
        raise ValueError("--randomizer is required unless --binary is used")


def make_enemizer_rom(options: argparse.Namespace) -> None:
    # Keep this read for compatibility with C# behavior where the file must exist/parse.
    _load_json_file(options.enemizer)

    rom_data = _expand_rom(Path(options.rom).read_bytes())

    # In binary mode, base/randomizer inputs are optional and ignored by C#.
    if options.base and options.randomizer:
        merged_patch = RandomizerPatch(
            Path(options.base).read_text(encoding="utf-8"),
            Path(options.randomizer).read_text(encoding="utf-8"),
        )
        merged_patch.patch_rom(rom_data)

    Path(options.output).write_bytes(rom_data)
    print(f"Generated SFC file {options.output}")


def make_enemizer_json_patch(options: argparse.Namespace) -> None:
    _require_json_patch_inputs(options)

    # Keep these reads for compatibility with C# workflow.
    _load_json_file(options.enemizer)
    _ = _expand_rom(Path(options.rom).read_bytes())

    merged_patch = RandomizerPatch(
        Path(options.base).read_text(encoding="utf-8"),
        Path(options.randomizer).read_text(encoding="utf-8"),
    )
    patch_json = json.dumps([{str(p.address): p.patch_data} for p in merged_patch.patches])

    Path(options.output).write_text(patch_json, encoding="utf-8")
    print(f"Generated JSON file {options.output}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()

    try:
        options = parser.parse_args(argv)

        started = time.perf_counter()
        _ = _get_seed(options.seed)

        if options.binary:
            make_enemizer_rom(options)
        else:
            make_enemizer_json_patch(options)

        elapsed = time.perf_counter() - started
        print(f"Seed generated in: {elapsed:.3f}s")
        return 0
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
