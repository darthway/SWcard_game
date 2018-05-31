#! /usr/bin/env python
import sys
import globals
#import pygame

from Tkinter import *
import tkMessageBox

from sys import stdin, exit

from clases import * # Incluye todas las clases
from time import sleep
from funciones_gral import *
#from cartas_test import *
from cartas import *

from check_intro import *
from PodSixNet.Connection import connection, ConnectionListener

#from PodSixNet.Connection import *

class ScreenBoard:
    
    def __init__(self):

        modes = pygame.display.list_modes(32)
        #self.screen = pygame.display.set_mode(globals.resolucion, FULLSCREEN, 32)
        self.screen = pygame.display.set_mode(globals.resolucion, RESIZABLE, 32)
        pygame.display.set_caption('STAR WARS TOTAL WAR Card Game by David Camino')
        pygame.display.set_icon(globals.icon)

        ## Frames que se cargan por defecto en la pantalla
        self.frame_scr = []
        self.text_scr = []
        self.msg_scr = [] ## Mensajes y objetos emergentes
        self.card_msg = [] ## Cartas que salen con mensajes a veces hay que elegir entre una
        self.btn_scr = [] ## Botones emergentes

        self.bando = '' ## Variable que incida el bando elegido o asignado del jugador
        
        # variable fase
        # 0: Colocacion de cartas
        # 1: Accion principal de la carta si la tiene
        # 2: Accion secundaria de la carta si la tiene. Poder principal
        self.fase = 0 ## Indica la fase del turno del jugador

        self.start = False ## Indica comienzo de la partida
        self.juega = False ## Esta variable indica si es tu turno para jugar
        self.rejuega = False ## Esta variable indica si es tu turno de nuevo (juegas otra carta extra)
        self.fin = False

        self.screen.blit(globals.background0,(0,0))
        txt = globals.menu_init.render(globals.USER+ " conectado. Esperando a otro jugador...", 1, (255, 255, 255))
        self.screen.blit(txt, (20,50))                             
        pygame.display.update()

        self.baraja = [] ## En la baraja estan todas las cartas tipo Card
        self.baraja_rival = [] ## En la baraja rival estan todas las cartas tipo Card del rival
        self.mano = [] ## Indica las cartas que tienes en tu mano
        self.card_mano = [] ## Cartas que hay en tu mano tipo Card_scr
        self.moving = False ## Carta moviendose (raton pulsado sobre ella y arrastrando)
        self.card_move = [] ## Carta tipo Card_scr que se esta moviendo, colocado o jugado
        self.ejecutor = None ## Es la carta que se coloca como tripulante y reataca, da el control a la nave para el ataque y luego ejecuta su accion
        self.card_mesa = [] ## Cartas que hay en la mesa colocadas tipo Card_scr
        self.card_mouse = [] ## Carta sobre la que esta situado el raton, interesante para hacer acciones sobre ella
        self.card_select = [] ## Carta sobre la que esta situado el raton, se ha seleecionado sobre varias

        self.card_colocada = False # nos indica si se ha colocado una carta = colocado en el tablero
        self.mousech = False # nos indica si el cursor esta sobre un elemento que indique que se puede hacer accion -> cambia cursor raton
        self.eliminada = False # Indica si la carta ha sido eliminada

        self.mano_rival_vacia = False
        self.hangar_out = False ## Indica si el hangar esta destruido
        self.hangar_out_rival = False ## Indica si el hangar del rival esta destruido
        self.accion = 'Z'
        ## Acciones:
            # Z: Nada como Null
            # A: Ataque
            # S: seleccion de nave

        self.selecciona = False ## Variable que indica que estamo en momento de seleccionar entre determinadas cartas elegidas
        self.card_mazo = False ## Variable que indica que estamo en momento de seleccionar entre cartas del mazo
        
        # Indican por que carta va en el mazo. Empezamos con 4 en la mano = 3 en mano y 1 en hangar
        self.ncards = 4

        self.naves = [] ## Lista de naves. Elementos tipo lista de Cards
        self.card_eliminadas = [] ## Lista con las cartas eliminadas

        ## Modificadores terrestres
        self.defensa = 0
        self.defensa_rival = 0
        self.ataque = 0
        self.ataque_rival = 0
        self.ignora_evasion = False ## Indica si la carta que ataca ignora evasion
        self.seleccion_tropa = False ## Indica si estamos en la fase de eleccion de una tropa para atacar (poder secundario)
        self.seleccion_nave = False ## Indica si estamos en la fase de eleccion de una nave para atacar (poder secundario)
        self.seleccion_vehiculo = False ## Indica si estamos en la fase de eleccion de un vehiculo para atacar (poder secundario)
        self.pilotoX = False ## Ver si se ha colocado un piloto capaz de inutilizar al hangar (Kylo y Poe en naves concretas)

        #Score
        self.score = 0 
        self.score_rival = 0

        ## Sonido
        self.sonido = True # Activo por defecto

        self.card_hangar = [] ## Cartas que estan en el HANGAR, no se cuentan en el recuento de puntos. 1 carta maxima por hangar
        self.hangar = False # Indica si la carta ha sido colocada en el hangar
        self.count_hangar = 1 # contador que indica las veces que se puede usar el hangar
        self.count_hangar_rival = 1 # contador que indica las veces que se puede usar el hangar por parte del rival

        ## Indica la accion a llevar a cabo posible como texto
        self.text_action = ''

    def Events(self):
        
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if not self.start:
                pygame.display.update()
                break

            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == 27):
                exit()

            elif event.type == pygame.KEYDOWN: # Pulsa ESC
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

            if event.type == pygame.MOUSEMOTION:
                # MOVIMIENTO DEL RATON

                self.upgrade_screen()
                
                # ZOOM CARTAS cuando pasa raton por encima
                if len(self.msg_scr) == 0:
                    ## Si no hay mensajes emergentes se puede hacer zoom a las cartas
                    self.card_mouse = zoom_cards(self.card_mano,self.card_mesa,self.card_hangar,self.juega,self.naves)
                    ## Mostrar info de la carta 
                    info_card(self.screen,self.card_mesa,self.ataque,self.defensa,self.ataque_rival,self.defensa_rival,self.bando)
                else:
                    ## En caso de que haya un mensaje emergente con cartas hacemos zoom a las cartas que hay dentro
                    if self.selecciona: # Esta variable indica que estamos seleccionado una de las que se muestran
                        self.card_select = zoom_cards_select(self.card_msg)
                    else:
                        zoom_cards_msg(self.card_msg)

                # Vamos a chequear que la carta que se esta moviendo puede jugarse en una posicion, cambiando cursor raton
                if self.moving:      
                    # Chequeamos si la carta puede ponerse sobre un frame cambiando puntero de raton
                    self.mousech, self.accion, action_text = check_cursor_movingcard_mouse(self.frame_scr,self.card_mesa,self.card_move,self.card_hangar,self.count_hangar)
        
                elif self.selecciona: # Hay un popup en el juego y nos dice que tenemos que seleecionar entre varias cartas
                    self.mousech, self.accion, action_text = check_card_select(self.card_msg)

                else:   
                    self.mousech, self.accion, action_text = check_cursor_mouse(self.text_scr,self.btn_scr,self.fase,self.card_mesa,self.card_move,self.ataque,self.defensa_rival,self.seleccion_tropa,self.seleccion_nave,self.seleccion_vehiculo)
                    
                    if self.pilotoX and self.fase == 1 and not self.hangar_out_rival and not self.mousech: # Si se cumplen las condiciones de piloto y nave. Si colocamos el cursor encima del hangar, se puede destruir
                        self.mousech, self.accion, action_text = check_cursor_hangar(self.frame_scr,self.bando) # accion = 'HD' si el raton esta encima del hangar
                # Cambiar cursor raton si hay accion posible     
                change_cursor_mouse(self.mousech,self.accion)

                # Pintamos la accion que es posible de ejecutar en formato texto si existe, abajo sobre las cartas 
                Text_scr(self.screen,action_text,(680,685),globals.normal_font,False,(100,100,100))

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #print (event)
                # Pulsa sobre el text SALIR
                if self.text_scr[0].rect.collidepoint(pygame.mouse.get_pos()):
                    # Puede salir en cualquier momento
                    pygame.quit()
                    exit()
###########################################
                ##### DEBUG
                if self.text_scr[4].rect.collidepoint(pygame.mouse.get_pos()) and self.text_scr[4].text == 'DEBUG':
                    print "BANDO: "+self.bando
                    print "CARTAS MANO\n"
                    for card in self.mano:
                        print card.nombre+" "
                    
                    if self.ejecutor == None:
                        print "Ejecutor: None"
                    else:
                        print "Ejecutor: "+self.ejecutor.carta.nombre
                    connection.Send({"action": "ask_mano", 
                        "jugador": self.num, 
                        "partida": self.gameid})
                    if self.card_move != []:
                        print "\nJUGANDO: "+self.card_move.carta.nombre

                    print "CARTAS MESA\n"    
                    for card in self.card_mesa:
                        print card.carta.nombre+"\t"
                        print 'Valor '+str(card.carta.valor)+"\t"
                        print 'Defensa '+str(card.carta.defensa)+"\t"
                        print 'Evasion '+str(card.carta.evasion*10)+"%\t"
                    
                    print "ELIMINADOS\n"    
                    for card in self.card_eliminadas:
                        print card.nombre+"\t"

                    #print "TABLERO\n"    
                    #for card in self.tablero:
                    #    try:
                    #        print card['card'].carta.nombre+"\t"
                    #    except:
                    #        print card['card']
                    #        print "\t"

                    print "NAVES \n"
                    for naves in self.naves:
                        i = 0
                        for nave in naves:
                            print nave.carta.nombre+"\t"
                            if i == 0:
                                print 'Valor '+str(nave.carta.valor)+"\t"
                                print 'Defensa '+str(nave.carta.defensa)+"\t"
                                print 'Ataque '+str(nave.carta.ata)+"\t"
                                print 'Evasion '+str(nave.carta.evasion)+"\t"
                                print 'Tripulacion '+str(nave.carta.tripulacion)+"\t"
                            i += 1
                        print '\n'

