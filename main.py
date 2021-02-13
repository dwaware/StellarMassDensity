import constants
import os
import math
import random
import pygame
import numpy as np

random.seed("seed_here",2)

# create/init the pygame SDL window components
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (630,30)
pygame.init()
screen = pygame.display.set_mode((constants.display_width, constants.display_height))
pygame.display.set_caption('Stellar Mass Density')
screen.fill(constants.background)

# create some splash text
font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
img = font.render('Generating Galaxy', True, constants.black, constants.background)
screen.blit(img, (20, 20))

# update the screen to reflect the above
pygame.display.flip()

# while the image data is being prepared, we need a progress marker:
img = font.render('%', True, constants.black, constants.background)

# our maparray consists is the same size as our map display, one pixel for each "density" cell
# we store color data so initialize 3 "zeros" wide
maparray = np.zeros((constants.map_size, constants.map_size, 3))
for x in range(0, constants.map_size):

    #while the map data is being generated, stop every so often to add a progress marker to the screen
    if x % (constants.map_size//10) == 0:
        screen.blit(img, (x/10+150, 20))
        pygame.display.update()

    for y in range(0, constants.map_size):

        #formulate the actual density values inside the x and y loop:
        #convert from a zero-based starting point (our screen) to a zero = map center reference frame
        mapX = x*constants.map_scale+constants.map_scale/2
        mapY = y*constants.map_scale+constants.map_scale/2

        #calculate the distance from the center of the map
        xDFC = mapX - constants.galaxy_size/2
        yDFC = mapY - constants.galaxy_size/2
        dfc = math.sqrt(xDFC * xDFC + yDFC * yDFC)

        #assign a decaying density value as distance approaches the edge of the core
        dCore = 1 - pow(dfc/(constants.core_radius),2)

        #now consider the arms--one of the components of arm density will be an atan function
        aArm = math.atan2(yDFC,xDFC)

        #using a decaying exponential curve and a rotating sin and atan component (from above) as well
        dArm = (pow(math.e,dfc/constants.galaxy_size)*0.5*pow(math.sin((pow(0.5*dfc,0.35)-aArm)),2)+0.5-dfc/(100*constants.galaxy_size))

        #dampen residual values down to zero as they approach the edge
        dArm = dArm*(1-2*dfc/constants.galaxy_size)

        #get ready to assgin density, with the assumption that if the core is more dense than the arm, we'll use the core value
        density = dCore
        if dArm > dCore: density = dArm
        if density < 0: density = 0
        if density > 1: density = 1

        #take the above value from 0 to 1 and multiply by 255 (color range) while also adding in noise
        density = 255 - int((2.55*density*78*(1+2.2*pow(random.random()-0.5,3))))

        #take the resulting int
        dInt = int(density)

        #fill the array with the initial dInt value
        maparray[x][y].fill(dInt)

        #if the value is empty/no stars, set the map array to our background color
        if dInt==255:
            maparray[x][y] = (constants.background)

        #if the distance is within the core radius, boost the core value and compare it to the original value of dInt
        if dfc < constants.core_radius:
            dGalCore = 255* (1 - dfc/constants.core_radius)
            dGreater = dInt;

            #if the core value is higher, set the red component to highlight that this is a core zone
            if dGalCore > dInt: dGreater = dGalCore

            #this will ensure that the overall density ramps up toward the core, as it should
            maparray[x][y] = (dGreater, dInt, dInt)

#create a rect to blit the map too
map_offset = (constants.display_height-constants.map_size)//2;
mapRect = pygame.Rect(map_offset,map_offset,constants.map_size,constants.map_size)

#put the rect on the surface
mapSurf = screen.subsurface(mapRect)

#blit to the screen
pygame.surfarray.blit_array(mapSurf, maparray)

#draw some distance rulers on the left side and bottom of the map
for si in range(0,5):
    pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(0, 200 * si, 1, 100), width=1)
    pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(200 * si, 0, 100, 1), width=1)

    pygame.draw.rect(screen, pygame.Color(constants.blue), pygame.Rect(0, 200 * si + 100, 1, 100), width=1)
    pygame.draw.rect(screen, pygame.Color(constants.blue), pygame.Rect(200 * si + 100, 0, 100, 1), width=1)

#add a distance ruler legand based on galaxy size
pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(1050, 950, 100, 1), width=1)

