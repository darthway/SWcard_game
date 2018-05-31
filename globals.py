#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import os
from pygame.locals import *

pygame.init()
# Estan todas las variables globales

#current_folder = os.path.dirname(os.path.abspath(__file__))
try:
    current_folder = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    import sys
    current_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

#images_folder = current_folder+'\images'+'\\'
#sounds_folder = current_folder+'\sounds'+'\\'

images_folder = '.\images'+'\\'
sounds_folder = '.\sounds'+'\\'

menu_font2 = pygame.font.SysFont('Arial',20,True,False)
menu_font = pygame.font.SysFont('Arial',25,True,False)
menu_init = pygame.font.SysFont('Arial',35,True,False)
normal_font = pygame.font.SysFont('Arial',15,True,False)
action_font = pygame.font.SysFont('Arial',18,True,False)
score_font = pygame.font.SysFont('Arial',25,True,False)

#menu_font2 = pygame.font.SysFont('starwars',10,True,False)
#menu_font = pygame.font.SysFont('starwars',20,True,False)
#menu_init = pygame.font.SysFont('starwars',30,True,False)
#normal_font = pygame.font.SysFont('Arial',15,True,False)
#action_font = pygame.font.SysFont('Elephant',18,True,False)
#score_font = pygame.font.SysFont('starwars',20,True,False)

clock = pygame.time.Clock()

## POSICIONES y MEDIDAS
resolucion = (1600, 900)
# Posicion de la carta que se pone en el hangar
pos_hangar_imp = (1490,80)
pos_hangar_reb = (10,80) 

#DISTRIBUCION DE TABLERO
#Space 10-100-5-680-10-680-5-100-10
#Tierra 10-785-10-785-10

# IMAGENES 
#rebels_deck = pygame.image.load(images_folder+"deck_rebels.jpg")
#empire_deck = pygame.image.load(images_folder+"deck_empire.jpg")
#rebels_deck0 = pygame.image.load(images_folder+"deck_rebels0.jpg")
#empire_deck0 = pygame.image.load(images_folder+"deck_empire0.jpg")

#sound_on = pygame.image.load(images_folder+"sound_on.png")
#sound_on = pygame.transform.scale(sound_on,(25,25))
#sound_off = pygame.image.load(images_folder+"sound_off.png")
#sound_off = pygame.transform.scale(sound_off,(25,25))

icon = pygame.image.load(images_folder+"R2D2_icon.png")

#shield = pygame.image.load(images_folder+"shield.png")
#shield = pygame.transform.rotozoom(shield,0,0.9)
#attack = pygame.image.load(images_folder+"attack.png")

#score_rebels = pygame.image.load(images_folder+"score_rebels.gif")
#score_rebels = pygame.transform.scale(score_rebels,(225,35))
#score_empire = pygame.image.load(images_folder+"score_empire.gif")
#score_empire = pygame.transform.scale(score_empire,(225,35))

user_disconnect = pygame.image.load(images_folder+'user_disconnected.gif')
server_disconnect = pygame.image.load(images_folder+'server_disconnected.gif')
server_disconnect = pygame.transform.scale(server_disconnect,(400,400))

#fin_partida = pygame.image.load(images_folder+"fin_partida.gif")

t_rebel = pygame.image.load(images_folder+"snow_rebels.jpg")
t_rebel = pygame.transform.scale(t_rebel,(785,315))
t_empire = pygame.image.load(images_folder+"snow_empire.jpg")
t_empire = pygame.transform.scale(t_empire,(785,315))
s_rebel = pygame.image.load(images_folder+"space_rebels.jpg")
s_rebel = pygame.transform.scale(s_rebel,(680,315))
s_empire = pygame.image.load(images_folder+"space_empire.jpg")
s_empire = pygame.transform.scale(s_empire,(680,315))
hangar_empire= pygame.image.load(images_folder+'hangar_empire.gif')
hangar_empire = pygame.transform.scale(hangar_empire,(100,315))
hangar_rebel= pygame.image.load(images_folder+'hangar_rebel.gif')
hangar_rebel = pygame.transform.scale(hangar_rebel,(100,315))

#image_erasecard = pygame.image.load(images_folder+"erase_card.jpg")

#image_playcard = pygame.image.load(images_folder+"play_card.jpg")
show_cards = pygame.image.load(images_folder+"show_cards1.png")
frame_img = pygame.image.load(images_folder+"frame_msg.gif")

btn_ok0 =pygame.image.load(images_folder+"btn0.gif")
btn_ok1 =pygame.image.load(images_folder+"btn1.gif")

#redindicator = pygame.image.load(images_folder+"redindicator.png")
#greenindicator = pygame.image.load(images_folder+"greenindicator.png")

background = pygame.image.load(images_folder+'tapiz_cardgame.jpg')
background = pygame.transform.scale(background,resolucion)
background0 = pygame.image.load(images_folder+'tapiz_cardgame0.jpg')
background0 = pygame.transform.scale(background0,resolucion)

#SOUNDS
try:
	blaster_sound = pygame.mixer.Sound(sounds_folder+"blaster.wav")
	saber_sound = pygame.mixer.Sound(sounds_folder+"saber_attack.wav")
	background_sound = pygame.mixer.Sound(sounds_folder+"rebel_theme3.wav")
	erase_sound = pygame.mixer.Sound(sounds_folder+"erase2.wav")
	place_effect = pygame.mixer.Sound(sounds_folder+"place1.wav")
	tie_sound = pygame.mixer.Sound(sounds_folder+"tie_fighter.wav")
	error_sound = pygame.mixer.Sound(sounds_folder+"error.wav")
	fin_rebels = pygame.mixer.Sound(sounds_folder+"R2D2.wav")
	fin_empire = pygame.mixer.Sound(sounds_folder+"Vader.wav")
	jabba_laughting = pygame.mixer.Sound(sounds_folder+"jabba-laughing.wav")
	chewie = pygame.mixer.Sound(sounds_folder+"chewy_roar.wav")
	vader = pygame.mixer.Sound(sounds_folder+"master_yes.wav")
	protocol = pygame.mixer.Sound(sounds_folder+"switch-off.wav")
	r2place = pygame.mixer.Sound(sounds_folder+"r2place.wav")
	xwing = pygame.mixer.Sound(sounds_folder+"xwing.wav")
	tie_attack = pygame.mixer.Sound(sounds_folder+"tie_fighter_fire.wav")
	xwing_attack = pygame.mixer.Sound(sounds_folder+"xwing_fire.wav")
	ship_attack = pygame.mixer.Sound(sounds_folder+"ship_fire.wav")
	explorador = pygame.mixer.Sound(sounds_folder+"explorador.wav")
	jedifly = pygame.mixer.Sound(sounds_folder+"jedifly.wav")
	saber_on = pygame.mixer.Sound(sounds_folder+"saber_on.wav")
	pc_sound = True
except:
	print "No hay tarjeta de sonido"
	pc_sound = False

GREEN = (1,169,130)
RED = (255,0,0)

HOST = 'localhost' ## Variable por defecto con el host o server
PORT = 7000 ## Variable por defecto con el puerto al que conectarse en el juego
USER = 'Anonymous'
VERSION = 'v 1.14'