# oneline_v2.py
import pygame
import re
import sys
import json
import subprocess

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

db_dict = dict()

station_number = 1

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
x_position = 2400
y_position = 2000


def set_x(position):
    global x_position
    return int(width * position / x_position)


def set_y(position):
    global y_position
    return int(height * position / y_position)


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
        scr.blit(text, [location[0], location[1]-50])
    elif write == "down":
        scr.blit(text, [location[0], location[1]+20])


def shape(scr, point, val):
    tl = re.compile("^6\\d7$")  # 6_7
    tr = re.compile("^6\\d33$")  # 61_1-3
    tie = re.compile("(^6\\d02$|^4\\d02$)")  # 6_02 // 4_02

    dl = re.compile("^4\\d44$")  # 4_4[124
    bank = re.compile("^4(.[7]$|\\d[78][9]$)")  # 4_[127] / 4_[78][129]

    section = re.compile("(^6\\d-6\\d-[2]$|^4\\d-4\\d-[2]$)")   # [46]_-[46]_-[012]

    try:
        if point in station.keys():
            x = station[point][0]
            text = station[point][1]
            size = config["size"]
            if tl.match(point):
                lines = []
                color = connection(db_dict[point]["conn"])
                drawer(val["kind"], scr, color, [set_x(x), set_y(300), size, size], text, point)
                lines.append({"x":point, "conn": db_dict[point]["conn"]})

                point = point[:-1]+"1"
                color = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, color, [set_x(x-40), set_y(450), size, size], text, point)
                lines.append({"x": point, "conn": db_dict[point]["conn"]})

                point = point[:-1]+"2"
                color = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, color, [set_x(x-40), set_y(600), size, size], text, point)
                lines.append({"x": point, "conn": db_dict[point]["conn"]})
            elif tr.match(point):
                if isinstance(x, int):
                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x+40), set_y(750), size, size], text, point)
                    point = point[:-1]+"1"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(450), size, size], text, point)
                    point = point[:-1]+"2"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(600), size, size], text, point)
            elif tie.match(point):
                if point[0] == "6":
                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x), set_y(600), size, size], text, point)
                    point = point[:-1]+"0"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(525), size, size], text, point)
                    point = point[:-1]+"1"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(450), size, size], text, point)
                elif point[0] == "4":
                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x), set_y(1400), size, size], text, point)
                    point = point[:-1] + "0"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1325), size, size], station[point][1], point)
                    point = point[:-1] + "1"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1250), size, size], station[point][1], point[:-1])
            elif dl.match(point):
                if isinstance(x, int):
                    print("add something")
                else:
                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x[0]+40), set_y(1000), size, size], text, point)
                    point = point[:-1] + "1"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x[1]), set_y(1250), size, size], "up", point[:-1])
                    point = point[:-1] + "2"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x[1]), set_y(1400), size, size], 'null', point)
            elif bank.match(point):
                color = connection(db_dict[point]["conn"])
                drawer(val["kind"], scr, color, [set_x(x+20), set_y(1550), size, size], text, point)
                point = point[:-1] + "1"
                color = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1250), size, size], station[point][1], point[:-1])
                point = point[:-1] + "2"
                color = connection(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1400), size, size], station[point][1], point)
            elif section.match(point):
                if point[0] == "4":
                    y = 1250 - 60 if int(point[1]) < 5 else 1400 + 60
                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x), set_y(y), size, size], text, point[-2:])
                    point = point[:-1] + "0"
                    x = station[point][0]
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(y), size, size], station[point][1], point[:-2])
                    point = point[:-1] + "1"
                    x = station[point][0]
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(y), size, size], station[point][1], point[-2:])

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
    # station = oneline_config.station[station_number]

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
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                x_position = x_position - 100 if event.key == 275 else x_position + 100
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                y_position = y_position - 100 if event.key == 274 else y_position + 100

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

        db_dict = dict()
        station_info = subprocess.run(["./shmon", str(station_number), "-n"], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")

        for row in station_info:
            row = row.strip()
            if row != "":
                if row.startswith(("#", "=")):
                    continue
                elif row.startswith("SS"):
                    title = row
                else:
                    value = row.split(",")
                    name = value[0].split(" ")[0]
                    kind = value[0].split(" ")[1]
                    conn = value[1].strip()
                    db_dict[name] = {"kind": str(kind), "conn": int(conn)}

        pygame.display.set_caption("{0} 단선도".format(title))
        # above this, or they will be erased with this command.
        screen.fill(BLACK)  # Clear the screen and set the screen background]

        for k, v in db_dict.items():
            shape(screen, k, v)

    # pygame.display.flip()
    pygame.display.update()
    clock.tick(config["screen"]["fps"])

#  close the window and quit.
pygame.quit()