#############################################
                # Pulsa sobre el texto FINALIZAR TURNO  
                elif self.text_scr[1].rect.collidepoint(pygame.mouse.get_pos()) and self.juega and self.text_scr[1].flash:
                    self.fin_turno()

                # Pulsa sobre el texto SALTAR ACCION
                elif self.text_scr[2].rect.collidepoint(pygame.mouse.get_pos()) and self.juega and (self.fase < 4) and self.text_scr[2].flash:
                    self.fase += 1
                    
                    if self.ejecutor != None: ## Si hay un ejecutor hacemos que aplique su poder
                        self.card_move = self.ejecutor

                    self.text_scr[2].flash = False ## No puede haber mas de dos acciones por turno
                    texto = self.set_text_accion()
                    if texto == '':
                        self.fin_turno()
                    else:
                        self.text_action = texto
                    self.upgrade_screen()
                
                #Pulsa en PODER SECUNDARIO / ACTIVAR PODER de la carta
                elif self.text_scr[3].rect.collidepoint(pygame.mouse.get_pos()) and self.juega and self.text_scr[3].flash:
                    self.text_scr[1].flash = False ## Desactivamos boton de fin de turno
                    self.text_scr[3].flash = False ## Desactivamos boton de poder

                    if not self.poder_secundario():
                        self.fin_turno() ## Depende del poder secundario            
                
                elif self.accion == 'HD': ## Inutilizar el Hangar del rival
                    self.hangar_out_rival = True
                    self.count_hangar_rival = 0
                    for card in self.card_hangar:
                        if card.carta.bando != self.bando: # eliminar la posible carta que hubiera en el hangar rival
                            self.card_hangar.remove(card)
                            break
                    print "Se ha destruido el hangar rival"

                    connection.Send({"action": "update_mesa", 
                        "jugador": self.num, 
                        "partida": self.gameid,
                        "accion": 'HD'})
                    self.fin_turno()

                # Fase de SELECCIONAR carta entre varias. Jugar carta seleccionada
                elif self.selecciona and self.accion == 'S':

                    # Resetea variables de seleccion
                    self.selecciona = False
                    self.card_msg = []
                    self.msg_scr = []
                    self.btn_scr = []

                    if self.card_mazo: # Seleccionar entre cartas del mazo
                        self.card_mazo = False
                        
                        # Ver que carta se ha elegido para actualizar la baraja
                        if self.card_select.carta == self.baraja[self.ncards]: # Si elige justo la que le tocaba no hacer nada
                            a = 0 # no hacer nada
                        elif self.card_select.carta == self.baraja[self.ncards+1]:
                            self.baraja[self.ncards+1] = self.baraja[self.ncards]
                        #elif self.card_select.carta == self.baraja[self.ncards+2]: # En caso de seleccionar 3 en vez de 2
                        #    self.baraja[self.ncards+2] = self.baraja[self.ncards]
                        self.baraja[self.ncards] = self.card_select.carta # Actualizamos la baraja con la carta seleccionada, como si estuviera en esa posicion

                        self.ncards += 1                        
                        ## Si hemos llegado al final de la baraja:
                        # cambiar la imagen del deck
                        # Resetear hangares
                        # impedir movimiento hangares
                        self.es_fin_mazo()
                        
                    else: # Accion sobre mazo de eliminados. Seleccionar entre eliminados
                        self.card_eliminadas.remove(self.card_select.carta) # Quitamos la carta de eliminados
                        
                        # Aqui tenemos que hacer un reset de los valores de la carta a los originales
                        #Hay dos cartas que no estan en la baraja original, Anakin Oscuro y Estrella de la muerte expuesta. Resetear sus valores
                        if self.card_select.carta.id == 127: # Anakin oscuro 
                            self.card_select.carta = anakin_oscuro()

                        elif self.card_select.carta.id == 155: # Estrella de la muerte expuesta
                            self.card_select.carta = ds_expuesta()

                        else: # Resto de cartas aparecen en sus respectivas barajas
                        # Cogemos la carta original de la baraja
                            if self.bando == 'I':
                                baraja = barajar_imperio()
                            elif self.bando == 'R':     
                                baraja = barajar_aliados()

                            for elegida in baraja:
                                if elegida.id == self.card_select.carta.id:
                                    self.card_select.carta = elegida
                                    break

                    self.update_mano('A',self.card_select.carta)
                    self.reset() ## Se actualiza la mano con la nueva carta
                    self.rejuega = True
                    self.bloquea_mano_menos(self.card_select.carta)
                    self.bloquea_hangar('Todo')

                # BOTONES EMERGENTES DE MENSAJES
                elif len(self.btn_scr) > 0:
                    if self.btn_scr[0].rect.collidepoint(pygame.mouse.get_pos()):
                        #Estos botones suelen salir cuando es un mensaje emergente con cierta informacion. Se resetea
                        if self.fase > 0:
                        # Si estamos en la fase 0 no podemos finalizar el turno, porque todavia no ha empezado
                        # El mesaje emergente que tenga sera informativo del otro rival
                            self.fin_turno()
                        else:
                            self.msg_scr = []
                            self.btn_scr = []
                            self.card_msg = []
                ## BOTON SONIDO
                elif self.frame_scr[14].rect.collidepoint(pygame.mouse.get_pos()):
                    if self.sonido and globals.pc_sound:
                        self.sonido = False
                        for i in range(len(self.frame_scr)):
                            if self.frame_scr[i].bando == 'X':
                                self.frame_scr[i].obj = globals.sound_off
                                break                    
                        #self.frame_scr[12] = Frame_scr(self.screen,globals.sound_off,(1565,10),10,'X')
                        globals.background_sound.stop()
                    elif globals.pc_sound:
                        self.sonido = True
                        for i in range(len(self.frame_scr)):
                            if self.frame_scr[i].bando == 'X':
                                self.frame_scr[i].obj = globals.sound_on
                                break
                        globals.background_sound.play(-1)

                #################################################
                # FASE DE ATAQUE
                ###################################################
                # Fase 1 es el ataque de cualquier tipo de carta
                # Fase 2 es la bonificacion de ataque de una carta
                if self.fase >= 1 and self.accion == 'A' and self.juega:
                    # Primero chequeamos indice de evasion o probabilidad de ataque
                    #print "Ataque"
                    if self.ignora_evasion: # Ver si la carta que ataca ignora avasion
                        a = 10
                        self.ignora_evasion = False ## Reseteamos variable
                    else:
                        a = random.randint(1,10)

                    if (a - self.card_mouse.carta.evasion) <= 0:
                        # Me acabo de librar de un ataque informar con un mensaje
                        if self.sonido and globals.pc_sound: globals.error_sound.play()
                        #self.mensage_emergente('La carta se ha evadido del ataque')

                    else: # Se ha superado el indice de evasion
                        if self.card_mouse.carta.tipo in [9,10,11]:
                            # buscamos la nave en la lista y eliminamos todas su tripulacion as well
                            for nave in self.naves:
                                if nave[0] == self.card_mouse:
                                    # Habra que ir eliminando todos los tripulantes de la nave
                                    for tripulacion in nave:
                                        # Vamos borrando la tripulacion y nave de la mesa
                                        #print "Tripulacion a eliminar: "+tripulacion.carta.nombre
                                        self.card_mesa.remove(tripulacion)
                                        ## Tengo que indicar al rival que he borrado una carta y que actualice su mesa
                                        connection.Send({"action": "update_mesa", 
                                            "idcard": tripulacion.carta.id, 
                                            "jugador": self.num, 
                                            "partida": self.gameid,
                                            "accion": 'E'})
                                    # Borramos la nave y todos sus tripulantes de self.naves
                                    print "Se ha eliminado la nave "+nave[0].carta.nombre+' con su tripulacion'
                                    self.naves.remove(nave)
                                    break
                        else:
                            # La carta a eliminar es tropa terrestre
                            print self.card_mouse.carta.nombre
                            self.card_mesa.remove(self.card_mouse)

                            ## Tengo que indicar al rival que he borrado una carta y que actualice su mesa
                            connection.Send({"action": "update_mesa", 
                                "idcard": self.card_mouse.carta.id, 
                                "jugador": self.num, 
                                "partida": self.gameid,
                                "accion": 'E'})
                            print "Se ha eliminado la carta "+self.card_mouse.carta.nombre

                            # Comprobar si la carta eliminada alteraba modificadores del tablero
                            if self.card_mouse.carta.modificador:
                                print "Se disipan sus modificadores terrestres"
                                self.unset_modificadores()
                        
                        # Sonido de ataque dependiendo de quien ataca
                        if self.sonido and globals.pc_sound: attack_sound(self.card_move.carta.tipo,self.bando)

                        # Notificar al rival para que actualice el marcador
                        self.update_score()
                        connection.Send({"action": "update_score", 
                            "jugador": self.num, 
                            "partida": self.gameid})

                    if self.fase >= self.card_move.carta.nactions:
                        self.text_scr[2].flash = False ## No puede haber mas de dos acciones por turno
                        self.text_scr[3].flash = False 
                        self.fin_turno()
                    else:
                        # La carta tiene mas acciones (2)
                        if self.ejecutor != None:
                            # Es una nave a la que se le ha colocado un tripulante con reataque y es el que aplica poder secundario
                            self.card_move = self.ejecutor

                        self.text_scr[2].flash = False ## No puede haber mas de dos acciones por turno
                        texto =  self.set_text_accion()
                        if texto == '':
                            # No puede aplicar accion que tiene
                            self.text_scr[3].flash = False 
                            self.fin_turno()
                        else:
                            self.text_action = texto
                            self.fase += 1
                
                elif self.fase == 2 and self.accion == 'S': ## Fase 2 Seleccion de carta de tropa o nave
                    if self.card_mouse.carta.tipo == 10 and self.seleccion_nave:
                        ## La carta de nave de asalto seleccionada puede atacar como si hubieran colocado un piloto en la misma
                        self.text_scr[1].flash = True
                        self.fase -= 1
                        self.text_action = "2. ATACA CON LA NAVE"
                        self.card_move = self.card_mouse
                        self.seleccion_nave = False
                        print "Se ha seleccionado la nave "+self.card_move.carta.nombre+ ' para atacar'

                    elif self.card_mouse.carta.tipo == 7 and self.seleccion_vehiculo:
                        ## La carta de vehiculo seleccionada puede atacar de nuevo
                        self.text_scr[1].flash = True
                        self.fase -= 1
                        self.text_action = "2. ATACA CON VEHICULO"
                        self.card_move = self.card_mouse
                        self.seleccion_vehiculo = False
                        print "Se ha seleccionado el vehiculo "+self.card_move.carta.nombre+ ' para atacar'

                    elif self.card_mouse.carta.tipo in [0,1,2] and self.seleccion_tropa: ## Llamado por Vader o Obi-Wan Viejo
                        # La carta seleccionada de TROPA O PILOTO que estuviera como tropa terrestre se vuelve a jugar otra vez
                        for card in self.card_mesa:
                            if card.carta.id == self.card_mouse.carta.id and not card.carta.en_nave:
                                
                                self.card_mesa.remove(card)
                                self.tablero = liberar_posicion(card,self.tablero)
                                print "Se ha seleccionado "+card.carta.nombre+' para rejugarla'
                                ## Tengo que indicar al rival que he borrado esa carta seleccionada de la mesa
                                connection.Send({"action": "update_mesa", 
                                    "idcard": card.carta.id, 
                                    "jugador": self.num, 
                                    "partida": self.gameid,
                                    "accion": 'E'})
                                if self.card_mouse.carta.modificador:
                                    print "Se disipan sus modificadores terrestres"
                                    self.unset_own_modificadores()

                                self.update_score()
                                
                                #self.mano.append(card.carta)
                                self.update_mano('A',card.carta)
                                self.reset() ## Se actualiza la mano con la nueva carta
                                self.rejuega = True
                                self.bloquea_mano_menos(card.carta)
                                self.bloquea_hangar('Todo')

                                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                                self.card_msg.append(Card_scr(self.screen,card.carta,(750,325)))
                                self.msg_scr.append(Text_scr(self.screen,"CARTA SELECCIONADA - JUEGALA AHORA",(620,280),globals.menu_font2,False,(255,255,255)))
                                self.btn_scr.append(Text_scr(self.screen,"OK",(782,498),globals.menu_font,True,(100,100,100)))
                                break
               ##################################################################

            if event.type == pygame.MOUSEBUTTONUP:
                
                # Comprobamos si se ha soltado sobre una carta de Nave y con posible ubicacion
                for index in range(len(self.card_mesa)):
                    card_nave = self.card_mesa[index]
                    # Se chequea la nave sobre la que nos posicionamos
                    ##################################
                    ### SUELTA LA CARTA SOBRE OTRA (UNA NAVE)
                    ####################################
                    if card_nave.rect.collidepoint(pygame.mouse.get_pos()) and self.moving and card_nave.carta.tipo in [9,10,11]:
                        card_nave = self.check_cardmesa_cardv2(card_nave)
                        
                        if not self.card_colocada:
                            break

                        ## Actualizamos la carta de nave con los datos modificados (tripulacion, dirigentes...)                   
                        self.card_mesa[index] = card_nave
                        
                        print "Tripulante colocado en: "+self.card_mesa[index].carta.nombre
                        # Enviar los cambios en la carta al rival 
                        connection.Send({"action": "update_mesa", 
                            "idcard": card_nave.carta.id, 
                            "jugador": self.num, 
                            "partida": self.gameid, 
                            "tripulacion": card_nave.carta.tripulacion,
                            "dirigentes": card_nave.carta.dirigentes,
                            "defensa": card_nave.carta.defensa,
                            "ataque": card_nave.carta.ata,
                            "evasion": card_nave.carta.evasion,
                            "accion": 'N'})
                        break

                # Si no ha puesto la carta sobre otra, chequeamos si la ha puesto encima de un frame
                if not self.card_colocada:
                    for frame in self.frame_scr:
                        if frame.rect.collidepoint(pygame.mouse.get_pos()) and self.moving:
                            pos_new_card = self.check_frame_cardv2(frame)
                            if frame.bando == 'E' and self.card_colocada:
                                # Se ha soltado sobre la pila de eliminados
                                self.eliminada = True
                                self.hangar = False
                            elif frame.tipo == 2 and self.card_colocada:
                                # Se ha soltado en el hangar
                                self.hangar = True
                                self.eliminada = False
                            else:
                                self.hangar = False
                                self.eliminada = False
                            break

                self.moving = False
            
                ## Si se cumple esta condicion es que se ha colocado una carta, luego SE HA JUGADO UNA CARTA 
                if self.card_colocada:
                    
                    # Ha colocado la carta en algun frame o parte de la pantalla, luego la ha jugado
                    self.card_colocada = False
                    self.bloquea_mano_menos(self.card_move.carta)
                    self.bloquea_hangar('Todo')
    
                    ## Al colocarse una carta en el tablero se actualiza la mano y la mesa
                    self.actualizar_mesa()

                    if not self.eliminada:
                        
                        ## Si la carta que se ha colocado tiene las mismas acciones que la fase, fin de turno.
                        if self.hangar:
                            ## CARTA (Nave de asalto) SOLTADA SOBRE EL HANGAR
                            
                            self.hangar = False
                            connection.Send({"action": "update_mesa", 
                                "idcard": self.card_move.carta.id, 
                                "jugador": self.num, 
                                "partida": self.gameid, 
                                "pos": self.card_move.pos,
                                "accion": 'H'})
                            self.fin_turno()
                        
                        ################################################
                        ## CARTA COMO TRIPULANTE O DIRIGENTE EN UNA NAVE
                        ##################################################
                        elif self.card_move.carta.tipo not in [7,9,10,11] and self.card_move.carta.en_nave:
                            
                            if self.card_move.carta.id in [115,132] and card_nave.carta.id == 155: # Krennic y Astromecanico en Estrella Danyada
                                print "Reparar escudos de la Estrella de la muerte"                                    
                                self.poder_secundario()

                            if self.card_move.carta.reataque:
                                
                                # Ojo que el tripulante ha cambiado los parametros de la nave ya
                                self.text_scr[1].flash = True
                                self.fase += 1
                                self.text_action = "2. ATACA CON LA NAVE"

                                if self.card_move.carta.id in [21,123,127]: # Anakin, Darth Vader y anakin convertido, ignoran evasion en ataque con nave
                                    self.ignora_evasion = True

                                if self.card_move.carta.nactions > 1:
                                    if self.card_move.carta.id in [17,117]: # Ackbar y Veers tienen una accion adicional
                                        self.seleccion_nave = True
                                    else:
                                        # Guardamos el ejecutor para que pueda aplicar su poder despues de que termine el ataque de nave
                                        self.ejecutor = self.card_move
                                    self.text_scr[2].flash = True

                                # Cambiar card_move para que sea la nave la que ataca, simulando que ha colocado la nave
                                self.card_move = card_nave
                                self.card_move.carta.nactions = 2  ## Cambiamos el numero de acciones de la nave para que pueda pedir apoyo

                            ## DROIDE DE INTERROGATORIO
                            elif self.card_move.carta.id == 131:
                                self.text_scr[1].flash = True ## Activamos finalizar turno
                                self.fase += 1
                            
                            # DROIDE DE PROTOCOLO
                            elif self.card_move.carta.id in [30,130]:
                                # Bloquear nave
                                self.fin_turno()
                            else: 
                                # Chequear si tiene acciones secundarias
                                if self.card_move.carta.nactions > 1:
                                    self.text_scr[1].flash = True
                                    self.text_scr[2].flash = False 
                                    texto =  self.set_text_accion()
                                    if texto == '':
                                        self.text_scr[3].flash = False 
                                        self.fin_turno()
                                    else:
                                        self.text_action = texto
                                        self.fase += 1
                                else:
                                    # no tiene poderes, luego fin de turno
                                    self.fin_turno()
                        ####################################
                        # COLOCADAS CARTAS SIN ACCIONES: NAVES 
                        ####################################
                        elif self.card_move.carta.nactions == 0:
                            # Cartas con 0 acciones (Naves de asalto o droides)
                            connection.Send({"action": "update_mesa", 
                                "idcard": self.card_move.carta.id, 
                                "jugador": self.num, 
                                "partida": self.gameid, 
                                "pos": self.card_move.pos,
                                "accion": 'C'})
                            self.fin_turno()

                        ################################################
                        ## CARTA COMO TROPA TERRESTRE
                        ##################################################                        
                        else: 
                            ## Despues de la primera accion o colocar una carta se activan los botones de:
                            self.text_scr[1].flash = True # FIN TURNO activo

                            self.fase += 1 # Una vez colocada la carta pasamos a fase 1

                            self.text_action = "2. APLICA SU PODER PRINCIPAL"
                            # Enviamos las coordenadas y carta colocada en frame al rival
                            connection.Send({"action": "update_mesa", 
                                "idcard": self.card_move.carta.id, 
                                "jugador": self.num, 
                                "partida": self.gameid, 
                                "pos": self.card_move.pos,
                                "accion": 'C'})

                            ### Revisamos que tipos de cartas hay en el tablero para activar acciones y ver si pasamos turno
                            hay_tropas = False # Hay tropas terrestres rivales
                            hay_rival = False # Hay cartas terrestres rivales
                            hay_vehi = False # Vehiculo aliado
                            hay_aliados = False # Hay tropas terrestres aliadas
                            for item in self.card_mesa:
                                # Cartas terrestres RIVAL
                                if (item.carta.bando != self.bando) and item.carta.tipo < 9:
                                    if item.carta.tipo == 7: # Vehiculos
                                        hay_rival = True
                                    elif item.carta.tipo in [0,1] and not item.carta.en_nave: ## Tropas
                                        hay_tropas = True
                                        hay_rival = True
                                    elif item.carta.tipo in [2,3,4,5,6,8] and not item.carta.en_nave: ## El resto
                                        hay_rival = True
                                # Cartas terrestres PROPIAS
                                elif (item.carta.bando == self.bando) and item.carta.tipo < 9:
                                    if item.carta.tipo == 7: # Vehiculos
                                        hay_vehi = True
                                    elif item.carta.tipo in [0,1,2] and not item.carta.en_nave: ## Tropas y pilotos
                                        hay_aliados = True
