from clases import *
import random

def barajar_aliados():
    
    #Tipos de carta
    #0: Tropa
    #1: Tropa Especial/Personaje (se comportan como tropa no aplica)
    #2: Pilotos
    #3: Oficial/Lider
    #4: Jedi/Sith
    #5: Lider
    #6: Contrabandista/Cazarecompensas
    #7: Vehiculo terrestre
    #8: Droide
    #9: Nave de combate
    #10: Nave de asalto
    #11: Nave especial

    #ID < 100 para todas las cartas rebeldes
    baraja_aliada =[]
    #Lista de cartas aliadas
    card1 = Tropa(1,'comando rebelde endor.jpg',0,'R','Comandos rebeldes Endor',1,1)
    card1.setup(1,1,0) # ataque, defensa, evasion
    card1.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card1)

    card2 = Tropa(2,'COMANDO REBELDE HOTH.jpg',0,'R','Comandos rebeldes hoth',1,1)
    card2.setup(1,1,0)
    card2.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card2)

    card3 = Tropa(3,'EWOKS.1.jpg',0,'R','Ewoks',1,1)
    card3.setup(1,0,0)
    card3.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card3.tripulante = False
    baraja_aliada.append(card3)

    card4 = Tropa(4,'EWOKS.jpg',0,'R','Ewoks',1,1)
    card4.setup(1,0,0)
    card4.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque 
    card4.tripulante = False
    baraja_aliada.append(card4)

    card5 = Tropa(5,'GUARDIA DE NABOO.jpg',0,'R','Guardia de Naboo',1,1)
    card5.setup(1,2,3)
    card5.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque 
    baraja_aliada.append(card5)

    card6 = Tropa(6,'rogue one.jpg',0,'R','Rogue One',1,2)
    card6.setup(3,2,4)
    card6.set_tripulante(1,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card6)

    card7 = Tropa(7,'COMANDO CLON.jpg',0,'R','Soldados Clon',2,1)
    card7.setup(1,1,0)
    card7.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card7)

    card8 = Tropa(8,'COMANDO REBELDE ELITE.jpg',0,'R','Comando rebelde de elite',1,1)
    card8.setup(2,2,3)
    card8.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card8.tripulante = False
    baraja_aliada.append(card8)

#   card9 = Tropa(9,'COMANDO REBELDE SCARIF.jpg',0,'R','Comando rebelde Scarif',1,1)
#   card9.setup(1,1,0)
#   card9.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
#   baraja_aliada.append(card9)

