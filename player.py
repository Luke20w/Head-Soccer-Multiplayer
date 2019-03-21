import pygame
import time
from pygame.locals import K_t, K_RETURN


class Player():
    def __init__(self, x, screenwidth, screenheight):
        # Variables
        self.screenwidth = screenwidth
        self.screenheight = screenheight
        self.radius = 30
        self.x = x
        self.y = screenheight / 2
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = -0.7  # (Gravity)
        self.speed = 7
        self.jump = 9
        self.friction_value = 0.7
        self.floor = self.screenheight * 0.82

        # Chat Stuff
        self.chatActive = False
        self.msg = ''
        self.pastMsgs = []

    def draw(self, screen):
        screen.blit(pygame.transform.scale(pygame.image.load('soccer_ball.png'), (self.radius * 2, self.radius * 2)), (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.vx = -self.speed

        if keys[pygame.K_RIGHT]:
            self.vx = self.speed

        if keys[pygame.K_UP]:
            if self.y + self.radius * 2 >= self.floor:
                self.vy = -self.jump

        # Chat On/Off
        if keys[K_RETURN] and self.chatActive and len(self.msg) > 1:
            self.pastMsgs.append([self.msg, time.time()])
            self.chatActive = False
            self.msg = ''
        if keys[K_t] and not self.chatActive:
            self.chatActive = True

        self.update()

    def friction(self):
        if self.vx > 0:
            self.ax = -self.friction_value
        if self.vx < 0:
            self.ax = self.friction_value
        if abs(self.vx) < 3:
            self.vx = 0
            self.ax = 0

    def collide(self):
        # Collide with floor
        if self.y + self.radius * 2 > self.floor:
            self.y = self.floor - self.radius * 2
        # Collide with wall
        if self.x + self.radius * 2 > self.screenwidth:
            self.x = self.screenwidth - self.radius * 2
        if self.x < 0:
            self.x = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= self.ay
        self.vx += self.ax

        self.friction()

        self.collide()


