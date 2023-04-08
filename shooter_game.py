#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

# Создаем экран и загружаем фон
win_height = 700
win_width = 900

lost = 0
global score
score = 0
life = 3

rel_time = False
num_fire = 0

win = display.set_mode((win_width,win_height))
display.set_caption("Космическая Одиссея")
background = image.load("galaxy.jpg")
background = transform.scale(background,(win_width,win_height))
# Создаем игровой таймер и частоту обновления
clock = time.Clock() 
FPS = 70

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")

# Класс персонажей
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, player_width, player_heigth, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_heigth))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
	# Метод перерисовки персонажа
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 100:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= self.speed 

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-6, self.rect.top, 
            15, 20, -15)
        bullets.add(bullet)

    def armageddon(self):
        x = 20
        step = 20
        for i in range(45):
            bullet = Bullet("bullet.png", x, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
            x += step

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 160)
            self.rect.y = -50
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 160)
            self.rect.y = -50
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.SysFont("Tahoma", 36)

spaceX = Player("rocket.png", round(win_width/2), win_height-100, 65, 95, 10)
monsters = sprite.Group()
for i in range(1, 7):
    monster = Enemy("ufo.png", randint(80, win_width - 160), 
                                    -40, 80, 50, randint(1,3))
    monsters.add(monster)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid("asteroid.png", randint(80, win_width - 160), 
                                    -40, 80, 50, randint(1,3))
    asteroids.add(asteroid)


game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    spaceX.fire()
                    fire.play()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True           
            
            if e.key == K_TAB:
                spaceX.armageddon()
                for i in range(10):
                    fire.play()
                    

    if finish != True:
        win.blit(background, (0,0))   
        spaceX.reset()
        monsters.draw(win)
        bullets.draw(win)
        asteroids.draw(win)
        spaceX.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font1.render("Перезаряжаю, ждите...", 1, (200, 250, 200))
                win.blit(reload, (340, 660))
            else:
                num_fire = 0
                rel_time = False

        text_lose = font1.render("Пропущено: "+str(lost), 1, (255,255,255))
        win.blit(text_lose, (10,10))
        text_win = font1.render("Поражено: " + str(score), 1, (255,255,255))
        win.blit(text_win, (10,60))
        text_life = font1.render("Жизни: " + str(life), 1, (255,255,255))
        win.blit(text_life, (730,10))


        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            
            score = score + 1
            monster = monster = Enemy("ufo.png", randint(80, win_width - 160), -40, 80, 50, randint(1,3))
            monsters.add(monster)

        if sprite.spritecollide(spaceX, monsters, True):
            life -= 1
            if life < 1:
                finish = True
                lose = font.SysFont("Arial", 120, "bold").render("Вы проиграли!", True, (255,255,255))
                win.blit(lose, (40,350))
            else:
                monster = Enemy("ufo.png", randint(80, win_width - 160), 
                                    -40, 80, 50, randint(1,3))
                monsters.add(monster)  
            

        if sprite.spritecollide(spaceX, asteroids, True):
            life -= 1
            if life < 1:
                finish = True
                lose = font.SysFont("Arial", 120, "bold").render("Вы проиграли!", True, (255,255,255))
                win.blit(lose, (40,350))
            else:
                asteroid = Asteroid("asteroid.png", randint(80, win_width - 160), 
                                    -40, 80, 50, randint(1,3))
                asteroids.add(asteroid)
                
        if lost > 3:
            finish = True
            lose = font.SysFont("Arial", 120, "bold").render("Вы проиграли!", True, (255,255,255))
            win.blit(lose, (40,350))

        if score >= 10:
            finish = True
            winner = font.SysFont("Arial", 120, "bold").render("Вы выиграли!", True, (255,255,255))
            win.blit(winner, (70,250))

    else:
        finish = False
        score = 0
        lost = 0
        life = 3

        for bullet in bullets:
            bullet.kill()
        for monster in monsters:
            monster.kill()
        for asteroid in asteroids:
            asteroid.kill()

        time.delay(3000)
        for i in range(1, 7):
            monster = Enemy("ufo.png", randint(80, win_width - 160), -40, 80, 50, randint(1,3))
            monsters.add(monster)
        for i in range(1, 4):
            asteroid = Asteroid("asteroid.png", randint(80, win_width - 160), 
                                    -40, 80, 50, randint(1,3))
            asteroids.add(asteroid)
            
    display.update()
    clock.tick(FPS)

