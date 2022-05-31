import wiiremote
import pygame
import GUIcomponents as GUI
import time
import sys

#Initialises pygame library
pygame.init()
appDisplay = pygame.display.set_mode((1000,1000))
pygame.display.set_caption('Digital Whiteboard')
pygame.display.update()

#Constant declerations
def Title_to_screen(msg,color):
    screen_text = Title_font.render(msg, True, color)
    appDisplay.blit(screen_text, [500,500])

def Caption_to_screen(msg,color):
    screen_text = Caption_font.render(msg, True, color)
    appDisplay.blit(screen_text, [500,600])
    
gameExit = False
calibrated = False
clock = pygame.time.Clock()
Title_font = pygame.font.SysFont(None,50)
Caption_font = pygame.font.SysFont(None,25)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)

#Initialises conncetion with the wiiremote
appDisplay.fill(white)
Title_to_screen("Connect to Wiiremote",black)
Caption_to_screen("Press 1 + 2 on the remote",red)
pygame.display.update()
time.sleep(1)
wii = wiiremote.init()
try:
    if not wii:
        appDisplay.fill(white)
        Title_to_screen("Connection Not Sucessful",red)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        quit()
finally:
    appDisplay.fill(white)
    Title_to_screen("Success",green)
    pygame.display.update()
    time.sleep(1)



#Main loop
while not gameExit:
    #Homography calibration for projector-sensor
    while not calibrated:
        appDisplay.fill(white)
        #Generation of 4 target markers
        pygame.draw.rect(appDisplay,red, [50,50,25,25])
        pygame.draw.rect(appDisplay,red, [50,1000-75,25,25])
        pygame.draw.rect(appDisplay,red, [1000-75,1000-75,25,25])
        pygame.draw.rect(appDisplay,red, [1000-75,50,25,25])
        Title_to_screen("Callibration Mode",black)
        Caption_to_screen("Tap the green squares with the pen",black)
        pygame.display.update()
        
        #Marker one callibration (Top-Left)
        pygame.draw.rect(appDisplay,green, [50,50,25,25])
        pygame.display.update()
        #Checks for next IR spot
        IR = False
        while not IR:
            IRdata= wiiremote.event(wii,pygame)
            print(IRdata)
            if IRdata != None:
                IR_coord1 = IRdata
                IR = True
        pygame.draw.rect(appDisplay,red, [50,50,25,25])
        pygame.display.update()
        print("=================================")
        
        #Sleep used to prevent a long press from being registered
        time.sleep(1)
        
        #Marker two callibration (Top-Right)
        pygame.draw.rect(appDisplay,green, [50,1000-75,25,25])
        pygame.display.update()
        #Checks for next IR spot
        IR = False
        while not IR:
            IRdata = wiiremote.event(wii,pygame)
            print(IRdata)
            if IRdata != None:
                IR_coord2 = IRdata
                IR = True
        pygame.draw.rect(appDisplay,red, [50,1000-75,25,25])
        pygame.display.update()
        print("=====================================================")
        
        pygame.display.update()
        calibrated = True
        
        appDisplay.fill(white)
        Title_to_screen("Calibration Success",green)
        pygame.display.update()
        time.sleep(1)
        sys.stdout.flush()
        appDisplay.fill(white)
        pygame.display.update()
    
    #Gets all events e.g keyboard,mouse 
    for event in pygame.event.get():
        #Checks if the 'X' button has been pressed then exits     
        if event.type == pygame.QUIT:
            gameExit = True
    #print(wiiremote.event(wii,pygame))
    
    
    
    #Updates the app display
    pygame.display.update()
    clock.tick(100)

Title_to_screen("Quit",red)
pygame.display.update()
time.sleep(2)

pygame.quit()
quit()