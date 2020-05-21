'''
项目：坦克大战
开发人员：梁国赞
版本:1.1
时间：5-14
更新：1.加入音效  2.墙壁可破坏成小块  3英雄机5秒后重生  4敌机偶尔停顿  5有个小boss

'''
import sys
import time
import pygame
import random

SCREEN_HEIGHT=480
SCREEN_WIDTH=900
ENEMY_COUNT=5
pygame.mixer.init()


#主逻辑类
class MainGame:
    #游戏主窗口
    window=None

    #记录我方坦克
    P1=None


    #记录敌方坦克
    enemy_list=[]

    # 记录墙体
    walls_list = []

    # 记录爆炸类
    bomb_list = []

    #游戏结束
    game_over=150

    #创建英雄坦克
    def creatMyTank(self):
        if not MainGame.P1:
            MainGame.P1=MyTank(420,420)

    #创建敌方坦克
    def creatEnemyTank(self):
        if len(MainGame.enemy_list)==0:
            for i in range(ENEMY_COUNT):
                MainGame.enemy_list.append(EnemyTank(random.randint(0,(SCREEN_WIDTH-100)),0))
            MainGame.enemy_list.append(Boss(random.randint(0, (SCREEN_WIDTH - 100)), 0))


    #创建墙体
    def creatWalls(self):
        list=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
              [2,3,3,4,3,3,3,0,3,3,3,4,3,3,2],
              [2,1,1,4,1,1,1,0,1,1,1,4,1,1,2],
              [2,0,0,4,0,0,0,0,0,0,0,4,0,0,2],
              [2,1,1,4,1,1,1,0,1,1,1,4,1,1,2],
              [2,1,1,4,1,0,0,0,0,0,1,4,1,1,2],
              [2,1,1,4,1,0,0,0,0,0,1,4,1,1,2],
              [2,2,2,2,2,0,0,0,0,0,2,2,2,2,2]]
        if len(MainGame.walls_list)==0:
            for i in range(len(list)):
                for j in range(len(list[i])):
                    if list[i][j]==1:
                        MainGame.walls_list.append(Wall(j*60,i*60))
                    elif list[i][j]==2:
                        MainGame.walls_list.append(Green_Wall(j * 60, i * 60))
                    elif list[i][j]==3:
                        MainGame.walls_list.append(Steels_Wall(j * 60, i * 60))
                    elif list[i][j]==4:
                        MainGame.walls_list.append(Water_Wall(j * 60, i * 60))

    #加载敌方坦克
    def loadEnemyTank(self):
        if len(MainGame.enemy_list)!=0 :
            for i in MainGame.enemy_list:
                if i.isAlive:
                    i.displayTank()
                    i.move()
                    i.fire()
                else:
                    MainGame.enemy_list.remove(i)
        else:
            self.creatEnemyTank()

    #加载英雄坦克
    def loadMyTank(self):
        if MainGame.P1 and MainGame.P1.isAlive:
            MainGame.P1.displayTank()
            MainGame.P1.move()
        else:
            del MainGame.P1
            MainGame.P1=None
            self.game_over_func()


    #加载墙体
    def loadWall(self):
        if len(MainGame.walls_list)!=0 :
            for i in MainGame.walls_list:
                if i.isAlive:
                    i.displayWall()
                else:
                    MainGame.walls_list.remove(i)

    #加载爆炸效果
    def loadBomb(self):
        for bomb in MainGame.bomb_list:
            if bomb.isAlive:
                bomb.displayBomb()
            else:
                MainGame.bomb_list.remove(bomb)

    #开始游戏
    def start_game(self):
        pygame.display.init()
        MainGame.window=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('坦克大战')
        self.creatMyTank()
        self.creatEnemyTank()
        self.creatWalls()
        # 加载背景音乐
        pygame.mixer.music.load("tank_img/bg2.ogg")
        # 循环播放背景音乐
        pygame.mixer.music.play(-1)
        while True:
            MainGame.window.fill((0,0,0))
            self.deal_even()
            self.loadMyTank()
            self.loadEnemyTank()
            self.loadBomb()
            self.loadWall()
            pygame.display.update()
            time.sleep(0.03)

    #键盘事件处理
    def deal_even(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("点击关闭窗口按钮")
                sys.exit()  # 关闭程序
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    print('左移')
                elif event.key==pygame.K_RIGHT:
                    print('右移')
                elif (event.key == pygame.K_h) or (event.key==pygame.K_SPACE):
                    if self.P1!=None:
                        self.P1.fire()

    #游戏结束方法
    def game_over_func(self):
        gameover=pygame.image.load("tank_img\over.gif")
        rect = gameover.get_rect()
        rect.x=SCREEN_WIDTH//2
        rect.y = SCREEN_HEIGHT // 2
        MainGame.window.blit(gameover, rect)
        self.game_over -= 1
        if self.game_over == 0:
            self.creatMyTank()
            self.game_over=150
        elif self.game_over == 149:
            boom_sound = pygame.mixer.Sound("tank_img/gameover.wav")
            # 播放音效
            boom_sound.play()


#基本坦克类
class Tank:
    def __init__(self,x,y):
        self.speed=3
        self.isAlive=True
        self.images = {'U': pygame.image.load("tank_img\enemy1U.gif"),
                       'D': pygame.image.load("tank_img\enemy1D.gif"),
                       'L': pygame.image.load("tank_img\enemy1L.gif"),
                       'R': pygame.image.load("tank_img\enemy1R.gif")}
        self.direction='U'
        self.image=self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.stop=False
        self.bullet_list=[]
        self.bullet_num=2
        self.hp = 1

    #基类坦克移动
    def move(self):
        if self.stop:
            pass
        else:
            tempx=self.rect.x
            tempy = self.rect.y
            if self.direction=='U':
                if self.rect.y>0 :
                    self.rect.y-=self.speed

            elif self.direction=='D':
                if self.rect.y<SCREEN_HEIGHT-self.rect.height :
                    self.rect.y+=self.speed

            elif self.direction=='L':
                if self.rect.x>0 :
                    self.rect.x-=self.speed

            elif self.direction=='R':
                if self.rect.x<SCREEN_WIDTH-self.rect.width:
                    self.rect.x+=self.speed

            for i in MainGame.walls_list:
                if not isinstance(i, Green_Wall):
                    if pygame.Rect.colliderect(self.rect, i.rect):
                        self.rect.x=tempx
                        self.rect.y=tempy
                        break

    #基类坦克开火
    def fire(self):
        if len(self.bullet_list)<self.bullet_num:
            bullet = Bullet(self)
            self.bullet_list.append(bullet)

    #刷新基类坦克
    def displayTank(self):
        self.image=self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


#我方坦克类
class MyTank(Tank):
    def __init__(self,x,y):
        super(MyTank,self).__init__(x,y)
        self.speed=5
        self.bullet_num = 3
        self.images = {'U': pygame.image.load("tank_img\p1tankU.gif"),
                       'D': pygame.image.load("tank_img\p1tankD.gif"),
                       'L': pygame.image.load("tank_img\p1tankL.gif"),
                       'R': pygame.image.load("tank_img\p1tankR.gif")}

    #我方坦克移动
    def move(self):
        '''我方坦克移动方法'''
        key_statu=pygame.key.get_pressed()
        if key_statu[pygame.K_w] or key_statu[pygame.K_UP]:
            self.direction='U'
            super(MyTank, self).move()
        elif key_statu[pygame.K_s] or key_statu[pygame.K_DOWN]:
            self.direction='D'
            super(MyTank, self).move()
        elif key_statu[pygame.K_a] or key_statu[pygame.K_LEFT]:
            self.direction='L'
            super(MyTank, self).move()
        elif key_statu[pygame.K_d] or key_statu[pygame.K_RIGHT]:
            self.direction='R'
            super(MyTank, self).move()

    #我方坦克刷新
    def displayTank(self):
        super(MyTank, self).displayTank()
        if len(self.bullet_list)!=0:
            for bullet in self.bullet_list:
                if bullet.isAlive:
                    bullet.hitEnemy()
                    bullet.hitWall()
                    bullet.move()
                    bullet.displayBullet()
                else:
                    self.bullet_list.remove(bullet)


#敌方坦克类
class EnemyTank(Tank):
    def __init__(self,x,y):
        super(EnemyTank,self).__init__(x,y)
        self.speed=4
        self.step=random.randint(5,20)
        self.fire_count=random.randint(20,50)

    #敌方坦克移动
    def move(self):
        if self.step>0:
            super(EnemyTank, self).move()
            self.step-=1
        else:
            self.direction=random.choice(['U','D','L','R'])
            self.stop=random.choice([0,0,0,0,1])
            self.step = random.randint(10, 50)
            self.speed = random.randint(3, 6)
            super(EnemyTank, self).move()

    #敌方坦克开火
    def fire(self):
        if self.fire_count==0:
            super(EnemyTank, self).fire()
            self.fire_count = random.randint(30, 100)
        else:
            self.fire_count-=1

    #敌方坦克刷新
    def displayTank(self):
        super(EnemyTank, self).displayTank()
        if len(self.bullet_list)!=0:
            for bullet in self.bullet_list:
                if bullet.isAlive:
                    bullet.hitMyTank()
                    bullet.hitWall()
                    bullet.move()
                    bullet.displayBullet()
                else:
                    self.bullet_list.remove(bullet)

class Boss(EnemyTank):
    def __init__(self,x,y):
        super(Boss,self).__init__(x,y)
        self.fire_count = random.randint(10, 30)
        self.bullet_num = 5
        self.hp = 12
        self.images = {'U': pygame.image.load("tank_img\enemy3U.gif"),
                       'D': pygame.image.load("tank_img\enemy3D.gif"),
                       'L': pygame.image.load("tank_img\enemy3L.gif"),
                       'R': pygame.image.load("tank_img\enemy3R.gif")}

    # boss坦克移动
    def move(self):
        if self.step > 0:
            super(EnemyTank, self).move()
            self.step -= 1
        else:
            self.direction = random.choice(['U', 'D', 'L', 'R'])
            self.stop = random.choice([0, 0, 0, 0, 1])
            self.step = random.randint(5, 30)
            self.speed = random.randint(4, 8)
            super(EnemyTank, self).move()

    # boss坦克开火
    def fire(self):
        if self.fire_count == 0:
            super(EnemyTank, self).fire()
            self.fire_count = random.randint(5, 30)
        else:
            self.fire_count -= 1


#子弹类
class Bullet:
    def __init__(self,tank):
        self.image=pygame.image.load("tank_img/tankmissile.gif")
        self.isAlive=True
        self.speed=8
        self.direction=tank.direction
        self.rect=self.image.get_rect()
        self.rect.x=tank.rect.centerx-self.rect.width//2
        self.rect.y = tank.rect.centery-self.rect.height//2

    #子弹刷新
    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)

    #子弹移动
    def move(self):
        if self.direction=='U':
            if self.rect.y>-self.rect.height//2 :
                self.rect.y-=self.speed
            else:
                self.isAlive=False
        elif self.direction=='D':
            if self.rect.y<SCREEN_HEIGHT :
                self.rect.y+=self.speed
            else:
                self.isAlive=False
        elif self.direction=='L':
            if self.rect.x>-self.rect.width//2 :
                self.rect.x-=self.speed
            else:
                self.isAlive=False
        elif self.direction=='R':
            if self.rect.x<SCREEN_WIDTH :
                self.rect.x+=self.speed
            else:
                self.isAlive=False

    #子弹消失
    def __del__(self):
        print('删除子弹')

    #射中敌军
    def hitEnemy(self):
        if len(MainGame.enemy_list)!=0:
            for tank in MainGame.enemy_list:
                if pygame.sprite.collide_circle(self,tank):
                    self.isAlive=False
                    tank.hp-=1
                    if tank.hp==0:
                        tank.isAlive=False
                        bomb = Bomb(tank)
                        MainGame.bomb_list.append(bomb)

    #射中我军
    def hitMyTank(self):
        if MainGame.P1!=None:
            if pygame.sprite.collide_circle(self, MainGame.P1):
                bomb = Bomb(MainGame.P1)
                MainGame.bomb_list.append(bomb)
                self.isAlive = False
                MainGame.P1.isAlive = False

    #射中墙体h
    def hitWall(self):
        if len(MainGame.walls_list) != 0:
            for wall in MainGame.walls_list:
                if (not isinstance(wall,Green_Wall)) and (not isinstance(wall,Water_Wall)):
                    if pygame.Rect.colliderect(self.rect, wall.rect):
                        if isinstance(wall,Steels_Wall):
                            self.isAlive = False
                        else:
                            self.isAlive = False
                            wall.hp-=1


