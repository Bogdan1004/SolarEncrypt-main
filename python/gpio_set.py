import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
gpio_number = 14
GPIO.setup(gpio_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
print("GPIO no " + str(gpio_number) + ": " + str(GPIO.input(gpio_number)))