#   card9 = Tropa(9,'COMANDO CLON.1.jpg',0,'R','Comando Clon',1,1)
#   card9.setup(1,1,0)
#   card9.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
#   baraja_aliada.append(card9)

    ## Vehiculos
    card10 = Tropa(10,'SPEEDER.jpg',7,'R','Deslizador de nieve',1,1)
    card10.setup(3,3,0)
    card10.tripulante = False
    baraja_aliada.append(card10)

    card11 = Tropa(11,'VEHICULO CLON LAAT.jpg',7,'R','Vehiculo clon LAAT',1,1)
    card11.setup(3,3,0)
    card11.tripulante = False   
    baraja_aliada.append(card11)

    card12 = Tropa(12,'VEHICULO CLON AT-DP.jpg',7,'R','Vehiculo clon AT-DP',1,1)
    card12.setup(4,4,0)
    card12.tripulante = False
    card12.set_terrain(0,1) # +1 ATA
    baraja_aliada.append(card12)

    ## Oficiales tipo 3
    card16 = Tropa(16,'MON MOTHMA.jpg',3,'R','Mon Mothma',1,1)
    card16.setup(0,2,0)
    card16.set_tripulante(0,2,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card16.set_terrain(1,0) # Aplica +1 defensa si se coloca como tropa
    baraja_aliada.append(card16)

    card17 = Tropa(17,'ALMIRANTE ACKBAR.jpg',5,'R','Almirante Ackbar',2,2)
    card17.setup(1,1,0)
    card17.set_tripulante(1,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque  
    baraja_aliada.append(card17)

    ## Lider tipo 5
    card18 = Tropa(18,'PRINCESA LEIA.jpg',5,'R','Princesa Leia',1,3)
    card18.setup(2,3,0)
    card18.set_tripulante(0,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card18.set_terrain(1,1) # Aplica modificadores terrestres +1 ATA y DEF
    baraja_aliada.append(card18)

    ## JEDIS tipo 4
    card20 = Tropa(20,'YODA.jpg',4,'R','Mestro Yoda',2,3)
    card20.setup(6,6,3)
    card20.set_tripulante(0,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card20)

    card21 = Tropa(21,'ANAKIN SKYWALKER.jpg',4,'R','Anakin Skywalker',2,2)
    card21.setup(5,5,0)
    card21.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card21)

    card22 = Tropa(22,'QUI GON JINN.jpg',4,'R','Qui-Gon Jinn',2,2)
    card22.setup(5,4,0)
    card22.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card22)

    card23 = Tropa(23,'KI-ADI MUNDI.jpg',4,'R','Ki-Adi Mundi',1,1)
    card23.setup(4,4,0)
    card23.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card23.set_terrain(0,1) # +1 ATA
    baraja_aliada.append(card23)

    card24 = Tropa(24,'GENERAL KENOBI.jpg',4,'R','General Kenobi',2,3)
    card24.setup(6,6,0)
    card24.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card24)

    card25 = Tropa(25,'MACE VINDU.jpg',4,'R','Mace Vindu',2,2)
    card25.setup(6,5,3)
    card25.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque 
    baraja_aliada.append(card25)

    card26 = Tropa(26,'LUMINARA UNDULI.jpg',4,'R','Luminara Unduli',1,2)
    card26.setup(5,4,3)
    card26.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card26.set_terrain(1,0)
    baraja_aliada.append(card26)

    card27 = Tropa(27,'OBI WAN KENOBI VIEJO.jpg',4,'R','Obi Wan Kenobi viejo',2,2)
    card27.setup(5,5,0)
    card27.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card27.set_terrain(-1,0)
    baraja_aliada.append(card27)

    card28 = Tropa(28,'LUKE SKYWALKER.jpg',4,'R','Luke Skywalker',1,2)
    card28.setup(4,4,0)
    card28.set_tripulante(0,2,3,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card28)

    ## Droides
    # Cambio bando del droide de protocolo
    card30 = Tropa(30,'C3PO.jpg',8,'I','Droide de protocolo C3-PO',0,0)
    card30.setup(0,0,0) # ataque, defensa, evasion
    card30.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card30)

    card31 = Tropa(31,'R2-D2.jpg',8,'R','R2-D2',2,1)
    card31.setup(0,0,0) # ataque, defensa, evasion
    card31.set_tripulante(0,1,1,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card31)

    card32 = Tropa(32,'BB-8.jpg',8,'R','BB-8',1,1)
    card32.setup(0,0,0) # ataque, defensa, evasion
    card32.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card32)

