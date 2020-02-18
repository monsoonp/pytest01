# diagram_v2.py
import pygame
import math
import csv
import re
import sys
import json

import oneline_config

# import testClass
# from test.testClass import Address
pygame.init()

# functions
ALPHA = (130, 130, 130, 0.5)
BLACK = (0,   0,   0)
GREY = (200, 200, 200, 0.5)
WHITE = (255, 255, 255)
# GREEN = (0, 255,   0)
GREEN = (55, 200,   55)
RED = (255,   0,   0)
BLUE = (0,   0, 255)
# A - 65, a - 97

db_list = []
db_dict = dict()
station_number = 1
file_name = "data/station_test{0}.csv". format(station_number)
# PI = math.pi
# 화면 사이즈, 튜플 형식
# size = (1800, 1000)
# 화면 띄우기
# screen = pygame.display.set_mode(size, pygame.RESIZABLE)

video_infos = pygame.display.Info()  # pygame, 화면정보
width, height = video_infos.current_w, video_infos.current_h  # 화면 너비, 높이
# 더블 버퍼, 리사이즈, 하드웨어 가속 pygame.HWSURFACE (전체화면에서만)
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.RESIZABLE)

title = ""
# 화면 제목
pygame.display.set_caption("{0} 단선도".format(title))
config = oneline_config.config
station = oneline_config.station[1]


def set_x(position):
    return int(width * position / 2000)


def set_y(position):
    return int(height * position / 2000)


def connection(val):
    return RED if val else GREEN


def drawer(kind, scr, color, location, write, point):
    if "DS" in kind:
        pygame.draw.ellipse(scr, color, location, 0)
    elif "CB" in kind:
        pygame.draw.rect(scr, color, location, 0)
    letter = config["text"]["font"]
    size = config["text"]["size"]
    bold = config["text"]["bold"]
    italic = config["text"]["italic"]
    font = pygame.font.SysFont(letter, size, bold, italic)
    text = font.render("{0}".format(point), True, WHITE)
    if not write:
        scr.blit(text, [location[0]-40, location[1]])
    elif write == "up":
        scr.blit(text, [location[0], location[1]-40])

def shape(scr, point, val):
    tl = re.compile("^6\\d7$")  # 6_7
    tr = re.compile("^6\\d31$")  # 61_1-3
    tie = re.compile("^6\\d02$")  # 61_0-2
    tr2 = re.compile("^4\\d44$")  # 4_41-2

    dl = re.compile("4\\d4[12]")  # 4_41-2
    tie2 = re.compile("4\\d0[012]")  # 4_41-2

    try:
        if point in station.keys():
            x = station[point][0]
            text = station[point][1]
            size = config["size"]

            if tl.match(point):
                conn = connection(db_dict[point]["conn"])
                drawer(val["kind"], scr, conn, [set_x(x), set_y(300), size, size], text, point)
                point = point.replace(point[2], str(1))
                conn = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, conn, [set_x(x-40), set_y(450), size, size], text, point)
                point = point.replace(point[2], str(2))
                conn = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, conn, [set_x(x-40), set_y(600), size, size], text, point)

            elif tr.match(point):
                if isinstance(x, int):
                    conn = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, conn, [set_x(x), set_y(450), size, size], text, point)
                    point = point[:-1]+"2"
                    conn = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, conn, [set_x(x), set_y(600), size, size], text, point)
                    point = point[:-1]+"3"
                    conn = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, conn, [set_x(x+40), set_y(750), size, size], text, point)
            elif tie.match(point):
                conn = connection(db_dict[point]["conn"])
                drawer(val["kind"], scr, conn, [set_x(x), set_y(600), size, size], text, point)
                point = point[:-1]+"0"
                conn = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, conn, [set_x(x), set_y(525), size, size], text, point)
                point = point[:-1]+"1"
                conn = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, conn, [set_x(x), set_y(450), size, size], text, point)
            elif tr2.match(point):
                if isinstance(x, int):
                    conn = connection(db_dict[point]["conn"])
                else:
                    conn = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, conn, [set_x(x[0]+40), set_y(1300), size, size], text, point)

                    point = point[:-1] + "1"
                    conn = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, conn, [set_x(x[1]-40), set_y(1450), size, size], "up", point)

                    point = point[:-1] + "2"
                    conn = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, conn, [set_x(x[1]-40), set_y(1600), size, size], 'null', point)

    except KeyError:
        print(f"key does not exist: {point}")
    except IOError:
        print("io error")

# Loop until the user clicks the close button.
done = False
menu = True

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    # station = oneline_config.station_info[station_number].point
    station = oneline_config.station[1]
    direction = config["direction"][station_number - 1]

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            print("Quit.")
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    # Esc to escape
                print("Quit.")
                done = True
            elif event.key == pygame.K_m:
                print("menu")
                menu = True
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                station_number = event.key - 48  # 0 = 48
                menu = False
    if menu:
        pygame.display.set_caption("MENU")

        screen.fill(BLACK)  # Clear the screen and set the screen background]
        font = pygame.font.SysFont('malgungothic', 35, True, False)
        text = font.render("=========== MENU ===========", True, (255, 100, 50))
        screen.blit(text, [400, 200])
        text = font.render("Press Station Number (1 ~ 7)", True, WHITE)
        screen.blit(text, [400, 350])
        text = font.render("Back to MENU (M)", True, WHITE)
        screen.blit(text, [400, 500])
        text = font.render("Close (ESC)", True, WHITE)
        screen.blit(text, [400, 650])

    else:
        file_name = "data/station_test{0}.csv".format(station_number)
        db_list = []
        db_dict = dict()

        with open(file_name, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar='|')
            for row in csv_reader:
                if not row or row[0].startswith(("#", "=")):
                    continue
                elif row[0].startswith("SS"):
                    title = row[0]
                else:
                    name = row[0].split(" ")[0]
                    kind = row[0].split(" ")[1]
                    conn = row[1].strip()
                    #db_list.append({f"{name}": kind, "conn": conn})
                    db_dict[name] = {"kind": str(kind), "conn": int(conn)}

        pygame.display.set_caption("{0} 단선도".format(title))
        # above this, or they will be erased with this command.
        screen.fill(BLACK)  # Clear the screen and set the screen background

        for k, v in db_dict.items():
            shape(screen, k, v)

    # pygame.display.flip()
    pygame.display.update()
    clock.tick(config["screen"]["fps"])

#  close the window and quit.
pygame.quit()


