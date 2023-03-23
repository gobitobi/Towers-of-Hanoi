import pygame as py

class Disk():
    
    def __init__(self, screen, width, height, y_pos, value):
        self.screen = screen
        self.width = width
        self.height = height
        self.y_pos = y_pos
        self.value = value
        self.rect = py.Rect(0, 0, self.width, self.height)
        self.rect.midtop = (120, self.y_pos)
        self.value = value
        self.tower = 0
        
    def draw(self):
        py.draw.rect(self.screen, 'blue', self.rect)