#   card33 = Tropa(33,'R5-D4.jpg',8,'R','R5-D4',1,1)
#   card33.setup(0,0,0) # ataque, defensa, evasion
#   card33.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
#   baraja_aliada.append(card33)

    ## Pilotos
    card35 = Tropa(35,'POE DAMERON.jpg',2,'R','Poe Dameron',1,1)
    card35.setup(2,1,0) # ataque, defensa, evasion
    card35.set_tripulante(0,1,2,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card35)

    card36 = Tropa(36,'WEDGE ANTILLES.jpg',2,'R','Wedge Antilles',1,1)
    card36.setup(1,1,0) # ataque, defensa, evasion
    card36.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card36)

    card37 = Tropa(37,'BIGGS DARKLIGHTER.jpg',2,'R','Biggs Darklighter',1,1)
    card37.setup(1,1,0) # ataque, defensa, evasion
    card37.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card37)

    ## Naves de asalto tipo 10 
    card41 = Nave(41,'ESCUADRON ORO ALA-B.jpg',10,'R','Escuadron Oro: B-Wing',0,1)
    card41.setup(3,3,2) # ataque, defensa y evasion
    card41.set_param_nave(1,1) # tripulacion max, max dirigentes
    baraja_aliada.append(card41)

    card42 = Nave(42,'ESCUADRON NEGRO ALA-X.jpg',10,'R','Escuadron azul: X-Wing',0,1)
    card42.setup(3,3,3) # ataque, defensa y evasion
    card42.set_param_nave(2,1) # tripulacion max, max dirigentes = droides
    baraja_aliada.append(card42)

    card43 = Nave(43,'ESCUADRON ROJO ALA-X.jpg',10,'R','Escuadron rojo: X-Wing',0,1)
    card43.setup(3,3,3) # ataque, defensa y evasion
    card43.set_param_nave(2,1) # tripulacion max, max dirigentes
    baraja_aliada.append(card43)

    card46 = Nave(46,'ESCUADRON AMARILLO ALA-Y.jpg',10,'R','Escuadron Amarillo: Y-Wing',0,1)
    card46.setup(3,3,0) # ataque, defensa y evasion
    card46.set_param_nave(1,1) # tripulacion max, max dirigentes  = droides
    baraja_aliada.append(card46)

    # Naves de asalto especiales tipo 11
    card47 = Nave(47,'HALCON MILENARIO.jpg',11,'R','Halcon Milenario',0,2)
    card47.setup(3,4,4) # ataque, defensa y evasion
    card47.set_param_nave(3,1) # tripulacion max, max dirigentes
    baraja_aliada.append(card47)

    card48 = Nave(48,'JEDI STARFIGHTER.jpg',11,'R','Jedi Starfighter',0,1)
    card48.setup(3,4,5) # ataque, defensa y evasion
    card48.set_param_nave(2,1) # tripulacion max, max dirigentes  = droides
    baraja_aliada.append(card48)

    card49 = Nave(49,'JEDI STARFIGHTER.1.jpg',11,'R','Jedi Starfighter',0,1)
    card49.setup(3,4,5) # ataque, defensa y evasion
    card49.set_param_nave(2,1) # tripulacion max, max dirigentes  = droides
    baraja_aliada.append(card49)

    # Naves de combate tipo 9
    card50 = Nave(50,'CORVETA CORELIANA.jpg',9,'R','Corveta Coreliana',0,2)
    card50.setup(4,5,0) # ataque, defensa y evasion
    card50.set_param_nave(3,1) # tripulacion max, max dirigentes
    baraja_aliada.append(card50)

