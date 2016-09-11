# coding:utf-8

import socket
import qrcode
import time
import pygame
# 导入pygame库
from pygame.locals import *
# 导入一些常用的函数和常量
from sys import exit

# 向sys模块借一个exit函数用来退出程序

problem = []
answer = []
f = open('problems.txt', 'r')
s = f.read()
start = 0
while True:
    start = s.find('\n', start)
    if start == -1:
        break
    end = s.find('答案', start)
    problem.append(s[start:end])
    start = end
f.close()

f = open('answer.txt', 'r')
for s in f.readlines():
    answer.append(s)
f.close()

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
# 初始化pygame,为使用硬件做准备
addr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
# 获取IP
clock_sound = pygame.mixer.Sound('dida.wav')
end_sound = pygame.mixer.Sound('end.wav')
web = pygame.mixer.Sound('qd.wav')
background_image_filename = '0.png'
# mouse_image_filename = 'touch.jpg'
# 指定图像文件名称
w = 1024
h = 768

screen = pygame.display.set_mode((w, h), 0, 32)
# 创建了一个窗口
pygame.display.set_caption('答题系统')
# 设置窗口标题
fontp = pygame.font.Font('myfont.ttf', 20)
# fontp.set_bold(True)
font = pygame.font.Font('myfont.ttf', 30)
font1 = pygame.font.Font('myfont.ttf', 50)

background = pygame.image.load(background_image_filename).convert()
# mouse_cursor = pygame.image.load(mouse_image_filename).convert_alpha()
clock = pygame.image.load('clock.jpg').convert_alpha()
img = qrcode.make("http://" + addr + ":8000/")
img.save('qr.png')
qrimage = pygame.image.load('qr.png').convert_alpha()
# 加载并转换图像
Fullscreen = False

di = 30
i = di
problemid = 0
turnid = 0
x = 150
y = 150
now = time.time()
split = 32

starttag = True
while starttag:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                starttag = not starttag
            if event.key == K_f:
                Fullscreen = not Fullscreen
                if Fullscreen:
                    screen = pygame.display.set_mode((w, h), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode((w, h), 0, 32)
    screen.blit(background, (0, 0)) #启动画面
    #tmp = font1.render(u"扫描二维码进入抢答系统", True, (255, 255, 255))
    tmp = font1.render(u"Author:AIRobot", True, (255, 255, 255))
    screen.blit(tmp,(300,200))
    #screen.blit(qrimage,(300,300))
    pygame.display.update()

while True:
    tag = 0
    qiangda = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            # 接收到退出事件后退出程序
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                i = di
                tag = 1
                end_sound.play(0)
            if event.key == K_f:
                Fullscreen = not Fullscreen
                if Fullscreen:
                    screen = pygame.display.set_mode((w, h), FULLSCREEN, 32)
                else:
                    screen = pygame.display.set_mode((w, h), 0, 32)
    screen.blit(background, (0, 0))
    # 将背景图画上去

    if i == 0:
        text_surface = font1.render(u"0!", True, (0, 255, 0))
        i = di
        tag = 1
        end_sound.play(0)
    elif tag == 0:
        text_surface = font1.render(str(i), True, (255, 0, 0))
    text_answer = font1.render(answer[problemid].decode('utf-8'), True, (255, 255, 255))

    p_split = problem[problemid].split('\n')
    y = 120
    for line in p_split:
        text_problem = fontp.render(line.decode('utf-8'), True, (255, 255, 255))
        screen.blit(text_problem, (50, y))
        y += 30
    while True:
        try:
            f = open('tag.txt', 'r')
        except:
            continue
        break 
    if int(f.read()) == -1:
        qiangda = 1
        tag = 1
        i = di
        web.play(0)
    f.close()
    if tag == 0:
        screen.blit(clock, (w - 200, 25))
        if i > 9:
            screen.blit(text_surface, (w - 175, 50))
        else:
            screen.blit(text_surface, (w - 160, 50))
        pygame.display.update()
        if time.time() - now > 1:
            now = time.time()
            i -= 1
            clock_sound.play(0)
    elif tag == 1:
        label = 0
        goon = 0
        while label == 0:
            screen.blit(clock, (w - 200, 25))
            screen.blit(text_surface, (w - 175, 50))
            if qiangda == 0:
                screen.blit(text_answer, (200, 600))
            elif qiangda == 1:
                while True:
                    try:
                        f = open('no.txt', 'r')
                    except:
                        continue
                    break
                no = f.read()
                f.close()
                while True:
                    try:
                        f = open('tag.txt', 'w')
                    except:
                        continue
                    break
                f.write('-1')
                f.close()
                declare = font1.render((no + '抢答成功！').decode('utf-8'), True, (255, 255, 255))
                screen.blit(declare, (100, 50))
                if goon == 1:
                    screen.blit(text_answer, (200, 600))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    # 接收到退出事件后退出程序
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if problemid < 39:
                            if goon == 0:
                                goon = 1
                            elif goon == 1:
                                label = 1
                                problemid += 1
                                while True:
                                    try:
                                        f = open('tag.txt', 'w')
                                    except:
                                        continue
                                    break
                                f.write('1')
                                f.close()
                        else:
                            while True:
                                try:
                                    f = open('tag.txt', 'w')
                                except:
                                    continue
                                break
                            f.write('0')
                            f.close()
                            screen.blit(text_answer, (200, 600))
                            pygame.display.update()
                            while True:
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        exit()
                                    if event.type == KEYDOWN:
                                        exit()

    tag = 0
