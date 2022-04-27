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

