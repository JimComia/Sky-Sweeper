import pygame
from pygame import mixer
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 780, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Sweeper")


astteroid1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "aster1.png")), (150,150))

plane = pygame.transform.scale(pygame.image.load(os.path.join("assets", "plane1.png")), (100,100))

BG1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background1.png")), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background2.png")), (WIDTH, HEIGHT))

mixer.init()
bulletSound = pygame.mixer.Sound('assets/bullet.mp3')
ed = pygame.mixer.Sound('assets/enemy1_down.mp3')
gmover = pygame.mixer.Sound('assets/gameover.mp3')

pygame.mixer.music.load('assets/game_music.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


class Ship:
    COOLDOWN = 25
    

    def __init__(self, x, y, health=100, score=0):
        self.x = x
        self.y = y
        self.health = health
        self.score = score
        self.ship_img = None
        self.bullts_img = None
        self.bulltss = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullts in self.bulltss:
            bullts.draw(window)

    def move_bulltss(self, vel, obj):
        self.cooldown()
        for bullts in self.bulltss:
            bullts.move(vel)
            if bullts.off_screen(HEIGHT):
                self.bulltss.remove(bullts)
            elif bullts.collision(obj):
                obj.health -= 10
                self.bulltss.remove(bullts)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        
        if self.cool_down_counter == 0:
            bulletSound.play()
            bullts = Bullts(self.x, self.y, self.bullts_img)
            self.bulltss.append(bullts)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
     
    
 