#   card51 = Nave(51,'CORVETA CORELIANA.jpg',9,'R','Corveta Coreliana',0,2)
#   card51.setup(4,5,0) # ataque, defensa y evasion
#   card51.set_para_nave(3,1) # tripulacion max, max dirigentes
#   baraja_aliada.append(card51)

    card52 = Nave(52,'FRAGATA NEBULON I.jpg',9,'R','Fragata Nebulon I',0,2)
    card52.setup(4,5,0) # ataque, defensa y evasion
    card52.set_param_nave(4,1) # tripulacion max, max dirigentes
    baraja_aliada.append(card52)

    card53 = Nave(53,'NAVE DE TRANSPORTE.jpg',9,'R','Nave de Transporte',0,2)
    card53.setup(4,5,0) # ataque, defensa y evasion
    card53.set_param_nave(4,2) # tripulacion max, max dirigentes
    baraja_aliada.append(card53)

    card54 = Nave(54,'CALAMARI.jpg',9,'R','Calamari',0,2)
    card54.setup(5,5,0) # ataque, defensa y evasion
    card54.set_param_nave(3,1) # tripulacion max, max dirigentes
    baraja_aliada.append(card54)

    # Cazarecompensas o Contrabandistas 6
    card60 = Tropa(60,'CHEWBACCA.jpg',6,'R','Chewbacca',2,1)
    card60.setup(2,2,4) # ataque, defensa, evasion
    card60.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card60)

    card61 = Tropa(61,'HAN SOLO.jpg',6,'R','Han Solo',2,2)
    card61.setup(3,3,5) # ataque, defensa, evasion
    card61.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card61)

    # Tropa Especial Tipo 1
    card65 = Tropa(65,'LANDO CALRISSIAN.jpg',1,'R','Lando Calrissian',1,2)
    card65.setup(2,1,3)
    card65.set_tripulante(0,1,1,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card65)

    card66 = Tropa(66,'FINN.jpg',1,'R','Finn',2,1)
    card66.setup(2,2,2)
    card66.set_tripulante(0,0,3,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card66)

    card67 = Tropa(67,'REY.jpg',1,'R','Rey',2,1)
    card67.setup(3,3,2) # ataque, defensa, evasion
    card67.set_tripulante(0,0,3,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_aliada.append(card67)

    random.shuffle(baraja_aliada)
    
    return baraja_aliada

def barajar_imperio():
    
    #Tipos de carta
    #0: Tropa
    #1: Tropa Especial/Personaje
    #2: Piloto
    #3: Oficial
    #4: Jedi/Sith
    #5: Lider
    #6: Contrabandista
    #7: Vehiculo terrestre
    #8: Droide
    #9: Nave de combate
    #10: Nave de asalto
    #11: Nave especial
    
    baraja_imperio = []
    # El ID de las cartas del imperioes > 100
    #Lista de cartas imperio
    card1 = Tropa(101,'SOLDADOS IMPERIALES.jpg',0,'I','Soldados de asalto',1,1)
    card1.setup(1,1,0) # ataque, defensa, evasion
    card1.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card1)

    card2 = Tropa(102,'SOLDADOS IMPERIALES.1.jpg',0,'I','Soldados de asalto',1,1)
    card2.setup(1,1,0)
    card2.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card2)
    
    card3 = Tropa(103,'DROIDES DE COMBATE.jpg',0,'I','Droides de combate',1,1)
    card3.setup(1,0,0)
    card3.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card3)

    card4 = Tropa(104,'SUPERDROIDES DE COMBATE.jpg',0,'I','Superdroides de combate',1,1)
    card4.setup(1,1,0)
    card4.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card4)
    
    card5 = Tropa(105,'SOLDADOS DE ASALTO OSCUROS.jpg',0,'I','Soldados de asalto oscuros',1,1)
    card5.setup(2,2,3)
    card5.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card5)

    card6 = Tropa(106,'SOLDADO EXPLORADOR.jpg',0,'I','Soldado explorador',2,1)
    card6.setup(2,1,4)
    #card6.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card6.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card6.tripulante = False
    baraja_imperio.append(card6)

    card7 = Tropa(107,'GUARDIA GAMORREANA.jpg',0,'I','Guardia Gamorreana',1,1)
    card7.setup(1,1,3)
    card7.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card7.tripulante = False
    baraja_imperio.append(card7)

    card8 = Tropa(108,'SOLDADOS IMPERIALES SCARIF.jpg',0,'I','Soldados imperiales Scarif',1,1)
    card8.setup(1,1,0)
    card8.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card8)

    card9 = Tropa(109,'ESCUADRON INFERNAL.jpg',0,'I','Escuadron infernal',1,1)
    card9.setup(2,2,0)
    card9.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card9)

    ## Vehiculos
    card10 = Tropa(110,'AT-AT.jpg',7,'I','Vehiculo AT-AT',1,1)
    card10.setup(4,5,0)
    card10.tripulante = False
    card10.set_terrain(0,1) # +1 ATA
    baraja_imperio.append(card10)

    card11 = Tropa(111,'AT-ST.jpg',7,'I','Vehiculo AT-ST',1,1)
    card11.setup(3,3,0)
    card11.tripulante = False   
    baraja_imperio.append(card11)

