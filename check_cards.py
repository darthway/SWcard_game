#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calcular_def(card,card_mesa,def_rival):
    # Esta funcion me calcula la defensa de la carta atacada (card)
    # card_mesa: Son todas las cartas de la mesa
    # Ademas indica si hay un senuelo en la mesa colocado

    senuelos = [32,132]
    senuelo = False
    comandos = [1,2,8] ## Comandos rebeldes
    def_com = 0
    soldados = [101,102,108] ## Soldados imperiales
    def_soldados = 0
    ewoks = [3,4]
    def_ewoks = 0
    droides_imp = [103,104] ## Droides de combate del imperio
    pot_droides = [113,153] ## Potenciadores de droides en defensa
    def_droides = 0
    clones = [7]
    pot_clones = [11,12,20] ## Vehiculos clon & YODA
    def_clones = 0
    oficiales_imp = [115,116,117,118] # Oficiales y líderes imperiales
    pot_oficiales = [105] ## Soldados oscuros como potenciador de defensa a oficiales
    def_oficiales = 0

    # Chequear las cartas de la mesa terrestres para activar potenciadores de defensa y ver si hay un senuelo
    for cartas in card_mesa:
        if not cartas.carta.tipo in [7,9,10,11] and not cartas.carta.en_nave:
            if cartas.carta.id in senuelos and cartas.carta.bando == card.carta.bando: ## Hay un senuelo terrestre en la mesa, aplicar escudo al resto de tropas
                senuelo = True
                break
            elif cartas.carta.id != card.carta.id: # No contar como potenciador la carta que estamos comparando
                if cartas.carta.id in comandos:
                    def_com += 1
                elif cartas.carta.id in soldados:
                    def_soldados += 1
                elif cartas.carta.id in ewoks:
                    def_ewoks += 1
                elif cartas.carta.id in droides_imp:
                    def_droides += 1
                elif cartas.carta.id in pot_oficiales:
                    def_oficiales += 1
                elif cartas.carta.id in pot_clones: # Yoda 
                    def_clones += 2    
        elif cartas.carta.id in pot_droides and cartas.carta.tipo in [7,9,10,11]: # Potenciador droides no tropa
            def_droides += 1
        elif cartas.carta.id in pot_clones and cartas.carta.tipo in [7,9,10,11]: # Potenciador clones no tropa
            def_clones += 1

    #Chequear la defensa de la carta terrestre, ver si tiene potenciadores por otras cartas
    if not card.carta.tipo in [7,9,10,11] and not card.carta.en_nave:
        # DEFENSA TROPAS TERRESTRES
        card_defensa = card.carta.defensa + def_rival ## Defensa de la carta que se intenta atacar
        if card.carta.id in comandos:
            card_defensa = card_defensa + def_com 
        elif card.carta.id in soldados:
            card_defensa = card_defensa + def_soldados ## Defensa de la carta que se intenta atacar
        elif card.carta.id in droides_imp:
            card_defensa = card_defensa + def_droides 
        elif card.carta.id in ewoks:
            card_defensa = card_defensa + def_ewoks
        elif card.carta.id in clones:
            card_defensa = card_defensa + def_clones 
        elif card.carta.id in oficiales_imp:
            card_defensa = card_defensa + def_oficiales 
    
    elif card.carta.tipo == 7: ## Aplicar a vehiculos la defensa terrestre
        card_defensa = card.carta.defensa + def_rival ## Defensa de la carta que se intenta atacar
    
    else: ## Naves no aplica potenciadores de defensa terrestre
        card_defensa = card.carta.defensa

    return senuelo, card_defensa