#add legend text
img = font.render(str(constants.galaxy_size//10)+" light years", True, constants.black, constants.background)
screen.blit(img, (1050, 970))

#apply updates to the screen
pygame.display.flip()

#create a minimap

#each pixel is enlarged by a factor of mmPixSize
mmPixSiz = 11

#note the square of this value for later use
mps = mmPixSiz*mmPixSiz

#assume the main window is open (not closed) by default
closed = False

#while the window is open:
while not closed:

    #check for events
    for event in pygame.event.get():

        #get the mouse position
        posX = pygame.mouse.get_pos()[0]
        posY = pygame.mouse.get_pos()[1]

        #if them mouse position is inside the map, within the marget of mmPixSiz//2
        if posX > mmPixSiz//2-1 and posX < constants.map_size - mmPixSiz//2 and posY > mmPixSiz//2-1 and posY < constants.map_size - mmPixSiz//2:

            #create a small rect of width and height mmPixSiz
            rect = pygame.Rect(posX-mmPixSiz//2, posY-mmPixSiz//2, mmPixSiz, mmPixSiz)

            #copy the part of the screen
            sub = screen.subsurface(rect)

            #create another surface with the same dimensions
            #This is done to unlock the screen surface
            screenshot = pygame.Surface((mmPixSiz, mmPixSiz))

            #blit the image on the surface
            screenshot.blit(sub, (0, 0))

            #scale up the image
            screenshot = pygame.transform.scale(screenshot, (mps, mps))

            #blit the larger image onto the screen to create a mini-map effect
            screen.blit(screenshot,(constants.mmxoff,constants.mmyoff+20))

            #add some text to describe where the mini-map is referencing
            plabel = font.render('Position: '+str(posX)+","+str(posY)+"        ", True, constants.black, constants.background)
            screen.blit(plabel, (constants.mmxoff, 10))

            #convert the 255-based color density to decimal density, from 0-99
            decDen = round((255-(maparray[posX][posY][2]))/2.55,2)

            #create a final density based on the decimal density
            finDen = decDen

            #check where the cell is on the map
            posXDFC = posX - constants.map_size/2
            posYDFC = posY - constants.map_size/2
            posDFC = math.sqrt(posXDFC * posXDFC + posYDFC * posYDFC)

            #if the distance from the center is within the core radius and our core density value (red) is higher...
            if posDFC < constants.core_radius/constants.map_scale and maparray[posX][posY][0] > maparray[posX][posY][1]:
                #...modify the final density
                finDen = constants.core_radius/constants.map_scale - posDFC + decDen

            #now check if we are are within half the radius of the core size, halfCoreMapRad
            halfCoreMapRad = (constants.core_radius/2)/constants.map_scale

            #if so, bump up the density
            if posDFC < halfCoreMapRad and maparray[posX][posY][0] > maparray[posX][posY][1]:
                finDen = 5000 * (1 - pow(posDFC/halfCoreMapRad,2)) + decDen/2

            #half the size again, and if we are within that even smaller distance, bump up density even more
            if posDFC < halfCoreMapRad/2:
                finDen = 25000 * (1 - pow(posDFC/(halfCoreMapRad/2),2)) + decDen/2

            #provide some textual data on screen relating to density
            scaledFinDen = int(80*finDen)
            dlabel = font.render('Density:  '+str(scaledFinDen)+"                   ", True, constants.black, constants.background)

            print("x y and density:  "+str(posX)+" "+str(posY)+" "+str(scaledFinDen)+" ")

            screen.blit(dlabel, (constants.mmxoff, mps+40))

            dlabel = font.render("units:", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 80))
            dlabel = font.render("stars", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 120))
            dlabel = font.render("----------", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 140))
            dlabel = font.render("100^3 light year pixel volume", True, constants.black, constants.background)
            screen.blit(dlabel, (constants.mmxoff, mps + 160))

            #add a higlight to the central pixel of the mini map
            pygame.draw.rect(screen, pygame.Color(constants.red), pygame.Rect(constants.mmxoff+mps//2-mmPixSiz//2, constants.mmyoff+mps//2-mmPixSiz//2+20, mmPixSiz, mmPixSiz), width=1)
            pygame.display.flip()

        #if the user quits, close the window and exit
        if event.type == pygame.QUIT:
            closed = True
pygame.quit()
quit()