#   card12 = Tropa(112,'AT-ST.jpg',7,'I','Vehiculo AT-ST',1,1)
#   card12.setup(3,3,0)
#   card12.tripulante = False
#   baraja_imperio.append(card12)

    card13 = Tropa(113,'VEHICULO DROIDE.jpg',7,'I','Vehiculo Droide',1,1)
    card13.setup(3,3,0)
    card13.tripulante = False   
    baraja_imperio.append(card13)

    ## Oficial Tipo 3
    card15 = Tropa(115,'DIRECTOR KRENNIC.jpg',3,'I','Director Krennic',1,1)
    card15.setup(2,1,2) # ataque, defensa, evasion
    card15.set_tripulante(1,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card15)

    card16 = Tropa(116,'MOF JERJERROD.jpg',3,'I','Mof Jerjerrod',1,1)
    card16.setup(0,2,0) # ataque, defensa, evasion
    card16.set_tripulante(0,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card16.set_terrain(1,0) # Aplica +1 defensa si se coloca como tropa
    baraja_imperio.append(card16)

    card17 = Tropa(117,'GENERAL VEERS.jpg',5,'I','General Veers',2,2)
    card17.setup(1,1,0) # ataque, defensa, evasion
    card17.set_tripulante(1,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card17)

    ## Lider Tipo 5
    card18 = Tropa(118,'GENERAL TARKIN.jpg',5,'I','General Tarkin',1,3)
    card18.setup(1,3,0) # ataque, defensa, evasion
    card18.set_tripulante(1,0,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card18.set_terrain(1,1) # Aplica modificadores terrestres +1 ATA y DEF
    baraja_imperio.append(card18)

    ## Siths Tipo 4
    card20 = Tropa(120,'EMPERADOR PALPATINE.jpg',4,'I','Emperador Palpatine',2,3)
    card20.setup(6,6,3) # ataque, defensa, evasion
    card20.set_tripulante(0,1,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card20)

    card21 = Tropa(121,'GENERAL GRIEVOUS.jpg',4,'I','General Grievous',2,2)
    card21.setup(4,4,3) # ataque, defensa, evasion
    card21.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card21.set_terrain(1,0) ## +1 defensa
    baraja_imperio.append(card21)

    card22 = Tropa(122,'DARTH MAUL.jpg',4,'I','Darth Maul',2,2)
    card22.setup(5,4,0) # ataque, defensa, evasion
    card22.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card22)

    card23 = Tropa(123,'DARTH VADER.jpg',4,'I','Darth Vader',2,3)
    card23.setup(6,6,0) # ataque, defensa, evasion
    card23.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card23)

    card24 = Tropa(124,'CONDE DOOKU.jpg',4,'I','Conde Dooku',2,2)
    card24.setup(4,4,0) # ataque, defensa, evasion
    card24.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card24)

    card25 = Tropa(125,'KYLO REN.jpg',4,'I','Kylo Ren',2,2)
    card25.setup(5,5,0) # ataque, defensa, evasion
    card25.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card25.set_terrain(-1,0)
    baraja_imperio.append(card25)

    card26 = Tropa(126,'DARTH SIDIOUS.jpg',4,'I','Darth Sidious',2,3)
    card26.setup(6,6,3) # ataque, defensa, evasion
    card26.set_tripulante(1,0,0,True,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card26.set_terrain(0,1) ## +1 Ataque
    baraja_imperio.append(card26)

    # Esta carta no se anyade a la baraja, solo es como muestra
#   card27 = Tropa(127,'ANAKIN OSCURO.jpg',4,'I','Anakin oscuro',0,2)
#   card27.setup(5,5,0) # ataque, defensa, evasion
#   card27.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
#   card27.set_terrain(1,0) ## +1 Defensa

    ## Droides
    # Cambio bando del droide de protocolo
    card30 = Tropa(130,'DROIDE PROTOCOLO IMPERIAL.jpg',8,'R','Droide de protocolo imperial',0,0)
    card30.setup(0,0,0) # ataque, defensa, evasion
    card30.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card30)

    card31 = Tropa(131,'DROIDE INTERROGATORIO.jpg',8,'I','Droide de interrogatorio imperial',1,1)
    card31.setup(50,0,0) # 100 ataque puede eliminar a cualquier carta menos Jedi o Vehiculo, defensa, evasion
    card31.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card31)

    card32 = Tropa(132,'DROIDE ASTROMECANICO.jpg',8,'I','Droide astromecanico imperial',1,1)
    card32.setup(0,0,0) # ataque, defensa, evasion
    card32.set_tripulante(0,1,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card32)

    # Pilotos
    card35 = Tropa(135,'PILOTO IMPERIAL.jpg',2,'I','Piloto imperial',1,1)
    card35.setup(1,1,0) # ataque, defensa, evasion
    card35.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card35)

    card36 = Tropa(136,'PILOTO IMPERIAL.1.jpg',2,'I','Piloto imperial',1,1)
    card36.setup(1,1,0) # ataque, defensa, evasion
    card36.set_tripulante(0,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card36)

    card37 = Tropa(137,'PILOTO PRIMERA ORDEN.jpg',2,'I','Piloto Primera Orden',1,1)
    card37.setup(1,1,0) # ataque, defensa, evasion
    card37.set_tripulante(0,1,1,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card37)

    ## Naves de asalto tipo 10 
    card41 = Nave(141,'ESCUADRON TIE FIGHTERS.jpg',10,'I','Escuadron Tie Fighters',0,1)
    card41.setup(3,3,2) # ataque, defensa y evasion
    card41.set_param_nave(1,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card41)

    card42 = Nave(142,'ESCUADRON TIE INTERCEPTORS.jpg',10,'I','Escuadron Tie Interceptors',0,1)
    card42.setup(3,3,3) # ataque, defensa y evasion
    card42.set_param_nave(1,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card42)

