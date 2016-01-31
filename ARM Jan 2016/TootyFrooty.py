import pygame.mixer
from pygame.mixer import Sound
import RPi.GPIO as GPIO
import time
import sys

#pygame init.#
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

soundBoard = "Horn" if (len(sys.argv) == 1) else sys.argv[1]

delay = float(sys.argv[2]) if (len(sys.argv) == 3) else 0.2

#Fruit Listed here with GPIO connectors.#
#('name', port, Sound("file"), False, 0)#
fruit = [['Apple',  26, Sound("./sounds/" + soundBoard + " 1.ogg"), False, 0],
         ['Orange', 21, Sound("./sounds/" + soundBoard + " 2.ogg"), False, 0],
         ['Banana', 20, Sound("./sounds/" + soundBoard + " 3.ogg"), False, 0],
         ['Tomato', 16, Sound("./sounds/" + soundBoard + " 4.ogg"), False, 0],
         ['Kiwi',   19, Sound("./sounds/" + soundBoard + " 5.ogg"), False, 0],
         ['Carrot', 13, Sound("./sounds/" + soundBoard + " 6.ogg"), False, 0]]

#GPIO Setup.#
GPIO.setmode(GPIO.BCM)
for i in fruit:
    GPIO.setup(i[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Input loop#
#Loops through the list of fruit, checks if being touched, plays sound if so.#
while True:
    for i in range(0,6):
        curButtonState = GPIO.input(fruit[i][1])
        if (fruit[i][3] != curButtonState):
            if (curButtonState):
                if (time.time() - fruit[i][4] > delay):
                    #print(fruit[i][0] + " Pressed")
                    fruit[i][2].play()
                    fruit[i][4] = time.time()
        fruit[i][3] = curButtonState
