# diagram.py
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
WHITE = (255, 255, 255)
# GREEN = (0, 255,   0)
GREEN = (55, 200,   55)
RED = (255,   0,   0)
BLUE = (0,   0, 255)
# A - 65, a - 97

db_list = []
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
# station = oneline_config.station_info[1].point
station = oneline_config.station[1]


def drawer(scr, line, data):

    name = data["name"].split(" ")[0]
    kind = data["name"].split(" ")[1]
    connection = int(data["conn"])
    conn = RED if connection else ALPHA
    try:
        position = station[name]
        if position:
            conn = RED if connection == 1 else GREEN
            if "DS" in kind:
                pygame.draw.ellipse(scr, conn, [set_x(position[0]),
                                                set_y(position[1]),
                                                config["size"]["ellipse"],
                                                config["size"]["ellipse"]], 0)
            elif "CB" in kind:
                pygame.draw.rect(scr, conn, [set_x(position[0]),
                                             set_y(position[1]),
                                             config["size"]["rect"],
                                             config["size"]["rect"]], 0)

            font = pygame.font.SysFont(config["text"]["font"], config["text"]["size"], config["text"]["bold"],
                                       config["text"]["italic"])
            text = font.render("{0}".format(name), True, WHITE)
            screen.blit(text, [set_x(position[0])+25, set_y(position[1])])
    except KeyError:
        pass

    """
    else:

        if line == "tl":
            pygame.draw.line(scr, conn, [x + 15, y], [x + 15, y + 165], 2)
            pygame.draw.line(scr, conn, [x + 15, y + 165], [x - 30, y + 165], 2)

        elif line == "tl2":  # top / bot
            if int(name) % 2 == 1:
                pygame.draw.line(scr, conn, [x + 15, y - 30], [x + 15, y + 45], 2)
            else:
                pygame.draw.line(scr, conn, [x + 15, y - 15], [x + 15, y + 60], 2)
        elif line == "tr2" or line == "tr3":
            pygame.draw.line(screen, conn, [x + 15, y - 30], [x + 15, y + 60], 2)
            if line == "tr2":
                pygame.draw.ellipse(scr, RED, [x - 8, y + 60, 46, 46], 2)
                pygame.draw.ellipse(scr, RED, [x - 8, y + 84, 46, 46], 2)
                # font = pygame.font.SysFont('malgungothic', 25, False, False)
                # text = font.render("{0}".format(name), True, ALPHA)
                # screen.blit(text, [x + 15, y + 77])
            else:
                pygame.draw.line(scr, conn, [x + 15, y], [x + 15, y + 155], 2)
                pygame.draw.line(scr, conn, [x + 15, y + 155], [x - 30, y + 155], 2)
        elif line == "tr":
            pygame.draw.line(screen, conn, [x + 15, y - 30], [x + 15, y + 60], 2)
        elif line == "dl":
            if int(name) % 2 == 1:
                pygame.draw.line(scr, conn, [x + 15, y - 45], [x + 15, y + 45], 2)
            else:
                pygame.draw.line(scr, conn, [x + 15, y - 15], [x + 15, y + 75], 2)
        elif line == "tie" or line == "tie2":
            pygame.draw.line(scr, conn, [x + 15, y - 15], [x + 15, y + 45], 2)
    """


def ds_draw(scr, data):
    # data / ex). ['1', '팔봉두마#1T/L617CB', '617', '[1]']

    tl = re.compile("6\\d[67]")  # 6_6-7
    tl2 = re.compile("6\\d[12]")  # 6_1-72
    tr = re.compile("6\\d3[12]")  # 61_1-2
    tr2 = re.compile("6\\d33")  # 6_31-2
    tr3 = re.compile("4\\d44")  # 4_41-2
    tie = re.compile("6\\d0[012]")  # 61_1-2
    dl = re.compile("4\\d4[12]")  # 4_41-2
    tie2 = re.compile("4\\d0[012]")  # 4_41-2
    name = data["name"].split(" ")[0]
    # kind = data["name"].split(" ")[1]

    if "-" not in name:

        if tl.match(name):  # 송전
            drawer(scr, "tl", data)
        elif tl2.match(name):  # 송전 - 1차
            drawer(scr, "tl2", data)
        elif tr.match(name):  # 1차 - MTR
            drawer(scr, "tr", data)
        elif tr2.match(name):  # 1차 - MTR
            drawer(scr, "tr2", data)
        elif tr3.match(name):  # MTR - 2차
            drawer(scr, "tr3", data)
        elif tie.match(name):  # bus-tie
            drawer(scr, "tie", data)
        elif dl.match(name):  # MTR - 2차
            drawer(scr, "dl", data)
        elif tie2.match(name):  # 2차 bus-tie
            drawer(scr, "tie2", data)

    else:  # (2차) bus section / 40-41-0, 40-41-1, 41-42-0 / 1차 60-61-0, 65-66-0
        drawer(scr, "sec", data)


def set_x(position):
    if direction:
        return int(width * position / 2000)
    else:
        return int(width * (2000 - position) / 2000)


def set_y(position):
    return int(height * position / 2000)

# py파일 import


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

        #  clock.tick(1)
    else:
        file_name = "data/station_test{0}.csv".format(station_number)
        db_list = []
        with open(file_name, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",", quotechar='|')
            for row in csv_reader:
                if not row or row[0].startswith(("#", "=")):
                    continue
                elif row[0].startswith("SS"):
                    title = row[0]
                else:
                    db_list.append({"name": row[0], "conn": row[1].strip()})

        pygame.display.set_caption("{0} 단선도".format(title))
        # above this, or they will be erased with this command.
        screen.fill(BLACK)  # Clear the screen and set the screen background]

        # pygame.draw.line(screen, WHITE, [0, 210], [width, 210], 3)
        # pygame.draw.line(screen, WHITE, [0, 360], [width, 360], 3)

        # pygame.draw.line(screen, WHITE, [0, 610], [width, 610], 3)
        # pygame.draw.line(screen, WHITE, [0, 800], [width, 800], 3)

        for i in db_list:
            ds_draw(screen, i)

        #  clock.tick(0.2)
    # --- Go ahead and update the screen with what we've drawn.
    # pygame.display.flip()
    pygame.display.update()
    # --- Limit to 10 frames per second
    clock.tick(config["screen"]["fps"])

#  close the window and quit.
pygame.quit()


