"""
    @Author: Dilara Demirhan
    @Date: 20 May 2020
"""

import pygame
from os import path
from time import sleep, time
import math
import sys

pygame.init()
pygame.mixer.init()

WIDTH = 700
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch The Coin")
FPS = 60
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255,255,255)


walkLeft = [pygame.image.load('images/sol1.png'), pygame.image.load('images/sol2.png'), pygame.image.load('images/sol3.png'),
            pygame.image.load('images/sol4.png')]
walkRight = [pygame.image.load('images/s1.png'), pygame.image.load('images/s2.png'), pygame.image.load('images/s3.png'),
             pygame.image.load('images/s4.png')]
walkUp = [pygame.image.load('images/u1.png'), pygame.image.load('images/u2.png'), pygame.image.load('images/u3.png'),
          pygame.image.load('images/u4.png')]
walkDown = [pygame.image.load('images/d1.png'), pygame.image.load('images/d2.png'), pygame.image.load('images/d3.png'),
            pygame.image.load('images/d4.png')]
yellow_m = [pygame.image.load('images/frame-1.png'), pygame.image.load('images/frame-2.png'), pygame.image.load('images/frame-3.png'),
            pygame.image.load('images/frame-4.png'), pygame.image.load('images/frame-5.png'), pygame.image.load('images/frame-6.png'),
            pygame.image.load('images/frame-7.png'), pygame.image.load('images/frame-8.png')]
yellow_mL = [pygame.image.load('images/y1.png'), pygame.image.load('images/y2.png'), pygame.image.load('images/y3.png'),
            pygame.image.load('images/y4.png'), pygame.image.load('images/y5.png'), pygame.image.load('images/y6.png'),
            pygame.image.load('images/y7.png'), pygame.image.load('images/y8.png')]
green_m = [pygame.image.load('images/g1.png'), pygame.image.load('images/g2.png'), pygame.image.load('images/g3.png'),
           pygame.image.load('images/g4.png')]
coins = [pygame.image.load('images/c1.png'), pygame.image.load('images/c2.png'), pygame.image.load('images/c3.png'),
         pygame.image.load('images/c4.png'), pygame.image.load('images/c5.png'), pygame.image.load('images/c6.png'),
         pygame.image.load('images/c7.png'), pygame.image.load('images/c8.png')]
bat = [pygame.image.load('images/b1.png'), pygame.image.load('images/b2.png'), pygame.image.load('images/b3.png'),
       pygame.image.load('images/b4.png'), pygame.image.load('images/b5.png'), pygame.image.load('images/b6.png'),
       pygame.image.load('images/b7.png'), pygame.image.load('images/b8.png')]
blue_bat = [pygame.image.load('images/bat_1.png'), pygame.image.load('images/bat_2.png')]
background = pygame.transform.scale(pygame.image.load('images/bg.png'), (700, 700)).convert()
background_rect = background.get_rect()

blood = []
for i in range(6):
    img = pygame.image.load('images/blood' + str(i) + ".jpg")
    img = pygame.transform.scale(img, (65, 65))
    img.set_colorkey(WHITE)
    blood.append(img)

