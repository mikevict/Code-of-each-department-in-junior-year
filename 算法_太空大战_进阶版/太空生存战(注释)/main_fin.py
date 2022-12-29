from hashlib import new
from turtle import back
import pygame
import random
import os
#import pygame.movie  居然不能用了，，服了
# from moviepy.editor import *

#参数
FPS = 60

#颜色参数
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)


WIDTH = 500
HEIGHT = 600
#游戏初始化和视窗
pygame.init()
pygame.mixer.init() #用于加载和播放声音的pygame模块 pygame.mixer.init  —  初始化混音器模块
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("first game")#设置当前窗口标题
clock = pygame.time.Clock()#控制下 帧的刷新速率使动画能够以一个平稳的速率运行


#载入图片
background_img = pygame.image.load(os.path.join("img","background.png")).convert()#连接路径名 + 转化为对应的像素值

#background_img = pygame.image.load(os.path.join("video","spacewar.gif")).convert()
#background_img = VideoFileClip(os.path.join("video","spacewar.mp4"))

player_img = pygame.image.load(os.path.join("img","player.png")).convert()
dead = pygame.image.load(os.path.join("img","dead.png")).convert()
player_mini_img = pygame.transform.scale(player_img,(30,30))#将图片缩放至指定的大小，并返回一个新的 Surface 对象。
player_mini_img.set_colorkey(BLACK)#img.set_colorkey()：设置透明颜色键,与黑色一样的就会显示为透明
pygame.display.set_icon(player_mini_img)#设置图标，就是exe的那个标志
# rock_img = pygame.image.load(os.path.join("img","rock.png")).convert()  #大小一致不符合
# bullet_imgs = []
bullet_img1 = pygame.image.load(os.path.join("img","bullet1.png")).convert() #子弹图形
bullet_img2 = pygame.image.load(os.path.join("img","bullet2.png")).convert() #子弹图形
# bullet_imgs.append(bullet_img1)
# bullet_imgs.append(bullet_img2)

rock_imgs = [] #陨石图形进行随机化处理了.
for i in range(7): #加入7张不同照片
    temp_img = pygame.image.load(os.path.join("img",f"rock{i}.png")).convert()
    # temp_img.set_colorkey(BLACK)
    rock_imgs.append(temp_img)
# rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

# 载入爆炸图片
expl_anim = {} #字典类型
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []

for i in range(9):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert() #几种不同特效
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img,(75,75))) #大小爆炸限制下规模
    expl_anim['sm'].append(pygame.transform.scale(expl_img,(30,30)))
    #玩家爆炸特效,被击中 hit中
    player_expl_img = pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(player_expl_img)

power_imgs = {} #添加掉落物照片
power_imgs['shield'] = pygame.image.load(os.path.join("img","shield.png")).convert() #护盾 ，加血的
power_imgs['gun'] = pygame.image.load(os.path.join("img","gun.png")).convert() #武器

# 载入音乐
shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound","ji.mp3"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound","鸡你太美.mp3"))
pygame.mixer.music.set_volume(0.4) #音量


#调整字体
font_name = os.path.join("font.ttf") #加载字体

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE)#文字，无锯齿，颜色 color
    text_rect = text_surface.get_rect() #我们的图象最终出现的位置
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect) #旨在将一个图像绘制到另一个图像的上方


def draw_text1(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    if int(text) <= 1000:
        text_surface = font.render(text, True, WHITE)  # 文字，无锯齿，yanse
    elif int(text) > 1000 and int(text) <= 5000:
        text_surface = font.render(text, True, YELLOW)  # 文字，无锯齿，yanse
    elif int(text) > 5000:
        text_surface = font.render(text, True, RED)  # 文字，无锯齿，yanse
    # text_surface = font.render(text,True,WHITE)#文字，无锯齿，yanse
    text_rect = text_surface.get_rect() #我们的图象最终出现的位置
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface,text_rect) #旨在将一个图像绘制到另一个图像的上方

def new_rock():
    r = Rock()
    rocks.add(r)
    all_sprites.add(r)

