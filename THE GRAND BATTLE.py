#librairies utulisees pour le jeu
import pygame
import time

#initialisation des caracteistiques du jeu
pygame.init()

#les parametres du jeu
win = pygame.display.set_mode((500,480))
pygame.display.set_caption("La Grande Bataille")

#les sprites utilises du hero

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

#chronologie du jeu
clock = pygame.time.Clock()

#la music
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

#variables du progre du jeu
score = 0
lives = 3

#definition des parametres du hero
class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def hit(self):
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.wait(2)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()


#definition de l'arme du hero
class projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

#definition des parametres de l'enemie
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 11
        self.visible = True
        self.left = False
        self.right = False

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 34:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
            font1 = pygame.font.SysFont('comicsans', 100)
            text = font1.render('YOU WON', 1, (255,0,0))
            pygame.display.update()


#la fonction utulise pour la projection des graphiques numeriques sur l'ecran
def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (350, 10))
    text = font.render('Lives: ' + str(lives), 1, (0,0,0))
    win.blit(text, (50, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)

    for gbullet in gbullets:
        gbullet.draw(win)

    pygame.display.update()


#boucle principale (le jeu actuel)
font = pygame.font.SysFont('comicsans', 30, True)
man = player(200, 410, 64, 64)
goblin = enemy(50, 60, 64, 64, 450)
shootLoop = 0
gshootLoop = 0
bullets = []
gbullets = []

run = True
while run:
    clock.tick(27)

    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
                lives -= 1
    else:
        font7 = pygame.font.SysFont('comicsans', 50, True)
        text7 = font7.render('VOUS AVEZ GAGNÉ!', 100, (255,0,0))
        win.blit(text7, (60, 250))
        pygame.display.update()
        pygame.time.wait(5000)
        run = False
    if lives == 0:
        font2 = pygame.font.SysFont('comicsans', 50, True)
        text = font2.render('VOUS ÊTES MORT', 100, (0,0,0))
        win.blit(text, (70, 250))
        pygame.display.update()
        pygame.time.wait(5000)
        run = False



    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 15:
        shootLoop = 0

    if gshootLoop > 0:
        gshootLoop += 1
    if gshootLoop > 20:
        gshootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                if goblin.visible == True:
                    score += 1
                    bullets.pop(bullets.index(bullet))

        if bullet.y < 500 and bullet.y > 0:
            bullet.y -= 5
        else:
            bullets.pop(bullets.index(bullet))

#-----------------------------

    for gbullet in gbullets:
        if gbullet.y + gbullet.radius < man.hitbox[1] + man.hitbox[3] and gbullet.y - gbullet.radius > man.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > gbullet.x + gbullet.radius > man.hitbox[0]: #and man.x - gbullet.radius < man.hitbox[0] + man.hitbox[2]:
                man.hit()
                if lives > 0:
                    lives -= 1
                if score > 5:
                    score -=5
                else:
                    score = 0
                gbullets.pop(gbullets.index(gbullet))

        if gbullet.y < 500 and gbullet.y > 0:
            gbullet.y += 5
        else:
            gbullets.pop(gbullets.index(gbullet))

#-------------------------------

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and goblin.visible == 1 and shootLoop == 0:
        if len(bullets) < 10:
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 6, (0,255,0)))
        shootLoop = 1

#-------------------------------------

    if goblin.visible == 1 and gshootLoop ==0 and lives > 0:
        if len(gbullets) < 10:
            gbullets.append(projectile(round(goblin.x + goblin.width //2), round(goblin.y + goblin.height//2), 6, (255,0,0)))
        gshootLoop = 1

#-------------------------------------

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    redrawGameWindow()

pygame.quit()
