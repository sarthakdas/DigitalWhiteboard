import wiiremote
import pygame
import GUIcomponents as GUI
import datahandle
import time
import sys
import random

#Initialises pygame library
pygame.init()
appDisplay = pygame.display.set_mode((1000,1000))
pygame.display.set_caption('Digital Whiteboard')
pygame.display.update()

#Constant declerations
def roundline(srf, color, start, end, radius=10):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int( start[0]+float(i)/distance*dx)
        y = int( start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)

#Title to the screen
def Title_to_screen(msg,color):
    screen_text = Title_font.render(msg, True, color)
    appDisplay.blit(screen_text, [500,500])

#Caption to the screen
def Caption_to_screen(msg,color):
    screen_text = Caption_font.render(msg, True, color)
    appDisplay.blit(screen_text, [500,600])

gameExit = False
calibrated = False
clock = pygame.time.Clock()
Title_font = pygame.font.SysFont(None,50)
Caption_font = pygame.font.SysFont(None,25)

posPrev = None
pointLast = False

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

#Initialises conncetion with the wiiremote
appDisplay.fill(white)
#Puts the title to the screen and the cpation and then refreshes it
Title_to_screen("Connect to Wiiremote",black)
Caption_to_screen("Press 1 + 2 on the remote",red)

pygame.display.update()
time.sleep(1)
wii = wiiremote.init()
try:
    if not wii:

        appDisplay.fill(white)
        #Puts the title to the screen and the cpation and then refreshes it
        Title_to_screen("Connection Not Sucessful",red)
        pygame.display.update()

        time.sleep(2)
        pygame.quit()
        quit()
finally:

    appDisplay.fill(white)
    #Puts the title to the screen and the cpation and then refreshes it
    Title_to_screen("Success",green)
    pygame.display.update()


    time.sleep(1)



#Main loop
while not gameExit:
    #Homography calibration for projector-sensor
    while not calibrated:
        appDisplay.fill(white)
        #Generation of 4 target markers
        pygame.draw.rect(appDisplay,red, [50,50,25,25])#top left
        pygame.draw.rect(appDisplay,red, [50,1000-75,25,25])#bottom left
        pygame.draw.rect(appDisplay,red, [1000-75,1000-75,25,25])#bottom right
        pygame.draw.rect(appDisplay,red, [1000-75,50,25,25])#top right
        Title_to_screen("Callibration Mode",black)
        Caption_to_screen("Tap the green squares with the pen",black)
        pygame.display.update()

        #Marker one callibration (Top-Left)
        pygame.draw.rect(appDisplay,green, [50,50,25,25])
        pygame.display.update()
        #Checks for next IR spot
        IR = False
        while not IR:
            #Gets the IR data
            IRdata= wiiremote.event(wii,pygame)
            #Checks that there was a visible IR point
            if IRdata != None:
                #Save the co-ordinate
                IR_coord1 = list(IRdata)
                IR = True

        pygame.draw.rect(appDisplay,red, [50,50,25,25])
        pygame.display.update()

        #Marker two callibration (Bottom-Left)
        pygame.draw.rect(appDisplay,green, [50,1000-75,25,25])
        pygame.display.update()
        #Checks for next IR spot
        IR = False
        while not IR:
            #Gets the IR data
            IRdata = wiiremote.event(wii,pygame)
            #Checks that there was a visible IR point
            if IRdata != None:
                #Saves the co-ordinate
                IR_coord2 = list(IRdata)
                #Checks that the co-ordinate if diffrent
                if datahandle.pointCompareY(IR_coord2, IR_coord1):
                    IR = True

        pygame.draw.rect(appDisplay,red, [50,1000-75,25,25])
        pygame.display.update()

        #Marker three callibration (Bottom-Right)
        pygame.draw.rect(appDisplay,green, [1000-75,1000-75,25,25])
        pygame.display.update()
        #Checks for next IR spot
        IR = False
        while not IR:
            IRdata = wiiremote.event(wii,pygame)
            if IRdata != None:
                IR_coord3 = list(IRdata)
                if datahandle.pointCompareX(IR_coord3, IR_coord2):
                    IR = True

        pygame.draw.rect(appDisplay,red, [1000-75,1000-75,25,25])
        pygame.display.update()

        #Marker four callibration (Top-Right)
        pygame.draw.rect(appDisplay,green, [1000-75,50,25,25])
        pygame.display.update

        #Checks for next IR spot
        IR = False
        while not IR:
            IRdata = wiiremote.event(wii,pygame)
            if IRdata != None:
                IR_coord4 = list(IRdata)
                if datahandle.pointCompareY(IR_coord4, IR_coord3):
                    IR = True

        pygame.draw.rect(appDisplay,red, [1000-75,50,25,25])
        pygame.display.update()
        pygame.display.update()

        appDisplay.fill(white)
        Title_to_screen("Calibration Success",green)
        pygame.display.update()

        appDisplay.fill(white)
        pygame.display.update()

        #Prints the edge co-ordinates
        print"============"
        print IR_coord1
        print IR_coord2
        print IR_coord3
        print IR_coord4
        print "==========="
        #gets the translationParameters
        translationParameters = datahandle.translationParameterGenerator(IR_coord1,IR_coord2,IR_coord3,IR_coord4)
        print translationParameters
        calibrated = True

    #gets the postion of the IR spot
    pos = wiiremote.event(wii,pygame)

    #Checks if there was a visible IR spot
    if pos != None:
        #Converts the point
        pos = datahandle.coordinateConverter(pos,translationParameters)
        color = black
        print pos
        #Plots the point
        pygame.draw.circle(appDisplay, color, pos, 10)
        pygame.display.update()
        pointLast = True


    #Gets all events e.g keyboard,mouse
    for event in pygame.event.get():
        #Checks if the 'X' button has been pressed then exits
        if event.type == pygame.QUIT:
            gameExit = True
    #print(wiiremote.event(wii,pygame))

    #Updates the app display
    pygame.display.update()
    clock.tick(2000)

Title_to_screen("Quit",red)
pygame.display.update()
time.sleep(2)


pygame.quit()
quit()
