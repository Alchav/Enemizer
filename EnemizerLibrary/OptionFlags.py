from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class BossType(IntEnum):
    Kholdstare = 0
    Moldorm = 1
    Mothula = 2
    Vitreous = 3
    Helmasaur = 4
    Armos = 5
    Lanmola = 6
    Blind = 7
    Arrghus = 8
    Trinexx = 9
    Agahnim = 10
    Agahnim2 = 11
    Ganon = 12
    NoBoss = 255


class RandomizeEnemiesType(IntEnum):
    Basic = 0
    Normal = 1
    Hard = 2
    Chaos = 3
    Insanity = 4


class RandomizeEnemyHPType(IntEnum):
    Easy = 0
    Medium = 1
    Hard = 2
    Patty = 3


class RandomizeBossesType(IntEnum):
    Basic = 0
    Normal = 1
    Chaos = 2


class SwordTypes(IntEnum):
    Normal = 0


class ShieldTypes(IntEnum):
    Normal = 0


class AbsorbableTypes(IntEnum):
    Heart = 0
    GreenRupee = 1
    BlueRupee = 2
    RedRupee = 3
    Bomb_1 = 4
    Bomb_4 = 5
    Bomb_8 = 6
    SmallMagic = 7
    FullMagic = 8
    Arrow_5 = 9
    Arrow_10 = 10
    Fairy = 11
    Key = 12
    BigKey = 13


class HeartBeepSpeed(IntEnum):
    Default = 0
    Half = 1
    Quarter = 2
    Off = 3


class BeeLevel(IntEnum):
    Level1 = 0
    Level2 = 1
    Level3 = 2
    Level4 = 3


@dataclass
class ManualBosses:
    EasternPalace: str | None = None
    DesertPalace: str | None = None
    TowerOfHera: str | None = None
    AgahnimsTower: str | None = None
    PalaceOfDarkness: str | None = None
    SwampPalace: str | None = None
    SkullWoods: str | None = None
    ThievesTown: str | None = None
    IcePalace: str | None = None
    MiseryMire: str | None = None
    TurtleRock: str | None = None
    GanonsTower1: str | None = None
    GanonsTower2: str | None = None
    GanonsTower3: str | None = None
    GanonsTower4: str | None = None
    Ganon: str | None = None


