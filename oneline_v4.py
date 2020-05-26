# oneline_v4.py
import pygame
import re
import sys
import json
import subprocess

import oneline_config

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
LIVE = (150, 150, 255)
# A - 65, a - 97

db_dict = dict()
station_number = 1

# 화면 사이즈, 튜플 형식
# size = (1800, 1000)
video_infos = pygame.display.Info()  # pygame, 화면정보
width, height = video_infos.current_w, video_infos.current_h  # 화면 너비, 높이

# 화면 띄우기
# 더블 버퍼, 리사이즈, 하드웨어 가속 pygame.HWSURFACE (전체화면에서만)
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.RESIZABLE)

title = ""
# 화면 제목
pygame.display.set_caption("{0} 단선도".format(title))
config = oneline_config.config
station = oneline_config.station[1]
x_position = 2400
y_position = 2000
check = True


def set_x(position):  # 스크린에 따른 x좌표
    global x_position
    return int(width * position / x_position)


def set_y(position):  # 스크린에 따른 y좌표
    global y_position
    return int(height * position / y_position)


def connection(val):  # 연결에 따른 색상
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
    elif write == "top":
        scr.blit(text, [location[0], location[1]-50])
    elif write == "up":
        scr.blit(text, [location[0], location[1]-20])
    elif write == "down":
        scr.blit(text, [location[0], location[1]+20])


def liner(scr, dic, line_list):
    # 1차
    l_color = station["color"]
    lines = line_list["1차"]
    if not len(lines):
        pygame.draw.line(scr, LIVE, [0, set_y(400)], [width, set_y(400)], 5)
        pygame.draw.line(scr, LIVE, [0, set_y(700)], [width, set_y(700)], 5)

    # MTR
    for i in enumerate([i for i in dic.keys() if re.match(r"6\d33", i)]):
        i = i[0]
        color = station["color"][i] if dic[f"6{i + 1}33"]["conn"] else GREY  # 6133 색상
        if isinstance(station[f"6{i + 1}33"][0], int):  # 6133 정수타입 유무/ 정수시
            pygame.draw.line(scr, color, [set_x(station[f"6{i + 1}33"][0] - 60), set_y(820)], [set_x(station[f"6{i + 1}33"][0] + 160), set_y(820)], 3)
            pygame.draw.line(scr, color, [set_x(station[f"6{i + 1}33"][0]+40)+10, set_y(780)], [set_x(station[f"6{i + 1}33"][0]+40)+10, set_y(820)], 3)
        else:
            print("6133 타입 체크")
        # MTR 텍스트 표시
        opt = pygame.font.SysFont(config["text"]["font"], 35, True, False)
        mtr = opt.render(f"# {i + 1} M.Tr", True, WHITE)
        screen.blit(mtr, [set_x(station[f"6{i + 1}33"][0] - 60), set_y(840)])

        color = station["color"][i] if dic[f"4{i + 1}44"]["conn"] else GREY  # 4144 색상
        if isinstance(station[f"4{i + 1}44"][0], int):  # 4144 정수타입 유무/ 정수시
            pygame.draw.line(scr, color, [set_x(station[f"4{i + 1}44"][0] - 60), set_y(960)], [set_x(station[f"4{i + 1}44"][0] + 160), set_y(960)], 3)
            pygame.draw.line(scr, color, [set_x(station[f"4{i + 1}44"][0] + 40)+10, set_y(960)], [set_x(station[f"4{i + 1}44"][0] + 40)+10, set_y(1000)], 3)
        else:   # 리스트일시 첫번째 값
            pygame.draw.line(scr, color, [set_x(station[f"4{i + 1}44"][0][0] - 60), set_y(960)], [set_x(station[f"4{i + 1}44"][0][0] + 160), set_y(960)], 3)
            pygame.draw.line(scr, color, [set_x(station[f"4{i + 1}44"][0][0] + 40)+10, set_y(960)], [set_x(station[f"4{i + 1}44"][0][0] + 40)+10, set_y(1000)], 3)
    # 2차
    lines = line_list["2차"] if station["direction"] else line_list["2차"][::-1]  # Mtr, 2차section에 따른 구분
    for i in range(0, len(lines)-1):
        try:
            if dic[f"4{i+1}44"]["conn"] and dic[f"4{i+1}41"]["conn"]:    # 4_44 and 4_41 연결시
                pygame.draw.line(scr, l_color[i], [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i+1]][0]), set_y(1205)], 5)
                # pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i + 1]][0]), set_y(1475)], 5)

                if i < len(lines) - 2:  # 마지막 section 이전까지
                    if dic[f"4{i+5}-4{i+6}-0"]["conn"]:
                        pygame.draw.line(scr, l_color[i+1], [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i + 1]][0]), set_y(1475)], 5)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i + 1]][0]), set_y(1475)], 5)
                else:   # 마지막 section
                    if dic[f"4{i+4}-4{i+5}-0"]["conn"]:
                        pygame.draw.line(scr, l_color[i], [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i + 1]][0]), set_y(1475)], 5)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i + 1]][0]), set_y(1475)], 5)

            elif dic[f"4{i+1}44"]["conn"] and dic[f"4{i+1}42"]["conn"]:    # 4_44 and 4_42 연결시
                pygame.draw.line(scr, l_color[i], [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i+1]][0]), set_y(1475)], 5)
                # pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i + 1]][0]), set_y(1205)], 5)

                if i < len(lines) - 2:
                    if dic[f"4{i}-4{i + 1}-0"]["conn"]:
                        pygame.draw.line(scr, l_color[i + 1], [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i + 1]][0]), set_y(1205)], 5)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i + 1]][0]), set_y(1205)], 5)
                else:
                    if dic[f"4{i-1}-4{i}-0"]["conn"]:
                        pygame.draw.line(scr, l_color[i + 1], [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i + 1]][0]), set_y(1205)], 5)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i + 1]][0]), set_y(1205)], 5)

            else:
                pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1205)], [set_x(station[lines[i + 1]][0]), set_y(1205)], 5)
                pygame.draw.line(scr, GREY, [set_x(station[lines[i]][0]), set_y(1475)], [set_x(station[lines[i + 1]][0]), set_y(1475)], 5)

        except KeyError:
            print("2차 BusLine KeyError")
            pass


