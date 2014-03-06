# Perimetri
#
# Art installation by Catodo and Lorenzo Kamerlengo
# MutaForma 2014 - Francavilla al Mare (Italy)
# (C) Copyright 2014 iamcatodo@gmail.com

from random import randint
import pygame, sys, random, re
import os.path, glob
from pygame.locals import *
import pygame.gfxdraw
from subprocess import call

WIDTH = 1024
HEIGHT = 768
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

path = os.path.abspath("img")
files = glob.glob(os.path.join(path, "*.png"))

pygame.init()
#screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 16)

images = []
for f in files:
    if re.search("[0-9]+\.png$", f):
        images.append(pygame.image.load(f).convert_alpha())

if not os.path.exists(os.path.join(path, "background.png")):
    label = myfont.render("Mapping... 'c' to close the polygon, 'q' to exit", 2, (255,255,255))
    screen.blit(label, (10, 18))
    pygame.display.flip()
    
    polygon = []
    points = []

    ismapping = 1
    while ismapping == 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    ismapping = 0
                    mapping = pygame.display.set_mode((WIDTH,HEIGHT))
                    mapping.convert_alpha()
                    for point in points:
                        pygame.gfxdraw.filled_polygon(mapping, point, WHITE)
                    pygame.image.save(mapping, os.path.join(path, "mapping.png"))
                    # convert transparent color using imagemagick
                    call(["convert", os.path.join(path, "mapping.png"), "-transparent", "rgb{0}".format(WHITE).replace(' ', ''), os.path.join(path,"background.png")])
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_c:
                    pygame.draw.lines(screen, GREEN, True, polygon)
                    pygame.display.flip()
                    points.append(polygon)
                    polygon = []


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()      
                pygame.draw.circle(screen, GREEN, pos, 4)
                pygame.display.flip()
                polygon.append(pos)

else:
    background= pygame.image.load(os.path.join(path, "background.png")).convert_alpha()

pygame.mouse.set_visible(False)

while 1:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    screen.fill((0,0,0))

    for img in images:
        x = randint(0,WIDTH/2)
        y = randint(0,HEIGHT/2)
        img.set_alpha(randint(150,230))
        xs = randint(x,WIDTH)
        ys = randint(y,y+100)
        screen.blit(img, (x,y), (x,y,xs,ys))
    
        if 'background' in globals():
            screen.blit(background, (0,0))

        pygame.display.update()
        clock.tick(1)

    pygame.display.flip()
    clock.tick(0.2)

