# Name: Aishwarya Varma
# Date: 3/13/2020
# Purpose: CS 111 Final Project

# File: utilities.py

"""
This module defines a library of four graphics functions
(create_filled_rect, create_filled_circle, create_centered_label, 
and center_label) that are used in several different applications.
Each of these functions is described in its docstring comment.
"""

from pgl import GRect, GOval, GLabel

def create_filled_rect(x, y, width, height, fill="Black", border=None):
    """
    Creates a GRect filled with the specified fill color.  If border is
    specified, the border appears in that color.
    """
    rect = GRect(x - width / 2, y - height / 2, width, height)
    rect.setFilled(True)
    if border is None:
        rect.setColor(fill)
    else:
        rect.setColor(border)
        rect.setFillColor(fill)
    return rect

def create_filled_circle(x, y, r, fill="Black", border=None):
    """
    Creates a circle of radius r centered at the point (x, y) with the
    specified fill color.  If border is specified, the border appears
    in that color.
    """
    circle = GOval(x - r, y - r, 2 * r, 2 * r)
    circle.setFilled(True)
    if border is None:
        circle.setColor(fill)
    else:
        circle.setColor(border)
        circle.setFillColor(fill)
    return circle

def create_centered_label(text, x, y, font=None):
    """
    Creates a new GLabel centered at the point (x, y) in both the
    horizontal and vertical directions.  If font is specified, it
    is used to set the font of the label.
    """
    label = GLabel(text)
    if font is not None:
        label.setFont(font)
    center_label(label, x, y)
    return label

def center_label(label, x, y):
    """
    Centers the GLabel label at the point (x, y) in both the horizontal 
    and vertical directions. Useful for re-centering a label when its
    text changes.
    """
    label.setLocation(x - label.getWidth() / 2, y + label.getAscent() / 2)