def bus_liner(scr, point, x, *args):
    # tl, bank
    if point[0] == "6":
        if db_dict[point]["conn"]:
            # 611 위에서 아래 우측
            pygame.draw.line(scr, LIVE, [set_x(x - 40) + 10, set_y(400) if point[-1] == "1" else set_y(450)+20], [set_x(x - 40) + 10, set_y(600 if point[-1] == "1" else 700)], 3)
            pygame.draw.line(scr, LIVE, [set_x(x - 40) + 10, set_y(540)], [set_x(x) + 10, set_y(540)], 3)
        else:
            pygame.draw.line(scr, GREY, [set_x(x - 40) + 10, set_y(400 if point[-1] == "1" else 600)], [set_x(x - 40) + 10, set_y(450 if point[-1] == "1" else 700)], 3)
    elif point[0] == "4":
        lines = station["line"]["2차"] if station["direction"] else station["line"]["2차"][::-1]  # Mtr, 2차section에 따른 구분
        l_color = args[0]
        if db_dict[point]["conn"]:
            # 411 위에서 아래 우측
            pygame.draw.line(scr, l_color, [set_x(x) + 10, set_y(1205) if point[-1] == "1" else set_y(1250)+20], [set_x(x) + 10, set_y(1400) if point[-1] == "1" else set_y(1475)], 3)
            pygame.draw.line(scr, l_color, [set_x(x) + 10, set_y(1325)+10], [set_x(x+(20 if not re.match(r"4\d4[12]", point) else 40)) + 10, set_y(1325)+10], 3)
        else:
            pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(1205) if point[-1] == "1" else set_y(1475)-20], [set_x(x) + 10, set_y(1250) if point[-1] == "1" else set_y(1475)], 3)


