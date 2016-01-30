import pygame.mixer
from pygame.mixer import Sound
import RPi.GPIO as GPIO
import time

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

fruit = [('Apple',  26, Sound("./snare.wav"), False),
         ('Orange', 21, Sound("./snare.wav"), False),
         ('Banana', 20, Sound("./snare.wav"), False),
         ('Tomato', 16, Sound("./snare.wav"), False),
         ('Kiwi',   19, Sound("./snare.wav"), False),
         ('Carrot', 13, Sound("./snare.wav"), False)]

GPIO.setmode(GPIO.BCM)

for x in fruits:
    GPIO.setup(x[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

buttonState = False




while True:
    for x in fruit:
        curButtonState = GPIO.input(26)
        if (buttonState != curButtonState):
            if (curButtonState):
                print("Button Pressed")
                if not (pygame.mixer.music.get_busy()):
                   drum.play()
                time.sleep(0.2)
                #os.system('mpg123 -q snare.wav &')
            else:
                print("Button Released")
        buttonState = curButtonState