def check_action1_card(card,card_move,card_mesa,ataque,def_rival):
    # SE EJECUTA EN FASE 1
    # Funcion que chequea que una carta puede aplicar poder principal sobre otra
    # card: Es la carta que esta en el tablero con la que se chequea la accion si es posible
    # card_move: Es la carta que realiza la accion
    # ataque: indica el modificador local de ataque
    # def_rival: indica el modificador de defensa rival
    
    action_text = '' ## indica la accion a llevar a cabo en texto
    
    if card.carta.bando == card_move.carta.bando:
        # No puede aplicarse sobre cartas del mismo bando
        return False, action_text 
    
    # Vemos si esta el senuelo y calculamos la defensa de la carta terrestre atacada 
    senuelo, card_defensa = calcular_def(card,card_mesa,def_rival)       
    
    senuelos = [32,132] # BB-8 y Droide funcional imperial

    ## CHEQUEAR SENUELO TERRESTRE
    if not card_move.carta.tipo in [9,10,11]: # A las naves no les afecta el senuelo
        if senuelo and card.carta.id in senuelos and (card.carta.defensa + def_rival) <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
            action_text = 'Eliminar senuelo '+ card.carta.nombre
            return True, action_text
        elif senuelo: # Esta el senuelo y no se cumple ninguna condicion principal
            return False, action_text

    card_ataque = card_move.carta.ata + ataque ## ataque de la carta que ataca
            
    # Ataque de Tropas, Tropa especial, especiales, oficiales, lideres, contrabandistas y vehiculos VS Tropa terrestre
    if card_move.carta.tipo in [0,1,2,3,5,6,8] and not card_move.carta.en_nave: 
        # Aplicar variables de entorno a la carta para ver si puede atacar a la carta destino
        # Chequear que cartas hay en la mesa para aplicar potenciadores de ATAQUE a la carta
        # ATAQUE

        for apoyo in card_mesa:
            if not apoyo.carta.tipo in [7,9,10,11] and not apoyo.carta.en_nave:
                # EWOKS Y DROIDES de combate, se apoyan entre ellos
                if (apoyo.carta.id == 4 and card_move.carta.id == 3) or (apoyo.carta.id == 104 and card_move.carta.id == 103):
                    card_ataque += 2
                elif (apoyo.carta.id == 3 and card_move.carta.id == 4) or (apoyo.carta.id == 103 and card_move.carta.id == 104):
                    card_ataque += 2
                # SOLDADOS IMPERIALES Y REBELDES
                elif (apoyo.carta.id in [101,108] and card_move.carta.id == 102) or (apoyo.carta.id in [1,8] and card_move.carta.id == 2):
                    card_ataque += 1
                elif (apoyo.carta.id in [102,108] and card_move.carta.id == 101) or (apoyo.carta.id in [2,8] and card_move.carta.id == 1):
                    card_ataque += 1
                elif (apoyo.carta.id in [101,102] and card_move.carta.id == 108) or (apoyo.carta.id in [1,2] and card_move.carta.id == 8):
                    card_ataque += 1
                elif (apoyo.carta.id in [8,109] and card_move.carta.tipo == 7): # Potenciadores de ataque a vehiculos
                    card_ataque += 1

        print "Ataque: "+ card_move.carta.nombre + str(card_ataque)
        print "Defensa: "+ card.carta.nombre + str(card_defensa)

        rivales = [0,1,2,3,4,5,6,8] # Puede atacar a cualquier rival terrestre, quito vehiculos porque no tiene atributo en nave
        if (card.carta.tipo in rivales) and card_defensa <= card_ataque and not card.carta.en_nave:
                action_text = 'Eliminar '+ card.carta.nombre
                return True, action_text
        elif (card.carta.tipo == 7): # Vehiculos
            if card_move.carta.id in [8,109]: # El escuadron infernal y comando de elite tienen un potenciador de ataque a vehiculos
                card_ataque += 1
            if card_defensa <= card_ataque:
                action_text = 'Derribar '+ card.carta.nombre
                return True, action_text

    # Jedis contra tropas terrestres
    elif card_move.carta.tipo == 4 and not card_move.carta.en_nave: #Jedi/Sith como tropa

        print "Ataque: "+ card_move.carta.nombre + str(card_ataque)
        print "Defensa: "+ card.carta.nombre + str(card_defensa)

        rivales = [4,8] ## Jedi/sith, Vehiculos y Droides escudo
        if (card.carta.tipo == 7) and card_defensa <= card_ataque:
            action_text = 'Inutilizar '+ card.carta.nombre
            return True, action_text

        if (card.carta.tipo in rivales) and card_defensa <= card_ataque and not card.carta.en_nave:
            action_text = 'Derrotar a '+ card.carta.nombre
            return True, action_text

    # Vehiculos
    elif card_move.carta.tipo == 7:

        print "Ataque: "+ card_move.carta.nombre + str(card_ataque)
        print "Defensa: "+ card.carta.nombre + str(card_defensa)

        rivales = [0,1,2,3,4,5,6,8] # Posibles rivales terrestres a los que atacar
        if card.carta.tipo == 7 and card_defensa <= card_ataque:
            action_text = 'Derribar '+ card.carta.nombre
            return True, action_text

        elif (card.carta.tipo in rivales) and card_defensa <= card_ataque and not card.carta.en_nave:
            action_text = 'Aniquilar '+ card.carta.nombre
            return True, action_text

    # Droides
    elif card_move.carta.tipo == 8:
        # El DROIDE DE INTERROGATORIO puede eliminar cualquier carta terrestre salvo un Jedi o Vehiculo
        if card_move.carta.id == 131 and not card.carta.tipo in [4,7,9,10,11] and not card.carta.en_nave:
            action_text = 'Interroga y elimina '+ card.carta.nombre
            return True, action_text
        
        ## Ataque de DROIDE cuando se coloca como tropa
