import pygame, sys, os
from pytmx.util_pygame import load_pygame


class Map:
    def __init__(self, data):
        self.tmx_data = data
