# setup_test.py
import pygame
import re
import os
import sys
import json
import configparser

# json
with open('data/test.json') as data:
    config = json.load(data)

print(config["color"]["conn"])
# print(tuple(map(int, config["color"]["tuple"].split(","))))   # string to tuple ex) "40,30,50"
print(tuple(config["color"]["tuple"]))  # list to tuple


# ini
config = configparser.ConfigParser()
config.read('data/test.ini')

secret_key = config['DEFAULT']['SECRET_KEY']    # 'secret-key-of-myapp'
ci_hook_url = config['CI']['HOOK_URL']  # 'web-hooking-url-from-ci-service'

print(secret_key)
print(ci_hook_url)
