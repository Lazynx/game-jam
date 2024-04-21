import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
SPEED = 5
SCORE = 0
COLLECT = 0
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont('Verdana', 40)

background = pygame.image.load('image/galaxy.png')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galaxy')

successful_pass = False
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('image/asteroid.png')
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, random.randint(40, SCREEN_HEIGHT - 40))  

    def move(self):
        global SCORE
        self.rect.move_ip(-SPEED, 0) 
        if self.rect.right < 0:  
            SCORE += 1
            self.rect.right = SCREEN_WIDTH  
            self.rect.centery = random.randint(40, SCREEN_HEIGHT - 40)  

class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('image/plane.png')
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

class Astronaut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('image/astronaut.png')
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, random.randint(40, SCREEN_HEIGHT - 40)) 

    def move(self):
        global COLLECT
        self.rect.move_ip(-SPEED, 0)  
        if self.rect.right < 0:  
            self.rect.right = SCREEN_WIDTH 
            self.rect.centery = random.randint(40, SCREEN_HEIGHT - 40) 

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xx,yy):
        super().__init__()
        self.image = pygame.image.load('image/bullet.png')  
        self.rect = self.image.get_rect()
        self.rect.centerx = xx
        self.rect.centery = yy
        self.speed = 10 

    def update(self):
        self.rect.x += self.speed  

P1 = Plane()
M2 = Astronaut()
asteroids = pygame.sprite.Group()
asteroid = Asteroid()
asteroids.add(asteroid)
bullets = pygame.sprite.Group()
astronauts = pygame.sprite.Group()
astronauts.add(M2)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(asteroids)
all_sprites.add(M2)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)
run = True

astro_image = pygame.image.load('image/astronaut.png')
winner = pygame.image.load('image/winner.png')
loser = pygame.image.load('image/loser.png')

level_up = 1
to_begin = 0

god_mode = False


while run:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                god_mode = True
        elif god_mode and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                 new_bullet = Bullet(P1.rect.centerx,P1.rect.centery)  
                 bullets.add(new_bullet)  
           
    screen.blit(background,(0,0))
    scores = font_small.render(str(SCORE), True, (255,255,255))
    screen.blit(scores, (10,10))
    collects = font_small.render(str(COLLECT), True, (255, 255,0))
    screen.blit(collects, (900, 10))
    screen.blit(astro_image,(930,10))

    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)
        if pygame.sprite.spritecollideany(bullet, asteroids):
            pygame.mixer.Sound('image/hitSound.mp3').play()
            bullet.kill()  # Удаляем пулю
            for asteroid in pygame.sprite.spritecollide(bullet, asteroids, True):
                asteroid.rect.top = 0
                asteroid.rect.center = (random.randint(40, SCREEN_HEIGHT - 40), 0)
                new_asteroid = Asteroid()
                asteroids.add(new_asteroid)
                all_sprites.add(new_asteroid)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    
    for asteroid in asteroids:
        asteroid.move()
    
    for astronaut in astronauts:
        astronaut.move()

    P1.update()  

    if pygame.sprite.spritecollideany(P1, asteroids):
        pygame.mixer.Sound('image/loseSound.mp3').play()
        time.sleep(0.2)
        screen.fill((255, 0, 0))
        screen.blit(loser,(410,170))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(4)
        pygame.quit()
        sys.exit()
   
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    
    if pygame.sprite.spritecollideany(P1,astronauts):
        pygame.mixer.Sound('image/takingSound.mp3').play()
        COLLECT+=1
        for astr in pygame.sprite.spritecollide(P1,astronauts,True):
            astr.rect.top = 0
            astr.rect.center = (random.randint(10,SCREEN_WIDTH-10),0)
            new_astr = Astronaut()
            astronauts.add(new_astr)
            all_sprites.add(new_astr)
        to_begin +=1
    
    if to_begin == level_up:
        SPEED +=1
        to_begin = 0

    if COLLECT == 10:
        successful_pass = True
    
    if successful_pass:
        pygame.mixer.Sound('image/winSound.mp3').play()
        screen.fill((255,255,255))
        screen.blit(winner,(230,60))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
 
    x = pygame.image.load('image/X.png')
    screen.blit(x,(927,23))
    pygame.display.flip()
    FramePerSec.tick(FPS)
