#Створи власний Шутер!
from random import randint
from pygame import *
from time import time as timer 
#створи вікно гри
win_hight = 600
win_width = 1080
window = display.set_mode((win_width,win_hight))
display.set_caption('Стрелялка')
#задай фон сцени
background = transform.scale(image.load('4a0577fb65b7f47a339c3-768x402.jpg'),(win_width,win_hight))
mixer.init()
fire_sound = mixer.Sound('fire.ogg')
mixer.music.load('polet_tolstaka_v_kosmos_video_prikol.ogg')
mixer.music.play()


clock = time.Clock()
FPS = 60

lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > 600:
            self.rect.y = 0
            self.rect.x = randint(80,1000)
            lost = lost + 1
monsters = sprite.Group()
for i in range (1,4):
    monster = Enemy('pngwing.png', randint(80,1000),-40, 80, 50, randint(1,2))
    monsters.add(monster)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 720:
            self.rect.y = 0
            self.rect.x = randint(80, 1000)

asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Asteroid('asteroid.png', randint(30, 1000), -40, 80, 50, randint(1,2))
   asteroids.add(asteroid)

bullets = sprite.Group()
life = 3
font.init()
font1= font.SysFont('Arial',36)
font2= font.SysFont('Arial',60)
player = Player('pngwing.png',5,win_hight - 110,80,100, 9)
finish = False
game = True
rel_time = False
num_fire = 0

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))
        text = font1.render('счет: ' + str(score),1,(255,255,255))
        window.blit(text, (10,20))
        text_lose = font1.render('проп: ' + str(lost),1,(255,255,255))
        window.blit(text_lose, (10,50))
        monsters.update()
        player.update()
        player.reset()
        asteroids.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        

        collides=sprite.groupcollide(monsters, bullets, True, True)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1:
                reload = font1.render('Идет перезарядка...', 1, (150,0,0))
                window.blit(reload, (450, 10))
            else:
                num_fire = 0
                rel_time = False
        for c in collides:
            score += 1
            monster = Enemy('pngwing.png', randint(80,1000),-40, 80, 50, randint(1,2))
            monsters.add(monster)
        if score >= 25:
            finish = True
            win  = font1.render('YOU WIN!', True, (255,255,255))
            window.blit(win,(200,200))
        if life == 0 or lost >= 3:
            finish = True 
            lose = font1.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (450, 300))
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (20,80))
        display.update()
    time.delay(5)



