# Name: Aishwarya Varma
# Date: 3/13/2020
# Purpose: CS 111 Final Project

from pgl import GImage
from constants import *
import random

class Worm():

    def __init__(self, xpos):
        self.xpos = xpos
        self.ypos = 0

        image = "uglyworm.png"
        self.worm = GImage(image, self.xpos, self.ypos)

