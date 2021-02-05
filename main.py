import os
import constants
import math
import random
import pygame
import numpy as np

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (630,30)
pygame.init()
screen = pygame.display.set_mode((constants.display_width, constants.display_height))
pygame.display.set_caption('Stellar Mass Density')
screen.fill(constants.background)
font = pygame.font.SysFont(None, 20)
img = font.render('Generating Galaxy', True, constants.black, constants.background)
screen.blit(img, (20, 20))

pygame.display.flip()

img = font.render('%', True, constants.black, constants.background)

maparray = np.zeros((constants.map_size, constants.map_size, 3))
for x in range(0, constants.map_size):

    if x % 100 == 0:
        screen.blit(img, (x/10+150, 20))
        pygame.display.update()

    for y in range(0, constants.map_size):

        mapX = x*constants.map_scale+constants.map_scale/2
        mapY = y*constants.map_scale+constants.map_scale/2

        xDFC = mapX - constants.galaxy_size/2
        yDFC = mapY - constants.galaxy_size/2
        dfc = math.sqrt(xDFC * xDFC + yDFC * yDFC)
        dCore = 1 - pow(dfc/(constants.core_radius),2)

        aArm = math.atan2(yDFC,xDFC)
        dArm = (pow(math.e,dfc/100000)*0.5*pow(math.sin((pow(0.5*dfc,0.35)-aArm)),2)+0.5-dfc/1000000)
        dArm = dArm*(1-2*dfc/constants.galaxy_size)

        density = dCore
        if dArm > dCore: density = dArm
        if density < 0: density = 0
        if density > 1: density = 1
        density = 255 - int((2.55*density*78*(1+2.2*pow(random.random()-0.5,3))))

        #if ((mapX-50)%1000==0 and (mapY-50)%1000==0):
        #    print(str(mapX-50)+" "+str(mapY-50)+"     dfc: "+str(int(dfc))+"     density: "+str(density))

        dInt = int(density)
        maparray[x][y].fill(dInt)
        if dInt==255:
            maparray[x][y] = (constants.background)

        if dfc < constants.core_radius:
            dGalCore = 255* (1 - dfc/constants.core_radius)
            dGreater = dInt;
            if dGalCore > dInt: dGreater = dGalCore
            maparray[x][y] = (dGreater, dInt, dInt)

mapRect = pygame.Rect(0,0,constants.map_size,constants.map_size)
mapSurf = screen.subsurface(mapRect)
pygame.surfarray.blit_array(mapSurf, maparray)

for si in range(0,5):
    pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(0, 200 * si, 1, 100), width=1)
    pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(200 * si, 1, 100, 1), width=1)

    pygame.draw.rect(screen, pygame.Color(constants.blue), pygame.Rect(0, 200 * si + 100, 1, 100), width=1)
    pygame.draw.rect(screen, pygame.Color(constants.blue), pygame.Rect(200 * si + 100, 1, 100, 1), width=1)

pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(1050, 950, 100, 1), width=1)

img = font.render(str(constants.galaxy_size//10)+" light years", True, constants.black, constants.background)
screen.blit(img, (1050, 970))

pygame.display.flip()


mmPixSiz = 11
mps = mmPixSiz*mmPixSiz

closed = False
while not closed:
    for event in pygame.event.get():
        posX = pygame.mouse.get_pos()[0]
        posY = pygame.mouse.get_pos()[1]
        if posX > mmPixSiz//2-1 and posX < constants.map_size - mmPixSiz//2 and posY > mmPixSiz//2-1 and posY < constants.map_size - mmPixSiz//2:
            rect = pygame.Rect(posX-mmPixSiz//2, posY-mmPixSiz//2, mmPixSiz, mmPixSiz)
            # copy the part of the screen
            sub = screen.subsurface(rect)
            # create another surface with dimensions
            # This is done to unlock the screen surface
            screenshot = pygame.Surface((mmPixSiz, mmPixSiz))
            screenshot.blit(sub, (0, 0))
            screenshot = pygame.transform.scale(screenshot, (mps, mps))
            screen.blit(screenshot,(constants.mmxoff,constants.mmyoff+20))

            plabel = font.render('Position: '+str(posX)+","+str(posY)+"        ", True, constants.black, constants.background)
            screen.blit(plabel, (constants.mmxoff, 10))

            decDen = round((255-(maparray[posX][posY][2]))/2.55,2)

            finDen = decDen
            posXDFC = posX - constants.map_size/2
            posYDFC = posY - constants.map_size/2
            posDFC = math.sqrt(posXDFC * posXDFC + posYDFC * posYDFC)

            if posDFC < constants.core_radius/constants.map_scale and maparray[posX][posY][0] > maparray[posX][posY][1]:
                finDen = constants.core_radius/constants.map_scale - posDFC + decDen
            coreMapRad = (constants.core_radius/2)/constants.map_scale
            if posDFC < coreMapRad:
                finDen = 10000 * (1 - pow(posDFC/coreMapRad,2)) - decDen
            if posDFC < coreMapRad/2:
                finDen = 60000 * (1 - pow(posDFC/(coreMapRad/2),2)) - decDen


            finDen = round(finDen,2)
            dlabel = font.render('Density:  '+str(finDen)+"                   ", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps+40))

            dlabel = font.render("units:", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 80))
            dlabel = font.render("1000s of stars", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 120))
            dlabel = font.render("----------", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 140))
            dlabel = font.render("100^3 light year pixel volume", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 160))

            #print("          ")
            #print(str(posDFC))
            #print(str(finDen))

            pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(constants.mmxoff+mps//2-mmPixSiz//2, constants.mmyoff+mps//2-mmPixSiz//2+20, mmPixSiz, mmPixSiz), width=1)
            pygame.display.flip()

        if event.type == pygame.QUIT:
            closed = True
pygame.quit()
quit()