#        elif card_move.carta.id in [31,32] and not card_move.carta.en_nave and (card.carta.tipo in [0,1,2,3,4,5,6,8]) and card_defensa <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
#            action_text = 'Eliminar '+ card.carta.nombre
#            return True, action_text

        # Los Vehiculos no tienen atributo en_nave poner como condicion aparte
#        elif card_move.carta.id in [31,32] and card.carta.tipo ==7 and card_defensa <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
#            action_text = 'Eliminar '+ card.carta.nombre
#            return True, action_text            
        else:
            return False, action_text

    elif card_move.carta.tipo == 9: # Nave de combate

        print "Ataque: "+ card_move.carta.nombre + str(card_move.carta.ata)
        print "Defensa: "+ card.carta.nombre + str(card.carta.defensa)

        rivales_aereos = [9,10,11]
            
        # La Estrella de la muerte solo puede atacar a Naves de combate
        if card_move.carta.id in [154,155] and card.carta.tipo == 9 and card.carta.defensa <= card_move.carta.ata:
            action_text = 'Pulverizar '+ card.carta.nombre+' con su tripulacion'
            return True, action_text

        # Resto de naves de combate pueden atacar a cualquier nave de asalto o de combate
        elif not card_move.carta.id in [154,155] and (card.carta.tipo in rivales_aereos) and card.carta.defensa <= card_move.carta.ata:
            action_text = 'Derribar '+ card.carta.nombre+' con su tripulacion'
            return True, action_text

    elif card_move.carta.tipo in [10,11]: # Nave de asalto o especial
        # El bombardero puede eliminar objectivos terrestres
        bombarderos = [46,146]
        if card_move.carta.id in bombarderos:

            rivales_terrestres = [0,1,2,3,4,5,6,8]
            if (card.carta.tipo in rivales_terrestres) and card_defensa <= (card_move.carta.ata+1) and not card.carta.en_nave:
                action_text = 'Bombardear y eliminar '+ card.carta.nombre
                return True, action_text
            elif (card.carta.tipo == 7) and (card.carta.defensa + def_rival) <= (card_move.carta.ata+1) :
                action_text = 'Bombardear y eliminar '+ card.carta.nombre
                return True, action_text

        rivales_aereos = [9,10,11]
        if (card.carta.tipo in rivales_aereos) and card.carta.defensa <= card_move.carta.ata:
            action_text = 'Derribar '+ card.carta.nombre+' con su tripulacion'
            return True, action_text

    return False, action_text


def check_action2_card(card,card_move,card_mesa,ataque,def_rival):
    # SE EJECUTA EN FASE 2 O ATAQUE DE BONIFICACION
    # Funcion que chequea que una carta puede aplicar poder principal sobre otra
    # card: Es la carta que esta en el tablero con la que se chequea la accion si es posible
    # card_move: Es la carta que realiza la accion
    # ataque: indica el modificador local de ataque
    # def_rival: indica el modificador de defensa rival
    
    action_text = '' ## indica la accion a llevar a cabo en texto
    
    if card.carta.bando == card_move.carta.bando:
        # No puede aplicarse sobre cartas del mismo bando
        return False, action_text 

    # Vemos si esta el senulo y calculamos la defensa de la carta atacada
    senuelo, card_defensa = calcular_def(card,card_mesa,def_rival)       

    try:
        
        # Chequear que no hay un senuelo en la mesa
        senuelos = [32,132]

        if senuelo and card.carta.id in senuelos and (card.carta.defensa + def_rival) <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
            action_text = 'Eliminar senuelo '+ card.carta.nombre
            return True, action_text
        elif senuelo: # Esta el senuelo y no se cumple ninguna condicion principal
            return False, action_text

        # Jedis contra tropas terrestres
        if card_move.carta.id in [25,125] and not card_move.carta.en_nave: #Kylo Ren and Mace Vindu

            rivales = [0,1] ## Cartas de Tropa o Tropa especial
            if (card.carta.tipo in rivales) and card_defensa <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
                action_text = 'Aniquilar a '+ card.carta.nombre
                return True, action_text

        # Finn o rey
        elif card_move.carta.id in [66,67] and not card_move.carta.en_nave: ## Finn o Rey

            rivales = [0,1,2,3,4,5,6,8] ## Sus rivales cualquier carta en tierra y le llegue el ataque
            if (card.carta.tipo in rivales) and card_defensa <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
                action_text = 'Eliminar a '+ card.carta.nombre
                return True, action_text
            elif (card.carta.tipo == 7) and card_defensa <= (card_move.carta.ata + ataque):
                action_text = 'Derribar '+ card.carta.nombre
                return True, action_text

        # General Greivous
        elif card_move.carta.id == 121 and not card_move.carta.en_nave: #General Greivous
            # Elimina una carta Jedi adicional
            if (card.carta.tipo == 4) and card_defensa <= (card_move.carta.ata + ataque) and not card.carta.en_nave:
                action_text = 'Derrotar a '+ card.carta.nombre
                return True, action_text

        return False, action_text
    except:
        return False, action_text

    #Chequeo sobre cartas de distinto bando ATAQUE
    #La carta sobre la que se comprueba no puede estar en una Nave como tripulante