#                                    elif item.carta.tipo in [3,4,5,6,8] and not item.carta.en_nave: ## El resto
#                                        hay_otros = True
                            if self.card_move.carta.nactions > 1:
                                if self.card_move.carta.id in [7,166]: #Comando clon y Nute Gunray
                                    if hay_vehi:
                                        self.seleccion_vehiculo = True
                                    else:
                                        self.text_scr[2].flash = False
                                elif self.card_move.carta.id in [25,125] and not hay_tropas: #Vindu & Kylo
                                    self.text_scr[2].flash = False
                                
                                elif self.card_move.carta.id in [17,117]: # Ackbar & Veers. Al colocarse como tropa no activan poder secundario
                                    self.text_scr[2].flash = False
                                elif self.card_move.carta.id in [27,123] and not hay_aliados: #Vader & Obi Wan
                                    self.text_scr[2].flash = False
                                else:
                                    # Si la carta tiene mas de un movimiento activamos boton de NEXT ACTION
                                    self.text_scr[2].flash = True
                            
                            # Cartas con casuisticas especiales
                            eliminar = False
                            if self.card_move.carta.id in [6,161]: # Rogue One y Boba Fett ignoran evasion en ataque
                                self.ignora_evasion = True
                            
                            ## Casuistica especial cuando se coloca a ANAKIN CONVERTIDO COMO TROPA y JABA EL HUTT
                            elif self.card_move.carta.id == 127: ## ANAKIN CONVERTIDO
                                print "Anakin colocado"
                                eliminar = True
                                eliminado = 166 # Nute Gunray
                            elif self.card_move.carta.id == 160: ## JABBA EL HUTT
                                eliminar = True
                                eliminado = 61 ## Han solo

                            if eliminar and hay_rival:
                                for card in self.card_mesa:
                                    if card.carta.id == eliminado and not card.carta.en_nave: # eliminado en la mesa pero como tropa
                                        # eliminado esta como tropa terrestre
                                        self.card_mesa.remove(card)

                                        ## Tengo que indicar al rival que he borrado una carta y que actualice su mesa
                                        connection.Send({"action": "update_mesa", 
                                            "idcard": card.carta.id, 
                                            "jugador": self.num, 
                                            "partida": self.gameid,
                                            "accion": 'E'})
                                        # Notificar al rival para que actualice el marcador
                                        self.update_score()
                                        connection.Send({"action": "update_score", 
                                            "jugador": self.num, 
                                            "partida": self.gameid})
                                        break
                            if not hay_rival and self.card_move.carta.nactions == 1:
                                self.fin_turno()

                    else:   
                        ## CARTA ELIMINADA
                        ## CAMBIAR TURNO AL OTRO JUGADOR
                        self.eliminada = False
                        self.fin_turno()

                else:
                    ## Se DESBLOQUEAN las cartas para que pueda hacerse zoom o moverse (no se ha colocado ninguna carta todavia)
                    # Seguimos en fase 0 y jugando
                    if self.fase == 0 and self.juega and not self.rejuega:
                        for bloquear in self.card_mano:
                            if self.card_move != bloquear: 
                                bloquear.lock = False
                        
                        self.bloquea_hangar(self.bando)

            if pygame.mouse.get_pressed()==(1,0,0):
                
                # Cartas de la mano que esten desbloqueadas
                for card in self.card_mano:
                    if not card.lock and card.rect.collidepoint(pygame.mouse.get_pos()):
                        self.card_move = card
                        self.moving = True
                        ## Para que no haya problemas en el arrastre cuando pasa por encima de otra carta
                        for bloquear in self.card_mano:
                            if self.card_move != bloquear:
                                bloquear.lock = True
                        self.bloquea_hangar('Todo')
                                
                        if len(self.msg_scr) > 0:
                            # Si hay mensajes emergentes los quitamos
                            self.msg_scr = []
                            self.card_msg = []
                            self.btn_scr = []
                        break

                # Cartas del hangar que esten desbloqueadas
                # Si se nos han acabado las cartas del mazo, ya no se puede mover la carta del hangar
                for card in self.card_hangar:
                    if not card.lock and not self.hangar_out and (self.ncards < len(self.baraja)) and card.rect.collidepoint(pygame.mouse.get_pos()):
                        self.card_move = card
                        self.moving = True
                        ## Para que no haya problemas en el arrastre cuando pasa por encima de otra carta
                        for bloquear in self.card_mano:
                            bloquear.lock = True

                        if len(self.msg_scr) > 0:
                            # Si hay mensajes emergentes los quitamos
                            self.msg_scr = []
                            self.card_msg = []
                            self.btn_scr = []
                        break

                if self.moving:
                    x-= self.card_move.obj.get_width() / 2
                    y-= self.card_move.obj.get_height() / 2
                    self.screen.blit(self.card_move.obj, (x, y))

            pygame.display.update()

    def bloquea_mano_menos(self,card):
        # Bloquea todas las cartas de la mano menos la que llega como parametro
        for i in range(len(self.card_mano)):
            if self.card_mano[i].carta != card:
                self.card_mano[i].lock = True
            else:
                self.card_mano[i].lock = False

    def bloquea_hangar(self,bando):
        # Se bloquean las cartas del hangar salvo las del mismo bando cuando se especifique
        # Si recibe 'Todo' como argumento se bloquean los dos bandos
        for i in range(len(self.card_hangar)):
            if self.card_hangar[i].carta.bando == bando:    
                self.card_hangar[i].lock = False
            else:
                self.card_hangar[i].lock = True 
    def update_mano(self,accion,carta):
        # Esta funcion actualiza la mano y se lo comunica al servidor
        if accion == 'A': # Anyade carta a tu mano
            self.mano.append(carta)
        elif accion == 'R': # Borra carta de tu mano
            self.mano.remove(carta)
        
        ## Actualizar en el server la mano
        connection.Send({"action": "update_mano", 
            "idcard": carta.id, 
            "accion": accion,
            "jugador": self.num, 
            "partida": self.gameid})         

    def actualizar_mano(self):
        # Si sigue habiendo cartas en el mazo, actualizamos la mano hasta tener 3 cartas
        while self.ncards < len(self.baraja) and (len(self.mano) <3):
            
            self.update_mano('A',self.baraja[self.ncards])
            # Anyade la siguiente carta del mazo a tu mano
#            self.mano.append(self.baraja[self.ncards])
                        
            ## Actualizar en el server la mano
#            connection.Send({"action": "update_mano", 
#                "idcard": self.baraja[self.ncards].id, 
#                "accion": 'A',
#                "jugador": self.num, 
#                "partida": self.gameid}) 

            self.card_mano = pintar_mano(self.screen,self.mano,False)
            self.ncards += 1
            self.es_fin_mazo()

    def es_fin_mazo(self):            
        ## Si hemos llegado al final de la baraja cambiar la imagen del deck
        if self.ncards == len(self.baraja):
            if self.bando == 'R':
                new_deck = globals.rebels_deck0
            elif self.bando == 'I':
                new_deck = globals.empire_deck0

            self.hangar_out = True

            for i in range(len(self.frame_scr)):
                if self.frame_scr[i].bando == 'D':
                    self.frame_scr[i].obj = new_deck
                    self.frame_scr[i].draw()
                    break

            # Comunicar al rival
            self.count_hangar = 0

            connection.Send({"action": "update_mesa", 
                "jugador": self.num, 
                "partida": self.gameid,
                "accion": 'F'})

    def actualizar_mesa(self):
        # Esta funcion actualiza la mano, despues de colocar una carta
        
        # La carta se ha movido del hangar
        if self.card_move in self.card_hangar: # La carta se ha cogido del hangar para colocarlo en la mesa
            self.card_hangar.remove(self.card_move)

            # Notificar al rival de que se ha movido la carta de frame y que actualice mesa
            connection.Send({"action": "update_mesa", 
                "idcard": self.card_move.carta.id, 
                "jugador": self.num, 
                "partida": self.gameid,
                "accion": 'M'})

        else: 
            # La carta se ha cogido de la mano 
            self.update_mano('R',self.card_move.carta)
            self.card_mano.remove(self.card_move)  ## Elimina la carta Tipo Card_scr de la mano 

        # Pintar la carta o lo mismo se ha eliminado
        if self.card_move.pos[0] > 0 and self.card_move.pos[1] > 0:
            # Comprobamos que la carta no se ha eliminado a las que se les da la posicion (0,0)

            if self.hangar:
                # La carta se ha posicionado en el hangar 
                self.card_hangar.append(self.card_move)
            else:
                # La carta se ha posicionado en la mesa     
                self.card_mesa.append(self.card_move)
                
                # Si la carta tiene modificadores globales, aplicarlos
                if not self.card_move.carta.tipo in [9,10,11] and self.card_move.carta.modificador:
                    self.set_modificadores()
                    
            self.card_move.draw()
            # Como ha cambiado la mesa, actualizar el marcador
            self.update_score()
            # Notificar al rival para que actualice el marcador
            connection.Send({"action": "update_score", 
                "jugador": self.num, 
                "partida": self.gameid})
#        else:
#            ## Lo anyade a la pila de eliminados
#            self.card_eliminadas.append(self.card_move.carta)
    
#############################
##### MODIFICADORES
#############################
    def unset_modificadores(self):
        # Esta funcion se llama cuando se ELIMINA una carta que tiene modificadores aplicados al terreno
        # Eliminar el efecto de dicha carta
        # Ver set_modificadores(). Hace totalmente lo contrario
        # self.card_mouse es la carta del rival a eliminar

        #DEFENSA
        if self.card_mouse.carta.terrain_def > 0:
            self.defensa_rival -= self.card_mouse.carta.terrain_def
            self.send_modificadores(0)
        elif self.card_mouse.carta.terrain_def == -1:
            self.defensa += 1
            self.send_modificadores(-2)
        #ATAQUE
        if self.card_mouse.carta.terrain_ata > 0:
            self.ataque_rival -= self.card_mouse.carta.terrain_ata
            self.send_modificadores(0)
        elif self.card_mouse.carta.terrain_ata == -1:
            self.ataque += 1
            self.send_modificadores(-2)
    def unset_own_modificadores(self):
        # Esta funcion se llama cuando se SELECCIONA para jugar de nuevo una carta propia que cambia los modificadores terrestres
        # Eliminar el efecto de dicha carta. si se coloca otra vez, se aplica con el efecto de colocarla
        # self.card_mouse es la carta propia a rejugar
        #DEFENSA
        if self.card_mouse.carta.terrain_def > 0:
            self.defensa -= self.card_mouse.carta.terrain_def
            self.send_modificadores(-2)
        elif self.card_mouse.carta.terrain_def == -1:
            self.defensa_rival += 1
            self.send_modificadores(0)
        #ATAQUE
        if self.card_mouse.carta.terrain_ata > 0:
            self.ataque -= self.card_mouse.carta.terrain_ata
            self.send_modificadores(-2)
        elif self.card_mouse.carta.terrain_ata == -1:
            self.ataque_rival += 1
            self.send_modificadores(0)

    def set_modificadores(self):
        if self.card_move.carta.tipo == 7 or not self.card_move.carta.en_nave:
            # Se llama cuando se COLOCA una carta
            # Si la carta se coloca como tripulante no aplica modificadores
                
            # Distinguimos entre los que modifican los parametros propios y los ajenos
            # Si el valor de ataque o defensa es -1 es que modifica los ajenos, sino solo los propios

            #DEFENSA
            if self.card_move.carta.terrain_def > 0:
                self.defensa += self.card_move.carta.terrain_def
                self.send_modificadores(1)
            elif self.card_move.carta.terrain_def == -1:
                self.defensa_rival -= 1
                self.send_modificadores(-1)
            # ATAQUE        
            if self.card_move.carta.terrain_ata > 0:
                self.ataque += self.card_move.carta.terrain_ata
                self.send_modificadores(1)
            elif self.card_move.carta.terrain_ata == -1:
                self.ataque_rival -= 1
                self.send_modificadores(-1)

    def send_modificadores(self,accion):
        # Esta funcion notifica al rival las modificaciones que se hacen en los modificadores terrestres

        # accion = -2 Se ha eliminado la carta que modificaba parametros del rival
        # accion = -1 La carta jugada altera modificadores del rival
        # accion = 0 Se ha eliminado una carta que alteraba modificadores del jugador rival
        # accion = 1 La carta jugada altera modificadores del propio jugador

        connection.Send({"action": "update_mods", 
            "jugador": self.num, 
            "partida": self.gameid,
            "defensa": self.defensa,
            "ataque": self.ataque,
            "def_rival": self.defensa_rival,
            "ata_rival": self.ataque_rival,
            "accion": accion})
#############################################################

