import pygame.mixer
from pygame.mixer import Sound
import RPi.GPIO as GPIO
import time

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

fruit = [('Apple',  26, Sound("./snare.wav"),     False, 0),
         ('Orange', 21, Sound("./snare.wav"),    False, 0),
         ('Banana', 20, Sound("./snare.wav"),  False, 0),
         ('Tomato', 16, Sound("./snare.wav"), False, 0),
         ('Kiwi',   19, Sound("./snare.wav"),     False, 0),
         ('Carrot', 13, Sound("./snare.wav"), False, 0)]
GPIO.setmode(GPIO.BCM)

for x in fruit:
    GPIO.setup(x[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    x = (x[0], x[1], x[2], x[3], time.process_time())

#buttonState = False

while True:
    #for x in fruit:
    #    curButtonState = GPIO.input(x[1])
    #    if (x[3] != curButtonState):
    #        if (curButtonState):
    #            print(x[0] + " Pressed")
    #            #if not (pygame.mixer.music.get_busy()):
    #            print("curTime = " + str(time.process_time()));
    #            #print("x[4] = " + str(x[4]))
    #            if (time.process_time() - x[4] > 1):
    #                x[2].play()
    #                x = (x[0], x[1], x[2], x[3], time.process_time())
    #                #print("x[4] = " + str(x[4]))
    #            #time.sleep(0.2)
    #            #os.system('mpg123 -q snare.wav &')
    #        else:
    #            print(x[0] + " Released")
    #    print(curButtonState)
    #    x = (x[0], x[1], x[2], curButtonState, x[4])
    #    print("x[3] = " + str(x[3]))
    for x in range(0,5):
        curButtonState = GPIO.input(fruit[x][1])
        if (fruit[x][3] != curButtonState):
            if (curButtonState):
                print(fruit[x][0] + " Pressed")
                #if not (pygame.mixer.music.get_busy()):
                #print("curTime = " + str(time.process_time()));
                print("x[4] = " + str(fruit[x][4]))
                if (time.process_time() - fruit[x][4] > 0.2):
                    fruit[x][2].play()
                    fruit[x] = (fruit[x][0], fruit[x][1], fruit[x][2], fruit[x][3], time.process_time())
                    #print("x[4] = " + str(x[4]))
                #time.sleep(0.2)
                #os.system('mpg123 -q snare.wav &')
            else:
                print(fruit[x][0] + " Released")
        #print(curButtonState)
        fruit[x] = (fruit[x][0], fruit[x][1], fruit[x][2], curButtonState, fruit[x][4])
        #print("x[3] = " + str(x[3]))