def check_movement_frame(frame,card_move,hangar,hangar_count):
    # Esta funcion chequea si el movimiento de la carta que se esta moviendo es posible sobre el frame correspondiente
    # frame: frame que se chequea
    # card_move: Card_scr que se esta moviendo
    # juega: quien esta jugando
    # hangar_count: dice si hay posibilidad de anyadir la carta al hangar (tiene que ser >0)

    action_text = ''
    # Funcion que chequea que una carta que se esta arrastrando por el tablero puede ponerse sobre un FRAME
    if frame.bando == card_move.carta.bando:
        # TERRESTRE
        if frame.tipo == 0:
            if (card_move.carta.tipo in [0,1,2,6]):
                # Tipo Tropa, Tropa especial, Contrabandista y Lider pueden colocarse
                action_text = 'Colocar como tropa terrestre'
                return True, action_text
            elif card_move.carta.tipo == 4: 
                # Tipo Jedi
                action_text = 'Posicionar Jedi/Sith como tropa terrestre'
                return True, action_text
            elif card_move.carta.tipo == 3: 
                # Tipo Oficial
                action_text = 'Posicionar Oficial como tropa terrestre'
                return True, action_text
            elif card_move.carta.tipo == 5: 
                # Tipo Oficial
                action_text = 'Posicionar Lider como tropa terrestre'
                return True, action_text
            elif card_move.carta.tipo == 7:
                # Tipo Vehiculo
                action_text = 'Desplegar Vehiculo terrestre'
                return True, action_text
            elif card_move.carta.tipo == 8 and card_move.carta.id in [31,32,132]:
                # Tipo Droide
                # Los droides de protocolo y de interrogatorio no se pueden colocar como tropa. Solo funcionales
                action_text = 'Colocar Droide como tropa terrestre'
                return True, action_text
        # ESPACIO
        elif frame.tipo == 1:
            if card_move.carta.tipo in [10,11]:
                # Tipo Nave de asalto o especial
                action_text = 'Colocar Nave de asalto'
                return True, action_text
            elif card_move.carta.tipo == 9:
                # Tipo Nave de combate
                action_text = 'Colocar Nave de combate'
                return True, action_text
        # HANGAR
        elif frame.tipo == 2 and hangar_count > 0:
            if card_move.carta.tipo in [10,11]:
                # Revisamos si hay sitio en el hangar
                nohaysitio = False
                for nave in hangar:
                    if nave.carta.bando == card_move.carta.bando:
                        nohaysitio = True
                if nohaysitio:
                    return False, action_text
                else:
                    # Se mueve una nave de asalto al Hangar
                    action_text = 'Posicionar nave de asalto en el hangar (no suma puntos)'
                    return True, action_text
    ## FRAME ELIMINAR CARTA
    elif frame.bando == 'E':
            ## Esta sobre el frame de eliminar carta. Es una accion que siempre se puede hacer
            action_text = 'Eliminar carta y pasar turno'
            return True, action_text

    # Inicialmente no se pueden colocar ni DROIDES ni OFICIALES sobre un frame. Las cartas especiales tampoco
    return False, action_text

