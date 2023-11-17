import RPi.GPIO as GPIO
import time

# Define the GPIO pins
#aceste numere reprezinta gpio pentru RPI

pin1 = 21  #pentru rotire la stanga, pin 1 de la punte
pin2 = 18  #pentru rotire la derapta, pin 2 de la punte
pin3 = 23  #pentru oscilatie sus jos(in caz ca avem motor)
pin4 = 25  #pentru oscilatie sus jos(in caz ca avem motor)

# Set up GPIO pe out
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)
GPIO.setwarnings(False)
def default():
      # rotire trigonometrica
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)
        #GPIO.output(pin3, GPIO.LOW)
        #GPIO.output(pin4, GPIO.LOW)

        # Wait for 1 seconds
        time.sleep(0.1)

        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        #GPIO.output(pin3, GPIO.LOW)
        #GPIO.output(pin4, GPIO.LOW)

        # Asteapta 10
        time.sleep(2)
		
		# rotire sendul acelor de ceasornic 1 secunda
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.HIGH)
        #GPIO.output(pin3, GPIO.LOW)
        #GPIO.output(pin4, GPIO.LOW)
        time.sleep(4)#aicu trebuie o valoare dubla
        
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)
        
        time.sleep(23)
        
def test():
    GPIO.output(pin1, GPIO.HIGH)
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)
    time.sleep(1)
try:
    while True:
      test()

except KeyboardInterrupt:
    GPIO.output(pin1, GPIO.LOW)
    GPIO.output(pin2, GPIO.LOW)
    GPIO.cleanup()
    GPIO.cleanup()  # Cleanup GPIO on program exit
