import pygame
from math import *


class Ball():
    def __init__(self, x, screenwidth, screenheight):
        # Variables
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.radius = 15
        self.x = x
        self.y = screenheight / 2
        self.vx = -5
        self.vy = 0
        self.ax = 0
        self.ay = -0.7  # (Gravity)
        self.bounce = 0.6
        self.floor = self.screenheight * 0.82

    def draw(self, screen):
        screen.blit(pygame.transform.scale(pygame.image.load('soccer_ball.png'), (self.radius * 2, self.radius * 2)), (self.x, self.y))

    def collide(self):
        # Collide with floor
        if self.y + self.radius * 2 > self.floor:
            self.y = self.floor - self.radius * 2
            self.vy *= -self.bounce
        # Collide with wall
        if self.x + self.radius * 2 > self.screenwidth:
            self.x = self.screenwidth - self.radius * 2
            self.vx *= -self.bounce
        if self.x < 0:
            self.x = 0
            self.vx *= -self.bounce

    def collide_player(self, player_x, player_y, player_radius):
        dx = (self.x + self.radius) - (player_x + player_radius)
        dy = -((self.y + self.radius) - (player_y + player_radius))
        angle = atan2(dy, dx)
        dist = sqrt(dx ** 2 + dy ** 2)
        if dist <= (self.radius + player_radius):
            self.vx = 10 * cos(angle)
            self.vy = -10 * sin(angle)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= self.ay
        self.vx += self.ax

        self.collide()