#墙壁类
class Wall:
    def __init__(self,x,y):
        self.hp=5
        self.isAlive=True
        self.status = 'A'
        self.images = {'A': pygame.image.load("tank_img\walls.gif"),
                       'B': pygame.image.load("tank_img\wall.gif")}
        self.image=self.images[self.status]
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    #刷新墙体
    def displayWall(self):
        if 0<self.hp<4:
            self.status='B'
        elif 3<self.hp<6:
            self.status = 'A'
        elif self.hp==0:
            self.isAlive=False
        oldx=self.rect.x
        oldy=self.rect.y
        self.image = self.images[self.status]
        self.rect = self.image.get_rect()
        self.rect.x=oldx
        self.rect.y = oldy
        MainGame.window.blit(self.image, self.rect)

#草地类
class Green_Wall(Wall):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.image=pygame.image.load("tank_img\grass.png")
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    #刷新墙体
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)

#钢墙类
class Steels_Wall(Wall):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.image=pygame.image.load("tank_img\steels.gif")
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    #刷新墙体
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)

#河流类
class Water_Wall(Wall):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.image=pygame.image.load("tank_img\water.gif")
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    #刷新墙体
    def displayWall(self):
        MainGame.window.blit(self.image, self.rect)

#爆炸类
class Bomb:
    def __init__(self,tank):
        self.images=[pygame.image.load("tank_img/blast0.gif"),
                     pygame.image.load("tank_img/blast1.gif"),
                     pygame.image.load("tank_img/blast2.gif"),
                     pygame.image.load("tank_img/blast3.gif"),
                     pygame.image.load("tank_img/blast4.gif"),
                     pygame.image.load("tank_img/blast3.gif")]
        self.image_index=0
        self.image=self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.centerx - self.rect.width // 2
        self.rect.y = tank.rect.centery - self.rect.height // 2
        self.isAlive=True
        self.wait=2
        boom_sound = pygame.mixer.Sound("tank_img/blast.wav")
        # 播放音效
        boom_sound.play()

    #刷新爆炸
    def displayBomb(self):
        if self.image_index<len(self.images):
            self.image=self.images[self.image_index]
            self.wait-=1
            if self.wait==0:
                self.image_index+=1
                self.wait=2
            MainGame.window.blit(self.image,self.rect)
        else:
            self.isAlive=False
            self.image_index=0

game=MainGame()
game.start_game()