# oneline_config.py
import pygame

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
        "font": "malgungothic",
        "size": 15,
        "bold": True,
        "italic": False
    },
    "screen": {
        "size": 0,
        "fps": 2
    },
    "size": 20,
    "direction": [True, False, True, False, True, True, True]  # 1 - 7 변전소 방향

}

station = {  # default 변전소 설정값
    1: {
        "617": [100, None],
        "6131": [180, None],

        "6102": [300, None],

        "627": [520, None],
        "6231": [600, None],

        "637": [740, None],
        "6331": [820, None],

        "647": [1160, None],
        "6431": [1260, None],


        "6531": [1700, None],

        "4144": [[180, 380], None],
        "4244": [[600, 720], None],
        "4344": [[820, 1260], None],
        "4444": [[1260, 1600], None],
        "4544": [[1700, 1800], None],

        """
    
        "4179",
        "4171",
        "4172",
    
        "427",
        "421",
        "422",
    
        "437",
        "431",
        "432",
    
        "447",
        "441",
        "442",
    
        "457",
        "451",
        "452",
    
        "4100",
        "4101",
        "4102",
    
        "467",
        "461",
        "462",
    
        "477",
        "471",
        "472",
    
        "4189",
        "4181",
        "4182",
    
    
        "497",
        "491",
        "492",
    
        "4A7",
        "4A1",
        "4A2",
    
        "40-41-0",
        "40-41-1",
        "40-41-2",
        "45-46-0",
        "45-46-1",
        "45-46-2",
    
        "49-4B-0",
        "49-4B-1",
        "40-41-0",
        "40-41-1",
        "40-41-2",
    
        "4289",
        "4281",
        "4282",
    
        "4C7",
        "4C1",
        "4C2",
    
        "4D7",
        "4D1",
        "4D2",
    
        "4F7",
        "4F1",
        "4F2",
    
    
        "4G7",
        "4G1",
        "4G2",
    
        "4H7",
        "4H1",
        "4H2",
    
        "4J7",
        "4J1",
        "4J2",
    
        "4K7",
        "4K1",
        "4K2",
    
        "4L7",
        "4L1",
        "4L2",
    
        "4279",
        "4271",
        "4272",
    
        "41-42-0",
        "41-42-1",
        " 41-42-2",
        "46-47-0",
        "46-47-1",
        "46-47-2",
    
        "4N7",
        "4N1",
        "4N2",
    
        "4P7",
        "4P1",
        "4P2",
    
        "4Q7",
        "4Q1",
        "4Q2",
    
        "4200",
        "4201",
        "4202",
    
        "4Q7",
        "4Q1",
        "4Q2",
    
        "4S7",
        "4S1",
        "4S2",
    
        "4T7",
        "4T1",
        "4T2",
    
    
        "4U7",
        "4U1",
        "4U2",
    
        "4379",
        "4371",
        "4372",
    
        "42-43-0",
        "42-43-1",
        "42-43-2",
        "47-48-0",
        "47-48-1",
        "47-48-2",
    
        "4W7",
        "4W1",
        "4W2",
    
        "4X7",
        "4X1",
        "4X2",
    
        "4Y7",
        "4Y1",
        "4Y2",
    
            
        "4Z7",
        "4Z1",
        "4Z2",
    
        "4가7",
        "4가1",
        "4가2"
        
        "4나7",
        "4나1",
        "4나2",
        
        "4다7",
        "4다1",
        "4다2",
    
        "4라7",
        "4라1",
        "4라2",
    
        "4479",
        "4471",
        "4472",
    
        "4마7",
        "4마1",
        "4마2"
        """: []
    },
    "shape": []
}


class Station_1:
    def __init__(self, ):
        # self.config = config
        self.point = station
        self.direction = [True, False, True, False, True, True, True]  # 1 - 7 변전소 방향

    def config_update(self, old, new):
        self.point[old] = new

    def station_update(self, station_number, point, new):
        self.station[station_number][point] = new


class Station_2(Station_1):
    def __init__(self):
        super().__init__()


station_info = {1: Station_1(),
                2: Station_2()
                }

