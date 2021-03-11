import pygame
from pygame.locals import *

ROWS, COLS = 9,9
SQUARE_SIZE = 70
MARGIN = 1
WIDTH, HEIGHT = SQUARE_SIZE * (COLS + 8) + 20, SQUARE_SIZE * ROWS
split = int(SQUARE_SIZE * ROWS / 13) - 6

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TAN = (210,180,140)
GREEN = (0, 255, 0)
GREY = (128,128,128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135,206,250)

pygame.init()
pygame.display.set_mode()
logos = {}


#Pieces
MarshallB = pygame.image.load("./Pictures/MarshallB.png").convert_alpha()
MarshallB = pygame.transform.scale(MarshallB, (SQUARE_SIZE, SQUARE_SIZE))
MarshallW = pygame.image.load("./Pictures/MarshallW.png").convert_alpha()
MarshallW = pygame.transform.scale(MarshallW, (SQUARE_SIZE, SQUARE_SIZE))

GeneralB = pygame.image.load("./Pictures/GeneralB.png").convert_alpha()
GeneralB = pygame.transform.scale(GeneralB, (SQUARE_SIZE, SQUARE_SIZE))
GeneralW = pygame.image.load("./Pictures/GeneralW.png").convert_alpha()
GeneralW = pygame.transform.scale(GeneralW, (SQUARE_SIZE, SQUARE_SIZE))

PawnB = pygame.image.load("./Pictures/PawnB.png").convert_alpha()
PawnB = pygame.transform.scale(PawnB, (SQUARE_SIZE, SQUARE_SIZE))
PawnW = pygame.image.load("./Pictures/PawnW.png").convert_alpha()
PawnW = pygame.transform.scale(PawnW, (SQUARE_SIZE, SQUARE_SIZE))

KnightB = pygame.image.load("./Pictures/KnightB.png").convert_alpha()
KnightB = pygame.transform.scale(KnightB, (SQUARE_SIZE, SQUARE_SIZE))
KnightW = pygame.image.load("./Pictures/KnightW.png").convert_alpha()
KnightW = pygame.transform.scale(KnightW, (SQUARE_SIZE, SQUARE_SIZE))

SamouraiB = pygame.image.load("./Pictures/SamouraiB.png").convert_alpha()
SamouraiB = pygame.transform.scale(SamouraiB, (SQUARE_SIZE, SQUARE_SIZE))
SamouraiW = pygame.image.load("./Pictures/SamouraiW.png").convert_alpha()
SamouraiW = pygame.transform.scale(SamouraiW, (SQUARE_SIZE, SQUARE_SIZE))

CannonB = pygame.image.load("./Pictures/CannonB.png").convert_alpha()
CannonB = pygame.transform.scale(CannonB, (SQUARE_SIZE, SQUARE_SIZE))
CannonW = pygame.image.load("./Pictures/CannonW.png").convert_alpha()
CannonW = pygame.transform.scale(CannonW, (SQUARE_SIZE, SQUARE_SIZE))


ArcherB = pygame.image.load("./Pictures/ArcherB.png").convert_alpha()
ArcherB = pygame.transform.scale(ArcherB, (SQUARE_SIZE, SQUARE_SIZE))
ArcherW = pygame.image.load("./Pictures/ArcherW.png").convert_alpha()
ArcherW = pygame.transform.scale(ArcherW, (SQUARE_SIZE, SQUARE_SIZE))

SpyB = pygame.image.load("./Pictures/SpyB.png").convert_alpha()
SpyB = pygame.transform.scale(SpyB, (SQUARE_SIZE, SQUARE_SIZE))
SpyW = pygame.image.load("./Pictures/SpyW.png").convert_alpha()
SpyW = pygame.transform.scale(SpyW, (SQUARE_SIZE, SQUARE_SIZE))

