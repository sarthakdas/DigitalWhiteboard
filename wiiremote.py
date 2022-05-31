#Library for interacting witht the wiiremote
#Library for controlling time and sleep
import cwiid
import time
import pygame

def init():

    print "Press 1+2 on the Wiimote now"
    try:
        wiimote = cwiid.Wiimote()
    except:
        return False

    #Rumble to indicate a connection
    wiimote.rumble = 1
    print "Connection established"
    time.sleep(0.2)
    wiimote.rumble = 0

    #Sets up reporting mode
    wiimote.enable(cwiid.FLAG_MESG_IFC)
    wiimote.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_IR

    return wiimote


def event(wiimote,pygame):

    messages = wiimote.get_mesg()
    for mesg in messages:

        #Detects whether HOME isheld down and if they are it quits the program
        if mesg[0] == cwiid.MESG_BTN:
            if mesg[1] & cwiid.BTN_HOME:
                print "Ending Program"
                pygame.quit()
                quit()

        #Detects whether there is any visable IR points
        elif mesg[0] == cwiid.MESG_IR:
            sources = mesg[1]
            found = False
            #Loops through all the found IR points
            for spot in sources:
                if spot:
                    #Converts the grouped points into individual points
                    position = spot["pos"]
                    found = True
            if found:
                #Return the co-ordinate of the point as a truple
                return position
