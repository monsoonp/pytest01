# diagram.py
import pygame
import math
import csv
import re
import sys

# import testClass
# from test.testClass import Address
pygame.init()

# functions
ALPHA = (200, 200, 200, 0.5)
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
# GREEN = (0, 255,   0)
GREEN = (55, 200,   55)
RED = (255,   0,   0)
BLUE = (0,   0, 255)
# A - 65, a - 97

db_list = []
file_name = "station_test{0}.csv". format(4)

# PI = math.pi
# 화면 사이즈, 튜플 형식
# size = (1800, 1000)
# 화면 띄우기
# screen = pygame.display.set_mode(size, pygame.RESIZABLE)

video_infos = pygame.display.Info()  # pygame, 화면정보
width, height = video_infos.current_w, video_infos.current_h  # 화면 너비, 높이
# 더블 버퍼, 리사이즈, 하드웨어 가속 pygame.HWSURFACE (전체화면에서만)
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.RESIZABLE)

# 화면 제목
pygame.display.set_caption("{0} 단선도".format(file_name))


def drawer(scr, line, data, x, y):
    name = data[0].split(" ")[0]
    kind = data[0].split(" ")[1]
    connection = int(data[1].replace(" ", ""))
    conn = RED if connection else BLUE
    # pygame.draw.line(screen, WHITE, [50, 200], [1600, 200], 3)
    if line == "tl":
        pygame.draw.line(scr, conn, [x+15, y], [x+15, y+165], 2)
        pygame.draw.line(scr, conn, [x+15, y+165], [x-30, y+165], 2)
    elif line == "tl2":  # top / bot
        if int(name) % 2 == 1:
            pygame.draw.line(scr, conn, [x+15, y-30], [x+15, y+45], 2)
        else:
            pygame.draw.line(scr, conn, [x+15, y-15], [x+15, y+60], 2)
    elif line == "tr" or line == "tr2":
        pygame.draw.line(screen, conn, [x + 15, y - 30], [x + 15, y + 60], 2)
        if line == "tr":
            pygame.draw.ellipse(scr, RED, [x - 8, y + 60, 46, 46], 2)
            pygame.draw.ellipse(scr, RED, [x - 8, y + 84, 46, 46], 2)
            # font = pygame.font.SysFont('malgungothic', 25, False, False)
            # text = font.render("{0}".format(name), True, ALPHA)
            # screen.blit(text, [x + 15, y + 77])
        else:
            pygame.draw.line(scr, conn, [x + 15, y], [x + 15, y + 155], 2)
            pygame.draw.line(scr, conn, [x + 15, y + 155], [x - 30, y + 155], 2)

    elif line == "dl":
        if int(name) % 2 == 1:
            pygame.draw.line(scr, conn, [x+15, y-45], [x+15, y+45], 2)
        else:
            pygame.draw.line(scr, conn, [x+15, y-15], [x+15, y+75], 2)
    elif line == "tie2":
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
    text = font.render("{0}".format(name, connection), True, ALPHA)
    screen.blit(text, [x, y-25])


def ds_draw(scr, data):
    # data / ex). ['1', '팔봉두마#1T/L617CB', '617', '[1]']

    tl = re.compile("6\\d[67]")  # 6_6-7
    tl2 = re.compile("6\\d[12]")  # 6_1-72
    # bus = re.compile("6\\d3[12]")  # 61_1-2 not exist
    # tie = re.compile("6\\d0[012]")  # 61_1-2 not exist
    tr = re.compile("6\\d33")  # 6_31-2
    tr2 = re.compile("4\\d44")  # 4_41-2
    dl = re.compile("4\\d4[12]")  # 4_41-2
    tie2 = re.compile("4\\d0[012]")  # 4_41-2
    name = data[0].split(" ")[0]
    kind = data[0].split(" ")[1]

    if "-" not in name:
        x = 0
        y = 0
        if name.isdigit():
            print(name)
            if len(name) == 3:
                x = int(name[1])
                y = int(name[2])
            elif len(name) == 4:
                x = int(name[1])
                y = int(name[3])

        if tl.match(name):       # 송전
            drawer(scr, "tl", data, x * 120 - 50, (y-5) * 60)
        elif tl2.match(name):    # 송전 - 1차
            drawer(scr, "tl2", data, x * 120 - 100, (y+3) * 60)
        elif tr.match(name):    # 1차 - MTR
            drawer(scr, "tr", data, x * 550 - 200, (y+3) * 60 + 30)
        elif tr2.match(name):    # MTR - 2차
            drawer(scr, "tr2", data, x * 550 - 200, (y+5) * 60 + 10)
        elif dl.match(name):     # MTR - 2차
            drawer(scr, "dl", data, x * 550 - 250, (y+10) * 60)
        elif tie2.match(name):   # 2차 버스타이
            if y == 0:
                y = 2
            elif y == 2:
                y = 3
            drawer(scr, "tie2", data, x * 550 - 100, (y+10) * 60 - 30)

    else:   # (2차) bus section / 40-41-0, 40-41-1, 41-42-0 / 1차 60-61-0, 65-66-0
        y = int(name[1])
        x = 2 if int(name[6]) == 0 else 1 if int(name[6]) == 1 else 3

        first_y = 610 if int(name[0]) == 4 else 210
        second_y = 800 if int(name[0]) == 4 else 360

        x_sec = (y-4)*550 + x*60 if y >= 5 else (y+1)*550 + x*60
        y_sec = second_y-15 if y >= 5 else first_y-15  # y - 610, 800 / 210, 360

        drawer(scr, "sec", data, x_sec, y_sec)


with open(file_name, encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='|')
    for row in csv_reader:

        if not row or row[0].startswith("#"):
            continue
            if not row: print("{0}".format(row))
        print(row)
        db_list.append(row)

# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
    pos = pygame.mouse.get_pos()
    x_position = pos[0]
    y_position = pos[1]
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            print("Quit.")
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("Quit.")
                done = True

        '''
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")
        '''
    # --- Game logic should go here

    # First, clear the screen to white. Don't put other drawing commands

    # above this, or they will be erased with this command.
    screen.fill(BLACK)  # Clear the screen and set the screen background]

    pygame.draw.line(screen, WHITE, [0, 210], [1800, 210], 3)
    pygame.draw.line(screen, WHITE, [0, 360], [1800, 360], 3)

    pygame.draw.line(screen, WHITE, [0, 610], [1800, 610], 3)
    pygame.draw.line(screen, WHITE, [0, 800], [1800, 800], 3)

    for i in db_list:
        ds_draw(screen, i)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(1)

#  close the window and quit.
pygame.quit()