FortressB = pygame.image.load("./Pictures/FortressB.png").convert_alpha()
FortressB = pygame.transform.scale(FortressB, (SQUARE_SIZE, SQUARE_SIZE))
FortressW = pygame.image.load("./Pictures/FortressW.png").convert_alpha()
FortressW = pygame.transform.scale(FortressW, (SQUARE_SIZE, SQUARE_SIZE))

CaptainB = pygame.image.load("./Pictures/CaptainB.png").convert_alpha()
CaptainB = pygame.transform.scale(CaptainB, (SQUARE_SIZE, SQUARE_SIZE))
CaptainW = pygame.image.load("./Pictures/CaptainW.png").convert_alpha()
CaptainW = pygame.transform.scale(CaptainW, (SQUARE_SIZE, SQUARE_SIZE))

LGeneralB = pygame.image.load("./Pictures/LGeneralB.png").convert_alpha()
LGeneralB = pygame.transform.scale(LGeneralB, (SQUARE_SIZE, SQUARE_SIZE))
LGeneralW = pygame.image.load("./Pictures/LGeneralW.png").convert_alpha()
LGeneralW = pygame.transform.scale(LGeneralW, (SQUARE_SIZE, SQUARE_SIZE))

MGeneralB = pygame.image.load("./Pictures/MGeneralB.png").convert_alpha()
MGeneralB = pygame.transform.scale(MGeneralB, (SQUARE_SIZE, SQUARE_SIZE))
MGeneralW = pygame.image.load("./Pictures/MGeneralW.png").convert_alpha()
MGeneralW = pygame.transform.scale(MGeneralW, (SQUARE_SIZE, SQUARE_SIZE))

MusketB = pygame.image.load("./Pictures/MusketeerB.png").convert_alpha()
MusketB = pygame.transform.scale(MusketB, (SQUARE_SIZE, SQUARE_SIZE))
MusketW = pygame.image.load("./Pictures/MusketeerW.png").convert_alpha()
MusketW = pygame.transform.scale(MusketW, (SQUARE_SIZE, SQUARE_SIZE))


