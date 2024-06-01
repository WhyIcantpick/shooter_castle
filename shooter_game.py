from operator import truediv
from turtle import update
from pygame import *
from random import randint
from time import time as timer #імпортуємо функцію для засікання часу, щоб інтерпретатор не шукав цю функцію в pygame модулі time, даємо їй іншу назву самі


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU WIN!', True, (255, 255, 255))
lose = font2.render('YOU LOSE!', True, (180, 0, 0))


img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_superEnemy = "big.png"
img_non_killable_enemy = "asteroid.png"
img_health = "healthPoint.png"

score = 0
lost = 0
goal = 100
max_lost = 50
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, sixe_y , sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_img),(size_x, sixe_y))
        self.speed = sprite_speed
        self.rect = self.image.get_rect()
        self.rect.x = sprite_x
        self.rect.y = sprite_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet("arrow.png", self.rect.centerx - 5, self.rect.centery, 25, 10, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x == 0:
            self.rect.x = 600
            self.rect.y = randint (50, 450)
            lost +=1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0

class SuperEnemy(Enemy):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed, max_hits):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        self.max_hits = max_hits
    def gotHit(self):
        self.max_hits -= 1
    def isKilled(self):
        if(self.max_hits <= 0):
            self.kill()
            return True
        else: return False

class HealthPack(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint (80, win_width - 80)
            self.rect.y = 0 
    def apply(self):
        global life
        life += 1
        self.kill()

class Bullet(GameSprite):
    def __init__(self, sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed):
        super().__init__(sprite_img, sprite_x, sprite_y, size_x, size_y, sprite_speed)
        # self.image = transform.rotate(self.image, 90)
    def update(self):
        self.rect.x -= self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x >= 700:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

player = Player(img_hero, 5, win_height - 100, 80, 100, 10)
# health_pack = HealthPack(img_health, randint(30, win_width - 30), -40, 30, 30, 7)



health_packs = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
superMonsters = sprite.Group()
# health_packs.add(health_pack)

for i in range(1, 6):
    monster = Enemy(img_enemy, 600, randint(50, 450), 80, 50, randint(1, 3))
    monsters.add(monster)
for i in range(1, 3):
    asteroid = Asteroid(img_non_killable_enemy, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
for i in range(1, 3):
    superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 50, randint(1, 3), 3)
    superMonsters.add(superMonster)

run = True
finish = False
clock = time.Clock()
FPS = 30
rel_time = False  # прапор, що відповідає за перезаряджання
num_fire = 0  # змінна для підрахунку пострілів    


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and not finish: ###
            if e.key == K_SPACE:
                if num_fire < 20 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                   
                if num_fire >= 20 and rel_time == False : #якщо гравець зробив 20 пострілів
                    last_time = timer() #засікаємо час, коли це сталося
                    rel_time = True #ставимо прапор перезарядки


    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        health_packs.update()
        superMonsters.update()
        
        health_packs.draw(window)
        player.reset()
        monsters.draw(window)
        superMonsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if life == 1 and len(health_packs) == 0:
            health_pack = HealthPack(img_health, randint(100, win_width - 30), -40, 30, 30, 3)
            health_packs.add(health_pack)

        if rel_time == True:
            now_time = timer() # зчитуємо час
            if now_time - last_time < 2: #поки не минуло 2 секунди виводимо інформацію про перезарядку
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (win_width/2-200, win_height-100))
            else:
                num_fire = 0     #обнулюємо лічильник куль
                rel_time = False #скидаємо прапор перезарядки


        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for collide in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            score = score + 1
            monster = Enemy(img_enemy, 600, randint(50, 450), 80, 50, randint(1, 3))
            monsters.add(monster)
        
        for superMonster in superMonsters:
            if sprite.spritecollide(superMonster, bullets, True):
                superMonster.gotHit()
                if superMonster.isKilled():
                    score = score + 1
                    superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 50, randint(1, 3), 3)
                    superMonsters.add(superMonster)
                    



        # якщо спрайт торкнувся ворога зменшує життя
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False) or sprite.spritecollide(player, superMonsters, False):
            life = life - 1
            if sprite.spritecollide(player, monsters, True):
                monster = Enemy(img_enemy, 600, randint(50, 450), 80, 50, randint(1, 3))
                monsters.add(monster)
            if sprite.spritecollide(player, asteroids, True):
                asteroid = Asteroid(img_non_killable_enemy, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
                asteroids.add(asteroid)
            if sprite.spritecollide(player, superMonsters, True):
                superMonster = SuperEnemy(img_superEnemy, 600, randint(50, 450), 80, 50, randint(1, 3), 3)
                superMonsters.add(superMonster)
            

        if sprite.spritecollide(player, health_packs, True):
            health_pack.apply()


        #програш
        if life == 0 or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))


        # перевірка виграшу: скільки очок набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        text = font1.render("Рахунок: " + str(score),1, (255,255,255))
        window.blit(text,(10, 20))

        text_lose = font1.render("Пропущенно: " + str(lost),1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        
        text_life = font1.render(str(life), 1, (0, 150, 0))
        window.blit(text_life, (650, 10))
        display.update()

    clock.tick(FPS)