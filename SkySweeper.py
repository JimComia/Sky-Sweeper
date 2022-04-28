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

bullets = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bullet.png")), (30,30))

BG1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background1.png")), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background2.png")), (WIDTH, HEIGHT))

mixer.init()
bulletSound = pygame.mixer.Sound('assets/bullet.mp3')
ed = pygame.mixer.Sound('assets/enemy1_down.mp3')
gmover = pygame.mixer.Sound('assets/gameover.mp3')

pygame.mixer.music.load('assets/game_music.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

class Bullts:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


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
    
class Player(Ship):
    
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = plane
        self.bullts_img = bullets
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_bulltss(self, vel, objs):
        self.cooldown()
        for bullts in self.bulltss:
            bullts.move(vel)
            if bullts.off_screen(HEIGHT):
                self.bulltss.remove(bullts)
            else:
                for obj in objs:
                    if bullts.collision(obj):
                        ed.play()
                        self.score += 100
                        objs.remove(obj)
                        
                        if bullts in self.bulltss:
                            self.bulltss.remove(bullts)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))    
    
     
class Enemy(Ship):
    
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = astteroid1
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    bullts_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG1, (0,0))
        # draw text
        #lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))
        score_label = main_font.render(f"Score: {player.score}", 1, (255,255,255))

        WIN.blit(score_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Game Over!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            fScore_label = lost_font.render(f"Score: {player.score}", 1, (255,255,255))
            WIN.blit(fScore_label, (WIDTH/2 - fScore_label.get_width()/2, 450))
            gmover.play()

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        # for buttons
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] or keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            if collide(enemy, player):
                player.health -= 10
                ed.play()
                enemies.remove(enemy)
                player.score += 50
            elif enemy.y + enemy.get_height() > HEIGHT:
                player.health -= 10
                ed.play()
                enemies.remove(enemy)

        player.move_bulltss(-bullts_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.blit(BG2, (0, 0))
        title_label = title_font.render("Click to Start", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
 
