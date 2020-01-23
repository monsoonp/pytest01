# diagramTest.py
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
file_name = "station{0}.csv". format(4)

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
    conn = RED if data[3] == "[1]" else BLUE
    # pygame.draw.line(screen, WHITE, [50, 200], [1600, 200], 3)
    if line == "tl":
        pygame.draw.line(scr, conn, [x+15, y], [x+15, y+165], 2)
        pygame.draw.line(scr, conn, [x+15, y+165], [x-30, y+165], 2)
    elif line == "tl2":  # top / bot
        if int(data[2]) % 2 == 1:
            pygame.draw.line(scr, conn, [x+15, y-30], [x+15, y+45], 2)
        else:
            pygame.draw.line(scr, conn, [x+15, y-15], [x+15, y+60], 2)
    elif line == "tr" or line == "tr2":
        pygame.draw.line(screen, conn, [x + 15, y - 30], [x + 15, y + 60], 2)
        if line == "tr":
            pygame.draw.ellipse(scr, RED, [x - 8, y + 60, 46, 46], 2)
            pygame.draw.ellipse(scr, RED, [x - 8, y + 84, 46, 46], 2)
            font = pygame.font.SysFont('malgungothic', 25, False, False)
            text = font.render("{0}".format(data[1][:6]), True, ALPHA)
            screen.blit(text, [x + 15, y + 77])
        else:
            pygame.draw.line(scr, conn, [x + 15, y], [x + 15, y + 155], 2)
            pygame.draw.line(scr, conn, [x + 15, y + 155], [x - 30, y + 155], 2)

    elif line == "dl":
        if int(data[2]) % 2 == 1:
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
    conn = RED if data[3] == "[1]" else GREEN
    if "DS" in data[1]:
        pygame.draw.ellipse(scr, conn, [x, y, 30, 30], 0)
    elif "CB" in data[1]:
        pygame.draw.rect(scr, conn, [x, y, 30, 30], 0)

    font = pygame.font.SysFont('malgungothic', 15, True, False)
    text = font.render("{0}".format(data[2], data[3]), True, ALPHA)
    screen.blit(text, [x-50, y])


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
    if "-" not in data[2]:
        x = 0
        y = 0
        if len(data[2]) == 3:
            x = int(data[2][1])
            y = int(data[2][2])
        elif len(data[2]) == 4:
            x = int(data[2][1])
            y = int(data[2][3])

        if tl.match(data[2]):       # 송전
            drawer(scr, "tl", data, x * 250 - 50, (y-5) * 60)
        elif tl2.match(data[2]):    # 송전 - 1차
            drawer(scr, "tl2", data, x * 250 - 100, (y+3) * 60)
        elif tr.match(data[2]):    # 1차 - MTR
            drawer(scr, "tr", data, x * 550 - 200, (y+3) * 60 + 30)
        elif tr2.match(data[2]):    # MTR - 2차
            drawer(scr, "tr2", data, x * 550 - 200, (y+5) * 60 + 10)
        elif dl.match(data[2]):     # MTR - 2차
            drawer(scr, "dl", data, x * 550 - 250, (y+10) * 60)
        elif tie2.match(data[2]):   # 2차 버스타이
            if y == 0:
                y = 2
            elif y == 2:
                y = 3
            drawer(scr, "tie2", data, x * 550 - 100, (y+10) * 60 - 30)

    else:   # (2차) bus section / 40-41-0, 40-41-1, 41-42-0 / 1차 60-61-0, 65-66-0
        y = int(data[2][1])
        x = 2 if int(data[2][6]) == 0 else 1 if int(data[2][6]) == 1 else 3

        first_y = 610 if int(data[2][0]) == 4 else 210
        second_y = 800 if int(data[2][0]) == 4 else 360

        x_sec = (y-4)*550 + x*60 if y >= 5 else (y+1)*550 + x*60
        y_sec = second_y-15 if y >= 5 else first_y-15  # y - 610, 800 / 210, 360

        drawer(scr, "sec", data, x_sec, y_sec)


with open(file_name, encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='|')
    for row in csv_reader:
        print(row)
        if row[0].startswith("#"):
            print("{0}".format(row))
            continue
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

    pygame.draw.line(screen, WHITE, [50, 210], [1600, 210], 3)
    pygame.draw.line(screen, WHITE, [50, 360], [1600, 360], 3)

    pygame.draw.line(screen, WHITE, [0, 610], [1800, 610], 3)
    pygame.draw.line(screen, WHITE, [0, 800], [1800, 800], 3)

    for i in db_list:
        ds_draw(screen, i)

    """
    # --- Drawing code should go here ##############
    pygame.draw.rect(screen, RED, [x_test+x_position, y_position, 20, 25], 0)  # 원점(x,y), 너비, 높이
    # Draw on the screen a green line from (0, 0) to (100, 100)
    # that is 5 pixels wide.
    pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    # Draw a rectangle
    pygame.draw.rect(screen, WHITE, [20, 20, 250, 100], 10)
    # Draw an ellipse, using a rectangle as the outside boundaries
    pygame.draw.ellipse(screen, GREEN, [20, 20, 250, 100], 2)
    # Draw an arc as part of an ellipse. Use radians to determine what
    # angle to draw.
    pygame.draw.arc(screen, GREEN, [100, 250, 150, 150], PI / 2, PI, 1)
    pygame.draw.arc(screen, WHITE, [100, 250, 150, 150], 0, PI / 2, 2)
    pygame.draw.arc(screen, RED, [100, 250, 150, 150], 3 * PI / 2, 2 * PI, 1)
    pygame.draw.arc(screen, BLUE, [100, 250, 150, 150], PI, 3 * PI / 2, 2)

    # This draws a triangle using the polygon command
    pygame.draw.polygon(screen, WHITE, [[100, 100], [0, 200], [200, 200]], 5)
    
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)
    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    text = font.render("My text : "+str(123), True, WHITE)
    # Put the image of the text on the screen at 250x250
    screen.blit(text, [150, 450])
    """
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(1)

#  close the window and quit.
pygame.quit()


