# Name: Aishwarya Varma
# Date: 3/13/2020
# Purpose: CS 111 Final Project

from pgl import GImage, GWindow
from constants import *
import random

class Character():

    def __init__(self):
        self.xpos = 400
        self.ypos = GWINDOW_HEIGHT - 300

        image = "isaacnewton.png"
        self.character = GImage(image, self.xpos, self.ypos)