snd_dir = path.join(path.dirname(__file__),'snd')
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
coin_sound = pygame.mixer.Sound(path.join(snd_dir, 'take_coin.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'music.mp3'))
pygame.mixer.music.set_volume(0.4)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('images/d1.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.radius = 12
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.rect.x, self.rect.y = 20, 300
        self.vel = 5

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 200:
            self.hidden = False
            self.rect.center = (20, 300)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.vel
            self.image = pygame.transform.scale(walkRight[self.rect.x % 4], (50, 50))
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.vel
            self.image = pygame.transform.scale(walkLeft[self.rect.x % 4], (50, 50))
        if keys[pygame.K_UP]:
            self.rect.y -= self.vel
            self.image = pygame.transform.scale(walkUp[self.rect.y % 4], (50, 50))
        if keys[pygame.K_DOWN]:
            self.rect.y += self.vel
            self.image = pygame.transform.scale(walkDown[self.rect.y % 4], (50, 50))
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom - self.image.get_width() < 0:
            self.rect.bottom = self.image.get_width()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (20, 300)


class Monster(pygame.sprite.Sprite):
    def __init__(self, velx, vely, pic, x, y, boundary):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pic[0], (35, 35))
        self.rect = self.image.get_rect()
        self.radius = 12
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.velx = velx
        self.vely = vely
        self.pic = pic
        self.boundary = boundary

    def update(self):
        self.rect.x += self.velx
        self.rect.y += self.vely
        if self.vely == 0:
            self.image = pygame.transform.scale(self.pic[self.rect.x % len(self.pic)], (45, 35))
        elif self.velx == 0:
            self.image = pygame.transform.scale(self.pic[self.rect.y % len(self.pic)], (45, 35))

        if self.velx < 0 and self.rect.x <= self.boundary:
            self.rect.x = self.x
        if self.velx > 0 and self.rect.x >= self.boundary:
            self.rect.x = self.x
        if self.velx == 0 and self.vely < 0 and self.rect.y <= self.boundary:
            self.rect.y = self.y
        if self.velx == 0 and self.vely > 0 and self.rect.y >= self.boundary:
            self.rect.y = self.y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = coins[math.floor(time() * 7) % 8]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (750, 750)


class Blood(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = blood[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 6:
                self.kill()
            else:
                center = self.rect.center
                self.image = blood[self.frame % 6]
                self.rect = self.image.get_rect()
                self.rect.center = center


all_sprites = pygame.sprite.Group()
all_sprites2 = pygame.sprite.Group()
all_sprites3 = pygame.sprite.Group()
all_sprites4 = pygame.sprite.Group()

level1 = True
level2 = False
level3 = False
level4 = False

def is_coin_taken(Coin):
    if player.rect.x >= Coin.rect.x - 20 and player.rect.x <= Coin.rect.x + 10 and player.rect.y >= Coin.rect.y - 30 \
        and player.rect.y <= Coin.rect.y + 10:
        return True


def pass_level():
    for c in level_coins:
        if not c.hidden:
            return False
    return player.rect.x > 607

player_mini_img = pygame.transform.scale(pygame.image.load('images/d1.png'), (25, 25))

chiller = pygame.font.match_font('Chiller')
cooper = pygame.font.match_font('Cooper Black')
def draw_text(font_name, surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_screen():
    screen.blit(background, background_rect)
    if level2:
        draw_text(cooper, screen, "Level 2", 44, WIDTH / 2, HEIGHT / 4 + 30)
    if level3:
        draw_text(cooper, screen, "Level 3", 44, WIDTH / 2, HEIGHT / 4 + 30)
    if level4 and not finished:
        draw_text(cooper, screen, "Level 4", 44, WIDTH / 2, HEIGHT / 4 + 30)
    if(player.lives == 0):
        draw_text(cooper, screen, "GAME OVER", 64, WIDTH / 2, HEIGHT / 4)
    elif finished:
        draw_text(cooper, screen, "CONGRATULATIONS!", 60, WIDTH / 2, HEIGHT / 4)
    else:
        if level1:
            draw_text(cooper, screen, "CATCH THE COIN!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(cooper, screen, "Press space to begin", 22,
              WIDTH / 2, HEIGHT / 2)
    if level1 and player.lives != 0 and not finished:
        draw_text(cooper, screen, "Arrow keys move", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def all_levels():
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, background_rect)
    draw_text(cooper, screen, "Level " + str(level), 30, WIDTH / 2, 10)
    for i in range(player.lives):
        screen.blit(player_mini_img, (600 + 30 * i, 10))

    hits = pygame.sprite.spritecollide(player, monsters, False, pygame.sprite.collide_circle)
    if hits:
        hit_sound.play()
        death_blood = Blood(hits[0].rect.center, 'player')
        all_sprites.add(death_blood)
        if level2:
            all_sprites2.add(death_blood)
        if level3:
            all_sprites3.add(death_blood)
        if level4:
            all_sprites3.add(death_blood)
        player.hide()
        player.lives -= 1


pygame.mixer.music.play(loops=-1)

player = Player()
finished = False

while 1:
    level_coins = []
    game_over = True
    while level1:
        if game_over:
            show_screen()
            game_over = False
            finished = False
            all_sprites = pygame.sprite.Group()
            monster = Monster(-10, 0, green_m, 585, 340, 60)
            monster2 = Monster(-10, 0, green_m, 585, 340, 60)
            monsters = [monster, monster2]
            all_sprites.add(monsters)
            if player.lives == 0:
                player = Player()
            player.lives = 3
            player.rect.x, player.rect.y = 20, 300
            all_sprites.add(player)
            c = Coin(350, 350)
            all_sprites.add(c)
            level_coins.append(c)
        level = 1
        all_levels()
        all_sprites.update()

        c.image = coins[math.floor(time() * 7) % 8]
        if is_coin_taken(c):
            coin_sound.play()
            c.hide()
        if player.lives == 0:
            game_over = True

        all_sprites.draw(screen)
        if pass_level():
            level1 = False
            level2 = True
        pygame.display.flip()


    game_over = True
    c = Coin(350, 350)

    while level2:
        if game_over:
            show_screen()
            game_over = False
            all_sprites2 = pygame.sprite.Group()
            monster = Monster(-10, 0, yellow_mL, 595, 395, 60)
            monster2 = Monster(10, 0, yellow_m, 60, 275, 590)
            monster3 = Monster(-5, 0, green_m, 585, 340, 60)
            monsters = [monster, monster2, monster3]
            all_sprites2.add(monsters)
            if player.lives == 0:
                player = Player()
            player.rect.x, player.rect.y = 20, 300
            all_sprites2.add(player)
            c = Coin(350, 350)
            all_sprites2.add(c)
            level_coins.append(c)

        level = 2
        all_levels()
        all_sprites2.update()

        c.image = coins[math.floor(time() * 7) % 8]
        if is_coin_taken(c):
            coin_sound.play()
            c.hide()

        if player.lives == 0:
            game_over = True
            level1 = True
            level2 = False

        all_sprites2.draw(screen)

        if pass_level():
            level2 = False
            level3 = True
        pygame.display.flip()

    monster1 = Monster(0, -10, bat, 115, 700, 0)
    monster2 = Monster(0, 10, bat, 575, 0,  700)
    monster3 = Monster(0, 10, bat, 210, 0, 700)
    monster4 = Monster(0, -10, bat, 300, 700,  0)
    monster5 = Monster(0, 10, bat, 395, 0, 700)
    monster6 = Monster(0, -10, bat, 484, 700,  0)
    monsters = [monster1, monster2, monster3, monster4, monster5, monster6]
    c = Coin(210, 350)
    c1 = Coin(484, 350)
    game_over = True
    while level3:
        if game_over:
            show_screen()
            game_over = False
            all_sprites3 = pygame.sprite.Group()
            all_sprites3.add(monsters)
            if player.lives == 0:
                player = Player()
            c = Coin(210, 350)
            c1 = Coin(484, 350)
            level_coins.append(c1)
            level_coins.append(c)
            all_sprites3.add(c)
            all_sprites3.add(c1)
            player.rect.x, player.rect.y = 20, 300
            all_sprites3.add(player)
        all_levels()
        level = 3
        all_sprites3.update()

        c.image = coins[math.floor(time() * 7) % 8]
        c1.image = coins[math.floor(time() * 7) % 8]
        if is_coin_taken(c):
            coin_sound.play()
            c.hide()
        if is_coin_taken(c1):
            coin_sound.play()
            c1.hide()

        if player.lives == 0:
            game_over = True
            level1 = True
            level3 = False

        all_sprites3.draw(screen)
        if pass_level():
            level3 = False
            level4 = True
        pygame.display.flip()

    game_over = True
    monster7 = Monster(0, -10, blue_bat, 70, 650,  0)
    monster8 = Monster(0, 10, blue_bat, 165, 0,  650)
    monster9 = Monster(0, -10, blue_bat, 255, 650,  0)
    monster10 = Monster(0, 10, blue_bat, 350, 0, 650)
    monster11 = Monster(0, -10, blue_bat, 530, 650,  0)
    monsters = [monster1, monster2, monster3, monster4, monster5, monster6, monster7, monster8, monster9, monster10,
                        monster11]
    c = Coin(150, 350)
    c1 = Coin(500, 350)
    c2 = Coin(315, 350)
    while level4:
        if game_over:
            show_screen()
            game_over = False
            all_sprites4 = pygame.sprite.Group()
            all_sprites4.add(monsters)
            if player.lives == 0:
                player = Player()
            player.rect.x, player.rect.y = 20, 300
            all_sprites4.add(player)
            c = Coin(150, 350)
            c1 = Coin(500, 350)
            c2 = Coin(315, 350)
            level_coins.append(c)
            level_coins.append(c1)
            level_coins.append(c2)
            all_sprites4.add([c, c1, c2])
        level = 4
        all_levels()
        all_sprites4.update()

        c.image = coins[math.floor(time() * 7) % 8]
        c1.image = coins[math.floor(time() * 7) % 8]
        c2.image = coins[math.floor(time() * 7) % 8]
        if is_coin_taken(c):
            coin_sound.play()
            c.hide()
        if is_coin_taken(c1):
            coin_sound.play()
            c1.hide()
        if is_coin_taken(c2):
            coin_sound.play()
            c2.hide()

        if player.lives == 0:
            game_over = True
            level1 = True
            level4 = False


        all_sprites4.draw(screen)

        if pass_level():
            finished = True
            game_over = True
            level4 = False
            level1 = True

        pygame.display.flip()

