# Name: Aishwarya Varma
# Date: 3/13/2020
# Purpose: CS 111 Final Project

from pgl import GWindow, GTimer, GImage, GRect, GOval, GLabel
from dataclasses import dataclass
from fallingobject import Falling_Object
from worm import Worm
from constants import *
from character import Character
import random
import math
from utilities import *
from addgraphics import *

# Below are instance variables of the class game_state. 
@dataclass()
class GameState:
    xvel = 0
    apple_yvel: float = 5
    update_timer: GTimer = None
    apple_timer: GTimer = None
    worm_timer: GTimer = None
    worm_yvel = 10

# Starts the round when the mouse is clicked. Also starts the timers that create the apples and the worms, updating
# ther movement. 
def start_round(gw, game_state, update_fn, update_fn_two, update_fn_three):
    if game_state.update_timer:
        game_state.update_timer.stop()
    if game_state.apple_timer:
        game_state.apple_timer.stop()
    if game_state.worm_timer:
        game_state.worm_timer.stop()
    
    instructions = GImage("instructions.png", 400, 270)
    gw.add(instructions)
    def onclick(e):
        game_state.update_timer = gw.setInterval(update_fn, TIME_STEP)
        game_state.apple_timer = gw.setInterval(update_fn_two, TIME_STEP_TWO)
        game_state.worm_timer = gw.setInterval(update_fn_three, TIME_STEP_THREE)
        gw.eventManager.clickListeners.pop()
        gw.remove(instructions)
    gw.addEventListener("click", onclick)

# When called, this function ends the game.
def end_game(game_state):
    if game_state.update_timer:
        game_state.update_timer.stop()
    if game_state.apple_timer:
        game_state.apple_timer.stop()
    if game_state.worm_timer:
        game_state.worm_timer.stop()

# Main code for the game
def game():
    gw = GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT)
    game_state = GameState()
    apples_collected = []
    objects_lost = []

    background = GImage("background.png", 0, 0)
    gw.add(background)

    scoreboard = GRect(GWINDOW_WIDTH - SB_WIDTH, 550, SB_WIDTH, SB_HEIGHT)
    scoreboard.setFilled(True)
    scoreboard.setColor("White")
    gw.add(scoreboard)

    collected_label = create_centered_label("Apples collected: ", GWINDOW_WIDTH - 160, 590, SB_FONT)
    gw.add(collected_label)
    collected_num_label = create_centered_label(str(len(apples_collected)), GWINDOW_WIDTH - 30, 590, SB_FONT)
    gw.add(collected_num_label)  

    lost_label = create_centered_label("Apples lost: ", GWINDOW_WIDTH - 195, 650, SB_FONT)
    gw.add(lost_label)
    lost_num_label = create_centered_label(str(len(objects_lost)), GWINDOW_WIDTH - 30, 650, SB_FONT)
    gw.add(lost_num_label)

    c = Character()
    isaac_newton = c.character
    gw.add(isaac_newton)
    
    # This function adds the apples to the game, according to the timestep provided in the list of constants. Apples 
    # added to a list and removed when they are either collected or they hit the ground.
    apples = []
    def add_apples():
        xpos = random.randint(0 + APPLE_WIDTH, GWINDOW_WIDTH - APPLE_WIDTH)
        f = Falling_Object(xpos)
        apple = f.apple
        gw.add(apple)
        apples.append(apple)

    # This function adds worms to the window. Worms will appear after some duration of the game (i.e. 5 apples 
    # have been collected). They appear according to the third timestep provided in constants.py.
    worms = []
    def add_worms():
        if len(apples_collected) > 5:
            xpos = random.randint(0 + WORM_WIDTH, GWINDOW_WIDTH - WORM_WIDTH) 
            w = Worm(xpos)
            worm = w.worm
            gw.add(worm)
            worms.append(worm)

    # This function increases the apples' y velocity every time 3 apples are collected so that the game becomes harder
    # as the player progresses. 
    def change_yvel():
        if len(apples_collected) % 3 == 0 and len(apples_collected) != 0:
            game_state.apple_yvel += 0.005
        return game_state.apple_yvel

    # This is the most important function. It makes both the apple and the worm objects move. It handles collisions 
    # between isaac_newton and objects, and deals with them accordingly. This function is called every timestep (constants)
    # If you lose < 3 apples and collect 25 without collecting a worm, you win the game!
    def update_objects(): 
        collected_num_label.setLabel(len(apples_collected))

        for apple in apples:
            apple_x_now = apple.getX() 
            apple_y_now = apple.getY() + APPLE_HEIGHT

            isaac_x = isaac_newton.getX()
            isaac_y = isaac_newton.getY()
            if isaac_x <= apple_x_now <= (isaac_x + ISAAC_WIDTH) and isaac_y <= apple_y_now <= (isaac_y + ISAAC_HEIGHT):
                gw.remove(apple)
                apples.remove(apple)
                apples_collected.append(apple)

            if apple_y_now >= GWINDOW_HEIGHT:
                objects_lost.append(apple)
                lost_num_label.setLabel(len(objects_lost))
                gw.remove(apple)
                apples.remove(apple)
                if len(objects_lost) >= 3:
                    end_game(game_state)
                    add_loser(gw)

            if len(apples_collected) == 25:
                collected_num_label.setLabel(len(apples_collected))
                end_game(game_state)
                add_winner(gw)

            game_state.apple_yvel = change_yvel()
            apple.move(game_state.xvel, game_state.apple_yvel)
        
        for worm in worms:
            worm_x_now = worm.getX()
            worm_y_now = worm.getY() + WORM_HEIGHT

            isaac_x = isaac_newton.getX()
            isaac_y = isaac_newton.getY()
            if isaac_x <= worm_x_now <= (isaac_x + ISAAC_WIDTH) and isaac_y <= worm_y_now <= (isaac_y + ISAAC_HEIGHT):
                gw.remove(worm)
                worms.remove(worm)
                end_game(game_state)
                add_loser(gw)

            if worm_y_now >= GWINDOW_HEIGHT:
                gw.remove(worm)
                worms.remove(worm)
        
            worm.move(game_state.xvel, game_state.worm_yvel)

    # This function handles the key movement for isaac_newton. If the player touches the left arrow, isaac will move left.
    # This is the same for the right arrow. 
    def key_action(event):
        if event.key == "<LEFT>":
            isaac_newton.move(-ISAAC_XVEL, ISAAC_YVEL)          
        elif event.key == "<RIGHT>":
            isaac_newton.move(ISAAC_XVEL, ISAAC_YVEL)
        
        if isaac_newton.getX() >= (GWINDOW_WIDTH - ISAAC_WIDTH):
            isaac_newton.setLocation(GWINDOW_WIDTH - ISAAC_WIDTH, Character().ypos)
            gw.addEventListener("key", key_action)
        
        if isaac_newton.getX() <= 0:
            isaac_newton.setLocation(0, Character().ypos)
            gw.addEventListener("key", key_action)

    # Adds key event listener for the arrows and starts the round calling the appropriate functions with the right 
    # timesteps.
    gw.addEventListener("key", key_action)
    start_round(gw, game_state, update_objects, add_apples, add_worms)

game()

    