#绘制血条
def draw_health(surf,hp,x,y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH #条状物_长度
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    if fill>=70:
        pygame.draw.rect(surf,GREEN,fill_rect) #创作矩形
    elif fill>=40 and fill<70:
        pygame.draw.rect(surf, YELLOW, fill_rect)  # 创作矩形
    elif fill<40:
        pygame.draw.rect(surf, RED, fill_rect)  # 创作矩形
    pygame.draw.rect(surf,WHITE,outline_rect,2)

#画生命条数
def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i #这次我们采用简单方法，紧贴边界来绘制，，，
        img_rect.y = y
        surf.blit(img,img_rect)


#这个地方可以修改，进去界面 ,待会再看看啊看啊看啊看再看看啊看啊看啊看再看看啊看啊看啊看再看看啊看啊看啊看
def draw_init():
    screen.blit(background_img,(0,0))
    draw_text(screen,'太空生存战',64,WIDTH/2,HEIGHT/4)
    draw_text(screen,'↑ ↓ ← →移动飞船,空白键发射子弹 ~~',22,WIDTH/2,HEIGHT*2/5)
    draw_text(screen,'按任意键开始游戏!',18,WIDTH/2,HEIGHT*4/5)

    draw_text(screen,'点击此处开始游戏!',40,WIDTH/2,HEIGHT*3/5)


    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        buttons = pygame.mouse.get_pressed()
        x1, y1 = pygame.mouse.get_pos()
        #print(buttons[0])
        for event in pygame.event.get():
            #print(x1,y1)
            if x1>=WIDTH*1/4 and x1<=WIDTH*3/4 and y1>=HEIGHT/2 and y1<= HEIGHT*3/4:
                #125.0 250.0 300.0 450.0
                #print(x1,y1,buttons[0])
                if buttons[0]:
                    print("right")
                    waiting = False
                    return False

            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP :
                waiting = False
                return False
def dead_init():
    def draw_text(surf,text,size,x,y):
        font = pygame.font.Font(font_name,size)
        text_surface = font.render(text,True,RED)#文字，无锯齿，yanse
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface,text_rect)
    screen.blit(dead,(0,0))
    draw_text(screen,'You have been slayed!',25,WIDTH/2,HEIGHT/4)
    draw_text(screen,'按任意键开始游戏!',18,WIDTH/2,HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
            
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #这一步什么意思??类构造出相同的self东西
        #这一句什么意思？？？？？#player_img是全局的，就可以用，self.image成为自己的，再限制下大小
        self.image = pygame.transform.scale(player_img,(60,60))  #加一个平面
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位 
        self.radius = 20 #半径,碰撞半径
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius) #显示碰撞半径
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10 #定出的位置+再调整->真的定位
        self.speedx = 8
        self.speedy = 8 #速度
        self.health = 100
        self.lives = 3
        self.hidden = False  #隐逸状态，就是死掉了那个保护时间
        self.hide_time = 0
        self.gun = 1 #武器数，捡道具++
        self.gun_time = 0
        # self.rect.x = 200
        # self.rect.y = 200
    def update(self):#上下左右控制方向
        now = pygame.time.get_ticks()
        #这个地方不是太懂，就是道具到时间就没了呗??  ：道具持续时间
        # 如果
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun = 1
            self.gun_time = now
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        key_pressed = pygame.key.get_pressed()#返回一串booling值
        #后期可加入wasd玩家二
        if key_pressed[pygame.K_RIGHT]:#判断按压的是不是右方向键
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
#######        #这一步防止越界
        if self.rect.top < 0 and not self.hidden:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT and not self.hidden:
            self.rect.bottom = HEIGHT
        if self.rect.right>WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        if not(self.hidden):#没有在隐逸状态才能发射 #隐逸状态就是死掉了，那个保护状态
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top,self.gun)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun == 2:#最多两个嘛？是滴，还有持续时间的
                bullet1 = Bullet(self.rect.left,self.rect.centery,self.gun)
                bullet2 = Bullet(self.rect.right,self.rect.centery,self.gun)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            elif self.gun == 3:
                bullet1 = Bullet(self.rect.left,self.rect.centery,self.gun)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.centerx,self.rect.top,self.gun)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                bullet3 = Bullet(self.rect.right,self.rect.centery,self.gun)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
            elif self.gun == 4:
                bullet1 = Bullet(self.rect.left-20,self.rect.centery,self.gun)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                bullet2 = Bullet(self.rect.centerx-10,self.rect.centery,self.gun)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                bullet3 = Bullet(self.rect.centerx+10,self.rect.centery,self.gun)
                all_sprites.add(bullet3)
                bullets.add(bullet3)
                bullet4 = Bullet(self.rect.right+20,self.rect.centery,self.gun)
                all_sprites.add(bullet4)
                bullets.add(bullet4)



    #设置隐逸状态之类的
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks() #起始时间
        self.rect.center = (WIDTH/2,HEIGHT+500)
    #设置枪状态
    def gunup(self):
        if(self.gun == 4):
            return
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
# me
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()  #加一个平面 #变成自己的
        

        self.rect = self.image.get_rect() #定位
        self.radius = int(self.rect.width*0.85/2) #碰撞半径
        # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)

        #随机出现位置，+随机速度
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180,-100)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-3,3)
        # self.rect.x = 200
        # self.rect.y = 200
        self.total_degree = 0
        self.rot_degree = random.randrange(-3,3)
    #优化，岩石旋转
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree%360 #限制在360度之内
        self.image = pygame.transform.rotate(self.image_ori,self.total_degree)
        center = self.rect.center  #用重定位的方法进行旋转
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate() #旋转
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-3,3)
       
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,op):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img2 if op >=3 else bullet_img1   #加一个平面
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect() #定位

        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        # self.rect.x = 200
        # self.rect.y = 200
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom<0:
            self.kill() #问题：没见设置kill函数啊???
