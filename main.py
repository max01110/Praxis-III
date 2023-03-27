'''
ESC204 - Evaporative Cooling Fridge

'''
# Import libraries needed for blinking the LED
import board
import digitalio
import time
import analogio
import pwmio
from adafruit_motor import servo

# Configure the internal GPIO connected to the LED as a digital output
led_green = digitalio.DigitalInOut(board.GP16)
led_green.direction = digitalio.Direction.OUTPUT

led_blue = digitalio.DigitalInOut(board.GP17)
led_blue.direction = digitalio.Direction.OUTPUT

led_red = digitalio.DigitalInOut(board.GP18)
led_red.direction = digitalio.Direction.OUTPUT

fans = digitalio.DigitalInOut(board.GP0)
fans.direction = digitalio.Direction.OUTPUT
fans1 = digitalio.DigitalInOut(board.GP1)
fans1.direction = digitalio.Direction.OUTPUT

#fans.value = False

buzzer = pwmio.PWMOut(board.GP19, duty_cycle = 1000, frequency = 500, variable_frequency = True)
buzzer.duty_cycle = 0
# Configure the internal GPIO connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull-up


pwm = pwmio.PWMOut(board.GP27, duty_cycle=2 ** 15, frequency=50)
my_servo = servo.Servo(pwm)

#Variables
pressed = False
door = 0
ranOnceClosed = 0
ranOnceOpen = 0

UVTimeON = 5
sleepTime = 5
doorOpenThreshold = 5
c = 0

closedDoorState = 0
timePrev = 0
temperature = 0
threshold = 20
lightVal = 0


########PHOTORESISTOR SETUP##############
# set display to show either ADC output representative integer or
# the voltage that it represents
INT_MODE = 0
VOLT_MODE = 1
mode = INT_MODE

# always 0xff (in hex) according to: https://learn.adafruit.com/
# circuitpython-basics-analog-inputs-and-outputs/
# analog-to-digital-converter-inputs
ADC_HIGH = 65535

# set up photoresistor as analog input over analog pin A0
# (on GPIO pin 26 for Pico, needs to be changed if using Nano)
photoresistor_pin = board.GP26_A0
photoresistor = analogio.AnalogIn(photoresistor_pin)

# show reference voltage (logic high, 3.3V) and the
# corresponding analog integer value
ADC_REF = photoresistor.reference_voltage

# convert ADC input value back to voltage
def adc_to_voltage(adc_value):
    return  ADC_REF * (float(adc_value)/float(ADC_HIGH))

#######LOW LEVEL FUNCTIONS############
def buzz():
    global buzzer
    print("buzzing")
    for duty in range(5):
        # increasing duty cycle
        buzzer.duty_cycle = 10000
        time.sleep(0.2)
        buzzer.duty_cycle = 0
        time.sleep(0.2)



#######HIGH LEVEL FUNCTIONS###########
def coolingOn():
    global fans
    print("Starting Cooling")

   # time.sleep(1)

    #OPEN LATCH (TBD)
    #Turn on fans
    #Update LCD Display

    #Dampen sponge (open valve)


    print("Cooling")


def coolingOff():
    global fans
    print("Stopping Cooling")
   # time.sleep(1)

def doorOpen():
    global ranOnceClosed, ranOnceOpen, led_red, led_green, led_blue, doorOpenThreshold, timePrev
    if ranOnceOpen == 0:
        ranOnceOpen = 1
        ranOnceClosed = 0
        print("UV Lights: OFF")
        print("Main Lights: ON")
        timePrev = time.time()

    if (time.time() - timePrev > doorOpenThreshold):
        buzz()
        timePrev = time.time()


    led_red.value = True
    led_green.value = True
    led_blue.value = False


def doorClosed():
    global ranOnceClosed, ranOnceOpen, interval, led_red, led_green, led_blue, UVTimeON, sleepTime, closedDoorState, timePrev
    if ranOnceClosed == 0:
        ranOnceClosed = 1
        ranOnceOpen = 0
        print("Door Closed")
        print("Main Lights: OFF")
        timePrev = time.time()
        led_green.value = False #TURN OFF MAIN LIGHTS
        led_red.value = False #TURN OFF MAIN LIGHTS
        closedDoorState = 1

    #LIGHTING (UV light)
    if closedDoorState == 0:
        if (time.time() - timePrev < sleepTime):
            print("UV Lights: ON")
            led_blue.value = True



        else:
            timePrev = time.time()
            closedDoorState = 1
            

    else:
        if (time.time() - timePrev < UVTimeON):
            print("UV Lights: OFF")
            led_blue.value = False
          
        else:

            timePrev = time.time()
            closedDoorState = 0








# Loop so the code runs continuously
while True:



    if mode == INT_MODE:
        lightVal = (photoresistor.value)
    # convert to voltage
    else:
        lightVal = (adc_to_voltage(photoresistor.value))

    time.sleep(0.1)

    if lightVal > 62000:
        door = 0
    else:
        door = 1


    #Water cooling system

   # if (temperature > threshold):
    #    coolingOn()
    #else:
    #    coolingOff()



    #Doors + lighting system
    if door == 0:
        fans.value = True
        fans1.value = True
        #fans2.duty_cycle = 500
        #coolingOn()
        doorClosed()
        time.sleep(0.2)

    else:
        fans.value = True
        fans1.value = True
        #fans2.duty_cycle = 500

        #coolingOff()
        doorOpen()
        time.sleep(0.2)





