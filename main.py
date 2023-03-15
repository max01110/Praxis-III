'''
ESC204 - Evaporative Cooling Fridge

'''
# Import libraries needed for blinking the LED
import board
import digitalio
import time

# Configure the internal GPIO connected to the LED as a digital output
led_green = digitalio.DigitalInOut(board.GP16)
led_green.direction = digitalio.Direction.OUTPUT

led_blue = digitalio.DigitalInOut(board.GP17)
led_blue.direction = digitalio.Direction.OUTPUT

led_red = digitalio.DigitalInOut(board.GP18)
led_red.direction = digitalio.Direction.OUTPUT


# Configure the internal GPIO connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up


#Variables
pressed = False
door = 0
ranOnceClosed = 0
ranOnceOpen = 0

UVTimeON = 5
sleepTime = 5
c = 0

closedDoorState = 0
timePrev = 0
temperature = 0
threshold = 20

#######LOW LEVEL FUNCTIONS############



#######HIGH LEVEL FUNCTIONS###########
def coolingOn():
    print("Starting Cooling")
   # time.sleep(1)
    
    #OPEN LATCH (TBD)
    #Turn on fans
    #Update LCD Display
    #Dampen sponge (open valve)
    print("Cooling")
    

def coolingOff():
    print("Stopping Cooling")
   # time.sleep(1)

def doorOpen():
    global ranOnceClosed, ranOnceOpen, led_red, led_green
    if ranOnceOpen == 0:
        ranOnceOpen = 1
        ranOnceClosed = 0
        print("UV Lights: OFF")
        print("Main Lights: ON")
    
    led_red.value = False
    led_green.value = True



    
    
def doorClosed():
    global ranOnceClosed, ranOnceOpen, interval, led_red, led_green, UVTimeON, sleepTime, closedDoorState, timePrev
    if ranOnceClosed == 0:
        ranOnceClosed = 1
        ranOnceOpen = 0
        print("Door Closed")
        print("Main Lights: OFF")
        timePrev = time.time()
        led_green.value = False #TURN OFF MAIN LIGHTS
        closedDoorState = 1
        
    #LIGHTING (UV light)
    if closedDoorState == 0:
        if (time.time() - timePrev < sleepTime):
            print("UV Lights: ON")
            led_red.value = True

        else:
            timePrev = time.time()
            closedDoorState = 1
    
    else:
        if (time.time() - timePrev < UVTimeON):
            print("UV Lights: OFF")
            led_red.value = False
        else:

            timePrev = time.time()
            closedDoorState = 0
            
    
    
    
    
    
    
    

# Loop so the code runs continuously
while True:
    
    
    
    if button.value == False:
        pressed = True
        if door == 1:
            door = 0
        else:
            door = 1

    #Water cooling system
    
    if (temperature > threshold):
        coolingOn()
        
    else:
        coolingOff()



    #Doors + lighting system
    if door == 0:
        doorClosed()
        time.sleep(0.2)
    
    else:
        doorOpen()
        time.sleep(0.2)
        

   


