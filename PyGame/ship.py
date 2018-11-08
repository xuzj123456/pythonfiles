# coding=utf-8
import sys
import pygame


class Settings():       #  存储设置的类

    def __init__(self):
        self.name = 'Alien Invasion'

        #   屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)     # 背景色

        # 飞船设置
        self.ship_speed = 1.5


class Ship():

    def __init__(self, screen, ai_settings):     # screen指定了飞船飞往的地方
        self.screen = screen        # 初始位置
        self.ai_settings = ai_settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(r'C:\Users\lenovo\Desktop\ship.jpg')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中存储小数值
        self.center = float(self.rect.centerx)

        # 移动标志
        self.moving_right = False
        self.moving_left = False

    def biltme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 根据移动标志调整飞船位置
        # 更新center值而不是rect
        if self.rect.right < self.screen_rect.right and self.moving_right:
            self.center += self.ai_settings.ship_speed
        if self.rect.left > 0 and self.moving_left:
            self.rect.centerx -= self.ai_settings.ship_speed

        # 根据self.center更新rect对象
        self.rect.centerx = self.center

class Game_Func():

    def check_events(self, ship):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()      # 若单机关闭按钮则退出

            elif event.type == pygame.KEYDOWN:      # 键盘按下
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    ship.moving_left = True

            elif event.type == pygame.KEYUP:        # 键盘抬起
                if event.key == pygame.K_RIGHT:
                    ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    ship.moving_left = False

    def update_screen(self, ai_settings, screen, ship):
        screen.fill(ai_settings.bg_color)  # 填充背景色
        ship.biltme()

        pygame.display.flip()  # 让最近绘制的屏幕可见


def run_game():
    pygame.init()       # 初始化游戏

    gf = Game_Func()

    ai_settings = Settings()

    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))       # 创建屏幕对象，制定窗口尺寸
    pygame.display.set_caption(ai_settings.name)        # 游戏名称

    ship = Ship(screen=screen, ai_settings=ai_settings)

    while True:     # 游戏主循环

        # 监视键盘和鼠标事件
        gf.check_events(ship=ship)
        ship.update()
        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship)


run_game()
