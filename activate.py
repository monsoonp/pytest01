import os
# import sys

number = input("substation number(1~ ) : ")
script = "./shmon {0} -n | python3 oneline.py".format(number)
os.system(script)
