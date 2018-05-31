#!/usr/bin/env python
# -*- coding: utf-8 -*-
from clases import *
import random
import pygame
import globals
from pygame.locals import *
from check_cards import *

def click_para_continuar(screen,bando):

    #screen.fill((255,255,255))
    screen.blit(globals.background0,(0,0)) ## Pinta una imagen de fondo como background

    if bando == 'I':
        txt_juegas = globals.USER+" JUEGAS CON EL IMPERIO"
        #icono = pygame.image.load(globals.images_folder+'empire_icon.jpg')
        icono = globals.empire_icon
    elif bando == 'R':
        txt_juegas = globals.USER+" JUEGAS CON LOS REBELDES"
        #icono = pygame.image.load(globals.images_folder+'rebel_icon.jpg')    
        icono = globals.rebel_icon
    click = "Pulsa click para continuar..."

    screen.blit(icono, (760,200))
    txt = globals.menu_init.render(txt_juegas, 1, (255, 255, 255))
    screen.blit(txt, (500,50))
    

    txt = globals.menu_font.render(click, 1, (255, 255, 255))
    screen.blit(txt, (650,100))
    pygame.display.update()

    while True:
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONDOWN:
                return

def escoge_bando(screen):
    
    options = [Text_scr(screen,"1. IMPERIO",(250,300),globals.menu_init,True,(255,255,255)),
    Text_scr(screen,"2. REBELDES",(250,350),globals.menu_init,True,(255,255,255)),
    Text_scr(screen,"SALIR",(250,400),globals.menu_init,True,(255,255,255))]
    
    #screen.fill((255,255,255))
    screen.blit(globals.background, (0,0)) ## Pinta una imagen de fondo como background
    escoge = globals.menu_init.render(globals.USER+" ESCOGE BANDO", 1, (255, 255, 255))
    screen.blit(escoge, (580,50))
    for text in options:
        text.draw()    
    
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_1:
                    bando = 'I'
                    return bando
                elif event.key == pygame.K_2:
                    bando = 'R'
                    return bando

            for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True

                    if event.type == MOUSEBUTTONDOWN:
                        
                        if option.text == "SALIR":
                            pygame.quit()
                            exit()
                        elif option.text == "1. IMPERIO":
                            bando = 'I'
                        elif option.text == "2. REBELDES":
                            bando = 'R'
                        return bando
                else:
                    option.hovered = False
                option.draw()
                
            pygame.display.update()

def pintar_accion_fase(screen,texto,juega):
    # Pintar texto de lo que hay que hacer en la fase actual
    text_fase =''
    
    if not juega:
        # No es tu turno 
        text_fase = "ESPERANDO TU TURNO..."
    else:
        # fase de Colocar carta
        text_fase = texto

    #rendered = globals.action_font.render (text_fase,0,(0,0,0))
    rendered = globals.action_font.render (text_fase,0,globals.GREEN)
    screen.blit(rendered, (120,15))  

def inicializa_posiciones_tablero():
    
    # El valor de True indica que la posicion esta LIBRE

    ## Esta funcion inicializa las posiciones en el tablero donde colocar cartas

    tablero = []
    # naves de combate y asalto rebeldes    
    new = {'sector':3,'bando':'R','pos':(115,40),'card':None}       
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(115,200),'card':None}      
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(455,40),'card':None}       
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(455,200),'card':None}      
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(285,40),'card':None}       
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(285,200),'card':None}  
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(625,40),'card':None}       
    tablero.append(new)
    new = {'sector':3,'bando':'R','pos':(625,200),'card':None}      
    tablero.append(new)

    # naves de combate y asalto imperiales
    new = {'sector':3,'bando':'I','pos':(805,40),'card':None}       
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(805,200),'card':None}      
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(1145,40),'card':None}      
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(1145,200),'card':None}     
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(975,40),'card':None}       
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(975,200),'card':None}      
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(1315,40),'card':None}      
    tablero.append(new)
    new = {'sector':3,'bando':'I','pos':(1315,200),'card':None}     
    tablero.append(new)

    gap = 110 ## Espacio entre cartas
    for i in range(0,7): # 7 tropas
        new = {'sector':0,'bando':'R','pos':(20+(i*gap),520),'card':None}       
        tablero.append(new)

    for i in range(0,5): # 5 jedis
        new = {'sector':1,'bando':'R','pos':(20+(i*gap),365),'card':None}
        tablero.append(new)

    for i in range(0,2): # 2 vehiculos
        new = {'sector':2,'bando':'R','pos':(570+(i*gap),365),'card':None}
        tablero.append(new)

    for i in range(0,7): # 7 tropas
        new = {'sector':0,'bando':'I','pos':(810+(i*gap),520),'card':None}      
        tablero.append(new)

    for i in range(0,5): ## 5 siths
        new = {'sector':1,'bando':'I','pos':(1030+(i*gap),365),'card':None}
        tablero.append(new)

    for i in range(0,2): # 2 vehiculos
        new = {'sector':2,'bando':'I','pos':(810+(i*gap),365),'card':None}
        tablero.append(new)

    return tablero