#######################################
########## ACCION DE COLOCAR CARTA SOBRE OTRA
#######################################

    def check_cardmesa_cardv2(self,card_nave):
        # Esta funcion verifica que se esta colocando una carta sobre otra en la mesa, lease nave
        self.card_colocada = False

        #pos_new_card = self.card_move.pos
        naves = [7,9,10,11]

        # Las naves o vehiculos no se posicionan unos sobre otros
        if self.card_move.carta.tipo in naves:
            
            #return pos_new_card, card_nave
            return card_nave
        
        elif self.card_move.carta.tripulante and (card_nave.carta.bando == self.card_move.carta.bando) and not self.card_move.carta.en_nave:
            # Revisar si la carta es un dirgiente sobre una Nave de combate y hay sitio
            if card_nave.carta.tipo == 9 and self.card_move.carta.dirige and (card_nave.carta.dirigentes < card_nave.carta.max_dirige) and (card_nave.carta.tripulacion < card_nave.carta.tripulacion_max):

                card_nave.carta.dirigentes += 1
                self.card_colocada = True

            # Revisar si la carta es un tripulante sobre una Nave de combate y hay sitio
            elif card_nave.carta.tipo == 9 and self.card_move.carta.tipo in [0,1,8] and (card_nave.carta.tripulacion < card_nave.carta.tripulacion_max):
                
                if self.card_move.carta.id in [65,67,165]: ## Lando, Rey y Capitan Phasma en nave de combate no reataca
                    self.card_move.carta.reataque = False

                self.card_colocada = True

            # Revisar si la carta es un tripulante sobre una Nave de asalto y hay sitio
            elif card_nave.carta.tipo == 10 and not self.card_move.carta.dirige and (card_nave.carta.tripulacion < card_nave.carta.tripulacion_max):
            
                pilotos = [28,165] ## Luke y Phasmna
                droides_nave = [31,32,33] ## R2D2 y BB-8 R5-D4
                ala_x = [42,43]
                
                # Piloto sobre nave de asalto
                if (self.card_move.carta.tipo == 2 or self.card_move.carta.id in pilotos) and (card_nave.carta.dirigentes < card_nave.carta.max_dirige):
                    card_nave.carta.dirigentes += 1
                    self.card_colocada = True
                    if self.card_move.carta.id == 35 and card_nave.carta.id == 42: # Poe Dameron en Ala-X escuadron Negro. Capaz de inutilizar hangar
                        self.pilotoX = True

                # DROIDES en Ala-X
                elif self.card_move.carta.id in droides_nave and card_nave.carta.id in ala_x and (card_nave.carta.tripulacion == card_nave.carta.dirigentes):
                    self.card_colocada = True
                
                # Darth Vader en Tie Advance
                elif self.card_move.carta.id == 123 and card_nave.carta.id == 145:
                    self.card_colocada = True

                # Kylo Ren en Tie Silencer. Capaz de inutilizar hangar
                elif self.card_move.carta.id == 125 and card_nave.carta.id == 144:
                    self.card_colocada = True
                    self.pilotoX = True

            # Revisar si la carta es un tripulante sobre una Nave de asalto especial y hay sitio            
            elif card_nave.carta.tipo == 11 and (card_nave.carta.tripulacion < card_nave.carta.tripulacion_max):
                # Chequear acciones sobre naves especiales
                naves_jedis_sith = [48,49,148] ## Naves Jedi y Sith
                no_pilotos = [20,27,28,120,126] ## Jedis y Sith que no son pilotos de naves Jedi/Sith
                pilotos_halcon = [61,65,67] ## Han Solo, Lando y Rey
                tripulantes_halcon = [60,66,67,31,32,27,18] ## Chewbacca, Finn, Rey, R2D2, BB8, ObiWan y Leia
                droides_nave = [31,32,33,132] ## R2D2 y BB-8 R5-D4 y astromecanico imperial

                # Jedi/Sith sobre nave de asalto especial que puedan ser pilotos
                if self.card_move.carta.tipo == 4 and card_nave.carta.id in naves_jedis_sith and not (self.card_move.carta.id in no_pilotos) and (card_nave.carta.dirigentes < card_nave.carta.max_dirige):
                    card_nave.carta.dirigentes += 1
                    self.card_colocada = True

                ## Boba Fett en Esclavo I
                elif self.card_move.carta.id == 161 and card_nave.carta.id == 147: 
                    self.card_colocada = True
                
                elif self.card_move.carta.id in pilotos_halcon and card_nave.carta.id == 47 and (card_nave.carta.dirigentes < card_nave.carta.max_dirige): 
                    ## Piloto Halcon y ataca. Solo puede haber un ataque de un dirigente o piloto en este caso  
                    card_nave.carta.dirigentes += 1
                    self.card_colocada = True
                
                elif self.card_move.carta.id in tripulantes_halcon and card_nave.carta.id == 47:     
                    ## Coloca tripulacion del Halcon
                    self.card_colocada = True
                    self.card_move.carta.reataque = False ## Modificamos el parametro de reataque en caso de que estuviera activo
                
                ## Coloca los droides como tripulacion en Nave Jedi Starfighter
                elif self.card_move.carta.id in droides_nave and card_nave.carta.id in naves_jedis_sith and (card_nave.carta.tripulacion == card_nave.carta.dirigentes):
                    self.card_colocada = True

        ## Si se cumple una de las anteriores condiciones, aplicar accion que corresponda
        if self.card_colocada:
            self.card_move = coloca_carta_navev2(self.card_mesa,card_nave,self.card_move)         
            card_nave = self.card_move.carta.modify_param_nave(card_nave)

            self.card_move.lock = True
            
            ## DROIDE DE PROTOCOLO sobre nave de combate. Bloquea el acceso
            if self.card_move.carta.id in [30,130]:
                if card_nave.carta.tripulacion == 0: # Solo tiene al droide, luego actualizar valor de nave a 0
                    # Buscamos la carta de nave para actualizar su valor
                    card_nave.carta.valor = 0
                card_nave.carta.tripulacion = card_nave.carta.tripulacion_max
                
                #Comunicar al rival para que actualice tripulacion de nave al maximo y marcador en caso de que no tuviera tripulacion
                accion = 'B' # Se Bloquea nave, no pueden acceder mas tripulantes
            else:
                card_nave.carta.tripulacion += 1
                accion = 'T' # Se anyade tripulante

            # Actualizar self.naves con los cambios en la nave
            for lista in self.naves:
                ## El primer elemento de la lista tiene que ser la nave donde anyadimos tripulacion
                if card_nave.carta.id == lista[0].carta.id:                      
                    self.naves[self.naves.index(lista)].append(self.card_move)
                    self.naves[self.naves.index(lista)][0].valor = card_nave.carta.valor # Actualizamos valor en self.naves
                    self.naves[self.naves.index(lista)][0].tripulacion = card_nave.carta.tripulacion # Actualizamos tripulacion en self.naves

                    break
            #Comunicar al rival para que actualice tripulacion de nave y valor en caso de que no tuviera tripulacion        
            connection.Send({"action": "update_mesa", 
                "idcard": self.card_move.carta.id, 
                "jugador": self.num, 
                "partida": self.gameid, 
                "pos": self.card_move.pos,
                "idnave": card_nave.carta.id,
                "accion": accion})

            ## Sonido de que se posiciona la carta como tripulante
            #if self.sonido and globals.pc_sound: globals.place_sound.play()
            if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,True)

        return card_nave

#####################################################
#### ACCION DE COLOCAR CARTA SOBRE FRAME O SOBRE LA MESA
#####################################################

    def check_frame_cardv2(self,frame):

        self.card_colocada = False
        pos_new_card = self.card_move.pos       
        
        ## Desde aqui se comparan frames terrestres (tipo 0)    
        tropas = [0,1,2,3,5,6]
        if frame.tipo == 0 and frame.bando == self.bando and (self.card_move.carta.tipo in tropas):
            # Tropa, Tropa especial, Lider o contrabandista. Se anyaden a la pila de tropa
            pos_new_card = self.card_move.pos
            self.card_move, self.tablero, sitio = coloca_carta(0,self.bando,self.card_move,self.tablero)

            if sitio:
                # La variable sitio nos dice si habia huecos libres para colocar la carta
                self.card_colocada = True
                if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)

        # JEDI O SITH A FRAME
        elif frame.tipo == 0 and frame.bando == self.bando and self.card_move.carta.tipo == 4: 
        
            pos_new_card = self.card_move.pos
            self.card_move, self.tablero, sitio = coloca_carta(1,self.bando,self.card_move,self.tablero)

            if sitio:
                # La variable sitio nos dice si habia huecos libres para colocar la carta
                self.card_colocada = True
                if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)
            else:
                # Lo intenta en donde van los Vehiculos
                self.card_move, self.tablero, sitio = coloca_carta(2,self.bando,self.card_move,self.tablero)                
                if sitio:
                    # La variable sitio nos dice si habia huecos libres para colocar la carta
                    self.card_colocada = True
                    if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)    

        # VEHICULO A FRAME
        elif frame.tipo == 0 and frame.bando == self.bando and self.card_move.carta.tipo == 7:
            pos_new_card = self.card_move.pos
            self.card_move, self.tablero, sitio = coloca_carta(2,self.bando,self.card_move,self.tablero)

            if sitio:
                # La variable sitio nos dice si habia huecos libres para colocar la carta
                self.card_colocada = True
                if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)   
            else:
                # Lo intenta en donde van los Jedi/Sith
                self.card_move, self.tablero, sitio = coloca_carta(1,self.bando,self.card_move,self.tablero)                
                if sitio:
                    # La variable sitio nos dice si habia huecos libres para colocar la carta
                    self.card_colocada = True
                    if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)   
        
        # Droides terrestres A FRAME
        elif frame.tipo == 0 and frame.bando == self.bando and (self.card_move.carta.tipo == 8):
            droides_terrestres = [31,32,132] ## R2-D2 y BB-8 y ASTROMECANICO
            if self.card_move.carta.id in droides_terrestres:
                pos_new_card = self.card_move.pos
                self.card_move, self.tablero, sitio = coloca_carta(0,self.bando,self.card_move,self.tablero)

                if sitio:
                    # La variable sitio nos dice si habia huecos libres para colocar la carta
                    self.card_colocada = True
                    if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)

        ## Desde aqui se comparan FRAMES DEL ESPACIO (tipo 1)   
        elif frame.tipo == 1 and frame.bando == self.bando and self.card_move.carta.tipo in [9,10,11]:
            # Naves de asalto
            pos_new_card = self.card_move.pos
            self.card_move, self.tablero, sitio = coloca_carta(3,self.bando,self.card_move,self.tablero)
            
            if sitio:
                # Anyadimos la nave a la lista de naves como lista para ir anyadiendo su tripulacion
                self.naves.append([self.card_move])
                # La variable sitio nos dice si habia huecos libres para colocar la carta
                self.card_colocada = True
                if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)
            else:
                print "No hay sitio para colocar la carta"
                if self.sonido and globals.pc_sound: globals.error_sound.play()
   
        elif frame.tipo == 2 and self.count_hangar > 0 and frame.bando == self.bando and self.card_move.carta.tipo in [10,11] and haysitio_hangar(self.card_hangar,self.bando):
            # Cheaqueamos que hay sitio en el hangar (haysitio_hangar())

            # Colocar nave de asalto en hangar
            pos_new_card = self.card_move.pos
            
            if self.bando == 'R':
                #self.card_move.pos = (25,80)
                #self.card_move.rect.x = 25
                self.card_move.pos = globals.pos_hangar_reb
                self.card_move.rect.x = globals.pos_hangar_reb[0]
                self.card_move.rect.y = globals.pos_hangar_reb[1]

            elif self.bando == 'I':
                #self.card_move.pos = (1455,80)
                #self.card_move.rect.x = 1455
                self.card_move.pos = globals.pos_hangar_imp
                self.card_move.rect.x = globals.pos_hangar_imp[0]
                self.card_move.rect.y = globals.pos_hangar_imp[1]
            
            self.count_hangar -= 1
            self.card_colocada = True
            if self.sonido and globals.pc_sound: place_sound(self.card_move.carta.id,False)

        elif frame.bando == 'E': 
            # Eliminar carta. No se anyade a la lista de la mesa
            # Si enviamos pos 0,0 como parametro esta eliminada
            self.card_move.pos = (0,0)
            self.card_eliminadas.append(self.card_move.carta)

            self.card_colocada = True  
            if self.sonido and globals.pc_sound: globals.erase_sound.play() 

        if self.card_colocada:
            # Se bloquea para que no pueda jugarse
            self.card_move.lock = True

        return pos_new_card

##########################################
######## PODER SECUNDARIO DE CADA CARTA
##########################################
    def set_text_accion(self):
        # En esta funcion se cambia el flasheado de ACCION Y LA ACCION POSIBLE, dependiendo de la carta que se juegue

        ## Valores por defecto
        text = "3. APLICA PODER SECUNDARIO"
        self.text_scr[3].flash = True

        if self.card_move.carta.id == 24 or self.card_move.carta.id == 122: ## General Kenobi y Darth Maul
            self.text_scr[3].text = "COGE 2 Y JUEGA 1"
        
        elif self.card_move.carta.id == 22 or self.card_move.carta.id == 106: ## Qui-Gon o Soldado explorador
            self.text_scr[3].text = "VER MANO RIVAL"
        
        elif self.card_move.carta.tipo == 6 and not self.mano_rival_vacia:
            self.text_scr[3].text = "ROBA CARTA RIVAL"

        elif self.card_move.carta.id in [25,125] and not self.card_move.carta.en_nave: ## Mace Vindu o Kylo Ren 
            self.text_scr[3].flash = False
            hay_tropas = False
            for card in self.card_mesa:
                if self.bando != card.carta.bando and card.carta.tipo in [0,1]:
                    hay_tropas = True
                    text = "3. BONIFICACION DE ATAQUE"
                    break  
            if not hay_tropas:
                return ''

        elif self.card_move.carta.id == 121 and not self.card_move.carta.en_nave: ## GREIVOUS
            self.text_scr[3].flash = False
            hay_jedis = False
            for card in self.card_mesa:
                if self.bando != card.carta.bando and card.carta.tipo == 4:
                    hay_jedis = True
                    text = "3. BONIFICACION DE ATAQUE"
                    break  
            if not hay_jedis:
                return ''

        elif self.card_move.carta.id in [27,123] and not self.card_move.carta.en_nave: ## Obi Wan Viejo y Darth Vader
            self.text_scr[3].flash = False
            tropa_en_mesa = False
            for card in self.card_mesa:
                if self.bando == card.carta.bando and card.carta.tipo in [0,1,2]:
                    tropa_en_mesa = True
                    text = "3. SELECCIONA CARTA PARA JUGARLA"
                    self.seleccion_tropa = True
                    break
            if not tropa_en_mesa:    
                return ''

        elif self.seleccion_nave: # Se ha colocado Veers o Ackbar como tripulantes y card_move es la nave
            self.card_move.carta.nactions = 0 ## Se vuelve al mismo numero de acciones que tenia la nave antes de colocar a Ackbar o Veers
            text = "3. SELECCIONA NAVE DE ASALTO"
            self.text_scr[3].flash = False
        elif self.seleccion_vehiculo: # Se ha colocado Nute Gunray o comando Clon como tropa
            text = "3. SELECCIONA VEHICULO"
            self.text_scr[3].flash = False


        elif self.card_move.carta.id in [20,120]: ## Yoda y el emperador
            self.text_scr[3].text = "RECUPERA CARTA"

        elif self.card_move.carta.id == 31: ## R2-D2
            
            estrella_en_mesa = False
            # Ver si esta la Estrella de la muerte en la mesa
            for estrella in self.card_mesa:
                if estrella.carta.id == 154:
                    self.text_scr[3].text = "EXPONER DEATH STAR"
                    estrella_en_mesa = True
                    break
            if not estrella_en_mesa:
                self.text_scr[3].flash = False
                return ''

        elif self.card_move.carta.id == 126 and not self.card_move.carta.en_nave: ## Darth Sidious
            self.text_scr[3].text = "ATRAER ANAKIN"
            anakin_en_mesa = False
            # Ver si anakin esta en la mesa como rebelde
            for anakin in self.card_mesa:
                if anakin.carta.id == 21 and not anakin.carta.en_nave:
                    anakin_en_mesa = True
                    break
            if not anakin_en_mesa:
                self.text_scr[3].flash = False
                return ''

        elif self.card_move.carta.id in [21,124]: ## Anakin y Conde Dooku
            self.text_scr[3].text = "RETIRAR DROIDE"
            protocolo_en_mesa = False
            # Ver si hay droides de protocolo en la mesa
            for protocolo in self.card_mesa:
                if protocolo.carta.id == 30 and self.bando == 'I':
                    protocolo_en_mesa = True
                    break
                elif protocolo.carta.id == 130 and self.bando == 'R':
                    protocolo_en_mesa = True
                    break
            if not protocolo_en_mesa:
                self.text_scr[3].flash = False
                return ''

        elif self.card_move.carta.id == 66 and not self.card_move.carta.en_nave: ## Finn. Mirar si Rey esta en la mesa como tropa
            rey_en_mesa = False
            
            for rey in self.card_mesa:
                if rey.carta.id == 67 and not rey.carta.en_nave:
                    rey_en_mesa = True
                    break
            self.text_scr[3].flash = False ## Desactivamos boton de ataque adicional
            if rey_en_mesa:
                text = "3. BONIFICACION DE ATAQUE"
            else:
                # Si no esta Rey acabamos el turno. No hay ataque de bonificacion
                return ''

        elif self.card_move.carta.id == 67 and not self.card_move.carta.en_nave: ## Rey. Mirar si finn esta en la mesa como tropa
            finn_en_mesa = False
            
            for finn in self.card_mesa:
                if finn.carta.id == 66 and not finn.carta.en_nave:
                    finn_en_mesa = True
                    break
            self.text_scr[3].flash = False ## Desactivamos boton de ataque adicional
            if finn_en_mesa:
                text = "3. BONIFICACION DE ATAQUE"
            else:
                # Si no esta Finn acabamos el turno. No hay ataque de bonificacion
                return ''

        else:
            return ''

        return text

    def poder_secundario(self): 
        ## Esta funcion es llamada cuando una carta activa su poder secundario

        if self.card_move.carta.tipo == 6: ## Contrabandista
            
            if self.card_move.carta.id in [61,161] and self.card_move.carta.en_nave: # Han solo o Boba Fett en su nave
                captura = True # Se captura la carta y se lleva a su nave como botin sumando su valor.
            else:
                captura = False
            ## Robamos una carta de la mano del rival
            connection.Send({"action": "ask_carta", 
                "accion": 'ROBO_UNA',
                "captura": captura,
                "contrabandista": self.card_move.carta.id,
                "jugador": self.num, 
                "partida": self.gameid})
    
            return True

            ## Aqui veriamos que hacemos con esa carta
            # Colocarla sobre una nave como recompensa (ver si esta la nave)
                
        elif self.card_move.carta.id == 24 or self.card_move.carta.id == 122: ## General Kenobi y Darth Maul
            # Coge las 3 cartas siguientes del mazo y juega 1
            if self.ncards >= len(self.baraja):
                self.mensage_emergente('No te quedan cartas en el mazo')
                self.selecciona = False
                return True
            
            elif (len(self.baraja) - self.ncards) == 1: # Queda solo una carta
                card_next1 = self.baraja[self.ncards]
                card_next1 = Card_scr(self.screen,card_next1,(750,325))

                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                self.card_msg.append(card_next1) ## Posicion del medio

            elif (len(self.baraja) - self.ncards) > 1:  
                card_next1 = self.baraja[self.ncards]
                card_next2 = self.baraja[self.ncards+1]
                card_next1 = Card_scr(self.screen,card_next1,(610,325))
                card_next2 = Card_scr(self.screen,card_next2,(890,325))
               
                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                self.card_msg.append(card_next1) # Izquierda
                self.card_msg.append(card_next2) # Derecha

            # Cuando se elige entre las 3 siguientes en vez de entre las 2
