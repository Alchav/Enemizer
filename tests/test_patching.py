from enemizer_py.patching import RandomizerPatch


def test_randomizer_patch_applies_data() -> None:
    base = '[{"16":[1,2]}]'
    rnd = '[{"18":[3,4]}]'
    patch = RandomizerPatch(base, rnd)

    rom = bytearray([0] * 32)
    patch.patch_rom(rom)

    assert rom[16:20] == bytes([1, 2, 3, 4])