def liberar_posicion(card,tablero):
    # Libera una posicion en el tablero para posicionar una nueva carta
    for item in tablero:
        if item['card'] != None:
            if card == item['card']:
                tablero[tablero.index(item)]['card'] = None
                return tablero
    print "No encuentro la carta en el tablero"
    return tablero

def modificar_tablero(oldcard,newcard,tablero):
    # Modifica una posicion del tablero con otra carta
    for item in tablero:
        if oldcard == item['card']:
            tablero[tablero.index(item)]['card'] = newcard
            return tablero
    print "No encuentro la carta a modificar en el tablero"
    return tablero

def coloca_carta(sector,bando,card,tablero):
# Esta accion coloca una carta en el tablero, de acuerdo a unas posiciones y sector prefijado
    for item in tablero:
        if sector == item['sector'] and bando == item['bando'] and item['card'] == None:
            #item['card'] = False
            tablero[tablero.index(item)]['card'] = card
            card.pos = item['pos']
            card.rect.x = item['pos'][0]
            card.rect.y = item['pos'][1]
            return card, tablero, True

    print "No hay posiciones libres. COMPACTAR"

    return card, tablero, False 

def coloca_carta_navev2(card_mesa,card_nave,card_move):
    # Coloca una carta sobre otra carta (normalmente de Nave)
    # Card_nave: Card_scr nave
    # Card_move: Card_scr carta a colocar
    # card_mesa tiene todas las cartas de la mesa
        
    for item in card_mesa:
        if item == card_nave:
            if card_nave.carta.tripulacion < 2:
                card_move.pos = (card_nave.pos[0]+(card_nave.carta.tripulacion+1)*30,card_nave.pos[1])
                card_move.rect.x = card_nave.pos[0]+(card_nave.carta.tripulacion+1)*30
                card_move.rect.y = card_nave.pos[1]
            else:
                # A partir de 2 tripulantes se solapan las cartas
                card_move.pos = (card_nave.pos[0]+60,card_nave.pos[1])
                card_move.rect.x = card_nave.pos[0]+60
                card_move.rect.y = card_nave.pos[1]
            card_move.carta.en_nave = True
            return card_move

    print "Algo pasa al colocar el tripulante en "+card_nave.carta.nombre

#   return card_move, tablero   
    return card_move
    
def pintar_mano(screen,mano,juega):
    # Despliega o pinta las cartas que hay en la mano sobre la mesa con objetos tipo Card_scr
    posx = 600
    posy = 730
    card_mano = []
    for i in range(len(mano)):
        card_new = Card_scr(screen,mano[i-1],(posx,posy))
        card_new.lock = not juega ## si no es el turno del jugador se bloquea la carta para que no la juegue
        card_mano.append(card_new)
        posx += 150 # Hay una separacion de 150 entre cartas

    return card_mano

def attack_sound(tipo, bando):
    if tipo == 4:
        globals.saber_sound.play()
    elif tipo == 9:
        globals.ship_attack.play()
    elif tipo in [10,11] and bando == 'R':
        globals.xwing_attack.play()
    elif tipo in [10,11] and bando == 'I':
        globals.tie_attack.play()
    else:
        globals.blaster_sound.play()

def place_sound(idcard,en_nave):
    if idcard in [140,141,142,144,145,146]: ## Sonido de Ties cuando se colocan en el espacio
        globals.tie_sound.play()
    elif idcard == 60: ## Chewie
        globals.chewie.play()
    elif idcard == 123: ## Vader
        globals.vader.play()
    elif idcard in [30,130]: ## Droides protocolo
        globals.protocol.play()
    elif idcard in [31]: ## R2D2
        globals.r2place.play()
    elif idcard == 106: ## Soldado explorador
        globals.explorador.play()
    elif idcard in [40,41,42,43]: ## XWings and Bwings
        globals.xwing.play()
    elif idcard in [48,49]: ## Jedi Starfighters
        globals.jedifly.play()
    elif not en_nave and ((idcard >= 20 and idcard < 30) or (idcard >= 120 and idcard < 130)): ## Jedi/Sith que no tienen sonido propio. tipo 4
        globals.saber_on.play()
    else:
        globals.place_effect.play()