#没太读懂，再看看扩扩扩扩扩扩扩叭叭叭吧
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self) #用self构建函数
        self.size = size
        self.image = expl_anim[self.size][0]
        
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

#这里每太读懂
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else :
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun']) #随机凋落物
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() #定位
        self.rect.center = center
        self.speedy = 3
        # self.rect.x = 200
        # self.rect.y = 200
#what???
    def update(self):
        self.rect.y += self.speedy
        #what?
        if self.rect.top > HEIGHT:
            self.kill()



# rock = Rock()
# all_sprites.add(rock)

#游戏开始，main

pygame.mixer.music.play(-1)

#游戏回圈
show_init = True
running = True
dead_flag = 0

while running:
    if show_init:
        if(dead_flag == 0):
            close = draw_init()
        elif(dead_flag ==1):
            close = dead_init()
        if close:
            break
        show_init = False
        dead_flag = 0
        all_sprites = pygame.sprite.Group()##定义精灵组
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        # init
        player = Player()
        all_sprites.add(player)
        for i in range(8): #建立新岩石
            new_rock()
        score = 0

    clock.tick(FPS)#一秒钟执行60次帧率
    #取得输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #页面显示

    all_sprites.update() #所有精灵组进行update函数操作
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)#检测是否碰撞
    # 石块和子弹相撞
    for hit in hits:
        random.choice(expl_sounds).play() #音效播放
        score += hit.radius #得分的增加
        expl = Explosion(hit.rect.center,'lg') #采用大爆炸
        all_sprites.add(expl) #添加爆炸
        if random.random() > 0.5:# 掉宝率
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    #碰撞能用函数检测就方便多了
    hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    #  石块和飞船相撞
    for hit in hits :
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center,'sm') #采用小爆炸
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center,'player')
            all_sprites.add(death_expl) #增加死亡特效
            die_sound.play()#增加死亡音效
            player.lives -= 1#生命--
            player.health = 100#恢复生命
            player.hide()#进入隐逸值状态
    # 判断宝物与飞船相撞
    hits = pygame.sprite.spritecollide(player,powers,True)
    for hit in hits:
        if hit.type == 'shield': #加血
            player.health += 10
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun': #加枪
            player.gunup()
            gun_sound.play()
    
    #死掉了，在这里可以更改加入死亡界面
    if player.lives == 0 and not(death_expl.alive()):
        show_init = True #就恢复初始界面
        dead_flag = 1

    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    draw_text1(screen,str(score),18,WIDTH/2,10)
    # settextcolor(screen,color='r')
    draw_health(screen,player.health,5,15)
    draw_lives(screen,player.lives,player_mini_img,WIDTH - 100,15)
    pygame.display.update()
 
pygame.quit()

