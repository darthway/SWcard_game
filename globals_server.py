#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import os
from pygame.locals import *

pygame.init()
# Estan todas las variables globales


#imgdir = os.path.join(os.path.dirname(__file__),"images_server")

imgdir = '.\images_server'+'\\'

## Iconos de escudo y ataque
shield = pygame.image.load(os.path.join(imgdir,"shield.png"))
shield = pygame.transform.rotozoom(shield,0,0.9)
attack = pygame.image.load(os.path.join(imgdir,"attack.png"))
attack = pygame.transform.rotozoom(attack,0,0.9)

# Indicador de turno
redindicator = pygame.image.load(os.path.join(imgdir,"redindicator.png"))
greenindicator = pygame.image.load(os.path.join(imgdir,"greenindicator.png"))

# Score
score_rebels = pygame.image.load(os.path.join(imgdir,"score_rebels.gif"))
score_rebels = pygame.transform.scale(score_rebels,(225,35))
score_empire = pygame.image.load(os.path.join(imgdir,"score_empire.gif"))
score_empire = pygame.transform.scale(score_empire,(225,35))

# Icono sonido
sound_on = pygame.image.load(os.path.join(imgdir,"sound_on.png"))
sound_on = pygame.transform.scale(sound_on,(25,25))
sound_off = pygame.image.load(os.path.join(imgdir,"sound_off.png"))
sound_off = pygame.transform.scale(sound_off,(25,25))

#decks
image_erasecard = pygame.image.load(os.path.join(imgdir,"erase_card.jpg"))
rebels_deck = pygame.image.load(os.path.join(imgdir,"deck_rebels.jpg"))
empire_deck = pygame.image.load(os.path.join(imgdir,"deck_empire.jpg"))
rebels_deck0 = pygame.image.load(os.path.join(imgdir,"deck_rebels0.jpg"))
empire_deck0 = pygame.image.load(os.path.join(imgdir,"deck_empire0.jpg"))

#Iconos
empire_icon = pygame.image.load(os.path.join(imgdir,'empire_icon.jpg'))
rebel_icon = pygame.image.load(os.path.join(imgdir,'rebel_icon.jpg'))

VERSION = 'v 1.14'