#   card43 = Nave(143,'ESCUADRON TIE INTERCEPTORS.jpg',10,'I','Escuadron Tie Interceptors',0,1)
#   card43.setup(3,3,3) # ataque, defensa y evasion
#   card43.set_param_nave(1,1) # tripulacion max, max dirigentes
#   baraja_imperio.append(card43)

    card44 = Nave(144,'TIE SILENCER.jpg',10,'I','Tie Silencer',0,1)
    card44.setup(3,4,4) # ataque, defensa y evasion
    card44.set_param_nave(1,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card44)

    card45 = Nave(145,'TIE ADVANCE.jpg',10,'I','Tie Advance',0,1)
    card45.setup(3,3,4) # ataque, defensa y evasion
    card45.set_param_nave(1,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card45)

    card46 = Nave(146,'TIE BOMBERS.jpg',10,'I','Tie Bombers',0,1)
    card46.setup(3,3,0) # ataque, defensa y evasion
    card46.set_param_nave(1,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card46)

    # Naves de asalto especiales tipo 11
    card47 = Nave(147,'ESCLAVO I.jpg',11,'I','Esclavo I',0,2)
    card47.setup(3,4,4) # ataque, defensa y evasion
    card47.set_param_nave(2,0) # tripulacion max, max dirigentes
    baraja_imperio.append(card47)

    card48 = Nave(148,'SITH INFILTRATOR.jpg',11,'I','Sith infiltrator',0,1)
    card48.setup(3,4,5) # ataque, defensa y evasion
    card48.set_param_nave(2,1) # tripulacion max, max dirigentes. Puede llevar droide funcional
    baraja_imperio.append(card48)


    # Naves de combate tipo 9
    card50 = Nave(150,'DESTRUCTOR IMPERIAL.jpg',9,'I','Destructor Imperial',0,2)
    card50.setup(4,5,0) # ataque, defensa y evasion
    card50.set_param_nave(3,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card50)