@dataclass
class OptionFlags:
    RandomizeEnemies: bool = True
    RandomizeEnemiesType: RandomizeEnemiesType = RandomizeEnemiesType.Chaos
    RandomizeBushEnemyChance: bool = True
    RandomizeEnemyHealthRange: bool = False
    RandomizeEnemyHealthType: RandomizeEnemyHPType = RandomizeEnemyHPType.Easy
    RandomizeEnemyDamage: bool = False
    AllowEnemyZeroDamage: bool = False
    ShuffleEnemyDamageGroups: bool = False
    EnemyDamageChaosMode: bool = False
    EasyModeEscape: bool = False
    EnemiesAbsorbable: bool = False
    AbsorbableSpawnRate: int = 0
    AbsorbableTypes: dict[AbsorbableTypes, bool] = field(
        default_factory=lambda: {k: False for k in AbsorbableTypes}
    )
    BossMadness: bool = False
    RandomizeBosses: bool = True
    RandomizeBossesType: RandomizeBossesType = RandomizeBossesType.Chaos
    RandomizeBossHealth: bool = False
    RandomizeBossHealthMinAmount: int = 0
    RandomizeBossHealthMaxAmount: int = 0
    RandomizeBossDamage: bool = False
    RandomizeBossDamageMinAmount: int = 0
    RandomizeBossDamageMaxAmount: int = 0
    RandomizeBossBehavior: bool = False
    RandomizeDungeonPalettes: bool = True
    SetBlackoutMode: bool = False
    RandomizeOverworldPalettes: bool = True
    RandomizeSpritePalettes: bool = True
    SetAdvancedSpritePalettes: bool = False
    PukeMode: bool = False
    NegativeMode: bool = False
    GrayscaleMode: bool = False
    GenerateSpoilers: bool = True
    RandomizeLinkSpritePalette: bool = False
    RandomizePots: bool = True
    ShuffleMusic: bool = False
    BootlegMagic: bool = False
    DebugMode: bool = False
    CustomBosses: bool = False
    HeartBeepSpeed: HeartBeepSpeed = HeartBeepSpeed.Half
    AlternateGfx: bool = False
    ShieldGraphics: str = "shield_gfx\\normal.gfx"
    SwordGraphics: str = "sword_gfx\\normal.gfx"
    BeeMizer: bool = False
    BeesLevel: BeeLevel = BeeLevel.Level1
    DebugForceEnemy: bool = False
    DebugForceEnemyId: int = 0
    DebugForceBoss: bool = False
    DebugForceBossId: BossType = BossType.Kholdstare
    DebugOpenShutterDoors: bool = False
    DebugForceEnemyDamageZero: bool = False
    DebugShowRoomIdInRupeeCounter: bool = False
    OHKO: bool = False
    RandomizeTileTrapPattern: bool = False
    RandomizeTileTrapFloorTile: bool = False
    AllowKillableThief: bool = False
    RandomizeSpriteOnHit: bool = False
    HeroMode: bool = False
    IncreaseBrightness: bool = False
    MuteMusicEnableMSU1: bool = False
    AgahnimBounceBalls: bool = False
    UseManualBosses: bool = False
    ManualBosses: ManualBosses | None = None

    ENEMIZER_INFO_FLAGS_LENGTH = 0x50

    @classmethod
    def from_bytes(cls, option_bytes: bytes) -> "OptionFlags":
        flags = cls()
        i = 0

        def b() -> int:
            nonlocal i
            val = option_bytes[i]
            i += 1
            return val

        flags.RandomizeEnemies = bool(b())
        flags.RandomizeEnemiesType = RandomizeEnemiesType(b())
        flags.RandomizeBushEnemyChance = bool(b())
        flags.RandomizeEnemyHealthRange = bool(b())
        flags.RandomizeEnemyHealthType = RandomizeEnemyHPType(b())
        flags.RandomizeEnemyDamage = bool(b())
        flags.AllowEnemyZeroDamage = bool(b())
        flags.EasyModeEscape = bool(b())
        flags.EnemiesAbsorbable = bool(b())
        flags.AbsorbableSpawnRate = b()

        for absorbable in AbsorbableTypes:
            flags.AbsorbableTypes[absorbable] = bool(b())

        flags.BossMadness = bool(b())
        flags.RandomizeBosses = bool(b())
        flags.RandomizeBossesType = RandomizeBossesType(b())
        flags.RandomizeBossHealth = bool(b())
        flags.RandomizeBossHealthMinAmount = b()
        flags.RandomizeBossHealthMaxAmount = b()
        flags.RandomizeBossDamage = bool(b())
        flags.RandomizeBossDamageMinAmount = b()
        flags.RandomizeBossDamageMaxAmount = b()
        flags.RandomizeBossBehavior = bool(b())
        flags.RandomizeDungeonPalettes = bool(b())
        flags.SetBlackoutMode = bool(b())
        flags.RandomizeOverworldPalettes = bool(b())
        flags.RandomizeSpritePalettes = bool(b())
        flags.SetAdvancedSpritePalettes = bool(b())
        flags.PukeMode = bool(b())
        flags.NegativeMode = bool(b())
        flags.GrayscaleMode = bool(b())
        flags.GenerateSpoilers = bool(b())
        flags.RandomizeLinkSpritePalette = bool(b())
        flags.RandomizePots = bool(b())
        flags.ShuffleMusic = bool(b())
        flags.BootlegMagic = bool(b())
        flags.DebugMode = bool(b())
        flags.CustomBosses = bool(b())
        flags.HeartBeepSpeed = HeartBeepSpeed(b())
        flags.AlternateGfx = bool(b())
        _ = b()  # shield index, unused in C# too
        flags.ShuffleEnemyDamageGroups = bool(b())
        flags.EnemyDamageChaosMode = bool(b())
        _ = b()  # sword index, unused in C# too
        flags.BeeMizer = bool(b())
        flags.BeesLevel = BeeLevel(b())
        flags.DebugForceEnemy = bool(b())
        flags.DebugForceEnemyId = b()
        flags.DebugForceBoss = bool(b())
        flags.DebugForceBossId = BossType(b())
        flags.DebugOpenShutterDoors = bool(b())
        flags.DebugForceEnemyDamageZero = bool(b())
        flags.DebugShowRoomIdInRupeeCounter = bool(b())
        flags.OHKO = bool(b())
        flags.RandomizeTileTrapPattern = bool(b())
        flags.RandomizeTileTrapFloorTile = bool(b())
        flags.AllowKillableThief = bool(b())
        flags.RandomizeSpriteOnHit = bool(b())
        flags.HeroMode = bool(b())
        flags.IncreaseBrightness = bool(b())
        flags.MuteMusicEnableMSU1 = bool(b())
        flags.AgahnimBounceBalls = bool(b())
        return flags

    def to_bytes(self) -> bytes:
        ret = bytearray(self.ENEMIZER_INFO_FLAGS_LENGTH)
        i = 0

        def w(v: int) -> None:
            nonlocal i
            ret[i] = v & 0xFF
            i += 1

        w(int(self.RandomizeEnemies))
        w(int(self.RandomizeEnemiesType))
        w(int(self.RandomizeBushEnemyChance))
        w(int(self.RandomizeEnemyHealthRange))
        w(int(self.RandomizeEnemyHealthType))
        w(int(self.RandomizeEnemyDamage))
        w(int(self.AllowEnemyZeroDamage))
        w(int(self.EasyModeEscape))
        w(int(self.EnemiesAbsorbable))
        w(self.AbsorbableSpawnRate)

        for absorbable in AbsorbableTypes:
            w(int(self.AbsorbableTypes.get(absorbable, False)))

        w(int(self.BossMadness))
        w(int(self.RandomizeBosses))
        w(int(self.RandomizeBossesType))
        w(int(self.RandomizeBossHealth))
        w(self.RandomizeBossHealthMinAmount)
        w(self.RandomizeBossHealthMaxAmount)
        w(int(self.RandomizeBossDamage))
        w(self.RandomizeBossDamageMinAmount)
        w(self.RandomizeBossDamageMaxAmount)
        w(int(self.RandomizeBossBehavior))
        w(int(self.RandomizeDungeonPalettes))
        w(int(self.SetBlackoutMode))
        w(int(self.RandomizeOverworldPalettes))
        w(int(self.RandomizeSpritePalettes))
        w(int(self.SetAdvancedSpritePalettes))
        w(int(self.PukeMode))
        w(int(self.NegativeMode))
        w(int(self.GrayscaleMode))
        w(int(self.GenerateSpoilers))
        w(int(self.RandomizeLinkSpritePalette))
        w(int(self.RandomizePots))
        w(int(self.ShuffleMusic))
        w(int(self.BootlegMagic))
        w(int(self.DebugMode))
        w(int(self.CustomBosses))
        w(int(self.HeartBeepSpeed))
        w(int(self.AlternateGfx))
        w(0)  # shield index
        w(int(self.ShuffleEnemyDamageGroups))
        w(int(self.EnemyDamageChaosMode))
        w(0)  # sword index
        w(int(self.BeeMizer))
        w(int(self.BeesLevel))
        w(int(self.DebugForceEnemy))
        w(self.DebugForceEnemyId)
        w(int(self.DebugForceBoss))
        w(int(self.DebugForceBossId))
        w(int(self.DebugOpenShutterDoors))
        w(int(self.DebugForceEnemyDamageZero))
        w(int(self.DebugShowRoomIdInRupeeCounter))
        w(int(self.OHKO))
        w(int(self.RandomizeTileTrapPattern))
        w(int(self.RandomizeTileTrapFloorTile))
        w(int(self.AllowKillableThief))
        w(int(self.RandomizeSpriteOnHit))
        w(int(self.HeroMode))
        w(int(self.IncreaseBrightness))
        w(int(self.MuteMusicEnableMSU1))
        w(int(self.AgahnimBounceBalls))

        return bytes(ret)
