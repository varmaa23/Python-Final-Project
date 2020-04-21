# Name: Aishwarya Varma
# Date: 3/13/2020
# Purpose: CS 111 Final Project

from pgl import GImage

def add_loser(gw):
        loser_img = GImage("loser.png", 525, 300)
        gw.add(loser_img)
        
def add_winner(gw):
    winner_img = GImage("winner.png", 560, 300)
    gw.add(winner_img)