def check_movement_card(card,card_move):
    # Funcion que chequea que una carta que se esta arrastrando por el tablero puede ponerse sobre una CARTA (como tripulante)
    # card: Es la carta que hay en el tablero con la que se chequea la accion
    # card_move: Es la carta que se esta moviendo por el tablero

    action_text = ''
    
    try:
        # Se esta moviendo un tripulante potencial
        if card_move.carta.tripulante and card.carta.bando == card_move.carta.bando:

            # Revisar que es un dirigente y hay sitio par ubicarse como tal en nave de combate
            if card.carta.tipo == 9 and card_move.carta.dirige and (card.carta.dirigentes < card.carta.max_dirige) and (card.carta.tripulacion < card.carta.tripulacion_max):
                action_text = card_move.carta.nombre+' dirigirá la nave y activa su ataque'
                return True, action_text

            # DROIDES DE PROTOCOLO
            elif card_move.carta.id in [30,130] and card.carta.tipo == 9 and (card.carta.tripulacion < card.carta.tripulacion_max):
                action_text = 'Bloquea la nave '+card.carta.nombre+' e impide anadir mas tripulacion'
                return True, action_text  

            # Revisar si la carta de tropa/droide puede ser tripulante sobre una Nave de combate y hay sitio
            elif card.carta.tipo == 9 and (card_move.carta.tipo in [0,1,8]) and (card.carta.tripulacion < card.carta.tripulacion_max):
                action_text = 'Colocar a '+card_move.carta.nombre+' como tripulación en la nave'
                return True, action_text

            # Revisar sobre las naves de asalto las diferentes casuisticas de tripulacion/pilotos
            elif (card.carta.tipo == 10) and (card.carta.tripulacion < card.carta.tripulacion_max):

                pilotos = [28,165] ## Luke y Capitan Phasma
                droides_nave = [31,32,33] ## R2D2 y BB-8
                alaX = [42,43]

                if card_move.carta.tipo == 2 or card_move.carta.id in pilotos and (card.carta.dirigentes < card.carta.max_dirige):
                # Pilotos sobre nave de asalto
                    action_text = card_move.carta.nombre+' pilota la nave y ataca' 
                
                elif card_move.carta.id in droides_nave and card.carta.id in alaX and (card.carta.tripulacion == card.carta.dirigentes): # ALA-x
                    ## Coloca los droides como tripulacion en Ala-X
                    action_text = 'Colocar a '+card_move.carta.nombre+' como tripulante de la nave'
                
                # Darth Vader en Tie Advance
                elif card_move.carta.id == 123 and card.carta.id == 145:
                    action_text = card_move.carta.nombre+' pilota la nave y ataca'

                # Kylo Ren en Tie Silencer
                elif card_move.carta.id == 125 and card.carta.id == 144:
                    action_text = card_move.carta.nombre+' pilota la nave y ataca'

                else:
                    return False, action_text
                return True, action_text        

            # Nave especial
            elif (card.carta.tipo == 11) and (card.carta.tripulacion < card.carta.tripulacion_max):

                naves_jedis_sith = [48,49,148] ## Naves Jedi y Sith
                no_pilotos = [20,27,28,120,126] ## Jedis y Sith que no son pilotos de naves Jedis/Sith incluye a Luke
                pilotos_halcon = [61,65,67] ## Han Solo, Lando y Rey
                tripulantes_halcon = [60,66,67,31,32,27,18] ## Chewbacca, Finn, Rey, R2D2, BB8, ObiWan y Leia
                droides_nave = [31,32,33,132] ## R2D2 y BB-8 y R5-D4 y astromecanico
                
                if card_move.carta.tipo == 4 and card.carta.id in naves_jedis_sith and not card_move.carta.id in no_pilotos and (card.carta.dirigentes < card.carta.max_dirige):
                    # Jedis o Siths en Naves de asalto
                    action_text = card_move.carta.nombre+' pilota la nave y ataca'
                
                elif card_move.carta.id == 161 and card.carta.id == 147:   ## Boba fett en Esclavo I
                    action_text = card_move.carta.nombre+' pilota Esclavo I y ataca'
                
                elif card_move.carta.id in pilotos_halcon and card.carta.id == 47 and (card.carta.dirigentes < card.carta.max_dirige):
                    ## Piloto Halcon y ataca. Solo puede haber un ataque    
                    action_text = card_move.carta.nombre+' pilota el Halcón y ataca'
                
                elif card_move.carta.id in tripulantes_halcon and card.carta.id == 47: ## Coloca tripulacion del Halcon
                    action_text = 'Colocar a '+card_move.carta.nombre+' como tripulante del Halcon'

                elif card_move.carta.id in droides_nave and card.carta.id in naves_jedis_sith and (card.carta.tripulacion == card.carta.dirigentes):
                    ## Coloca los droides como tripulacion en Nave Jedi o Sith Infiltrator
                    action_text = 'Colocar a '+card_move.carta.nombre+' en la nave como apoyo'

                else:
                    return False, action_text
                return True, action_text

        return False, action_text
    except:
        return False, action_text    