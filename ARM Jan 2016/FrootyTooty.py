import pygame.mixer
from pygame.mixer import Sound
import RPi.GPIO as GPIO
import time
import os

delay = 0.2

#pygame init.#
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

class Fruit():
    def __init__(name, pin, soundPaths, Pressed, deltaTime, delay):
        self.name = name
        self.pin = pin
        self.soundSelected = 0
        self.Sounds = sounds
        for path in soundPaths:
            self.sounds.append(Sound(path))
        self.listSize = len(soundPaths)
        self.pressed = pressed
        self.deltaTime = deltaTime
        self.delay = delay
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def play():
        self.sounds[self.soundSelected].play()

    def getName():
        return self.name

    def cycle():
        self.soundsSelected = (self.soundsSelected + 1) % self.listSize

    def isPressed():
        if GPIO.input(self.pin) and shouldPlay():
            return true

    def shouldPlay():
        print(self.name + " Pressed")
        return (time.time() - self.deltaTime) > self.delay

fruitList = []
soundList = []
for filename in os.listdir(os.getcwd() + "/sounds"):
    placed = False
    if len(soundList) == 0:
        soundList.append([os.path.basename(filename)[:-5]])
        placed == True
    else:
        for list in soundList:
            if list[0] == os.path.basename(filename)[:-5]:
                list.append(filename)
                placed = True
        if placed == False:
            soundList.append([os.path.basename(filename[:-5])])
            soundList[len(soundList) - 1].append(filename)


for i in range(0, len(soundList) - 1):
    print(soundList[i])
    soundList[i].pop(0)
    soundList[i] = sorted(soundList[i], key=str.lower)

soundList = [list(x) for x in zip(*soundList)]
fruitList.append(Fruit('Apple', 26, soundList[0], False, 0, 0.2))
fruitList.append(Fruit('Orange', 21, soundList[1], False, 0, 0.2))
fruitList.append(Fruit('Banana', 20, soundList[2], False, 0, 0.2))
fruitList.append(Fruit('Tomato', 16, soundList[3], False, 0, 0.2))
fruitList.append(Fruit('Kiwi', 19, soundList[4], False, 0, 0.2))
fruitList.append(Fruit('Carrot', 13, soundList[5], False, 0, 0.2))

#Fruit Listed here with GPIO connectors.#
#('name', port, Sound("file"), False, 0)#
fruit = [['Apple',  26, [Sound("./sounds/Horn 1.ogg"), Sound("./sounds/Drum 1.ogg")], False, 0],
         ['Orange', 21, [Sound("./sounds/Horn 2.ogg"), Sound("./sounds/Drum 1.ogg")], False, 0],
         ['Banana', 20, [Sound("./sounds/Horn 3.ogg"), Sound("./sounds/Drum 1.ogg")], False, 0],
         ['Tomato', 16, [Sound("./sounds/Horn 4.ogg"), Sound("./sounds/Drum 1.ogg")], False, 0],
         ['Kiwi',   19, [Sound("./sounds/Horn 5.ogg"), Sound("./sounds/Drum 1.ogg")], False, 0],
         ['Carrot', 13, 0, False, 0]];

#GPIO Setup.#
#Input loop#
#Loops through the list of fruit, checks if being touched, plays sound if so.#
while True:
    for fruit in fruitList:
        if fruit.isPressed():
            if fruit.getName() != 'Carrot':
                fruit.play()
            else:
                for item in fruitList:
                    item.cycle()