def check_card_select(card_select):
    action_text = ''
    for card in card_select:
        if card.rect.collidepoint(pygame.mouse.get_pos()):
            action = 'S' # Selecciona carta
            action_text = 'Selecciona esta carta para jugarla'
            return True, action, action_text
    return False, 'Z', action_text

def check_cursor_hangar(frame_scr,bando):
    # Funcion que solo es llamada si se ha colocado un piloto sobre una nave que puede atacar al hangar:
    # Poe en Ala-X Negro
    # Kylo Ren en Tie Silencer
    action_text = ''
    for frame in frame_scr:
    # Se esta posicionando el cursor en el hangar
        if frame.tipo == 2 and (frame.bando != bando) and frame.rect.collidepoint(pygame.mouse.get_pos()):
            action = 'HD' # HD indica que se puede aplicar una accion de ataque sobre el hangar
            action_text = 'Inutilizar hangar enemigo'
            return True, action, action_text
    return False, 'Z', action_text

def check_cursor_mouse(text_scr,btn_scr,fase,card_mesa,card_move,ataque,def_rival,seleccion_tropa,seleccion_nave,seleccion_vehiculo):

    # Chequeamos si estamos encima de un Texto
    action_text = ''
    for text in text_scr:
        if text.rect.collidepoint(pygame.mouse.get_pos()) and text.flash:
            text.hovered = True
            return True, 'T', action_text #T indica que se esta encima de Texto
        else:
            text.hovered = False

    for btn in btn_scr:
        if btn.rect.collidepoint(pygame.mouse.get_pos()):
            btn.hovered = True
            return True, 'B', action_text #B indica que se esta encima de Boton
        else:
            btn.hovered = False

    if card_mesa == [] or card_move == []:
        return False, 'Z', action_text

    # Si estamos en la fase de accion principal chequear la carta a atacar
    if fase == 1:
        # Chequear si se puede aplicar una accion sobre una carta (cambio de cursor)
        for card in card_mesa:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                mousech, action_text = check_action1_card(card,card_move,card_mesa,ataque,def_rival)
                if mousech:
                    action = 'A' # Aplica accion de ataque
                else:
                    action = 'Z'
                return mousech, action, action_text # A indica que se puede aplicar una accion de ataque                

    elif fase == 2 and seleccion_tropa:
        # seleccionar carta de tropa para que reataque 
        for card in card_mesa:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                if card.carta.tipo in [0,1,2] and card.carta.bando == card_move.carta.bando and not card.carta.en_nave:
                    action = 'S' # Selecciona carta tipo tropa, tropa especial o piloto
                    mousech = True
                    action_text = 'Seleccionar '+card.carta.nombre+' para jugarla de nuevo'
                else:
                    action = 'Z'
                    mousech = False
                    action_text = ''                    
                return mousech, action, action_text # A indica que se puede aplicar una accion de ataque

    elif fase == 2 and seleccion_nave:
        # seleccionar nave para que reataque 
        for card in card_mesa:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                if card.carta.tipo == 10 and card.carta.bando == card_move.carta.bando:
                    action = 'S' # Selecciona carta
                    mousech = True
                    action_text = 'Seleccionar '+card.carta.nombre+' para activar su ataque'
                else:
                    action = 'Z'
                    mousech = False
                    action_text = ''                    
                return mousech, action, action_text # A indica que se puede aplicar una accion de ataque

    elif fase == 2 and seleccion_vehiculo:
        # seleccionar nave para que reataque 
        for card in card_mesa:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                if card.carta.tipo == 7 and card.carta.bando == card_move.carta.bando:
                    action = 'S' # Selecciona carta
                    mousech = True
                    action_text = 'Seleccionar '+card.carta.nombre+' para activar su ataque'
                else:
                    action = 'Z'
                    mousech = False
                    action_text = ''                    
                return mousech, action, action_text # A indica que se puede aplicar una accion de ataque
    
    elif fase == 2:
        # Chequear si se puede aplicar una accion de bonificacion sobre una carta (cambio de cursor)
        for card in card_mesa:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                mousech, action_text = check_action2_card(card,card_move,card_mesa,ataque,def_rival)
                if mousech:
                    action = 'A' # Aplica accion de ataque
                else:
                    action = 'Z'
                return mousech, action, action_text # A indica que se puede aplicar una accion de ataque
    return False, 'Z', action_text

