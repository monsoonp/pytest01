# diagram.py
import pygame
import math
import random
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
station_number = ""
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


def drawer(scr, line, data, x, y):
    name = data["name"].split(" ")[0]
    kind = data["name"].split(" ")[1]
    connection = int(data["conn"])
    conn = RED if connection else ALPHA

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
    '''    
    elif line == "sec":
        if data[2][6] == "0":
            pygame.draw.line(scr, conn, [x + 15, y-135], [x + 15, y], 2)
            pygame.draw.line(scr, conn, [x + 15, y-135], [x - 25, y-135], 2)
        else:
            if int(data[2][6]) % 2 == 1:
                pygame.draw.line(scr, conn, [x+15, y-45], [x+15, y+45], 2)
            else:
                pygame.draw.line(scr, conn, [x+15, y-15], [x+15, y+75], 2)
    '''
    conn = RED if connection == 1 else GREEN
    if "DS" in kind:
        pygame.draw.ellipse(scr, conn, [x, y, 30, 30], 0)
    elif "CB" in kind:
        pygame.draw.rect(scr, conn, [x, y, 30, 30], 0)

    font = pygame.font.SysFont('malgungothic', 15, True, False)
    text = font.render("{0}".format(name), True, WHITE)
    screen.blit(text, [x, y - 25])


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
        x = 0
        y = 0
        if name.isdigit():
            if len(name) == 3:
                x = int(name[1])
                y = int(name[2])
            elif len(name) == 4:
                x = int(name[1])
                y = int(name[3])

        if tl.match(name):  # 송전
            drawer(scr, "tl", data, x * 210 - 50, (y - 5) * 60)
        elif tl2.match(name):  # 송전 - 1차
            drawer(scr, "tl2", data, x * 210 - 100, (y + 3) * 60)
        elif tr.match(name):  # 1차 - MTR
            drawer(scr, "tr", data, x * 550 - 250, (y + 3) * 60)
        elif tr2.match(name):  # 1차 - MTR
            drawer(scr, "tr2", data, x * 550 - 200, (y + 3) * 60 + 30)
        elif tr3.match(name):  # MTR - 2차
            drawer(scr, "tr3", data, x * 550 - 200, (y + 5) * 60 + 10)
        elif tie.match(name):  # bus-tie
            if y == 0:
                y = 2
            elif y == 2:
                y = 3
            drawer(scr, "tie", data, x * 550 - 100, (y + 3) * 60 - 30)
        elif dl.match(name):  # MTR - 2차
            drawer(scr, "dl", data, x * 550 - 250, (y + 10) * 60)
        elif tie2.match(name):  # 2차 bus-tie
            if y == 0:
                y = 2
            elif y == 2:
                y = 3
            drawer(scr, "tie2", data, x * 550 - 100, (y + 10) * 60 - 30)

    else:  # (2차) bus section / 40-41-0, 40-41-1, 41-42-0 / 1차 60-61-0, 65-66-0
        y = int(name[1])
        x = 2 if int(name[6]) == 0 else 1 if int(name[6]) == 1 else 3

        first_y = 610 if int(name[0]) == 4 else 210
        second_y = 800 if int(name[0]) == 4 else 360

        x_sec = (y - 4) * 550 + x * 60 if y >= 5 else (y + 1) * 550 + x * 60
        y_sec = second_y - 15 if y >= 5 else first_y - 15  # y - 610, 800 / 210, 360

        drawer(scr, "sec", data, x_sec, y_sec)


# py파일 import
config = oneline_config.config
print(tuple(config["color"]["option"][config["color"]["conn"]]))
# json import
with open('oneline_config.json') as conf:
    config = json.load(conf)
print(tuple(config["color"]["option"][config["color"]["conn"]]))

# Loop until the user clicks the close button.
done = False
menu = True
station = 0
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            print("Quit.")
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Quit.")
                done = True
            elif event.key == pygame.K_r:
                print("reset")
            elif event.key == pygame.K_m:
                print("menu")
                menu = True
            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7]:
                station_number = event.key - 48  # 0 = 48
                menu = False
    if menu:
        pygame.display.set_caption("MENU")

        screen.fill(BLACK)  # Clear the screen and set the screen background]
        pygame.draw.rect(screen, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), [50, 50, 150, 150], 0)
        font = pygame.font.SysFont('malgungothic', 25, True, False)
        text = font.render("=========== MENU ===========", True, WHITE)
        screen.blit(text, [400, 400])
        text = font.render("Press Station Number (1~7)", True, WHITE)
        screen.blit(text, [400, 600])
        text = font.render("Back to MENU (M)", True, WHITE)
        screen.blit(text, [400, 800])

        clock.tick(1)
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

        pygame.draw.line(screen, WHITE, [0, 210], [width, 210], 3)
        pygame.draw.line(screen, WHITE, [0, 360], [width, 360], 3)

        pygame.draw.line(screen, WHITE, [0, 610], [width, 610], 3)
        pygame.draw.line(screen, WHITE, [0, 800], [width, 800], 3)

        for i in db_list:
            ds_draw(screen, i)
        pygame.draw.rect(screen, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)),[50, 50, 15, 15], 0)
        clock.tick(0.2)
    # --- Go ahead and update the screen with what we've drawn.
    # pygame.display.flip()
    pygame.display.update()
    # --- Limit to 60 frames per second


#  close the window and quit.
pygame.quit()