#Logos
Marshall_B = pygame.image.load("./Pictures/Marshall_B.png").convert_alpha()
Marshall_B = pygame.transform.scale(Marshall_B, (SQUARE_SIZE, SQUARE_SIZE))
Marshall_W = pygame.image.load("./Pictures/Marshall_W.png").convert_alpha()
Marshall_W = pygame.transform.scale(Marshall_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['MarshallB'] = Marshall_B
logos['MarshallW'] = Marshall_W

General_B = pygame.image.load("./Pictures/General_B.png").convert_alpha()
General_B = pygame.transform.scale(General_B, (SQUARE_SIZE, SQUARE_SIZE))
General_W = pygame.image.load("./Pictures/General_W.png").convert_alpha()
General_W = pygame.transform.scale(General_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['GeneralB'] = General_B
logos['GeneralW'] = General_W

Pawn_B = pygame.image.load("./Pictures/Pawn_B.png").convert_alpha()
Pawn_B = pygame.transform.scale(Pawn_B, (SQUARE_SIZE, SQUARE_SIZE))
Pawn_W = pygame.image.load("./Pictures/Pawn_W.png").convert_alpha()
Pawn_W = pygame.transform.scale(Pawn_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['PawnB'] = Pawn_B
logos['PawnW'] = Pawn_W

Knight_B = pygame.image.load("./Pictures/Knight_B.png").convert_alpha()
Knight_B = pygame.transform.scale(Knight_B, (SQUARE_SIZE, SQUARE_SIZE))
Knight_W = pygame.image.load("./Pictures/Knight_W.png").convert_alpha()
Knight_W = pygame.transform.scale(Knight_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['KnightB'] = Knight_B
logos['KnightW'] = Knight_W

Samourai_B = pygame.image.load("./Pictures/Samourai_B.png").convert_alpha()
Samourai_B = pygame.transform.scale(Samourai_B, (SQUARE_SIZE, SQUARE_SIZE))
Samourai_W = pygame.image.load("./Pictures/Samourai_W.png").convert_alpha()
Samourai_W = pygame.transform.scale(Samourai_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['SamouraiB'] = Samourai_B
logos['SamouraiW'] = Samourai_W

Cannon_B = pygame.image.load("./Pictures/Cannon_B.png").convert_alpha()
Cannon_B = pygame.transform.scale(Cannon_B, (SQUARE_SIZE, SQUARE_SIZE))
Cannon_W = pygame.image.load("./Pictures/Cannon_W.png").convert_alpha()
Cannon_W = pygame.transform.scale(Cannon_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['CannonB'] = Cannon_B
logos['CannonW'] = Cannon_W

Archer_B = pygame.image.load("./Pictures/Archer_B.png").convert_alpha()
Archer_B = pygame.transform.scale(Archer_B, (SQUARE_SIZE, SQUARE_SIZE))
Archer_W = pygame.image.load("./Pictures/Archer_W.png").convert_alpha()
Archer_W = pygame.transform.scale(Archer_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['ArcherB'] = Archer_B
logos['ArcherW'] = Archer_W

Spy_B = pygame.image.load("./Pictures/Spy_B.png").convert_alpha()
Spy_B = pygame.transform.scale(Spy_B, (SQUARE_SIZE, SQUARE_SIZE))
Spy_W = pygame.image.load("./Pictures/Spy_W.png").convert_alpha()
Spy_W = pygame.transform.scale(Spy_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['SpyB'] = Spy_B
logos['SpyW'] = Spy_W

Fortress_B = pygame.image.load("./Pictures/Fortress_B.png").convert_alpha()
Fortress_B = pygame.transform.scale(Fortress_B, (SQUARE_SIZE, SQUARE_SIZE))
Fortress_W = pygame.image.load("./Pictures/Fortress_W.png").convert_alpha()
Fortress_W = pygame.transform.scale(Fortress_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['FortressB'] = Fortress_B
logos['FortressW'] = Fortress_W

Captain_B = pygame.image.load("./Pictures/Captain_B.png").convert_alpha()
Captain_B = pygame.transform.scale(Captain_B, (SQUARE_SIZE, SQUARE_SIZE))
Captain_W = pygame.image.load("./Pictures/Captain_W.png").convert_alpha()
Captain_W = pygame.transform.scale(Captain_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['CaptainB'] = Captain_B
logos['CaptainW'] = Captain_W

LGeneral_B = pygame.image.load("./Pictures/LGeneral_B.png").convert_alpha()
LGeneral_B = pygame.transform.scale(LGeneral_B, (SQUARE_SIZE, SQUARE_SIZE))
LGeneral_W = pygame.image.load("./Pictures/LGeneral_W.png").convert_alpha()
LGeneral_W = pygame.transform.scale(LGeneral_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['LGeneralB'] = LGeneral_B
logos['LGeneralW'] = LGeneral_W

MGeneral_B = pygame.image.load("./Pictures/MGeneral_B.png").convert_alpha()
MGeneral_B = pygame.transform.scale(MGeneral_B, (SQUARE_SIZE, SQUARE_SIZE))
MGeneral_W = pygame.image.load("./Pictures/MGeneral_W.png").convert_alpha()
MGeneral_W = pygame.transform.scale(MGeneral_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['MGeneralB'] = MGeneral_B
logos['MGeneralW'] = MGeneral_W

Musket_B = pygame.image.load("./Pictures/Musket_B.png").convert_alpha()
Musket_B = pygame.transform.scale(Musket_B, (SQUARE_SIZE, SQUARE_SIZE))
Musket_W = pygame.image.load("./Pictures/Musket_W.png").convert_alpha()
Musket_W = pygame.transform.scale(Musket_W, (SQUARE_SIZE, SQUARE_SIZE))
logos['MusketeerB'] = Musket_B
logos['MusketeerW'] = Musket_W