def check_cursor_movingcard_mouse(frame_scr,card_mesa,card_move,hangar,count_hangar):
    
    action_text = ''
    ifmovement = False
    for frame in frame_scr:
        if frame.rect.collidepoint(pygame.mouse.get_pos()):
            ifmovement, action_text = check_movement_frame(frame,card_move,hangar,count_hangar)
    
    if card_mesa == [] or card_move == []:
        return ifmovement, 'M', action_text
    else:
        #Chequeamos si la carta puede ponerse como piloto o tripulante en una nave
        for card in card_mesa:
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                ifmovement, action_text = check_movement_card(card,card_move)
                return ifmovement, 'M', action_text 

    return ifmovement, 'M', action_text
            
def change_cursor_mouse(tag,fase):

    __hand_cursor_string = (
    "     XX         ",
    "    X..X        ",
    "    X..X        ",
    "    X..X        ",
    "    X..XXXXX    ",
    "    X..X..X.XX  ",
    " XX X..X..X.X.X ",
    "X..XX.........X ",
    "X...X.........X ",
    " X.....X.X.X..X ",
    "  X....X.X.X..X ",
    "  X....X.X.X.X  ",
    "   X...X.X.X.X  ",
    "    X.......X   ",
    "     X....X.X   ",
    "     XXXXX XX   ")
    __hcurs, __hmask = pygame.cursors.compile(__hand_cursor_string, ".", "X")
    __hand = ((16, 16), (5, 1), __hcurs, __hmask)

    if tag:
        # cursor raton en forma de diamante
        if fase in ['A','HD']: # Ataque o destruccion de hangar
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        elif fase == 'T': ## Esta sobre un texto  
            pygame.mouse.set_cursor(*__hand)
        elif fase == 'M': # Se esta moviendo y quiere colocarse en la mesa sobre algun elemento
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        elif fase == 'S': # Se esta seleccionando una carta para activar su poder o rejugarla
            #pygame.mouse.set_cursor(*pygame.cursors.ball)
            pygame.mouse.set_cursor(*__hand)
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    #return False

def haysitio_hangar(hangar,bando):
    for card in hangar:
        if card.carta.bando == bando:
            # Ya existe una carta en el hangar, solo admite una
            return False
            break
    return True


def calcular_def_ata(card,card_mesa):
    # Esta funcion me calcula la defensa adicional de una carta (card)
    # card_mesa: Son todas las cartas de la mesa

    comandos = [1,2,8] ## Comandos rebeldes
    def_com = 0
    ewoks = [3,4]
    def_ewoks = 0
    soldados = [101,102,108] ## Soldados imperiales
    def_soldados = 0
    droides_imp = [103,104] ## Droides de combate del imperio
    pot_droides = [113,153] ## Potenciadores de droides en defensa
    def_droides = 0
    clones = [7,9]
    pot_clones = [11,12,20] ## LAAT y Yoda
    def_clones = 0
    oficiales_imp = [115,116,117,118] # Oficiales y líderes imperiales
    pot_oficiales = [105] ## Soldados oscuros como potenciador de defensa a oficiales
    def_oficiales = 0
    pot_ataque = 0
    pot_defensa = 0

    # Chequear las cartas de la mesa terrestres para sumar potenciadores de defensa 
    for cartas in card_mesa:
        if not cartas.carta.tipo in [7,9,10,11] and not cartas.carta.en_nave:
            ## Potenciador de defensa
            if cartas.carta.id != card.carta.id: # No contar como potenciador la carta que estamos comparando
                if cartas.carta.id in pot_oficiales:
                    def_oficiales += 1
                elif cartas.carta.id in pot_clones: ## Yoda
                    def_clones += 2
                elif cartas.carta.id in ewoks and card.carta.id in ewoks:
                    def_ewoks += 2
                    pot_ataque += 2
                elif cartas.carta.id in droides_imp and card.carta.id in droides_imp:
                    def_droides += 2
                    pot_ataque += 2
                elif cartas.carta.id in comandos and card.carta.id in comandos:
                    pot_ataque += 1
                    def_com += 1
                elif cartas.carta.id in soldados and card.carta.id in soldados:
                    pot_ataque += 1
                    def_soldados += 1
       
        # Potenciadores que no son tropas
        elif cartas.carta.id in pot_droides and cartas.carta.tipo in [7,9,10,11]: # Potenciador droides no tropa
            def_droides += 1
        elif cartas.carta.id in pot_clones and cartas.carta.tipo in [7,9,10,11]: # Potenciador clones vehiculo y naves
            def_clones += 1

    #Calcular el potenciador de defensa de la carta terrestre
    if not card.carta.tipo in [7,9,10,11] and not card.carta.en_nave:
        # Calcular DEFENSA TROPAS TERRESTRES       
        if card.carta.id in comandos:
            pot_defensa = def_com 
        elif card.carta.id in soldados:
            pot_defensa = def_soldados 
        elif card.carta.id in droides_imp:
            pot_defensa = def_droides 
        elif card.carta.id in ewoks:
            pot_defensa = def_ewoks
        elif card.carta.id in clones:
            pot_defensa = def_clones 
        elif card.carta.id in oficiales_imp:
            pot_defensa = def_oficiales

    return pot_defensa, pot_ataque

