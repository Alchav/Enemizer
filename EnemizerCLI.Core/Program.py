from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import sys
from pathlib import Path as _Path

ROOT = _Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(_Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(_Path(__file__).resolve().parent))

from EnemizerLibrary.OptionFlags import OptionFlags
from EnemizerLibrary.RomData import RomData
from RandomizerPatch import RandomizerPatch


def get_seed(seed: str) -> int:
    if not seed:
        return random.randint(0, 999_999_999)
    try:
        parsed = int(seed)
    except ValueError as exc:
        raise ValueError("Invalid Seed Number entered. Please enter an integer value.") from exc
    if parsed < 0:
        raise ValueError("Please enter a positive Seed Number.")
    return parsed


def throw_if_already_enemized(rom_data: RomData) -> None:
    if rom_data.IsEnemizerRom:
        raise ValueError("It appears that the provided base ROM is already enemized. Please ensure you are using an original game ROM.")


def make_enemizer_json_patch(args: argparse.Namespace) -> None:
    if not args.base or not args.randomizer:
        raise ValueError("--base and --randomizer are required unless --binary is used")

    option_json = json.loads(Path(args.enemizer).read_text(encoding="utf-8"))
    _ = OptionFlags(**{k: v for k, v in option_json.items() if k in OptionFlags.__dataclass_fields__})

    raw_data = bytearray(Path(args.rom).read_bytes())
    raw_data.extend(b"\x00" * max(0, (2 * 1024 * 1024) - len(raw_data)))
    rom_data = RomData(raw_data)
    throw_if_already_enemized(rom_data)

    merged = RandomizerPatch(
        Path(args.base).read_text(encoding="utf-8"),
        Path(args.randomizer).read_text(encoding="utf-8"),
    )

    patch_json = json.dumps([{str(p.address): p.patchData} for p in merged.Patches])
    Path(args.output).write_text(patch_json, encoding="utf-8")
    print(f"Generated JSON file {args.output}")


def make_enemizer_rom(args: argparse.Namespace) -> None:
    _ = json.loads(Path(args.enemizer).read_text(encoding="utf-8"))

    raw_data = bytearray(Path(args.rom).read_bytes())
    raw_data.extend(b"\x00" * max(0, (2 * 1024 * 1024) - len(raw_data)))
    rom_data = RomData(raw_data)
    throw_if_already_enemized(rom_data)

    if args.base and args.randomizer:
        merged = RandomizerPatch(
            Path(args.base).read_text(encoding="utf-8"),
            Path(args.randomizer).read_text(encoding="utf-8"),
        )
        merged.PatchRom(raw_data)

    Path(args.output).write_bytes(raw_data)
    print(f"Generated SFC file {args.output}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="EnemizerCLI.Core Python port")
    p.add_argument("--rom", required=True)
    p.add_argument("--seed", default="")
    p.add_argument("--base")
    p.add_argument("--randomizer")
    p.add_argument("--enemizer", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--binary", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    start = time.perf_counter()
    _ = get_seed(args.seed)
    if args.binary:
        make_enemizer_rom(args)
    else:
        make_enemizer_json_patch(args)
    print(f"Seed generated in: {time.perf_counter() - start}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
