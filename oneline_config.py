# oneline_config.py
import pygame
import re
import random

BLACK = (0,   0,   0)
GREY = (200, 200, 200, 0.5)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (100, 200,   100)
BLUE = (0,   0, 255)
YELLOW = (255, 255, 0)
RAN_COLOR = (lambda: [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

pygame.font.init()
fonts = pygame.font.get_fonts()
font = [f for f in fonts if re.match(".+gothic$|.*nanumgothic.*|.*malgungothic.*", f)][0]

config = {
    "color": {
        "conn": "RED",
        "disConn": "BLUE",
        "close": "RED",
        "open": "GREEN",
        "option": {
          "WHITE": [255, 255, 255],
          "GREY": [200, 200, 200],
          "BLACK": [0, 0, 0],
          "RED": [255, 0, 0],
          "GREEN": [55, 200, 55],
          "BLUE": [0, 0, 255],
          "YELLOW": [255, 255, 0]
        },
        "station": ["RED", "BLUE", "YELLOW", "GREEN"]
    },
    "text": {
        "font": font,  # nanumgothic, "malgungothic"
        "size": 13,
        "bold": True,
        "italic": False
    },
    "screen": {
        "size": 0,
        "fps": 2
    },
    "size": 20
    # "direction": [True, False, True, False, True, True, True]  # 1 - 7 변전소 방향

}

station = {  # default 변전소 설정값
    1: {
        "color": [RED, BLUE, YELLOW, GREEN, RAN_COLOR],
        "direction": True,
        "line": {"1차": [], "2차": ["start", "40-41-0", "41-42-0", "42-43-0", "end"]},
        "start": [0, None],
        "end": [10000, None],
        "617": [100, None],
        "6133": [180, None],

        "6102": [300, None],    # 1 bus_tie

        "627": [560, None],
        "6233": [700, None],

        "637": [940, None],
        "6333": [1100, None],

        "647": [1600, None],
        "6433": [1700, None],


        "6533": [2000, None],

        "4144": [[180, 380], None],
        "4244": [[700, 780], None],
        "4344": [[1100, 1460], None],
        "4444": [[1700, 1820], None],
        "4544": [[2000, 1980], None],

        # 1 bank
        "4179": [20, 'down'],
        "4171": [0, 'top'],
        "4172": [0, 'null'],

        "427": [60, 'down'],
        "421": [40, 'top'],
        "422": [40, 'null'],

        "437": [100, 'down'],
        "431": [80, 'top'],
        "432": [80, 'null'],

        "447": [140, 'down'],
        "441": [120, 'top'],
        "442": [120, 'null'],

        "457": [180, 'down'],
        "451": [160, 'top'],
        "452": [160, 'null'],

        "4100": [220, 'null'],
        "4101": [220, 'top'],
        "4102": [220, 'null'],

        "467": [260, 'down'],
        "461": [240, 'top'],
        "462": [240, 'null'],

        "477": [300, 'down'],
        "471": [280, 'top'],
        "472": [280, 'null'],

        "4189": [340, 'down'],
        "4181": [320, 'top'],
        "4182": [320, 'null'],


        "497": [420, 'down'],
        "491": [400, 'top'],
        "492": [400, 'null'],

        "4A7": [460, 'down'],
        "4A1": [440, 'top'],
        "4A2": [440, 'null'],

        "40-41-0": [540, 'up'],
        "40-41-1": [500, 'null'],
        "40-41-2": [580, 'null'],
        "45-46-0": [540, 'down'],
        "45-46-1": [500, 'null'],
        "45-46-2": [580, 'null'],

        "4289": [620, 'down'],
        "4281": [600, 'top'],
        "4282": [600, 'null'],

        "4C7": [660, 'down'],
        "4C1": [640, 'top'],
        "4C2": [640, 'null'],

        "4D7": [700, 'down'],
        "4D1": [680, 'top'],
        "4D2": [680, 'null'],

        "4F7": [740, 'down'],
        "4F1": [720, 'top'],
        "4F2": [720, 'null'],

        "4G7": [820, 'down'],
        "4G1": [800, 'top'],
        "4G2": [800, 'null'],

        "4H7": [860, 'down'],
        "4H1": [840, 'top'],
        "4H2": [840, 'null'],

        "4J7": [900, 'down'],
        "4J1": [880, 'top'],
        "4J2": [880, 'null'],

        "4K7": [940, 'down'],
        "4K1": [920, 'top'],
        "4K2": [920, 'null'],

        "4L7": [980, 'down'],
        "4L1": [960, 'top'],
        "4L2": [960, 'null'],

        "4279": [1020, 'down'],
        "4271": [1000, 'top'],
        "4272": [1000, 'null'],

        "41-42-0": [1100, 'up'],
        "41-42-1": [1060, "null"],
        "41-42-2": [1140, "null"],
        "46-47-0": [1100, 'down'],
        "46-47-1": [1060, "null"],
        "46-47-2": [1140, "null"],

        "4N7": [1180, 'down'],
        "4N1": [1160, 'top'],
        "4N2": [1160, 'null'],

        "4P7": [1220, 'down'],
        "4P1": [1200, 'top'],
        "4P2": [1200, 'null'],

        "4Q7": [1260, 'down'],
        "4Q1": [1240, 'top'],
        "4Q2": [1240, 'null'],

        # 2 bus_tie
        "4200": [1300, 'null'],
        "4201": [1300, 'top'],
        "4202": [1300, 'null'],

        "4R7": [1340, 'down'],
        "4R1": [1320, 'top'],
        "4R2": [1320, 'null'],

        "4S7": [1380, 'down'],
        "4S1": [1360, 'top'],
        "4S2": [1360, 'null'],

        "4T7": [1420, 'down'],
        "4T1": [1400, 'top'],
        "4T2": [1400, 'null'],


        "4U7": [1500, 'down'],
        "4U1": [1480, 'top'],
        "4U2": [1480, 'null'],

        "4379": [1540, 'down'],
        "4371": [1520, 'top'],
        "4372": [1520, 'null'],

        "42-43-0": [1620, 'up'],    # section
        "42-43-1": [1580, "null"],
        "42-43-2": [1660, "null"],
        "47-48-0": [1620, 'down'],
        "47-48-1": [1580, "null"],
        "47-48-2": [1660, "null"],

        "4W7": [1700, "down"],
        "4W1": [1680, "top"],
        "4W2": [1680, "null"],

        "4X7": [1740, "down"],
        "4X1": [1720, "top"],
        "4X2": [1720, "null"],

        "4Y7": [1780, "down"],
        "4Y1": [1760, "top"],
        "4Y2": [1760, "null"],

        "4Z7": [1860, "down"],
        "4Z1": [1840, "top"],
        "4Z2": [1840, "null"],

        "4가7": [1900, "down"],
        "4가1": [1880, "top"],
        "4가2": [1880, "null"],

        "4나7": [1940, "down"],
        "4나1": [1920, "top"],
        "4나2": [1920, "null"],

        "4다7": [2020, "down"],
        "4다1": [2000, "top"],
        "4다2": [2000, "null"],

        "4라7": [2060, "down"],
        "4라1": [2040, "top"],
        "4라2": [2040, "null"],

        "4479": [2100, "down"],
        "4471": [2080, "top"],
        "4472": [2080, "null"],

        "4마7": [2140, "down"],
        "4마1": [2120, "top"],
        "4마2": [2120, "null"]
    },
    4: {
        "color": [RED, BLUE, YELLOW],
        "direction": False,
        "line": {"1차": [], "2차": ["start", "41-42-0", "40-41-0", "end"]},   # 좌 -> 우
        "start": [0, None],
        "end": [10000, None],

        "617": [2100, None],
        "6133": [1900, None],

        "627": [1650, None],

        "6233": [1100, None],

        "6102": [850, None],    # 1 bus_tie

        "657": [700, None],

        "6333": [400, None],

        "687": [300, None],

        # 1 bank
        "447": [2120, 'down'],
        "441": [2100, 'top'],
        "442": [2100, 'null'],

        "457": [2080, 'down'],
        "451": [2060, 'top'],
        "452": [2060, 'null'],

        "4144": [[1900, 2020], None],

        "467": [1960, 'down'],
        "461": [1940, 'top'],
        "462": [1940, 'null'],

        "477": [1920, 'down'],
        "471": [1900, 'top'],
        "472": [1900, 'null'],

        "4100": [1860, 'null'],
        "4101": [1860, 'top'],
        "4102": [1860, 'null'],

        "487": [1780, 'down'],
        "481": [1760, 'top'],
        "482": [1760, 'null'],

        "4189": [1710, 'down'],
        "4181": [1690, 'top'],
        "4182": [1690, 'null'],

        "40-41-0": [1630, 'down'],
        "40-41-1": [1670, 'up'],
        "40-41-2": [1590, 'up'],
        "45-46-0": [1630, 'down'],
        "45-46-1": [1670, 'up'],
        "45-46-2": [1590, 'up'],

        "4289": [1520, 'down'],
        "4281": [1500, 'top'],
        "4282": [1500, 'null'],

        "4B7": [1460, 'down'],
        "4B1": [1440, 'top'],
        "4B2": [1440, 'null'],

        "4244": [[1100, 1400], None],

        "4C7": [1320, 'down'],
        "4C1": [1300, 'top'],
        "4C2": [1300, 'null'],

        "4F7": [1240, 'down'],
        "4F1": [1220, 'top'],
        "4F2": [1220, 'null'],

        "4G7": [1160, 'down'],
        "4G1": [1140, 'top'],
        "4G2": [1140, 'null'],

        "4H7": [1080, 'down'],
        "4H1": [1060, 'top'],
        "4H2": [1060, 'null'],

        "41-42-0": [800, 'down'],
        "41-42-1": [840, "up"],
        "41-42-2": [760, "up"],
        "46-47-0": [800, 'down'],
        "46-47-1": [840, "up"],
        "46-47-2": [760, "up"],

        "4J7": [640, 'down'],
        "4J1": [620, 'top'],
        "4J2": [620, 'null'],

        # 2 bus_tie
        "4200": [520, 'null'],
        "4201": [520, 'top'],
        "4202": [520, 'null'],

        "4344": [400, None],

        "4K7": [320, 'down'],
        "4K1": [300, 'top'],
        "4K2": [300, 'null'],

        "4L7": [245, 'down'],
        "4L1": [225, 'top'],
        "4L2": [225, 'null'],

        "4M7": [170, 'down'],
        "4M1": [150, 'top'],
        "4M2": [150, 'null'],

        "4N7": [95, 'down'],
        "4N1": [75, 'top'],
        "4N2": [75, 'null']
    }

}
