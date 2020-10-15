import pickle
import os
from configparser import ConfigParser

def parse_tuple(string):
    try:
        s = eval(string)
        if type(s) == tuple:
            return s
        return
    except:
        return


parser = ConfigParser()
parser.read("config.ini")
deffont = parse_tuple(parser['DEFAULT']['font'])
left = parser['Movement']['left']
right = parser['Movement']['right']
up = parser['Movement']['up']
down = parser['Movement']['down']