def info_card(screen,card_mesa,mod_ata,mod_def,mod_ata_rival,mod_def_rival,bando):

    # Cartas de la mesa
    for card in card_mesa: # Mostrar datos informativos con modificadores de las cartas que hay en la mesa desplegadas  
        if card.rect.collidepoint(pygame.mouse.get_pos()):
            #Evasion aplica a todas las cartas
            Text_scr(screen,'Evasion: '+str(card.carta.evasion*10)+'%',(400,770),globals.normal_font,False,(100,100,100))
            if card.carta.tipo in [9,10,11]:
                Text_scr(screen,'Ataque: '+str(card.carta.ata),(400,730),globals.normal_font,False,(100,100,100))
                Text_scr(screen,'Defensa: '+str(card.carta.defensa),(400,750),globals.normal_font,False,(100,100,100))
                Text_scr(screen,'Tripulacion: '+str(card.carta.tripulacion)+'/'+str(card.carta.tripulacion_max),(400,790),globals.normal_font,False,(100,100,100))           
            elif card.carta.tipo == 7 or not card.carta.en_nave:
                pot_def, pot_ata = calcular_def_ata(card,card_mesa) ## Calcular el potenciador de defensa para una carta terrestre
                if card.carta.bando == bando:
                    Text_scr(screen,'Ataque: '+str(card.carta.ata+mod_ata+pot_ata),(400,730),globals.normal_font,False,(100,100,100))
                    Text_scr(screen,'Defensa: '+str(card.carta.defensa+mod_def+pot_def),(400,750),globals.normal_font,False,(100,100,100))
                else:
                    Text_scr(screen,'Ataque: '+str(card.carta.ata+mod_ata_rival+pot_ata),(400,730),globals.normal_font,False,(100,100,100))
                    Text_scr(screen,'Defensa: '+str(card.carta.defensa+mod_def_rival+pot_def),(400,750),globals.normal_font,False,(100,100,100))
            return
def zoom_cards(card_mano,card_mesa,card_hangar,juega,naves):
    for card in card_mano: # Zoom a las cartas de la mano en ese momento
        if card.rect.collidepoint(pygame.mouse.get_pos()) and not (card.lock and juega):
            card.zoom()
            return card

    # Cartas de la mesa
    for card in card_mesa: # Zoom a las cartas que hay en la mesa desplegadas     
        if card.rect.collidepoint(pygame.mouse.get_pos()):
            # Cuando se va encima de una nave y tiene mas de dos tripulantes se hace zoom a todos
            #if card.carta.tipo in [9,10,11] and card.carta.tripulacion > 2:
            if card.carta.tipo in [9,10,11]:
                for nave in naves:
                    if nave[0] == card:
                        i = 0
                        gap = (5-card.carta.tripulacion)*130 + 20
                        for tripu in nave:
                            #260 de ancho cada carta
                            tripu.draw_t((gap+(i*260),300))
                            i += 1
                            #20 6
                            #150 5
                            #280 4
                            #410 3
                            #540
            elif card.carta.tipo == 7 or not card.carta.en_nave:
                card.zoom()
            return card

    # Cartas dek hangar
    for card in card_hangar: # Zoom a las cartas que hay en los hangares desplegadas     
        if card.rect.collidepoint(pygame.mouse.get_pos()):
            card.zoom()
            return card

def zoom_cards_select(card_msg):
    for card in card_msg: # Zoom a las cartas que se muestran en mensage emergente
        if card.rect.collidepoint(pygame.mouse.get_pos()):
            card.zoom_v2()
            return card
    return ''

def zoom_cards_msg(card_msg):
    try:
        for card in card_msg: # Zoom a las cartas que se muestran en mensage emergente
            if card.rect.collidepoint(pygame.mouse.get_pos()):
                card.zoom_v2()
                return
    except:
        print "exception"
        return


