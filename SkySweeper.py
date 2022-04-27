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