#            elif (len(self.baraja) - self.ncards) > 2: # Quedan mas de 2 cartas en el mazo
#                card_next1 = self.baraja[self.ncards]
#                card_next2 = self.baraja[self.ncards+1]
#                card_next3 = self.baraja[self.ncards+2]
#                card_next1 = Card_scr(self.screen,card_next1,(610,325))
#                card_next2 = Card_scr(self.screen,card_next2,(750,325))
#                card_next3 = Card_scr(self.screen,card_next3,(890,325))

#                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
#                self.card_msg.append(card_next1) # Izquierda
#                self.card_msg.append(card_next2) # Centro
#                self.card_msg.append(card_next3) # Derecha

            # Variable que nos dice que estamos en momento de seleccionar entre varias
            self.selecciona = True
            self.card_mazo = True

            self.msg_scr.append(Text_scr(self.screen,"ELIGE UNA CARTA Y JUEGALA AHORA",(610,280),globals.menu_font2,False,(255,255,255)))
            return True

        elif self.card_move.carta.id == 126: # DARTH SIDIOUS, atraer Anakin
            # Elimina a Anakin de la mesa

            anakin_en_mesa = False
            for anakin in self.card_mesa:
                if anakin.carta.id == 21 and not anakin.carta.en_nave:
                    anakin_en_mesa = True
                    self.card_mesa.remove(anakin)
                    print "Anakin Skywalker eliminado y pasado al lado oscuro"
                    ## Tengo que indicar al rival que he borrado a Anakin de la mesa y que no lo ponga en la pila de eliminados
                    connection.Send({"action": "update_mesa", 
                        "idcard": 21, 
                        "jugador": self.num, 
                        "partida": self.gameid,
                        "accion": 'A'})
                    self.update_score()
                    
                    # Anadir a Anakin convertido a la mano
                    card_anakin = anakin_oscuro()
                    #self.mano.append(card_anakin)
                    self.update_mano('A',card_anakin)
                    self.reset() ## Se actualiza la mano con la nueva carta
                    self.rejuega = True
                    self.bloquea_mano_menos(card_anakin)
                    self.bloquea_hangar('Todo')

                    self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                    self.card_msg.append(Card_scr(self.screen,card_anakin,(750,325)))
                    self.msg_scr.append(Text_scr(self.screen,"ANAKIN OSCURO - JUEGALA AHORA",(620,280),globals.menu_font2,False,(255,255,255)))
                    self.btn_scr.append(Text_scr(self.screen,"OK",(782,498),globals.menu_font,True,(100,100,100)))
                    break

            if not anakin_en_mesa:
                return False
            else:
                return True

        elif self.card_move.carta.id == 31: # R2-D2 Reducir escudo estrella de la muerte
            # Ver si esta la Estrella de la muerte en la mesa
            for index in range(len(self.card_mesa)):
                if self.card_mesa[index].carta.id == 154:
                    # Sustituimos una carta por otra
                    ds_expuesta = Nave(155,'ESTRELLA DE LA MUERTE EXPUESTA.jpg',9,'I','Estrella de la muerte expuesta',0,2)
                    ds_expuesta.setup(self.card_mesa[index].carta.ata,self.card_mesa[index].carta.defensa-7,self.card_mesa[index].carta.evasion) # ataque, defensa y evasion
                    ds_expuesta.set_param_nave(5,2) # tripulacion max, max dirigentes
                    card_ds_expuesta = Card_scr(self.screen,ds_expuesta,self.card_mesa[index].pos)

                    # Guardamos la tripulacion y dirigentes que tuviera previamente
                    tripu = self.card_mesa[index].carta.tripulacion
                    dirige = self.card_mesa[index].carta.dirigentes

                    #self.tablero = modificar_tablero(self.card_mesa[index],card_ds_expuesta,self.tablero)
                    self.card_mesa[index] = card_ds_expuesta
                    self.card_mesa[index].carta.tripulacion = tripu
                    self.card_mesa[index].carta.dirigentes = dirige
                    
                    print "Estrella de la muerte expuesta"
                    # Enviar cambio al rival
                    connection.Send({"action": "update_mesa", 
                        "jugador": self.num, 
                        "partida": self.gameid,
                        "accion": 'R2'})

                    # modificar self.naves
                    for nave in self.naves:
                        for i in range(len(nave)):
                            if nave[0].carta.id == 154:
                                #nave[0] = card_ds_expuesta
                                self.naves[self.naves.index(nave)][0] = self.card_mesa[index]

                                # Al rival ya se le ha comunicado con la accion 'R2'                                
                                return False ## Fin turno

        elif self.card_move.carta.id == 22 or self.card_move.carta.id == 106: ## Qui-Gon o Soldado Explorador
            # Son capaces de ver la mano del rival
            connection.Send({"action": "ask_carta", 
                "accion": 'VER_TODAS', 
                "jugador": self.num, 
                "partida": self.gameid})
            return True
            
        # RETIRAR DROIDE DE PROTOCOLO - DOOKU - ANAKIN
        elif self.card_move.carta.id in [21,124]:
            for nave in self.naves:
                for i in range(len(nave)):
                    # Retirar droide de protocolo de nave
                    if (self.naves[self.naves.index(nave)][i].carta.id == 30 and self.card_move.carta.id == 124) or (self.naves[self.naves.index(nave)][i].carta.id == 130 and self.card_move.carta.id == 21):
                        
                        #Actualizar nave con valores de tripulacion y valor en caso de que fuera 0
                        for j in range(len(self.card_mesa)):
                            if self.naves[self.naves.index(nave)][0].carta.id == self.card_mesa[j].carta.id:
                                # Se le modifico el valor de la nave, solo estaba el droide de protocolo
                                if self.card_mesa[j].carta.valor == 0:
                                    self.card_mesa[j].carta.valor = 2
                                    self.naves[self.naves.index(nave)][0].carta.valor = 2
                                    print "Restaurado valor de nave"
                                
                                self.card_mesa[j].carta.tripulacion = i-1
                                # Enviar los cambios en la nave carta al rival 
                                connection.Send({"action": "update_mesa", 
                                    "idcard": self.naves[self.naves.index(nave)][0].carta.id, 
                                    "jugador": self.num, 
                                    "partida": self.gameid, 
                                    "tripulacion": i-1,
                                    "valor": 2,
                                    "accion": 'P'})      
                                break
                        self.card_mesa.remove(nave[i]) ## Eliminamos el droide de la mesa y de naves
                        print "Droide de protocolo eliminado"        

                        # Comunicar al rival que elimine el droide de la mesa Tripulante de nave
                        connection.Send({"action": "update_mesa", 
                            "idcard": self.naves[self.naves.index(nave)][i].carta.id, 
                            "jugador": self.num, 
                            "partida": self.gameid,
                            "accion": 'ET'})
                        self.naves[self.naves.index(nave)].remove(self.naves[self.naves.index(nave)][i])
                        self.update_score()
                        return False ## Enviamos False para finalizar turno
        
        elif self.card_move.carta.id in [115,132] and self.card_move.carta.en_nave: ## KRENNIC Y ASTROMECANICO
            # Si estamos aqui es que se cumplia la condicion de que Krennic o droide astromecanico estan en la estrella de tripulantes                           
            # Buscamos la carta en self.mesa
            for index in range(len(self.card_mesa)):
                if self.card_mesa[index].carta.id == 155:
                    ds_reparada = Nave(154,'ESTRELLA DE LA MUERTE.jpg',9,'I','Estrella de la muerte',0,2)
                    ds_reparada.setup(self.card_mesa[index].carta.ata,self.card_mesa[index].carta.defensa+7,self.card_mesa[index].carta.evasion) # ataque, defensa y evasion
                    ds_reparada.set_param_nave(5,2) # tripulacion max, max dirigentes
                    card_ds_reparada = Card_scr(self.screen,ds_reparada,self.card_mesa[index].pos)

                    # Guardamos la tripulacion que tuviera previamente
                    tripu = self.card_mesa[index].carta.tripulacion
                    dirige = self.card_mesa[index].carta.dirigentes

                    self.tablero = modificar_tablero(self.card_mesa[index],card_ds_reparada,self.tablero)
                    self.card_mesa[index] = card_ds_reparada
                    self.card_mesa[index].carta.tripulacion = tripu
                    self.card_mesa[index].carta.dirigentes = dirige

                    # Enviar cambio al rival
                    connection.Send({"action": "update_mesa", 
                        "jugador": self.num, 
                        "partida": self.gameid,
                        "accion": 'K'})

                    # modificar self.naves
                    for nave in self.naves:
                        for i in range(len(nave)):
                            if nave[0].carta.id == 155:
                                #nave[0] = card_ds_expuesta
                                self.naves[self.naves.index(nave)][0] = self.card_mesa[index]

                                # Al rival ya se le ha comunicado con la accion 'K'                                
                                return False

        elif self.card_move.carta.id == 20 or self.card_move.carta.id == 120: ## Yoda y el emperador
            # Pueden jugar una carta de los eliminados
            if len(self.card_eliminadas) == 0:
                self.mensage_emergente('No tienes ninguna carta en el mazo de eliminados')
                self.selecciona = False
                return True
                       
            elif len(self.card_eliminadas) == 1:
                card_erased1 = self.card_eliminadas[0]
                card_erased1 = Card_scr(self.screen,card_erased1,(750,325))

                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                self.card_msg.append(card_erased1) ## Posicion del medio

            elif len(self.card_eliminadas) > 1:
                card_erased1 = random.choice(self.card_eliminadas)
                card_erased2 = random.choice(self.card_eliminadas)
                while card_erased1 == card_erased2:
                    card_erased2 = random.choice(self.card_eliminadas)

                card_erased1 = Card_scr(self.screen,card_erased1,(610,325))
                card_erased2 = Card_scr(self.screen,card_erased2,(890,325))
               
                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                self.card_msg.append(card_erased1) # Izquierda
                self.card_msg.append(card_erased2) # Derecha
            
            # Variable que nos dice que estamos en momento de seleccionar entre varias
            self.selecciona = True

            self.msg_scr.append(Text_scr(self.screen,"ELIGE UNA CARTA Y JUEGALA AHORA",(620,280),globals.menu_font2,False,(255,255,255)))
            return True

        return False

#######################################
##### FUNCIONES FIN E INICIO TURNO
#######################################
    def fin_turno(self):
        self.fase += 1
        if not self.es_fin_partida():
            if self.mano == []:
                ## Si estamos aqui es que la mano del rival todavia tiene cartas
                ## Comunicar al rival que ya no tengo cartas para que actualice self.mano_rival_vacia a True    
                connection.Send({"action": "mano_vacia", "vacio": True, "jugador": self.num, "partida": self.gameid}) 
                
                #Como el rival todavia tiene cartas, finalizamos turno y le damos paso a el
                connection.Send({"action": "fin_turno", "jugador": self.num, "partida": self.gameid})
            else:
                ## Todavia sigo teniendo cartas
                if self.mano_rival_vacia:
                    ## Si el rival no tiene cartas, yo sigo jugando
                    self.juega = True
                    self.reset()
                else:
                    #Si el rival todavia tiene cartas y yo tambien finalizamos turno normal
                    self.juega = False
                    connection.Send({"action": "fin_turno", "jugador": self.num, "partida": self.gameid})
        
            # sonido de FIN DE TURNO
            if self.bando == 'R':
                if self.sonido and globals.pc_sound: 
                    globals.fin_rebels.set_volume(0.3) 
                    globals.fin_rebels.play()
            else:
                if self.sonido and globals.pc_sound: 
                    globals.fin_empire.set_volume(0.3)
                    globals.fin_empire.play()

        ## Quitamos todos los mensajes emergentes           
        self.btn_scr = []
        self.msg_scr = []
        self.card_msg = []
        self.text_scr[3].text = "ACTIVAR PODER"
        self.actualizar_mano()

    def reset(self):
        ## Resetea todas las variables
        self.card_colocada = False
        self.ignora_evasion = False
        self.ejecutor = None
        self.seleccion_tropa = False
        self.seleccion_nave = False
        self.seleccion_vehiculo = False
        self.pilotoX = False

        self.fase = 0
        self.text_action = "1. JUEGA UNA CARTA"
        self.rejuega = False
        self.card_mano = pintar_mano(self.screen,self.mano,self.juega)
        self.text_scr[1].flash = False
        self.text_scr[2].flash = False
        self.text_scr[3].flash = False

        # En el reset desbloquea la carta que haya en el hangar de mi mismo bando
        self.bloquea_hangar(self.bando if self.juega else 'Todo')

        self.upgrade_screen()
