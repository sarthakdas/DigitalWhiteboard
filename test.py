import cwiid
import time

print "Press 1+2 on the Wiimote now"
try:
    wiimote = cwiid.Wiimote()
except:
    print("error")

#Rumble to indicate a connection
wiimote.rumble = 1
print "Connection established"
time.sleep(0.2)
wiimote.rumble = 0

#Sets up reporting mode
wiimote.enable(cwiid.FLAG_MESG_IFC)
wiimote.rpt_mode = cwiid.RPT_ACC | cwiid.RPT_BTN | cwiid.RPT_IR

while True:
    messages = None
    time.sleep(1)
    messages = wiimote.get_mesg()
    print messages
    for mesg in messages:
        print("======================")
        #Detects whether HOME is held down and if they are it quits the program
        if mesg[0] == cwiid.MESG_BTN:
            if mesg[1] & cwiid.BTN_HOME:
                print "Ending Program"
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
