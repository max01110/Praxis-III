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
import adafruit_rgbled


led_uv = digitalio.DigitalInOut(board.GP21)
led_uv.direction = digitalio.Direction.OUTPUT


led_blue = board.GP20


led_green = board.GP17

led_red = board.GP16

led = adafruit_rgbled.RGBLED(led_red, led_blue, led_green)


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
doorOpenThreshold = 2
c = 0

closedDoorState = 0
timePrev = 0
temperature = 0
threshold = 20
lightVal = 0
coolOn = 0
openValve = False

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


button = digitalio.DigitalInOut(board.GP2)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set the internal resistor to pull−up
pressed = 0
valveOpenThreshold = 5

# convert ADC input value back to voltage
def adc_to_voltage(adc_value):
    return  ADC_REF * (float(adc_value)/float(ADC_HIGH))

#######LOW LEVEL FUNCTIONS############
def buzz():
    global buzzer, led
    for duty in range(5):
        # increasing duty cycle
        buzzer.duty_cycle = 10000
        led.color = (255, 0, 0)
        time.sleep(0.2)
        led.color = (0, 0, 0)
        buzzer.duty_cycle = 0
        time.sleep(0.2)




#######HIGH LEVEL FUNCTIONS###########
def coolingOn():
    global fans, my_servo, openValve, valveOpenThreshold, timePrev, fans1
    fans1.value = True

    print("Cooling On")

    if openValve == False:
        openValve = True
        my_servo.angle = 90
        timePrev = time.time()
        for i in range(8):
            my_servo.angle = 1
            time.sleep(0.001)



    my_servo.angle = 90

    #Turn on fans





def coolingOff():
    global fans1, openValve
    fans1.value = False
    openValve = False

    print("Cooling Stopped")
   # time.sleep(1)

def doorOpen():
    global ranOnceClosed, ranOnceOpen, led, led_red, led_green, led_blue, led_uv, doorOpenThreshold, timePrev
    if ranOnceOpen == 0:
        ranOnceOpen = 1
        ranOnceClosed = 0
        print("UV Lights: OFF")
        print("Main Lights: ON")
        timePrev = time.time()

    if (time.time() - timePrev > doorOpenThreshold):
        buzz()
        timePrev = time.time()

    led.color = (0, 0, 0)
    led_uv.value = False


def doorClosed():
    global ranOnceClosed, ranOnceOpen, interval, led, led_red, led_green, led_blue, led_uv, UVTimeON, sleepTime, closedDoorState, timePrev
    led.color = (255, 255, 255)

    if ranOnceClosed == 0:
        ranOnceClosed = 1
        ranOnceOpen = 0
        print("Main Lights: OFF")
        timePrev = time.time()
        led.color = (0, 0, 0)

        closedDoorState = 1

    #LIGHTING (UV light)
    if closedDoorState == 0:
        if (time.time() - timePrev < sleepTime):
            print("UV Lights: ON")
            led_uv.value = True



        else:
            timePrev = time.time()
            closedDoorState = 1


    else:
        if (time.time() - timePrev < UVTimeON):
            print("UV Lights: OFF")
            led_uv.value = False

        else:

            timePrev = time.time()
            closedDoorState = 0




timePrevValve = 0
valveClosed = 1

# Loop so the code runs continuously
while True:

    if (time.time() - timePrevValve > valveOpenThreshold):
        if valveClosed == 0:
            valveClosed = 1
            for i in range(7):
                my_servo.angle = 1
                time.sleep(0.001)

            my_servo.angle = 90



    if pressed == False:
        if button.value == False: # If the button is pressed
            if coolOn == False:
                coolOn = True
                timePrevValve = time.time()
                valveClosed = 0
            else:
                coolOn = False


            pressed = True
    elif pressed == True: # If
        if button.value == True: # If the button is depressed
            pressed = False


    if mode == INT_MODE:
        lightVal = (photoresistor.value)
    # convert to voltage
    else:
        lightVal = (adc_to_voltage(photoresistor.value))

    time.sleep(0.1)
    print(lightVal)

    if lightVal > 55000:
        door = 0
    else:
        door = 1


    #Water cooling system
    if coolOn == True:
        coolingOn()

    else:
        coolingOff()


    #Doors + lighting system
    if door == 0:

        doorClosed()



    else:
        doorOpen()
        time.sleep(0.1)