###########################################

    def mensage_emergente(self,texto):
        #tkMessageBox.showinfo("Info", texto)
        frame = pygame.transform.scale(globals.frame_img,(500,180))
        self.msg_scr.append(Frame_scr(self.screen,frame,(550,310),20,'F'))
        self.btn_scr.append(Button_scr(self.screen,globals.btn_ok0,globals.btn_ok1,(760,420)))
        self.msg_scr.append(Text_scr(self.screen,texto,(580,350),globals.normal_font,False,(255,255,255)))

    def update_score(self):
        imp = 0
        reb = 0
        ## Recorre todas las cartas de la mesa, no las del Hangar, para actualizar los marcadores
        for card_in_mesa in self.card_mesa:
            if card_in_mesa.carta.bando == 'I':
                imp += card_in_mesa.carta.valor
            elif card_in_mesa.carta.bando == 'R':   
                reb += card_in_mesa.carta.valor

        if self.bando == 'I':       
            self.score = imp
            self.score_rival = reb
        else:
            self.score = reb
            self.score_rival = imp

class Client(ConnectionListener, ScreenBoard):
    def __init__(self, host, port):
#        try:
        self.Connect((host, port))
#        except:
#            print "Error Connecting to Server"  
#            exit()

        #self.players = {}
        #print "Enter your nickname: ",
        #connection.Send({"action": "nickname", "nickname": stdin.readline().rstrip("\n")})      
        # Hay que escoger con que bando juega este jugador

        ScreenBoard.__init__(self)

        self.running=False

    def Loop(self):
        self.Pump()
        connection.Pump()
        self.Events()

    def upgrade_screen(self):
        self.pintar_screen()

        # Pinta el texto que indica la accion a realizar a continuacion
        pintar_accion_fase(self.screen,self.text_action,self.juega)
        # Se pinta un circulo verde o rojo dependiendo si es tu turno o no
        self.screen.blit(globals.greenindicator if self.juega else globals.redindicator, (150,820))

        ## Indica el numero de cartas que quedan en el mazo
        remain_cartas = len(self.baraja) - self.ncards
        rendered = globals.menu_font.render(str(remain_cartas),0,(255,255,255))
        self.screen.blit(rendered, (90,840)) 

        ## Indica los usos que quedan del HANGAR propios y del rival
        render_h = globals.menu_font.render(str(self.count_hangar),0,(255,255,255))
        render_h_rival = globals.menu_font.render(str(self.count_hangar_rival),0,(255,255,255))
        self.screen.blit(render_h, (57,315) if self.bando == 'R' else (1535,315))
        self.screen.blit(render_h_rival, (1535,315) if self.bando == 'R' else (57,315))

        ## Pintar los modificadores terrestres
        pos = (0,0,150)
        neg = (255,0,0)
        render_def = globals.menu_font.render(str(self.defensa),0,pos if self.defensa >=0 else neg)
        self.screen.blit(render_def, (33,687) if self.bando == 'R' else (1553,687))
        render_def_rival = globals.menu_font.render(str(self.defensa_rival),0,pos if self.defensa_rival >=0 else neg)
        self.screen.blit(render_def_rival, (1553,687) if self.bando == 'R' else (33,687)) 
        render_atack = globals.menu_font.render(str(self.ataque),0,pos if self.ataque >=0 else neg)
        self.screen.blit(render_atack, (110,687) if self.bando == 'R' else (1470,687) ) 
        render_atack_rival = globals.menu_font.render(str(self.ataque_rival),0,pos if self.ataque_rival >=0 else neg)
        self.screen.blit(render_atack_rival, (1470,687) if self.bando == 'R' else (110,687)) 

        # Actualizar el marcador propio y del rival
        render_score = globals.score_font.render(str(self.score),0,(255,255,255))
        self.screen.blit(render_score, (995,8) if self.bando == 'I' else (760,8)) 
#        self.screen.blit(render_score, (1060,20) if self.bando == 'I' else (770,20)) 

        render_score = globals.score_font.render(str(self.score_rival),0,(255,255,255))
        self.screen.blit(render_score, (760,8) if self.bando == 'I' else (995,8))
#        self.screen.blit(render_score, (770,20) if self.bando == 'I' else (1060,20))

    def pintar_screen(self):
        self.screen.fill((255,255,255))
        try:
            self.screen.blit(self.icon, (130,730))
            for frame in self.frame_scr:
                frame.draw()           
            for card in self.card_mano:                
                card.draw()
                # Linea que dice si la carta es jugable o no
                pygame.draw.line(self.screen,globals.RED if card.lock else globals.GREEN,(card.pos[0]+5,card.pos[1]-10),(card.pos[0]+105,card.pos[1]-10), 5)

            for card in self.card_mesa:
                card.draw()
            for card in self.card_hangar:
                card.draw_h()         
            for text in self.text_scr:
                text.draw()     
            for msg in self.msg_scr:
                msg.draw()  
            for card in self.card_msg:
                card.draw() 
            for btn in self.btn_scr:
                btn.draw()
            #if self.comienzo: # Estamos al principio cuando se nos entrega la primera mano
            #    pygame.draw.rect(self.screen,(0,0,20),(200,150,400,200))
            #    txt = globals.menu_font.render("Quieres cambiar tu mano inicial?" ,0,(255,255,255))
            #    self.screen.blit(txt, (220,180))
            #    options = [Text_scr(self.screen,"SI",(250,280),globals.menu_font,True,(255,255,255)),Text_scr(self.screen,"NO",(460,280),globals.menu_font,True,(255,255,255))]
            if self.hangar_out:
                pygame.draw.line(self.screen,globals.RED,(20,350) if self.bando == 'R' else (1500,350),(100,50) if self.bando == 'R' else (1580,50), 5)
#                elif self.bando == 'I':
#                    pygame.draw.line(self.screen,globals.RED,(1500,350),(1580,50), 5)            
            if self.hangar_out_rival:
                pygame.draw.line(self.screen,globals.RED,(20,350) if self.bando == 'I' else (1500,350),(100,50) if self.bando == 'I' else (1580,50), 5)
#                elif self.bando == 'R':
#                    pygame.draw.line(self.screen,globals.RED,(1500,350),(1580,50), 5)            
        except:
            print "Hay algun problema al pintar la pantalla"

    def set_baraja(self):
        # Esta funcion inicializa la baraja, la mano y la pinta. Se llama al principio del juego
        print "inicializa baraja y mano..."

        # Inicializamos con una Nave de asalto en el hangar de cada rival
        naveimp = Nave(140,'ESCUADRON TIE FIGHTERS.jpg',10,'I','Escuadron Tie Fighters',0,1)
        naveimp.setup(3,3,2) # ataque, defensa y evasion
        naveimp.set_param_nave(1,1) # tripulacion max, max dirigentes
        naveimp_scr = Card_scr(self.screen,naveimp,globals.pos_hangar_imp)
        naveimp_scr.lock = True ## Inicialmente  bloqueada

        navereb = Nave(40,'ESCUADRON ORO ALA-B.jpg',10,'R','Escuadron Oro: B-Wing',0,1)
        navereb.setup(3,3,2) # ataque, defensa y evasion
        navereb.set_param_nave(1,1) # tripulacion max, max dirigentes
        navereb_scr = Card_scr(self.screen,navereb,globals.pos_hangar_reb)
        navereb_scr.lock = True ## Inicialmente  bloqueada

        self.card_hangar.append(naveimp_scr)
        self.card_hangar.append(navereb_scr)

        if self.bando == 'I':
            self.baraja = barajar_imperio() ## Actualiza baraja = imperio
            self.baraja.insert(0,naveimp) # Posicion 0 nave del hangar
            self.baraja_rival = barajar_aliados()
            self.baraja_rival.insert(0,navereb) # Posicion 0 nave del hangar
            for i in range(len(self.frame_scr)):
                if self.frame_scr[i].bando == 'D':
                    self.frame_scr[i].obj = globals.empire_deck
                    break
            #self.icon = pygame.image.load(globals.images_folder+'empire_icon.jpg')
            self.icon = globals.empire_icon
        else: ## bando Rebelde
            self.baraja = barajar_aliados() ## actualiza baraja = aliados
            self.baraja.insert(0,navereb)
            self.baraja_rival = barajar_imperio()
            self.baraja_rival.insert(0,naveimp)
            for i in range(len(self.frame_scr)):
                if self.frame_scr[i].bando == 'D':
                    self.frame_scr[i].obj = globals.rebels_deck
                    break
#            self.frame_scr[0] = Frame_scr(self.screen,globals.rebels_deck,(20,730),20,'D')
            #self.icon = pygame.image.load(globals.images_folder+'rebel_icon.jpg')
            self.icon = globals.rebel_icon
        self.mano = [self.baraja[1],self.baraja[2],self.baraja[3]] # Nos saltamos la posicion 0 que es la nave que ponemos por defecto en el hangar

        ## Actualizamos la mano en el server
        for new_card in self.mano:
            connection.Send({"action": "update_mano", 
                "idcard": new_card.id,
                "accion": 'A', 
                "jugador": self.num, 
                "partida": self.gameid})

        self.card_mano = pintar_mano(self.screen,self.mano,self.juega)
        ## Inicializamos el tablero con todas sus posiciones para las cartas que se vayan colocando
        self.tablero = inicializa_posiciones_tablero()

    def es_fin_partida(self):
        if self.fin:
            ## Ya hemos llegado al fin de la partida
            return True
        if self.mano == [] and self.mano_rival_vacia:
            connection.Send({"action": "fin_partida", "fin": True, "partida": self.gameid})
            ##Reset
            self.juega = False
            self.reset()
            return True
        else:
            return False    

    ####################### 
    ### Event callbacks ###
    #######################

    def Network_mano_vacia(self,data):
        print "mano vacia del rival"
        self.mano_rival_vacia = data['vacio']

    def Network_update_score(self,data):
        self.update_score()

    def Network_update_mods(self,data):
        #Modifica parametros modificadores del terreno propios o del rival

        # accion = -2 Se ha eliminado la carta que modificaba parametros del rival
        # accion = -1 La carta jugada altera modificadores del rival
        # accion = 0 Se ha eliminado una carta que alteraba modificadores 
        # accion = 1 La carta jugada altera modificadores del jugador
        
        if data['accion'] == -1 or data['accion'] == 0: 
            self.defensa = data['def_rival']
            self.ataque = data['ata_rival']
        elif data['accion'] == -2 or data['accion'] == 1: 
            self.defensa_rival = data['defensa']
            self.ataque_rival = data['ataque']
        self.upgrade_screen()

    def Network_fin_partida(self,data):
        ## Pintar cuadro de Fin de partida y decidir quien es el ganador
        self.fin = True
        if globals.pc_sound: globals.background_sound.stop()
        if self.score > self.score_rival:
            # Has ganado
            self.mensage_emergente('   La partida se ha acabado - GANASTE')
        elif self.score == self.score_rival:
            self.mensage_emergente('   La partida se ha acabado - EMPATE')
        else:
            if self.sonido and globals.pc_sound: globals.jabba_laughting.play()
            self.mensage_emergente('   La partida se ha acabado - PERDISTE')

    def Network_accion_recibida(self,data):
        ## Se ejecutra cuando el rival nos roba una carta o nos ve la mano
        mensaje = ''
        if data['accion'] == 'ROBO_UNA':
            # A esta funcion se le llama para actualizar la mano, ya que el rival nos ha robado una carta
            for card in self.card_mano:
                if data['idcard'] == card.carta.id:
                    #self.mano.remove(card.carta)
                    self.update_mano('R',card.carta)
                    self.card_mano.remove(card)
                    break

            if self.mano == []:
                ## Comunicar al rival que ya no tengo cartas para que actualice self.mano_rival_vacia a True    
                connection.Send({"action": "mano_vacia", 
                    "vacio": True, 
                    "jugador": self.num, 
                    "partida": self.gameid})
            mensaje = "El rival ha robado la carta "+card.carta.nombre+ " de mi mano"

        elif data['accion'] == 'VER_TODAS':
            mensaje = " El rival ha visto mi mano"  

        if mensaje > 0:
            self.mensage_emergente(mensaje)     

    def Network_receive_carta(self,data):
        # A esta funcion se le llama desde el servidor para enviar una carta o toda la mano del rival y que la vea

        if data['accion'] == 'ROBO_UNA': ## Es una carta robada
            cuadro = '' # Indica el titulo que sale si robas una carta, pero no la capturas
            for card in self.baraja_rival:
                if card.id == data['idcard']:
                    capturada = Card_scr(self.screen,card,(750,325))

                    # Ver si la carta robada puede capturarse para pasarla a la nave
                    if data['captura'] and card.tipo in [1,2,3,4,5,6,8]: # Es un personaje que se puede capturar
                        # Cartas capturables en nave nodriza
                        if data['contrabandista'] == 61:
                            naveid = 47 # Han nave Halcon 47
                        elif data['contrabandista'] == 161:
                            naveid = 147 # Boba nave Esclavo I 147
                        
                        # Buscar la nave en la mesa
                        for i in range(len(self.card_mesa)):
                            if self.card_mesa[i].carta.id == naveid:
                                if self.card_mesa[i].carta.tripulacion < self.card_mesa[i].carta.tripulacion_max:
                                    capturada.carta.bando = self.bando ## Cambiamos el bando de la carta para que nos cuente
                                    capturada = coloca_carta_navev2(self.card_mesa,self.card_mesa[i],capturada)
                                    # Nota: La carta capturada no modifica parametros de nave
                                    capturada.lock = True
                                    capturada.carta.en_nave = True
                                    self.card_mesa[i].carta.tripulacion += 1

                                    # Anyadimos capturada a la mesa####
                                    self.card_mesa.append(capturada) ## Add capturada a la mesa para pintar
                                    capturada.draw() 
                                    
                                    # Actualizar self.naves con los cambios en la nave
                                    for lista in self.naves:
                                        ## El primer elemento de la lista tiene que ser la nave donde anyadimos tripulacion
                                        if self.card_mesa[i].carta.id == lista[0].carta.id:                      
                                            self.naves[self.naves.index(lista)].append(capturada)
                                            self.naves[self.naves.index(lista)][0].tripulacion = self.card_mesa[i].carta.tripulacion # Actualizamos tripulacion en self.naves
                                            break

                                    #Comunicar al rival para que actualice tripulacion de nave y valor en caso de que no tuviera tripulacion        
                                    connection.Send({"action": "update_mesa", 
                                        "idcard": capturada.carta.id, 
                                        "jugador": self.num, 
                                        "partida": self.gameid, 
                                        "pos": capturada.pos,
                                        "idnave": naveid,
                                        "accion": 'R'})
                                    self.mensage_emergente(" Has capturado en tu nave a "+card.nombre)
                                    
                                    # Como ha cambiado la mesa, actualizar el marcador
                                    self.update_score()
                                else: # No hay sitio en la nave para la carta capturada
                                    cuadro = 'NO HAY SITIO - CARTA ROBADA'
                                break
                    else: ## NO SE CUMPLEN RIQUISITO DE CAPTURA
                        cuadro = "CARTA ROBADA"
                        # Dependiendo quien capture la carta se pone en una nave u en otra
                    break

            if len(cuadro) > 0: # Mostrar cuadro de la carta que has robado de la mano del rival
                self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
                self.card_msg.append(capturada)
                self.msg_scr.append(Text_scr(self.screen,cuadro,(720,275),globals.menu_font,False,(255,255,255)))
                self.btn_scr.append(Text_scr(self.screen,"OK",(782,498),globals.menu_font,True,(100,100,100)))              

        elif data['accion'] == 'VER_TODAS': ## Solo quiere ver las cartas robadas
            self.msg_scr.append(Frame_scr(self.screen,globals.show_cards,(560,250),20,'F'))
            self.msg_scr.append(Text_scr(self.screen,"MANO DE TU RIVAL",(690,275),globals.menu_font,False,(255,255,255)))
            if len(data['cartas']) > 0:
                mano_rival = []
                space = 610
                for card in self.baraja_rival:
                    if card.id in data['cartas']:
                        mano_rival.append(card)
                        self.card_msg.append(Card_scr(self.screen,card,(space,325)))
                        pygame.display.flip()
                        space += 140
            else:
                # No hay ninguna carta en la mano del rival
                self.mensage_emergente("    El rival no tiene cartas en su mano")

            self.btn_scr.append(Text_scr(self.screen,"OK",(782,498),globals.menu_font,True,(100,100,100)))

        pygame.display.flip()               
            
    def Network_bando(self,data):
        # Esta funcion fija el bando de cada jugador

        if self.bando == '' and data['player'] == 0:
            # El jugador 0 es el que escoge el bando. Pero empieza jugando el jugador 1
            self.bando = escoge_bando(self.screen)

            self.juega = False
            if self.bando == 'I':
                connection.Send({"action": "bando", "bando_p0": self.bando, "bando_p1": 'R', "partida": self.gameid})
            else:
                connection.Send({"action": "bando", "bando_p0": self.bando, "bando_p1": 'I', "partida": self.gameid})

            # IMAGEN DE CARGANDO ya que tiene que traer todas las imagenes
            self.screen.blit(globals.background0, (0,0)) ## Pinta una imagen de fondo como background
            cargando = globals.menu_init.render("CARGANDO...", 1, (255, 255, 255))
            self.screen.blit(cargando, (700,250))
            pygame.display.update()

        else:
            # Se fija bando para el jugador 1 y empieza jugando
            self.bando = data['bando']
            self.juega = True

            # IMAGEN DE CARGANDO ya que tiene que traer todas las imagenes
            self.screen.blit(globals.background0, (0,0)) ## Pinta una imagen de fondo como background
            cargando = globals.menu_init.render("CARGANDO...", 1, (255, 255, 255))
            self.screen.blit(cargando, (700,250))
            pygame.display.update()
            
            connection.Send({"action": "check_version", "partida": self.gameid})            
            connection.Send({"action": "send_images", "partida": self.gameid})            
            connection.Send({"action": "start", "start": True, "partida": self.gameid})

