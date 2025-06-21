import pygame,random,subprocess,os
os.chdir(r'C:\PYTHON By RISHI\PYTHON FILES\Self\Pygame trails\images')
pygame.init()

SCREEN_HEIGHT=700;SCREEN_WIDTH=700
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("CAR")

bg=pygame.image.load('desert.png')
bg=pygame.transform.scale(bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
bg_rect=bg.get_rect(topleft=(0,0))
bg1_rect=bg.get_rect(topleft=(0,-SCREEN_HEIGHT))

blast=pygame.image.load('bla1_1.png')
blast=pygame.transform.scale(blast,(200,200))
blast_rect=blast.get_rect(topleft=(300,SCREEN_HEIGHT));t=0
blit=1

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car=pygame.image.load('car1.png')
        self.car=pygame.transform.scale(self.car,(50,130))
        self.car_rect=self.car.get_rect(topleft=(300,550))
        self.lives=5
        self.score=0
        self.score_text=pygame.font.SysFont('calliber',30)
        self.lives_text=pygame.font.SysFont('calliber',30)
        self.x=[]
    def update(self,k):
        self.move(k)
        self.display()
    def move(self,k):
        global t,blit
        if self.car_rect.x + 50 >= SCREEN_WIDTH: self.car_rect.x = SCREEN_WIDTH-50
        elif self.car_rect.x <= 0: self.car_rect.x = 0
        if self.car_rect.y + 50 >= SCREEN_HEIGHT: self.car_rect.y = SCREEN_HEIGHT-50
        elif self.car_rect.y <= 0: self.car_rect.y = 0 
        if k[pygame.K_UP]:
            self.car_rect.y-=2
        if k[pygame.K_DOWN]:
            self.car_rect.y+=3
        if k[pygame.K_RIGHT]:
            self.car_rect.x+=3
        if k[pygame.K_LEFT]:
            self.car_rect.x-=3

        centers=[[car.car_rect.x+4,car.car_rect.x+25,car.car_rect.x+45],[car.car_rect.y+50,car.car_rect.y+60,car.car_rect.y+50]]
        i=0
        for bomb in BOMB:
            bomb.update([centers[0][i%3],centers[1][i%3]])
            i+=1
        for truck in TRUCKS:
            if truck not in collided:
                if truck.rect.colliderect(self.car_rect):
                    screen.blit(blast,(car.car_rect.x-60,car.car_rect.y-100))
                    t+=1
                    if t==1 : 
                        print(t)
                        self.lives-=1
                        self.x.append(truck)
                    if self.lives<=0:
                        self.lives=0
                        blit=0
                        
                elif truck in self.x:
                    t=0;self.x=[]

    def display(self):
        self.scores_text = self.score_text.render(f'Score--{self.score}',True,'yellow')
        self.lifes_text = self.lives_text.render(f'Lives--{self.lives}',True,'yellow')
        screen.blit(self.scores_text,(0,0))
        screen.blit(self.lifes_text,(600,0))

class Truck(pygame.sprite.Sprite):
    def __init__(self,i,j):
        super().__init__()
        self.truck=pygame.image.load(f'truck{i}.png')
        self.truck=pygame.transform.scale(self.truck,(60,130))
        self.j=j
        self.score = 0
        self.rect=self.truck.get_rect()
        self.rect.topleft=(self.j,-130)
        self.speed=random.randint(3,5)
        self.Truckscore=pygame.font.SysFont('calliber',30)
        
        self.blit=True
    def update(self):
        self.move()
        for truck in collided:
            if truck.rect.y>=700:
                collided.remove(truck)
    def move(self):
        self.rect.y+=self.speed
        if self.rect.y>=SCREEN_HEIGHT+200:
            i=random.randint(1,10)
            self.__init__(i,self.j)
        self.Truckscore_ = self.Truckscore.render(f'{self.score}',True,'white')

collided = []

class Bombs(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.bomb=pygame.image.load('bomb.png')
        self.image=pygame.transform.scale(self.bomb,(20,20))
        self.rect= self.image.get_rect()
        self.rect.center=(x,y)
        self.fire=False;self.clash = False
    def update(self,cords):
        if self.fire:
            self.shoot()
        else:self.rect.center = cords
    def shoot(self):
        self.rect.y-=5
        collide=pygame.sprite.spritecollide(self,TRUCKS,0)
        for truck in collide:
            if truck.score < 3:
                collided.append(truck)
                truck.score+=1
                truck.blit = False
                car.score+=1
                self.clash = True
                self.kill()
        if self.rect.y<=0:
            self.kill()

TRUCKS=pygame.sprite.Group()
BOMB=pygame.sprite.Group()
car=Car()

Truckcords=[84,161,251,361,463,563,]
for j in Truckcords:
    i=random.randint(1,10)
    truck=Truck(i,j)
    TRUCKS.add(truck)
def MakeBomb():
   centers=[[car.car_rect.x+4,car.car_rect.x+20,car.car_rect.x+100],[car.car_rect.y+50,car.car_rect.y+60,car.car_rect.y+50]]
   for i in range(3):
       bomb=Bombs(centers[0][i],centers[1][i])
       BOMB.add(bomb)
MakeBomb()

def move_bg(bg_rect):
    bg_rect.y+=1
    if bg_rect.y==SCREEN_HEIGHT:
        bg_rect.y=-SCREEN_HEIGHT
    screen.blit(bg,bg_rect)

fps=100
clock=pygame.time.Clock()
run=1

while run:
    k=pygame.key.get_pressed()
    if blit:
        move_bg(bg_rect);move_bg(bg1_rect)
        screen.blit(car.car,car.car_rect)
        BOMB.draw(screen)
        for truck in TRUCKS:
            if truck.blit:
                screen.blit(truck.truck,truck.rect)
            elif truck.rect.y <= car.car_rect.y:
                screen.blit(truck.Truckscore_,truck.rect)
        TRUCKS.update()
        car.update(k)
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            run=False
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_SPACE:
                for bomb in BOMB:
                    bomb.fire=True
                MakeBomb()
    pygame.display.update()
    clock.tick(fps);pos=pygame.mouse.get_pos()
    if not (blit):
        f = open('high score','r')
        for data in f:
            a = data
            if car.score >= int(data):
                f =  open('high score','w')
                a=str(car.score)
                f.write(a)
        restart=pygame.image.load('restart.png')
        restart_rect=restart.get_rect(topleft=(280,290))
        highscore = pygame.font.SysFont('caliber',30)
        highscore_ = highscore.render(f'HIGHSCORE --{a}',True,'yellow')
        screen.blit(highscore_,(280,350))
        screen.blit(restart,restart_rect)
        if restart_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                pygame.quit() 
                subprocess.run((['python',r'C:\PYTHON By RISHI\Self\Pygame trails\SPRITES CAR.py']))
pygame.quit()