def bus_color(point):
    color = (0, 0, 0)
    mtr = [i for i in station if re.match(r"6\d33", i)]
    section = [i for i in station if re.match(r"\d\d-\d\d-0", i) and int(i[1]) < 5]
    for val in enumerate(section):  # config 섹션
        if station[point][0] < station[val[1]][0] if station["direction"] else station[point][0] > station[val[1]][0]:
            if db_dict[f"4{val[0]+1}44"]["conn"]:
                color = station["color"][val[0]]
            else:
                color = GREY
            return color
        else:
            continue
    last = -(len(mtr)-len(section))
    if db_dict[f"4{len(mtr)+last+1}44"]["conn"]:
        color = station["color"][last]  # mtr 수와 2차 섹션 차이에 따른 2차 bus 색상 / 마지막 mtr 미사용
    else:
        color = GREY
    return color


def shape(scr, point, val):
    global check
    tl = re.compile(r"^6\d7$")  # 6_7
    tr = re.compile(r"^6\d33$")  # 61_1-3
    tie = re.compile(r"(^6\d02$|^4\d02$)")  # 6_02 // 4_02
    dl = re.compile(r"^4\d44$")  # 4_4[124
    bank = re.compile(r"^4(.[7]$|\d[78][9]$)")  # 4_[127] / 4_[78][129]

    section = re.compile(r"(^6\d-6\d-[2]$|^4\d-4\d-[2]$)")   # [46]_-[46]_-[012]
    checker = []
    try:
        if point in station.keys():  # config key 값안에 존재하는 point
            x = station[point][0]
            text = station[point][1]
            size = config["size"]
            if tl.match(point):
                color = connection(db_dict[point]["conn"])
                # 617 위에서 아래
                pygame.draw.line(scr, LIVE, [set_x(x)+10, set_y(320)], [set_x(x)+10, set_y(540)], 3)
                drawer(val["kind"], scr, color, [set_x(x), set_y(300), size, size], text, point)

                point = point[:-1]+"1"
                color = connection(db_dict[point]["conn"])
                bus_liner(scr, point, x)
                drawer(db_dict[point]["kind"], scr, color, [set_x(x-40), set_y(450), size, size], text, point)

                point = point[:-1]+"2"
                color = connection(db_dict[point]["conn"])
                bus_liner(scr, point, x)
                drawer(db_dict[point]["kind"], scr, color, [set_x(x-40), set_y(600), size, size], text, point)

            elif tr.match(point):  # 6133
                if isinstance(x, int):
                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x+40), set_y(750), size, size], text, point)

                    # 6131 선
                    point = point[:-1]+"1"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    bus_liner(scr, point, x+40, LIVE)
                    # 6131
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(450), size, size], text, point)

                    # 6132 선
                    point = point[:-1]+"2"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    bus_liner(scr, point, x+40, LIVE)
                    # 6132
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(600), size, size], text, point)

                    # 6131, 6132 연결이 있을 시
                    if True in checker:
                        pygame.draw.line(scr, LIVE, [set_x(x + 40) + 10, set_y(750)], [set_x(x + 40) + 10, set_y(540)], 3)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(x + 40) + 10, set_y(750)], [set_x(x + 40) + 10, set_y(540)], 3)
                        pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(490)], [set_x(x) + 10, set_y(600)], 3)
                        pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(540)], [set_x(x + 40) + 10, set_y(540)], 3)

            elif tie.match(point):  # 6100
                if point[0] == "6":
                    # 6100 연결상태에 따른 선
                    if db_dict[point[:-1]+"0"]["conn"]:
                        pygame.draw.line(scr, LIVE, [set_x(x) + 10, set_y(400)], [set_x(x) + 10, set_y(700)], 3)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(400)], [set_x(x) + 10, set_y(700)], 3)

                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x), set_y(600), size, size], text, point)

                    point = point[:-1]+"0"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(525), size, size], text, point)

                    point = point[:-1]+"1"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(450), size, size], text, point)
                elif point[0] == "4":  # 4100
                    # 4100 연결상태에 따른 선 연결
                    color = station["color"][int(point[1])]
                    if db_dict[point[:-1]+"0"]["conn"]:
                        pygame.draw.line(scr, color, [set_x(x) + 10, set_y(1210)], [set_x(x) + 10, set_y(1470)], 3)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(1210)], [set_x(x) + 10, set_y(1470)], 3)

                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x), set_y(1400), size, size], text, point)

                    point = point[:-1] + "0"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1325), size, size], station[point][1], point)

                    point = point[:-1] + "1"
                    color = connection(db_dict[point]["conn"])
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1250), size, size], station[point][1], point[:-1])
            elif dl.match(point):  # 4144
                l_color = station["color"][int(point[1])-1]  # 선 색상
                if not db_dict[point]["conn"] or not (db_dict[point[:-1]+"1"]["conn"] or db_dict[point[:-1]+"2"]["conn"]):
                    l_color = GREY
                # 4144 x값 정수 타입 유무
                if isinstance(x, int):
                    color = connection(db_dict[point]["conn"])
                    pygame.draw.line(scr, l_color, [set_x(x + 40) + 10, set_y(1000) + 20], [set_x(x + 40) + 10, set_y(1325) +10], 3)
                    drawer(val["kind"], scr, color, [set_x(x + 40), set_y(1000), size, size], text, point)

                    point = point[:-1] + "1"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    bus_liner(scr, point, x, l_color)
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1250), size, size], "top", point[:-1])

                    point = point[:-1] + "2"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    bus_liner(scr, point, x, l_color)
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1400), size, size], 'null', point)

                    if True not in checker:
                        pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(1250) + 20], [set_x(x) + 10, set_y(1400)], 3)
                        pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(1325) + 10], [set_x(x + 40) + 10, set_y(1325) + 10], 3)
                else:
                    pygame.draw.line(scr, l_color, [set_x(x[0]+40)+10, set_y(1000)+20], [set_x(x[0]+40)+10, set_y(1100)], 3)
                    pygame.draw.line(scr, l_color, [set_x(x[0] + 40) + 10, set_y(1100)], [set_x(x[1] + 20) + 10, set_y(1100)], 3)
                    pygame.draw.line(scr, l_color, [set_x(x[1] + 20) + 10, set_y(1100)], [set_x(x[1] + 20) + 10, set_y(1325)+10], 3)

                    color = connection(db_dict[point]["conn"])
                    drawer(val["kind"], scr, color, [set_x(x[0]+40), set_y(1000), size, size], text, point)

                    point = point[:-1] + "1"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    if db_dict[point]["conn"]:  # 4141 연결시 선
                        pygame.draw.line(scr, l_color, [set_x(x[1]) + 10, set_y(1205)], [set_x(x[1]) + 10, set_y(1400)], 3)
                        pygame.draw.line(scr, l_color, [set_x(x[1]) + 10, set_y(1325)+10], [set_x(x[1]+20) + 10, set_y(1325)+10], 3)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(x[1]) + 10, set_y(1205)], [set_x(x[1]) + 10, set_y(1250)], 3)
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x[1]), set_y(1250), size, size], "top", point[:-1])

                    point = point[:-1] + "2"
                    color = connection(db_dict[point]["conn"])
                    checker.append(db_dict[point]["conn"])
                    if db_dict[point]["conn"]:  # 4142 연결시 선

                        pygame.draw.line(scr, l_color, [set_x(x[1]) + 10, set_y(1250)+20], [set_x(x[1]) + 10, set_y(1475)], 3)
                        pygame.draw.line(scr, l_color, [set_x(x[1]) + 10, set_y(1325)+10], [set_x(x[1]+20) + 10, set_y(1325)+10], 3)
                    else:
                        pygame.draw.line(scr, GREY, [set_x(x[1]) + 10, set_y(1400)+20], [set_x(x[1]) + 10, set_y(1475)], 3)
                    drawer(db_dict[point]["kind"], scr, color, [set_x(x[1]), set_y(1400), size, size], 'null', point)
                    if True not in checker:
                        pygame.draw.line(scr, GREY, [set_x(x[1]) + 10, set_y(1250) + 20], [set_x(x[1]) + 10, set_y(1400)], 3)
                        pygame.draw.line(scr, GREY, [set_x(x[1]) + 10, set_y(1325) + 10], [set_x(x[1] + 20) + 10, set_y(1325) + 10], 3)
            elif bank.match(point):  # 4179. 4189, 427
                color = connection(db_dict[point]["conn"])
                l_color = bus_color(point)
                low_color = l_color if (db_dict[point[:-1] + "1"]["conn"] or db_dict[point[:-1] + "2"]["conn"]) else GREY
                pygame.draw.line(scr, low_color, [set_x(x + 20) + 10, set_y(1325) + 10], [set_x(x + 20) + 10, set_y(1550)], 3)
                drawer(val["kind"], scr, color, [set_x(x+20), set_y(1550), size, size], text, point)
                point = point[:-1] + "1"

                bus_liner(scr, point, x, l_color)
                color = connection(db_dict[point]["conn"])
                checker.append(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1250), size, size], station[point][1], point[:-1])

                point = point[:-1] + "2"
                bus_liner(scr, point, x, l_color)
                color = connection(db_dict[point]["conn"])
                checker.append(db_dict[point]["conn"])
                drawer(db_dict[point]["kind"], scr, color, [set_x(x), set_y(1400), size, size], station[point][1], point)

                if True not in checker:
                    pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(1250) + 20], [set_x(x) + 10, set_y(1400)], 3)
                    pygame.draw.line(scr, GREY, [set_x(x) + 10, set_y(1325) + 10], [set_x(x + 20) + 10, set_y(1325) + 10], 3)

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
        else:
            # config에 없지만 존재하는 point
            if check:
                if point not in db_dict.keys():
                    print(f"{point} config not exist")
                check = False
            else:
                pass

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
                menu = True
                x_position = 2400
                y_position = 2000
            elif event.key == pygame.K_r:
                x_position = 2400
                y_position = 2000
            elif event.key in [pygame.K_1, pygame.K_4]:  # , pygame.K_2, pygame.K_3, pygame.K_5, pygame.K_6, pygame.K_7
                station_number = event.key - 48  # 0 = 48
                station = oneline_config.station[station_number]
                menu = False
            elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                x_position = x_position - 100 if event.key == 275 else x_position + 100
            elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                y_position = y_position - 100 if event.key == 274 else y_position + 100

    if menu:
        pygame.display.set_caption("MENU")

        screen.fill(BLACK)  # Clear the screen and set the screen background]
        font = pygame.font.SysFont(config["text"]["font"], 35, True, False)
        text = font.render("=========== MENU ===========", True, (255, 100, 50))
        screen.blit(text, [400, 200])
        text = font.render("Press Station Number (1, 4)", True, WHITE)
        screen.blit(text, [400, 350])
        text = font.render("Back to MENU (M)", True, WHITE)
        screen.blit(text, [400, 500])
        text = font.render("Reset (R) / Close (ESC)", True, WHITE)
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

        font = pygame.font.SysFont(config["text"]["font"], 25, True, False)
        text = font.render(re.sub(r"SS : (\d)\(([가-힣]{2})\)", r"\2 (\1)", title), True, WHITE)
        screen.blit(text, [0, 0])

        if not station["direction"]:
            pygame.draw.polygon(screen, (255, 255, 0), [[width-10, set_y(900)], [width-10, set_y(900)+50], [width-60, set_y(900)+25]])
        liner(screen, db_dict, station["line"])
        for k, v in db_dict.items():
            shape(screen, k, v)

    pygame.display.update()
    clock.tick(config["screen"]["fps"])

#  close the window and quit.
pygame.quit()