############################
## UPDATE MESA ENVIADO POR EL RIVAL
############################
    def Network_update_mesa(self, data):
        # Actualiza la mesa con la carta colocada por el rival o accion realizada
        ## En la variable data['accion'] Se indica la accion que se ha llevado a cabo en la mesa o tablero
            # 'C' Colocar carta
            # 'T' Tripulante de nave
            # 'H' Colocada carta Hangar
            # 'E' Eliminar carta
            # 'ET' Eliminar tripulante de una nave
            # 'B' Bloquear nave
            # 'A' Eliminar Anakin porque se ha convertido y no poner en eliminados
            # 'N' Carta como tripulante
            # 'P' Modifica parametros de nave al eliminar un droide de protocolo
            # 'K' Reparar escudos de la estrella de la muerte
            # 'R' Captura de carta sobre nave insignia
            # 'F' Fin mazo rival, pintar lineas

        action_text = ''
        if data['accion'] == 'C':       

            if data['idcard'] == 127: # Anakin convertido no aparece en la baraja inicialmente. Anyadirlo a pelo
                card = anakin_oscuro()
                card_scr = Card_scr(self.screen,card,data['pos'])
            else:
                ## Buscamos la carta que ha colocado el rival en su baraja para pintarla
                for card in self.baraja_rival:
                    if card.id == data['idcard']:
                        card_scr = Card_scr(self.screen,card,data['pos'])
                        
                        if card.tipo in [9,10,11]: ## Si es una nave anyadir a la lista de lista de naves
                            self.naves.append([card_scr])
                        break   
            try:   
                # Actualizamos el tablero con la nueva carta colocada por el rival
                self.card_mesa.append(card_scr) ## Add la Card_scr a la mesa para pintar

                card_scr.draw() ## Carga la foto con efecto 
                action_text = "El rival ha colocado la carta: "+card.nombre

            except:
                print "ERROR: No se encuentra la carta "+str(data['idcard'])

        elif data['accion'] == 'T':       

            if data['idcard'] == 127: # Anakin convertido no aparece en la baraja inicialmente
                card_anakin = anakin_oscuro()
                card_scr = Card_scr(self.screen,card_anakin,data['pos'])
                # Actualizar la lista de naves
                for nave in self.naves:
                    if data['idnave'] == nave[0].carta.id:
                        self.naves[self.naves.index(nave)].append(card_scr)
                        break
            else:
                ## Buscamos la carta que ha colocado el rival en su baraja para pintarla
                for card in self.baraja_rival:
                    if card.id == data['idcard']:
                        card_scr = Card_scr(self.screen,card,data['pos'])
                        
                        # Actualizar la lista de naves
                        for nave in self.naves:
                            if data['idnave'] == nave[0].carta.id:
                                self.naves[self.naves.index(nave)].append(card_scr)
                                break
                        break
            try:# Actualizamos el tablero con la nueva carta colocada por el rival
                card_scr.carta.en_nave = True
                self.card_mesa.append(card_scr) ## Add la Card_scr a la mesa para pintar
                card_scr.draw() ## Carga la foto con efecto 
                action_text = "El rival ha colocado la carta "+card_scr.carta.nombre+' como tripulante'
            except:
                print "ERROR: No se encuentra la carta "+str(data['idcard'])

        elif data['accion'] == 'R': ## CAPTURA DE CARTA POR CONTRABANDISTA

            ## Buscamos la carta que ha capturado el rival en mi baraja para pintarla
            for card in self.baraja:
                if card.id == data['idcard']:
                    card_scr = Card_scr(self.screen,card,data['pos'])
                    # Cambiamos el bando de la carta para que le cuente al rival
                    if self.bando == 'R':
                        card_scr.carta.bando = 'I'
                    elif self.bando == 'I':
                        card_scr.carta.bando = 'R'    
                    # Actualizar la lista de naves
                    for nave in self.naves:
                        if data['idnave'] == nave[0].carta.id:
                            self.naves[self.naves.index(nave)].append(card_scr)
                            break
                    # Actualizamos el tablero con la nueva carta colocada por el rival
                    card_scr.carta.en_nave = True
                    self.card_mesa.append(card_scr) ## Add la Card_scr a la mesa para pintar
                    card_scr.draw() ## Carga la foto con efecto 
                    action_text = "El rival ha capturado la carta "+card_scr.carta.nombre+' como rehen en nave'
                    break

        elif data['accion'] == 'H':       
            ## El rival ha colocado una carta en el hangar
            for card in self.baraja_rival:
                if card.id == data['idcard']:
                    card_scr = Card_scr(self.screen,card,data['pos'])
                    break
            try:   
                # Actualizamos el tablero con la nueva carta colocada por el rival
                self.card_hangar.append(card_scr) ## Add la Card_scr al hangar para pintar
                card_scr.draw() ## Carga la foto con efecto 
                action_text = "El rival ha colocado la nave "+card.nombre+' en el Hangar'
                self.count_hangar_rival -=1

            except:
                print "ERROR: No se encuentra la carta "+str(data['idcard'])

        elif data['accion'] == 'A': # ELIMINAR ANAKIN PERO NO PONER EN ELIMINADOS
            for i in range(len(self.card_mesa)):
                if self.card_mesa[i].carta.id == data['idcard']:
                    action_text = "El rival ha eliminado la carta: "+self.card_mesa[i].carta.nombre

                    self.tablero = liberar_posicion(self.card_mesa[i],self.tablero)
                    self.card_mesa.remove(self.card_mesa[i])

                    break
        elif data['accion'] == 'E':
            for i in range(len(self.card_mesa)):
                #print self.card_mesa[i].carta.nombre+'\t'+'ID '+str(self.card_mesa[i].carta.id)
                
                if self.card_mesa[i].carta.id == data['idcard']:
                    action_text = "El rival ha eliminado la carta: "+self.card_mesa[i].carta.nombre

                    if self.card_mesa[i].carta.bando == self.bando:
                        if (self.bando == 'R' and self.card_mesa[i].carta.id < 100) or (self.bando == 'I' and self.card_mesa[i].carta.id > 100): 
                            #Las cartas que esten en tu mesa pero son del bando rival no pasan a eliminados
                            #id Rebeldes < 100
                            #id Imperio > 100
                            self.card_eliminadas.append(self.card_mesa[i].carta) ## La guardamos en eliminadas propias

                    # Si la carta a eliminar es una nave, eliminamos la nave y toda su tripulacion de naves
                    for nave in self.naves:
                        if nave[0].carta.id == data['idcard']:
                            # Borramos la nave y todos sus tripulantes de self.naves
                            self.naves.remove(nave)

                    self.tablero = liberar_posicion(self.card_mesa[i],self.tablero)
                    self.card_mesa.remove(self.card_mesa[i])
                    break

        elif data['accion'] == 'ET':
            for i in range(len(self.card_mesa)):
                if self.card_mesa[i].carta.id == data['idcard']:
                    action_text = "El rival ha eliminado el tripulante: "+self.card_mesa[i].carta.nombre

                    self.card_eliminadas.append(self.card_mesa[i].carta) ## La guardamos en eliminadas propias

                    for nave in self.naves:
                        for tripulante in range(len(nave)):
                            if data['idcard'] == self.naves[self.naves.index(nave)][tripulante].carta.id:
                                self.naves[self.naves.index(nave)].remove(self.naves[self.naves.index(nave)][tripulante])
                                self.card_mesa.remove(self.card_mesa[i])
                                break
                    break

        elif data['accion'] == 'M': # La carta se ha movido del hangar a un frame
            for i in range(len(self.card_hangar)):
                if self.card_hangar[i].carta.id == data['idcard']:
                    action_text = "El rival ha sacado la nave: "+self.card_hangar[i].carta.nombre+" del hangar"

                    self.card_hangar.remove(self.card_hangar[i])
                    break

        elif data['accion'] == 'B': # Impedir que entre nadie en la nave de combate. 
            # DROIDE DE PROTOCOLO anyadido
            # Actualizar tripulacion de la nave al maximo
            print "Bloquean mi nave: "+str(data['idnave'])

            for i in range(len(self.card_mesa)):
                if self.card_mesa[i].carta.id == data['idnave']:
                    if self.card_mesa[i].carta.tripulacion == 0:
                        ## En caso de que no hubiera nadie, eliminar valor de nave
                        #Solo tiene al droide, luego actualizar marcador y el bando del droide
                        self.card_mesa[i].carta.valor = 0
                        
                    self.card_mesa[i].carta.tripulacion = self.card_mesa[i].carta.tripulacion_max                   
                    action_text = "El rival ha bloqueado mi nave "+self.card_mesa[i].carta.nombre
                    break

            for card in self.baraja_rival:
                if card.id == data['idcard']:
                    card_scr = Card_scr(self.screen,card,data['pos'])
                        
                    # Actualizar la lista de naves
                    for nave in self.naves:
                        if data['idnave'] == nave[0].carta.id:
                            if nave[0].carta.tripulacion == 0:
                                self.naves[self.naves.index(nave)][0].valor = 0    
                            self.naves[self.naves.index(nave)].append(card_scr)
                            break
                    break
            try:   
                # Actualizamos el tablero con la nueva carta colocada por el rival
                self.card_mesa.append(card_scr) ## Add la Card_scr a la mesa para pintar

                card_scr.draw() ## Carga la foto con efecto 
                
            except:
                print "ERROR: No se encuentra la carta "+str(data['idcard'])

        elif data['accion'] == 'N':
            # Actualiza una nave en la mesa. Se ha colocado un tripulante o se modifican sus parametros
            for i in range(len(self.card_mesa)):
                if self.card_mesa[i].carta.id == data['idcard']:
                    self.card_mesa[i].carta.tripulacion = data['tripulacion']
                    self.card_mesa[i].carta.dirigentes = data['dirigentes']
                    self.card_mesa[i].carta.defensa = data['defensa']
                    self.card_mesa[i].carta.ata = data['ataque']
                    self.card_mesa[i].carta.evasion = data['evasion']

                    break
            action_text = "El rival ha colocado un tripulante en "+self.card_mesa[i].carta.nombre

        elif data['accion'] == 'P':
            # Actualiza una nave en la mesa. Se ha eliminado un droide de protocolo en una nave y se modifican sus parametros
            for i in range(len(self.card_mesa)):
                if self.card_mesa[i].carta.id == data['idcard']:
                    self.card_mesa[i].carta.tripulacion = data['tripulacion']
                    self.card_mesa[i].carta.valor = data['valor']
                    break
            action_text = "Se ha eliminado un droide de protocolo de la nave "+self.card_mesa[i].carta.nombre

        elif data['accion'] == 'R2': # R2-D2 reduce escudos de la Estrella de la muerte, cambia de carta

            for index in range(len(self.card_mesa)):
                if self.card_mesa[index].carta.id == 154:
                    # Sustituimos una carta por otra
                    ds_expuesta = Nave(155,'ESTRELLA DE LA MUERTE EXPUESTA.jpg',9,'I','Estrella de la muerte expuesta',0,2)
                    ds_expuesta.setup(self.card_mesa[index].carta.ata,self.card_mesa[index].carta.defensa-7,self.card_mesa[index].carta.evasion) # ataque, defensa y evasion
                    ds_expuesta.set_param_nave(5,2) # tripulacion max, max dirigentes

                    # Mantenemos la tripulacion que tenia la estrella la muerte antes de convertirse
                    tripu = self.card_mesa[index].carta.tripulacion
                    dirige = self.card_mesa[index].carta.dirigentes

                    card_ds_expuesta = Card_scr(self.screen,ds_expuesta,self.card_mesa[index].pos)
                    self.tablero = modificar_tablero(self.card_mesa[index],card_ds_expuesta,self.tablero)

                    self.card_mesa[index] = card_ds_expuesta
                    self.card_mesa[index].carta.tripulacion = tripu
                    self.card_mesa[index].carta.dirigentes = dirige

                    for nave in self.naves:
                        for i in range(len(nave)):
                            if nave[0].carta.id == 154:
                                self.naves[self.naves.index(nave)][0] = self.card_mesa[index]
                            break
                    break
            action_text = "El rival ha reducido los escudos de la Estrella de la muerte"

        elif data['accion'] == 'K': # Krennic o droide astromecanico reparan escudos de la Estrella de la muerte

            for index in range(len(self.card_mesa)):
                if self.card_mesa[index].carta.id == 155:
                    # Sustituimos una carta por otra
                    ds_reparada = Nave(154,'ESTRELLA DE LA MUERTE.jpg',9,'I','Estrella de la muerte',0,2)
                    ds_reparada.setup(self.card_mesa[index].carta.ata,self.card_mesa[index].carta.defensa+7,self.card_mesa[index].carta.evasion) # ataque, defensa y evasion
                    ds_reparada.set_param_nave(5,2) # tripulacion max, max dirigentes
                    card_ds_reparada = Card_scr(self.screen,ds_reparada,self.card_mesa[index].pos)

                    # Mantenemos la tripulacion y defensa que tenia la estrella la muerte antes de convertirse
                    tripu = self.card_mesa[index].carta.tripulacion
                    dirige = self.card_mesa[index].carta.dirigentes

                    #self.tablero = modificar_tablero(self.card_mesa[index],card_ds_reparada,self.tablero)
                    self.card_mesa[index] = card_ds_reparada
                    self.card_mesa[index].carta.tripulacion = tripu
                    self.card_mesa[index].carta.dirigentes = dirige

                    for nave in self.naves:
                        for i in range(len(nave)):
                            if nave[0].carta.id == 155:
                                self.naves[self.naves.index(nave)][0] = self.card_mesa[index]
                            break
                    break
        
        elif data['accion'] == 'F': # Fin mazo rival
            self.count_hangar_rival = 0
            self.hangar_out_rival = True
            action_text = "El rival ya no tiene cartas en el mazo"

        elif data['accion'] == 'HD': # Hangar destruido por el rival y las naves que hubiera dentro
            self.count_hangar = 0
            self.hangar_out = True
            for card in self.card_hangar:
                if card.carta.bando == self.bando:
                    action_text = "El rival ha destruido el hangar y la nave "+card.carta.nombre
                    self.card_hangar.remove(card)
                    break
            if action_text == '':
                action_text = "El rival ha destruido e inutilizado el hangar"

        print action_text
        self.mensage_emergente(action_text)

        # Como ha cambiado la mesa, actualizar el marcador
        self.update_score()
        
        ## Actualiza el tablero
        self.upgrade_screen()
        
        pygame.display.update()

    def Network_initgame(self, data):
        self.running=True
        self.num=data["player"] ## Indica el identificador del jugador dentro del juego
        self.gameid=data["gameid"] ## Indica el identificador del juego

        connection.Send({"action": "set_alias", 
            "alias": globals.USER,
            "jugador": self.num, 
            "partida": self.gameid,})
     
        self.screen.blit(globals.background0,(0,0))
        txt = globals.menu_init.render("Rival encontrado. Esperando a establecer partida...", 1, (255, 255, 255))
        #encuentro = globals.menu_init.render(user+" VS "+self.rival, 1, (255, 255, 255))
        self.screen.blit(txt, (20,50)) 
        #self.screen.blit(encuentro, (50,90)) 
        pygame.display.update()

    def Network_check_version(self, data):
        if globals.VERSION != data['version']:
            print "cliente y servidor tienen distintas versiones... desconectar"
            pygame.quit()
            exit()

    def Network_images_set(self, data):
        # Recibe imagenes del servidor para pintarlas en el tablero
        while len(data['image']) != data['long']:
            print 'lleva'+str(len(data['image']))
            print 'source'+str(data['long'])

        image = pygame.image.frombuffer(data['image'],data['size'],"RGBA")

        if data['tipo'] == 'S': # Shield
            self.frame_scr.append(Frame_scr(self.screen,image,(1540,680),20,'S'))
            self.frame_scr.append(Frame_scr(self.screen,image,(20,680),20,'S'))
        elif data['tipo'] == 'A': # Logo Attack
            self.frame_scr.append(Frame_scr(self.screen,image,(65,683),20,'A'))
            self.frame_scr.append(Frame_scr(self.screen,image,(1495,683),20,'A'))
        elif data['tipo'] == 'R': #Redindicator
            globals.redindicator = image
        elif data['tipo'] == 'G': #Greenindicator
            globals.greenindicator = image
        elif data['tipo'] == 'DR': # Deck rebel
            globals.rebels_deck = image
        elif data['tipo'] == 'DR0': # Deck rebel 0
            globals.rebels_deck0 = image
        elif data['tipo'] == 'DI': # Deck imperio
            globals.empire_deck = image
        elif data['tipo'] == 'DI0': # Deck imperio 0
            globals.empire_deck0 = image

        elif data['tipo'] == 'SCR': # Score Rebel
            self.frame_scr.append(Frame_scr(self.screen,image,(570,5),20,'SC'))
        elif data['tipo'] == 'SCI': # Score Empire
            self.frame_scr.append(Frame_scr(self.screen,image,(805,5),20,'SC'))
        elif data['tipo'] == 'ON': # Sound_on
            globals.sound_on = image
        elif data['tipo'] == 'OFF': # Sound_off
            globals.sound_off = image
        elif data['tipo'] == 'E': # Erase card
            self.frame_scr.append(Frame_scr(self.screen,image,(1100,730),20,'E'))
        elif data['tipo'] == 'RI': # Rebel icon
            globals.rebel_icon = image
        elif data['tipo'] == 'EI': # Empire icon
            globals.empire_icon = image

    def Network_start(self, data):
        ## Inicio de cada jugador pendiente de pulsar click
        self.start = data['start']
        print "User: "+globals.USER
        print "Rival: "+data['rival']
        self.rival = data['rival']

        click_para_continuar(self.screen,self.bando)

        self.frame_scr.append(Frame_scr(self.screen,globals.rebels_deck,(20,730),20,'D'))
        #self.frame_scr.append(Frame_scr(self.screen,globals.image_erasecard,(1100,730),20,'E'))
        
        #self.frame_scr.append(Frame_scr(self.screen,globals.image_playcard,(1150,730),20,'P'))
       
        #Modificadores de Escudos y ataque terrestre
        #self.frame_scr.append(Frame_scr(self.screen,globals.shield,(20,680),20,'S'))
        #self.frame_scr.append(Frame_scr(self.screen,globals.shield,(1540,680),20,'S'))

        self.frame_scr.append(Frame_scr(self.screen,globals.hangar_rebel,(10,40),2,'R'))
        self.frame_scr.append(Frame_scr(self.screen,globals.s_rebel,(115,40),1,'R'))
        self.frame_scr.append(Frame_scr(self.screen,globals.s_empire,(805,40),1,'I'))
        self.frame_scr.append(Frame_scr(self.screen,globals.hangar_empire,(1490,40),2,'I'))
        
        self.frame_scr.append(Frame_scr(self.screen,globals.t_rebel,(10,360),0,'R'))
        self.frame_scr.append(Frame_scr(self.screen,globals.t_empire,(805,360),0,'I'))

        # Sound ON al principio
        self.frame_scr.append(Frame_scr(self.screen,globals.sound_on,(1565,10),10,'X'))

