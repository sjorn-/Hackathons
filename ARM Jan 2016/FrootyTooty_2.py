import pygame.mixer
from pygame.mixer import Sound
import RPi.GPIO as GPIO
import time

#pygame init#
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

#Fruit Listed here with GPIO connectors#
#('name', port, Sound("file"), False, 0)#
fruit = [('Apple',  26, Sound("./Horn 1.ogg"), False, 0),
         ('Orange', 21, Sound("./Horn 2.ogg"), False, 0),
         ('Banana', 20, Sound("./Horn 3.ogg"), False, 0),
         ('Tomato', 16, Sound("./Horn 4.ogg"), False, 0),
         ('Kiwi',   19, Sound("./Horn 5.ogg"), False, 0),
         ('Carrot', 13, Sound("./Horn 6.ogg"), False, 0)]

#GPIO Setup#
GPIO.setmode(GPIO.BCM)
for x in fruit:
    GPIO.setup(x[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    x = (x[0], x[1], x[2], x[3], time.process_time())

#Input loop#
#Loops through the list of fruit, checks if being touched, plays sound if so#
while True:
    for x in range(0,6):
        curButtonState = GPIO.input(fruit[x][1])
        if (fruit[x][3] != curButtonState):
            if (curButtonState):
                #print("x[4] = " + str(fruit[x][4]))
                if (time.process_time() - fruit[x][4] > 0.2):
                    print(fruit[x][0] + " Pressed")
                    fruit[x][2].play()
                    fruit[x] = (fruit[x][0], fruit[x][1], fruit[x][2], fruit[x][3], time.process_time())
        fruit[x] = (fruit[x][0], fruit[x][1], fruit[x][2], curButtonState, fruit[x][4])
