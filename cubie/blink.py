import SUNXI_GPIO as GPIO
import time
RED_LED = GPIO.PD0

GPIO.init()
GPIO.setcfg(RED_LED, GPIO.OUT)

while True:
    GPIO.output(RED_LED, GPIO.HIGH)
    print 'high'
    time.sleep(1)
    GPIO.output(RED_LED, GPIO.LOW)
    print 'low'
time.sleep(1)
