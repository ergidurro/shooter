from pygame import *
from random import randint
from time import time as timer
class loja(sprite.Sprite):
    def __init__(self, imazh, x1, y1, s1, s2, speed):
        super().__init__()
        self.image = transform.scale(image.load(imazh), (s1, s2))
        self.s1 = s1
        self.s2 = s2
        self.speed = speed
        
        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1

    def show(self):
        game_window.blit(self.image, (self.rect.x, self.rect.y))

    
imazhi_i_enemy = 'asteroid.png'
imazhi_i_enemy1 = 'ufo.png'


class Player(loja):
    def move(self):
        press_key = key.get_pressed()
        if press_key[K_RIGHT] and self.rect.x < 655:
            self.rect.x += self.speed
        if press_key[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 14, 25, -15)
        bullets.add(bullet)


class Enemy(loja):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost += 1
            self.kill()
        

class Bullet(loja):
    def update(self):
        self.rect.y += self.speed
        if self.rect.x < 0:
            self.kill()

        

clock = time.Clock()
FPS = 30
finish = False
lost = 0
score = 0
max_score = 10
max_lost = 30
rel_time = False
num_fire = 0
life = 3
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 72)
win = font1.render('YOU WIN!', True, (51, 255, 51))
lose = font1.render('YOU LOSE!', True, (255, 0, 0))
loser = font2.render('Missed: ' + str(lost), 1, (255, 0, 0))
winner = font2.render('Score: ' + str(score), 1, (255, 0, 0))
game_window = display.set_mode((700, 500))
display.set_caption("Space Rangers")
background = transform.scale(image.load("galaxy2.jpg"),(700, 500))
lojtari = Player('rocket1.png', 20, 450, 50, 50, 10)
game = True
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
monsters = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    monster = Enemy(imazhi_i_enemy1, randint(80, 620), 20, 50, 50, randint(1, 4))
    monsters.add(monster)

for i in range(1, 6):
    asteroid = Enemy(imazhi_i_enemy, randint(80, 620), 20, 50, 50, randint(1, 4))
    asteroids.add(asteroid)
bullets = sprite.Group()


while game:
    if finish != True:
        game_window.blit(background,(0, 0))
        game_window.blit(loser,(0, 0))
        game_window.blit(winner,(0, 20))
        lojtari.show()
        lojtari.move()
        monsters.update()
        bullets.update()
        monsters.draw(game_window)
        bullets.draw(game_window)
        loser = font2.render('Missed: ' + str(lost), 1, (255, 0, 0))
        winner = font2.render('Score: ' + str(score), 1, (255, 0, 0))
        


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(imazhi_i_enemy, randint(80, 620), 20, 50, 50, randint(1, 4))
            monsters.add(monster)
            
        if score >= max_score:
            finish = True
            game_window.blit(win, (200, 200))

        if sprite.spritecollide(lojtari, monsters, False) or sprite.spritecollide(lojtari, asteroids, False):
            sprite.spritecollide(lojtari, monsters, True)
            sprite.spritecollide(lojtari, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            game_window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        game_window.blit(text_life, (650, 10))
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Reloading', 1,(150, 0, 0))
                game_window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        


        

        
        

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 7 and rel_time == False:
                    lojtari.fire()
                    num_fire += 1
                if num_fire >= 7 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    clock.tick(FPS)
    display.update()