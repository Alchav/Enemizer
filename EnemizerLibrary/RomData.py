from __future__ import annotations

from dataclasses import dataclass

from EnemizerLibrary.OptionFlags import OptionFlags


@dataclass
class PatchObject:
    address: int
    patchData: list[int]


class AddressConstants:
    EnemizerFileLength = 0x200000


class RomData:
    EnemizerInfoSeedOffset = 0x0
    EnemizerInfoSeedStringLength = 12
    EnemizerInfoVersionOffset = EnemizerInfoSeedOffset + EnemizerInfoSeedStringLength
    EnemizerInfoVersionLength = 8
    EnemizerInfoFlagsOffset = EnemizerInfoVersionOffset + EnemizerInfoVersionLength
    EnemizerInfoFlagsLength = 0x50

    def __init__(self, rom_data: bytes, enemizer_info_table_base_address: int = 0, enemizer_flags_base_address: int = 0):
        self.EnemizerInfoTableBaseAddress = enemizer_info_table_base_address
        self.EnemizerOptionFlagsBaseAddress = enemizer_flags_base_address
        self.romData = bytearray(rom_data[512:] if len(rom_data) % 1024 == 512 else rom_data)
        self.OriginalLength = len(self.romData)
        self._seed = -1
        self.patch_data: dict[int, int] = {}

    def _set_patch_bytes(self, offset: int, length: int) -> None:
        for i in range(offset, offset + length):
            self.patch_data[i] = self.romData[i]

    @property
    def IsEnemizerRom(self) -> bool:
        base = self.EnemizerInfoTableBaseAddress
        return (
            len(self.romData) == AddressConstants.EnemizerFileLength
            and self.romData[base + self.EnemizerInfoSeedOffset] == ord("E")
            and self.romData[base + self.EnemizerInfoSeedOffset + 1] == ord("N")
        )

    @property
    def EnemizerSeed(self) -> int:
        if self._seed < 0 and self.IsEnemizerRom:
            base = self.EnemizerInfoTableBaseAddress
            seed_bytes = self.romData[
                base + self.EnemizerInfoSeedOffset : base + self.EnemizerInfoSeedOffset + self.EnemizerInfoSeedStringLength
            ]
            seed_string = bytes(seed_bytes).decode("ascii", errors="ignore").rstrip("\x00")
            self._seed = int(seed_string[2:])
        return self._seed

    @EnemizerSeed.setter
    def EnemizerSeed(self, value: int) -> None:
        if len(self.romData) < AddressConstants.EnemizerFileLength:
            raise ValueError("You need to expand the rom before you can use Enemizer features.")
        base = self.EnemizerInfoTableBaseAddress
        seed_bytes = bytearray(f"EN{value}".encode("ascii"))
        seed_bytes.extend(b"\x00" * (self.EnemizerInfoSeedStringLength - len(seed_bytes)))
        self.romData[base + self.EnemizerInfoSeedOffset : base + self.EnemizerInfoSeedOffset + self.EnemizerInfoSeedStringLength] = seed_bytes[: self.EnemizerInfoSeedStringLength]
        self._seed = value
        self._set_patch_bytes(base + self.EnemizerInfoSeedOffset, self.EnemizerInfoSeedStringLength)

    @property
    def EnemizerVersion(self) -> str:
        if not self.IsEnemizerRom:
            return "Not Enemizer Rom"
        base = self.EnemizerInfoTableBaseAddress
        version_bytes = self.romData[
            base + self.EnemizerInfoVersionOffset : base + self.EnemizerInfoVersionOffset + self.EnemizerInfoVersionLength
        ]
        return bytes(version_bytes).decode("ascii", errors="ignore").rstrip("\x00")

    @EnemizerVersion.setter
    def EnemizerVersion(self, value: str) -> None:
        if len(self.romData) < AddressConstants.EnemizerFileLength:
            raise ValueError("You need to expand the rom before you can use Enemizer features.")
        base = self.EnemizerInfoTableBaseAddress
        version_bytes = bytearray(value.encode("ascii"))
        version_bytes.extend(b"\x00" * (self.EnemizerInfoVersionLength - len(version_bytes)))
        self.romData[
            base + self.EnemizerInfoVersionOffset : base + self.EnemizerInfoVersionOffset + self.EnemizerInfoVersionLength
        ] = version_bytes[: self.EnemizerInfoVersionLength]
        self._set_patch_bytes(base + self.EnemizerInfoVersionOffset, self.EnemizerInfoVersionLength)

    def SetRomInfoOptionFlags(self, option_flags: OptionFlags) -> None:
        option_bytes = option_flags.to_bytes()
        if len(option_bytes) > 0x100 - self.EnemizerInfoFlagsOffset:
            raise ValueError("Option flags is too long to fit in the space allocated.")
        base = self.EnemizerInfoTableBaseAddress
        start = base + self.EnemizerInfoFlagsOffset
        self.romData[start : start + len(option_bytes)] = option_bytes
        self._set_patch_bytes(start, len(option_bytes))

    def GetOptionFlagsFromRom(self) -> OptionFlags | None:
        if not self.IsEnemizerRom:
            return None
        base = self.EnemizerInfoTableBaseAddress
        start = base + self.EnemizerInfoFlagsOffset
        option_bytes = bytes(self.romData[start : start + self.EnemizerInfoFlagsLength])
        return OptionFlags.from_bytes(option_bytes)

    def GeneratePatch(self) -> list[PatchObject]:
        patches: list[PatchObject] = []
        current: PatchObject | None = None
        last = -2
        for address in sorted(self.patch_data.keys()):
            if address != last + 1:
                current = PatchObject(address=address, patchData=[])
                patches.append(current)
            current.patchData.append(self.patch_data[address])
            last = address
        return patches
