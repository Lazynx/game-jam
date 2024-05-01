import pygame
import sys
from pygame.locals import *
import random
import time

pygame.init()

def gaxgame_game(screen):
    FPS = 60
    FramePerSec = pygame.time.Clock()
    backdround_music = pygame.mixer.Sound('image/gaxgame_music.mp3')
    backdround_music.play(-1)

    blaster_sound = pygame.mixer.Sound('image/blaster.mp3')

    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    SPEED = 5
    global SCORE
    SCORE = 0
    COLLECT = 0
    font = pygame.font.Font("PIXY.ttf", 60)
    font_small = pygame.font.Font("PIXY.ttf", 40)

    border_image = pygame.image.load('image/border.png')
    border_image = pygame.transform.scale(border_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    background = pygame.image.load('image/galaxy.png')
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    instructions_background = pygame.image.load('image/instructions.png')
    instructions_background = pygame.transform.scale(instructions_background, (SCREEN_WIDTH, SCREEN_HEIGHT))


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
                self.rect.right = SCREEN_WIDTH
                self.rect.centery = random.randint(40, SCREEN_HEIGHT - 40)

    class Plane(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('image/plane.png')
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]*2, self.image.get_size()[1]*2))
            self.rect = self.image.get_rect()
            self.rect.center = (100, 300)

        def update(self):
            pressed_keys = pygame.key.get_pressed()
            if self.rect.top > 0 and (pressed_keys[K_UP] or pressed_keys[K_w]):
                self.rect.move_ip(0, -8)
            if self.rect.bottom < SCREEN_HEIGHT and (pressed_keys[K_DOWN] or pressed_keys[K_s]):
                self.rect.move_ip(0, 8)

    class Astronaut(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('image/astronaut.png')
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0]*2, self.image.get_size()[1]*2))
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

    god_mode = True
    
    instructions_time = 3000
    instructions_time0 = 0

    while run:
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.5
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    blaster_sound.play()
                    new_bullet = Bullet(P1.rect.centerx,P1.rect.centery)
                    bullets.add(new_bullet)
            elif god_mode and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    blaster_sound.play()
                    new_bullet = Bullet(P1.rect.centerx,P1.rect.centery)
                    bullets.add(new_bullet)
        
        
        screen.blit(background,(0,0))
        scores = font_small.render("time: " + str(SCORE//1000) + " sec", True, (255,255,255))
        screen.blit(scores, (70, 50))
        collects = font_small.render(str(COLLECT), True, (255, 255,0))
        screen.blit(collects, (SCREEN_WIDTH - collects.get_size()[0] - 65, collects.get_size()[1]//2 + 5))
        screen.blit(astro_image,(SCREEN_WIDTH - astro_image.get_size()[0] - 100, astro_image.get_size()[1] ))

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
            pygame.mixer.stop()
            pygame.mixer.Sound('image/loseSound.mp3').play()
            time.sleep(0.2)
            screen.fill((255, 0, 0))
            screen.blit(loser,(SCREEN_WIDTH//2 - loser.get_size()[0]//2, SCREEN_HEIGHT//2 - loser.get_size()[0]//2))
            screen.blit(border_image, border_image.get_rect())
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(4)
            return
       
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

        if COLLECT == 15:
            successful_pass = True
        
        if successful_pass:
            pygame.mixer.stop()
            pygame.mixer.Sound('image/winSound.mp3').play()
            screen.fill((255,255,255))
            screen.blit(winner,(SCREEN_WIDTH//2 - winner.get_size()[0]//2, SCREEN_HEIGHT//2 - winner.get_size()[0]//2))
            screen.blit(border_image, border_image.get_rect())
            pygame.display.update()
            time.sleep(5)
            return
     
        screen.blit(border_image, border_image.get_rect())
        pygame.display.flip()
        SCORE += 14
        FramePerSec.tick(FPS)