#   card51 = Nave(151,'DESTRUCTOR IMPERIAL.jpg',9,'I','Destructor Imperial',0,2)
#   card51.setup(4,5,0) # ataque, defensa y evasion
#   card51.set_param_nave(3,1) # tripulacion max, max dirigentes
#   baraja_imperio.append(card51)

    card52 = Nave(152,'SUPERDESTRUCTOR IMPERIAL.jpg',9,'I','SuperDestructor Imperial',0,2)
    card52.setup(5,5,0) # ataque, defensa y evasion
    card52.set_param_nave(3,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card52)

    card53 = Nave(153,'NAVE FEDERACION COMERCIO.jpg',9,'I','Nave Federacion de comercio',0,2)
    card53.setup(4,5,0) # ataque, defensa y evasion
    card53.set_param_nave(2,1) # tripulacion max, max dirigentes
    baraja_imperio.append(card53)

    card54 = Nave(154,'ESTRELLA DE LA MUERTE.jpg',9,'I','Estrella de la muerte',0,2)
    card54.setup(5,10,0) # ataque, defensa y evasion
    card54.set_param_nave(5,2) # tripulacion max, max dirigentes
    baraja_imperio.append(card54)

#   card55 = Nave(155,'ESTRELLA DE LA MUERTE DANADA.jpg',9,'I','Estrella de la muerte',0,2)
#   card55.setup(5,3,0) # ataque, defensa y evasion
#   card55.set_param_nave(5,2) # tripulacion max, max dirigentes

    # Cazarecompensas o Contrabandistas 6
    card60 = Tropa(160,'JABBA EL HUTT.jpg',6,'I','Jabba el Hutt',2,1)
    card60.setup(2,0,5) # ataque, defensa, evasion
    card60.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card60.tripulante = False
    baraja_imperio.append(card60)

    card61 = Tropa(161,'BOBA FETT.jpg',6,'I','Boba Fett',2,2)
    card61.setup(3,3,5) # ataque, defensa, evasion
    card61.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card61)

#   card62 = Tropa(162,'GREEDO.jpg',6,'I','Greedo',2,1)
#   card62.setup(2,2,3) # ataque, defensa, evasion
#   card62.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
#   card62.tripulante = False
#   baraja_imperio.append(card62)

    # Tropa especial
    card65 = Tropa(165,'CAPITAN PHASMA.jpg',1,'I','Capitan Phasma',1,2)
    card65.setup(2,2,4) # ataque, defensa, evasion
    card65.set_tripulante(0,1,2,False,True) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card65)

    card66 = Tropa(166,'NUTE GUNRAY.jpg',1,'I','Virrey Nute Gunray',2,2)
    card66.setup(1,1,2) # ataque, defensa, evasion
    card66.set_tripulante(0,0,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    baraja_imperio.append(card66)

    card67 = Tropa(167,'GUARDIA IMPERIAL.jpg',1,'I','Guardia Imperial',1,1)
    card67.setup(2,2,0) # ataque, defensa, evasion
    card67.set_tripulante(0,2,0,False,False) # nave_ataque,nave_defensa,nave_evasion,dirige,reataque
    card67.set_terrain(1,0) ## +1 Defensa tropas terrestres
    baraja_imperio.append(card67)

    random.shuffle(baraja_imperio)
    
    return baraja_imperio

# CARTAS INDEPENDIENTES
def ds_expuesta():
    # Death Star expuesta
    ds_expuesta = Nave(155,'ESTRELLA DE LA MUERTE EXPUESTA.jpg',9,'I','Estrella de la muerte expuesta',0,2)
    ds_expuesta.setup(5,3,0) # ataque, defensa y evasion
    ds_expuesta.set_param_nave(5,2) # tripulacion max, max dirigentes
    return ds_expuesta

def anakin_oscuro():
    # Anakin Oscuro
    anakin = Tropa(127,'ANAKIN OSCURO.jpg',4,'I','Anakin oscuro',1,2) 
    anakin.setup(5,5,0) # ataque, defensa, evasion
    anakin.set_tripulante(1,1,0,False,True) # nave_ataque,nave_defensa,dirige,reataque
    anakin.set_terrain(1,0) ## +1 Defensa terrestre    
    return anakin