#        for i in range(len(self.frame_scr)):
#            print self.frame_scr[i].bando

        self.text_scr.append(Text_scr(self.screen,"SALIR",(1490,10),globals.menu_font,True,(100,100,100)))
        self.text_scr.append(Text_scr(self.screen,"FINALIZAR TURNO",(1270,750),globals.menu_font,False,(100,100,100)))    
        self.text_scr.append(Text_scr(self.screen,"SALTAR ACCION",(1270,780),globals.menu_font,False,(100,100,100)))
        self.text_scr.append(Text_scr(self.screen,"ACTIVAR PODER",(1270,810),globals.menu_font,False,(100,100,100)))

        # Marcador de cada jugador en tipo imagen
#        self.frame_scr.append(Frame_scr(self.screen,globals.score_rebels,(570,5),20,'S'))
#        self.frame_scr.append(Frame_scr(self.screen,globals.score_empire,(805,5),20,'S'))

        #self.text_scr.append(Text_scr(self.screen,"PUNTOS ALIADOS",(560,10),globals.menu_font,False,(0,0,0)))
        #self.text_scr.append(Text_scr(self.screen,"PUNTOS IMPERIO",(810,10),globals.menu_font,False,(0,0,0)))

        #### Debug. descomentar en caso de querer hacer debug     
        #self.text_scr.append(Text_scr(self.screen,"DEBUG",(1100,10),globals.menu_font,False,(0,0,0)))

        # ALias & version
        self.text_scr.append(Text_scr(self.screen,globals.USER,(225,755),globals.menu_font,False,(0,0,0))) 
        self.text_scr.append(Text_scr(self.screen,globals.VERSION,(1520,870),globals.normal_font,False,(0,0,0)))
        
        # Accion
        self.text_scr.append(Text_scr(self.screen,"ACCION: ",(15,10),globals.menu_font,False,(0,0,0)))
        
        ### Sonido Background
        if globals.pc_sound:
            globals.background_sound.set_volume(0.05)
            globals.background_sound.play(-1)
        
        # Indicamos la accion inicial para el que juega
        if self.juega:
            self.text_action = "1. JUEGA UNA CARTA"

        ## Se actualiza la baraja y la mano. Se pinta
        self.set_baraja()
        self.upgrade_screen()
        pygame.display.update()

    ###############################
    ### Network event callbacks ###
    ###############################


    def Network_turno(self, data):
        # Esta funcion se ejecuta al inicio de CAMBIAR EL TURNO de cada jugador
        self.juega = data['juega']
        self.reset()
        
    def Network_players(self, data):
        # Cuando se conecta o desconecta un usuario
        #print "*** players: " + ", ".join([p for p in data['players']])
        self.rival = data['players']
        #print data

    def Network_connected(self, data):
        print "You are now connected to the server"
    
    def Network_error(self, data):
        print 'error:', data['error'][1]
        connection.Close()

    def Network_finish(self, data):
        print 'El usuario rival se ha desconectado'
        if globals.pc_sound: globals.background_sound.stop()
        self.screen.fill((255, 255, 255))
        self.screen.blit(globals.user_disconnect, (600,250))
        pygame.display.flip()
        pygame.time.delay(3000)
        exit()
        #connection.Close()
    
    def Network_disconnected(self, data):
        print 'Server disconnected'
        if globals.pc_sound: globals.background_sound.stop()
        self.screen.fill((255, 255, 255))
        #txt = globals.menu_init.render("Servidor desconectado...", 1, (0, 0, 0))
        self.screen.blit(globals.server_disconnect, (600,250))
        #self.screen.blit(txt, (20,50))  
        pygame.display.flip()
        pygame.time.delay(3000)

        exit()

class Client_intro(Frame):
    # Esta clase abre la ventana para poder meter los valores tipo GUI
    def __init__(self, master=None):
        self.root = Tk()
        self.root.title('CARD GAME')
        self.root.resizable(False,False) # Horizontal y vertical
        self.root.geometry("207x490")
        Frame.__init__(self, master)

        self.root.iconbitmap(globals.images_folder+ICON) # Icono de la intro
        #self.root.protocol("WM_DELETE_WINDOW", self.salir())
        photo = PhotoImage(file=globals.images_folder+INTRO_PHOTO)
        w = Label(self.root, image=photo)
        w.photo = photo
        w.grid(row=0, column=0,columnspan=3, sticky=W+E+N+S, padx=5, pady=5)

        self.lablhost = Label(text="Server").grid(row=1, column=0, padx=5, sticky=W)
        self.lablport = Label(text="Port").grid(row=2, column=0, padx=5, sticky=W)
        self.labluser = Label(text="User").grid(row=3, column=0, padx=5, sticky=W)

        # Colocar los text box
        self.host = Entry() ## entry Host
        self.host.grid(row=1, padx=5, column=1,columnspan=2)
        self.port = Entry() ## entry Port
        self.port.grid(row=2, padx=5, column=1,columnspan=2)
        self.user = Entry() ## entry User
        self.user.grid(row=3, padx=5, column=1,columnspan=2)


        # Colocar los botones
        self.okbutton = Button(self.root, text="OK", command=self.on_button)
        self.okbutton.grid(row=4, column=0, columnspan=2, padx=15, sticky="nsew")
        self.exitbutton = Button(self.root, text="Salir", command=self.salir)
        self.exitbutton.grid(row=4, column=2, padx=15,sticky="nsew")

        self.hostvar = StringVar()
        self.portvar = IntVar()
        self.uservar = StringVar()
        # Valores por defecto
        self.hostvar.set("localhost")
        self.portvar.set(7000)
        self.uservar.set("Anonymous")
        
        # Poner los valores por defecto
        self.host["textvariable"] = self.hostvar
        self.user["textvariable"] = self.uservar
        self.port["textvariable"] = self.portvar
        
    def on_button(self):
        if len(self.uservar.get()) > 15:
            tkMessageBox.showwarning("Warning","The user is limit to 15 characters")
            return
        try:
            globals.HOST = self.hostvar.get()
            if not isUp(globals.HOST):
                tkMessageBox.showerror("Error","No se alcanza el Host: "+globals.HOST)
                #print "No se alcanza el Host: "+host
            else:
                globals.PORT = self.portvar.get()
                globals.USER = self.uservar.get()
                #print "Server: "+self.hostvar.get()+': '+str(self.portvar.get())+' & User: '+self.uservar.get()
                self.root.destroy()        
        except:
            ## Mensaje de error en la entrada de parametros
            tkMessageBox.showwarning("Warning","Usage host:port. Ej: localhost:31425")
            #print "Usage host:port. Ej: localhost:31425"
    def salir(self):
        exit()

# COMIENZO DEL CLIENTE
# Ventana de entrada
input_values = Client_intro()

input_values.mainloop()
# Se lanza el cliente contra el server 
global jugador
print "Server: "+globals.HOST+': '+str(globals.PORT)+' & User: '+globals.USER

jugador = Client(globals.HOST, int(globals.PORT))
while 1:
    jugador.Loop()
    sleep(0.01)


#if len(sys.argv) != 2:
#    print "Usage:", sys.argv[0], "host:port"
#    print "e.g.", sys.argv[0], "localhost:31425"
#else:
#    host, port = sys.argv[1].split(":")
#    global jugador
#    jugador = Client(host, int(port))
#    while 1:
#        jugador.Loop()
#        sleep(0.01)




