import sys
import json

args = sys.argv
st = {"fcode": 4, "group": 5, "variation": 1, "count": 1, "result": [
    {"point": {"pr": 0, "gr": 0, "t": 1, "p": int(args[1])}, "value": 0, "A\/E Code": "CCOSP",
     "TLQ": {"T": "", "L": "", "Q": ""}, "update time": "1585025153.495166", "scan time": "1585025604.240000",
     "A\/E Text": " C..  Pgm Cmd COS >占쏙옙占쏙옙 by nexegop"}], "error": 0}

st2 = '"{"fcode": 4, "group": 5, "variation": 1, "count": 1, "result": [{"point": {"pr": 0, "gr": 0, "t": 1, "p": argument, "value": 0, "A\/E Code": "CCOSP","TLQ": {"T": "", "L": "", "Q": ""}, "update time": "1585025153.495166", "scan time": "1585025604.240000","A\/E Text": " C..  Pgm Cmd COS >占쏙옙占쏙옙 by nexegop"}], "error": 0}"'

if __name__ == "__main__":
    print(st2.replace("argument",args[1]))
    # print('%s' %st)
