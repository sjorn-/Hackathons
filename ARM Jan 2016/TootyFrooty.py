import pygame.mixer
from pygame.mixer import Sound
import RPi.GPIO as GPIO
import time

#pygame init.#
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

#Fruit Listed here with GPIO connectors.#
#('name', port, Sound("file"), False, 0)#
fruit = [['Apple',  26, Sound("./sounds/Horn 1.ogg"), False, 0],
         ['Orange', 21, Sound("./sounds/Horn 2.ogg"), False, 0],
         ['Banana', 20, Sound("./sounds/Horn 3.ogg"), False, 0],
         ['Tomato', 16, Sound("./sounds/Horn 4.ogg"), False, 0],
         ['Kiwi',   19, Sound("./sounds/Horn 5.ogg"), False, 0],
         ['Carrot', 13, Sound("./sounds/Horn 6.ogg"), False, 0]]

#GPIO Setup.#
GPIO.setmode(GPIO.BCM)
for x in fruit:
    GPIO.setup(x[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Input loop#
#Loops through the list of fruit, checks if being touched, plays sound if so.#
while True:
    for i in range(0,6):
        curButtonState = GPIO.input(fruit[i][1])
        if (fruit[i][3] != curButtonState):
            if (curButtonState):
                if (time.time() - fruit[i][4] > 0.2):
                    print(fruit[i][0] + " Pressed")
                    fruit[i][2].play()
                    fruit[i][4] = time.time()
        fruit[i][3] = curButtonState
