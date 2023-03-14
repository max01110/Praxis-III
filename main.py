'''
ESC204 2023S Lab 2 Task D
Task: Light up onboard LED on button press.
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

UVTimeON = 10
c = 0

#######LOW LEVEL FUNCTIONS############



#######HIGH LEVEL FUNCTIONS###########
def coolingOn():
    print("Starting Cooling")
    time.sleep(1)
    
    #OPEN LATCH (TBD)
    #Turn on fans
    #Update LCD Display
    #Dampen sponge (open valve)
    print("Cooling")
    

def coolingOff():
    print("Stopping Cooling")
    time.sleep(1)

def doorOpen():
    global ranOnceClosed, ranOnceOpen, led_red
    if ranOnceOpen == 0:
        ranOnceOpen = 1
        ranOnceClosed = 0
        print("UV Lights: OFF")
        print("Main Lights: ON")
    
    led_red.value = False



    
    
def doorClosed():
    global ranOnceClosed, ranOnceOpen, interval, led_red, c
    if ranOnceClosed == 0:
        ranOnceClosed = 1
        ranOnceOpen = 0
        print("Door Closed")
        print("Main Lights: OFF")
        sleepTimePrev = time.time()
    
    
    
    if (time.time() - sleepTimePrev < sleepTime):
        led_red.value = False
        
    else
    if (time.time() - c < UVTimeON):
        led_red.value = True
    
    
    
    
    


# Loop so the code runs continuously
while True:
    
    if button.value == False:
        pressed = True
        if door == 1:
            door = 0
        else:
            door = 1

    if door == 0:
        doorClosed()
        time.sleep(0.2)
    
    else:
        doorOpen()
        time.sleep(0.2)
        

   





