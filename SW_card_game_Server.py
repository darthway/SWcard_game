#! /usr/bin/env python
import sys
import random
import globals_server
from Tkinter import *
import tkMessageBox
from globals_server import *

#from clases import * # Incluye todas las clases
from sys import stdin, exit

from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

#from check_intro import *
host = 'localhost' ## Variable por defecto del server
port = 7000 ## Variable por defecto con el puerto al que conectarse en el juego

# Esta es la clase que corresponde a cada partida en juego y tiene las varaibles particulares de cada partida
class Game:
    def __init__(self, player0, currentgame, bando):
        # whose turn (1 or 0)
        # Determina quien juega en cada momento
        self.jugando = ''
        
        #initialize the players including the one who started the game
        self.player0={'playerid': player0, 'bando': bando, 'alias': "Anonymous"}
        self.player1={'playerid': None, 'bando': '', 'alias': "Anonymous"}

        #gameid of game
        self.gameid=currentgame

        ## Nos interesa saber las cartas que tiene cada jugador en su mano, para ver info o robar una de ellas
        self.mano0 = [] ## Mano del jugador 0
        self.mano1 = [] ## Mano del jugador 1

class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    Cada cliente tiene su propio canal para hablar con el servidor que es este por cliente
    """
    def __init__(self, *args, **kwargs):
        self.alias = "Anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    #########################
    #########

    def PassOn(self, data):
        # pass on what we received to all connected clients
        data.update({"id": self.id})
        self._server.SendToAll(data)
        
    def Network_set_alias(self, data):
        # Esta funcion se llama desde el cliente para inicializar su alias
        partida = data ['partida']
        
        if data ['jugador'] == 0:
            player = self._server.games[partida].player0['alias'] = data['alias']
        elif data ['jugador'] == 1:
            player = self._server.games[partida].player1['alias'] = data['alias']
        
    def Network_bando(self, data):
        #El bando que viene es el del jugador 0
        self._server.set_bando(data['bando_p0'],data['bando_p1'],data['partida'])

    def Network_check_version(self, data):
        partida = data ['partida']
        self._server.games[partida].player0['playerid'].Send({"action": "check_version", "version": globals_server.VERSION})
        self._server.games[partida].player1['playerid'].Send({"action": "check_version", "version": globals_server.VERSION})

    def Network_send_images(self, data):
        partida = data ['partida']

        # MANDAR IMAGENES A CADA CLIENTE
        #Convertimos a string las imagenes globales
        strshield = pygame.image.tostring(globals_server.shield, "RGBA")
        strattack = pygame.image.tostring(globals_server.attack, "RGBA")


        # Enviamos las imagenes a los jugadores
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strshield,"size":globals_server.shield.get_size(),'tipo':'S','long':len(strshield)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strshield,"size":globals_server.shield.get_size(),'tipo':'S','long':len(strshield)})
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strattack,"size":globals_server.attack.get_size(),'tipo':'A','long':len(strattack)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strattack,"size":globals_server.attack.get_size(),'tipo':'A','long':len(strattack)})

        # Indicators
        strred = pygame.image.tostring(globals_server.redindicator, "RGBA")
        strgreen = pygame.image.tostring(globals_server.greenindicator, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strred,"size":globals_server.redindicator.get_size(),'tipo':'R','long':len(strred)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strred,"size":globals_server.redindicator.get_size(),'tipo':'R','long':len(strred)})
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strgreen,"size":globals_server.greenindicator.get_size(),'tipo':'G','long':len(strgreen)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strgreen,"size":globals_server.greenindicator.get_size(),'tipo':'G','long':len(strgreen)})

        # Score
        strscore_rebels = pygame.image.tostring(globals_server.score_rebels, "RGBA")
        strscore_empire = pygame.image.tostring(globals_server.score_empire, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strscore_rebels,"size":globals_server.score_rebels.get_size(),'tipo':'SCR','long':len(strscore_rebels)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strscore_rebels,"size":globals_server.score_rebels.get_size(),'tipo':'SCR','long':len(strscore_rebels)})
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strscore_empire,"size":globals_server.score_empire.get_size(),'tipo':'SCI','long':len(strscore_empire)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strscore_empire,"size":globals_server.score_empire.get_size(),'tipo':'SCI','long':len(strscore_empire)})

        # Icon_Sound
        strsound_on = pygame.image.tostring(globals_server.sound_on, "RGBA")
        strsound_off = pygame.image.tostring(globals_server.sound_off, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strsound_on,"size":globals_server.sound_on.get_size(),'tipo':'ON','long':len(strsound_on)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strsound_on,"size":globals_server.sound_on.get_size(),'tipo':'ON','long':len(strsound_on)})
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strsound_off,"size":globals_server.sound_off.get_size(),'tipo':'OFF','long':len(strsound_off)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strsound_off,"size":globals_server.sound_off.get_size(),'tipo':'OFF','long':len(strsound_off)})

        # IMG ERASE CARD
        strerase = pygame.image.tostring(globals_server.image_erasecard, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strerase,"size":globals_server.image_erasecard.get_size(),'tipo':'E','long':len(strerase)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strerase,"size":globals_server.image_erasecard.get_size(),'tipo':'E','long':len(strerase)})

        # IMG DECKS
        strrebeldeck = pygame.image.tostring(globals_server.rebels_deck, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strrebeldeck,"size":globals_server.rebels_deck.get_size(),'tipo':'DR','long':len(strrebeldeck)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strrebeldeck,"size":globals_server.rebels_deck.get_size(),'tipo':'DR','long':len(strrebeldeck)})
        strrebeldeck0 = pygame.image.tostring(globals_server.rebels_deck0, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strrebeldeck0,"size":globals_server.rebels_deck0.get_size(),'tipo':'DR0','long':len(strrebeldeck0)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strrebeldeck0,"size":globals_server.rebels_deck0.get_size(),'tipo':'DR0','long':len(strrebeldeck0)})
        strempiredeck = pygame.image.tostring(globals_server.empire_deck, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strempiredeck,"size":globals_server.empire_deck.get_size(),'tipo':'DI','long':len(strempiredeck)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strempiredeck,"size":globals_server.empire_deck.get_size(),'tipo':'DI','long':len(strempiredeck)})
        strempiredeck0 = pygame.image.tostring(globals_server.empire_deck0, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strempiredeck0,"size":globals_server.empire_deck0.get_size(),'tipo':'DI0','long':len(strempiredeck0)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strempiredeck0,"size":globals_server.empire_deck0.get_size(),'tipo':'DI0','long':len(strempiredeck0)})

        #Icons
        strrebelicon = pygame.image.tostring(globals_server.rebel_icon, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strrebelicon,"size":globals_server.rebel_icon.get_size(),'tipo':'RI','long':len(strrebelicon)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strrebelicon,"size":globals_server.rebel_icon.get_size(),'tipo':'RI','long':len(strrebelicon)})
        strempireicon = pygame.image.tostring(globals_server.empire_icon, "RGBA")
        self._server.games[partida].player0['playerid'].Send({"action": "images_set", "image":strempireicon,"size":globals_server.empire_icon.get_size(),'tipo':'EI','long':len(strempireicon)})
        self._server.games[partida].player1['playerid'].Send({"action": "images_set", "image":strempireicon,"size":globals_server.empire_icon.get_size(),'tipo':'EI','long':len(strempireicon)})

    def Network_start(self, data):
        # Da por iniciada la partida
        partida = data ['partida']

        # Comenzar la partida
        self._server.games[partida].player0['playerid'].Send({"action": "start", "start": True, "rival":self._server.games[partida].player1['alias']})
        self._server.games[partida].player1['playerid'].Send({"action": "start", "start": True, "rival":self._server.games[partida].player0['alias']})

    def Network_fin_partida(self,data):
        partida = data ['partida']
        self._server.games[partida].player0['playerid'].Send({"action": "fin_partida", "fin": True})
        self._server.games[partida].player1['playerid'].Send({"action": "fin_partida", "fin": True})

    def Network_mano_vacia(self, data):
        ## Indica al rival que se ha quedado sin cartas
        partida = data ['partida']
        
        if data ['jugador'] == 0:
            player = self._server.games[partida].player1['playerid']
        elif data ['jugador'] == 1:
            player = self._server.games[partida].player0['playerid']
        
        player.Send({"action": "mano_vacia", 
            "vacio": data['vacio']})

    def Network_update_mesa(self, data):
        # A esta funcion se le llama despues de hacer algo sobre el tablero, actualiza la mesa del rival
        partida = data ['partida']
        
        # Enviamos al jugador contrario para que lo pinte el id de la carta y la posicion
        if data ['jugador'] == 0:
            player = self._server.games[partida].player1['playerid']
        elif data ['jugador'] == 1:
            player = self._server.games[partida].player0['playerid']
        
        if data['accion'] == 'C': ## Colocar una carta en frame
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "pos": data['pos'],
                "accion": data['accion']})

        elif data['accion'] == 'T': ## Tripulante de nave
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "pos": data['pos'],
                "idnave": data['idnave'],
                "accion": data['accion']})

        elif data['accion'] == 'R': ## Tripulante capturado de nave
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "pos": data['pos'],
                "idnave": data['idnave'],
                "accion": data['accion']})
            
        elif data['accion'] == 'H': ## Colocada en el hangar
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "pos": data['pos'],
                "accion": data['accion']})

        elif data['accion'] == 'E': ## Eliminar una carta
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "accion": data['accion']})

        elif data['accion'] == 'A': ## Eliminar anakin como tropa
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "accion": data['accion']})

        elif data['accion'] == 'ET': ## Eliminar tripulante de una nave
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "accion": data['accion']})

        elif data['accion'] == 'M': ## Actualiza el hangar
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "accion": data['accion']})

        elif data['accion'] == 'N': ## Modificar una carta tipo Nave
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "tripulacion": data['tripulacion'],
                "dirigentes": data['dirigentes'],
                "defensa": data['defensa'],
                "ataque": data['ataque'],
                "evasion": data['evasion'],
                "accion": data['accion']})

        elif data['accion'] == 'P': ## Elimina un droide de protocolo de una nave. Actualiza valores de nave
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "tripulacion": data['tripulacion'],
                "valor": data['valor'],
                "accion": data['accion']})

        elif data['accion'] == 'B': ## Bloquear nave de combate. no se permite acceso de ningun tripulante mas
            player.Send({"action": "update_mesa", 
                "idcard": data['idcard'],
                "pos": data['pos'],
                "idnave": data['idnave'],
                "accion": data['accion']})

        elif data['accion'] == 'R2':    ## R2-D2 reducir escudos de la Estrella de la muerte
            player.Send({"action": "update_mesa", 
                "accion": data['accion']})

        elif data['accion'] == 'K': ## Krennic reparar escudos de la Estrella de la muerte
            player.Send({"action": "update_mesa", 
                "accion": data['accion']})

        elif data['accion'] == 'F': ## Fin mazo, comunicar al rival
            player.Send({"action": "update_mesa", 
                "accion": data['accion']})

        elif data['accion'] == 'HD': ## Hangar destruido y las naves que pudiera haber dentro, comunicar al rival
            player.Send({"action": "update_mesa", 
                "accion": data['accion']})

    def Network_update_mano(self, data):
        #A esta funcion se le llama para actualizar la mano en el servidor por cada jugador
        partida = data ['partida']
        
        # Enviamos al jugador contrario para que lo pinte el id de la carta y la posicion
        if data ['jugador'] == 0:
            mano = self._server.games[partida].mano0
        elif data ['jugador'] == 1:
            mano = self._server.games[partida].mano1
        
        # Accion que se lleva a cabo sobre la mano de ese jugador
        if data['accion'] == 'A': ## Anyadir carta
            mano.append(data['idcard'])
        elif data['accion'] == 'R': ## Remove carta
            mano.remove(data['idcard'])
#       for i in mano:
#           print "Mano: "+str(i)
#       print "\n"
        #print "La carta "+str(data['idcard'])+" ya no esta en la mano"
    def Network_ask_mano(self,data):
        #A esta funcion se le llama para actualizar la mano en el servidor por cada jugador
        partida = data['partida']
        # Enviamos al jugador contrario para que lo pinte el id de la carta y la posicion
        if data ['jugador'] == 0:
            mano = self._server.games[partida].mano0
        elif data ['jugador'] == 1:
            mano = self._server.games[partida].mano1
        print "Partida: "+str(partida)
        print "Mano: \n"
        for i in mano:
            print str(i)+" "
        print "\n"
        #print "La carta "+str(data['idcard'])+" ya no esta en la mano"


    def Network_update_score(self, data):
        # Se actualiza el marcador en el rival, ya que se ha colocado una carta
        partida = data ['partida']
        
        if data ['jugador'] == 0:
            player = self._server.games[partida].player1['playerid']
        elif data ['jugador'] == 1:
            player = self._server.games[partida].player0['playerid']
        else:
            print "El numero de jugador no es correcto"
        player.Send({"action": "update_score", 
            "score": 0})

    def Network_update_mods(self, data):
        # Se actualizan los modificadores en el rival
        # Si rival = 0 resetea sus parametros, si es =1 el que lo llama solo ha modificado los propios
        partida = data ['partida']
        
        if data ['jugador'] == 0:
            player = self._server.games[partida].player1['playerid']
        elif data ['jugador'] == 1:
            player = self._server.games[partida].player0['playerid']
        else:
            print "El numero de jugador no es correcto"
            
        # accion = -2 Se ha eliminado la carta que modificaba parametros del rival
        # accion = -1 La carta jugada altera modificadores del rival
        # accion = 0 Se ha eliminado una carta que alteraba modificadores del propio jugador
        # accion = 1 La carta jugada altera modificadores del jugador
        player.Send({"action": "update_mods", 
            "defensa": data['defensa'],
            "ataque": data['ataque'],
            "def_rival": data['def_rival'],
            "ata_rival": data['ata_rival'],
            "accion": data['accion']})
        
    def Network_ask_carta(self, data):
        # Esta funcion se llama para pedir de la MANO DEL CONTRARIO una carta, ya sea
        # o bien para robarla o toda la mano para verlas
        partida = data ['partida']
        
        # Pedimos al jugador contrario (manoX) una de sus cartas y la cogemos.
        if data ['jugador'] == 0:
            mano = self._server.games[partida].mano1
            player = self._server.games[partida].player0['playerid']
            player_rival = self._server.games[partida].player1['playerid']

        elif data ['jugador'] == 1:
            mano = self._server.games[partida].mano0        
            player = self._server.games[partida].player1['playerid']
            player_rival = self._server.games[partida].player0['playerid']
        else:
            print "El numero de jugador no es correcto"

        if data['accion'] == 'ROBO_UNA':
            # Elegimos una carta al azar y la eliminamos de la mano
            card_stolen = random.choice(mano)
            #mano.remove(card_stolen)
            player.Send({"action": "receive_carta", 
                "idcard": card_stolen,
                "contrabandista": data['contrabandista'],
                "captura": data['captura'],
                "accion": data['accion']})
            ## Indicar al rival que elimine esa carta de su mano
            player_rival.Send({"action": "accion_recibida", 
                "idcard": card_stolen,
                "accion": data['accion']})

        elif data['accion'] == 'VER_TODAS':
            player.Send({"action": "receive_carta", 
                "cartas": mano,
                "accion": data['accion']})  
            ## Indicar al rival que ha visto su mano
            player_rival.Send({"action": "accion_recibida", 
                "accion": data['accion']})

    def Network_fin_turno(self, data):
        # Se finaliza el turno de uno de los jugadores
        partida = data['partida']
        if data ['jugador'] == 0:
            # El Jugador 0 es el que finaliza el turno, cambiamos al jugador 1
            self._server.games[partida].player1['playerid'].Send({"action": "turno", "juega": True})
            self._server.games[partida].player0['playerid'].Send({"action": "turno", "juega": False})
        elif data ['jugador'] == 1:
            self._server.games[partida].player0['playerid'].Send({"action": "turno", "juega": True})
            self._server.games[partida].player1['playerid'].Send({"action": "turno", "juega": False})

class MyServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.games = [] ## lista que contiene todos los juegos en curso
        self.queue = None
        self.currentgame=0
        self.activegames=0
        #self.currentplayer =0
        print 'Server launched'
        self.start = False

    def Connected(self, channel, addr):
        print 'new connection:', channel
        if self.queue==None: #Entra jugador 0
            #self.currentIndex+=1
            #channel.gameid=self.currentgame
            self.queue=Game(channel, self.currentgame, '')
            game = self.queue
            jugador = 0
        else: #Entra jugador 1
            #channel.gameid=self.currentgame
            game = self.queue
            jugador = 1
            game.player1['playerid']=channel ## Define jugador 1 en el Game
            game.player0['playerid'].Send({"action": "initgame","player":0, "gameid": game.gameid})
            game.player1['playerid'].Send({"action": "initgame","player":1, "gameid": game.gameid})
            # En alias se envia el del rival
            # Hacemos que el jugador 0 escoja bando
            game.player0['playerid'].Send({"action": "bando", "player": 0})
            
            self.currentgame+= 1
            self.activegames+=1
            self.games.append(game)
            self.queue=None # Maximo dos jugadores por Game
            print "Partida iniciada num: "+str(game.gameid)
            #print "Numero de partidas activas: "+str(self.activegames)
            
        self.AddPlayer(channel,jugador,game.gameid)
        
    def set_bando(self,bando_player0,bando_player1,partida):
        # Set el bando de cada jugador dependiendo de lo que elijiera el Jugador0
        ### ESTO LO VEO UN POCO ARRIESGADO CON MUCHAS PARTIDAS EN JUEGO
        self.games[partida].player0['bando'] = bando_player0
        self.games[partida].player1['bando'] = bando_player1

        self.games[partida].player1['playerid'].Send({"action": "bando", "player": 1, "bando": bando_player1})

    def AddPlayer(self, player, jugador, gameid):
        print "New Player" + str(player.addr)
        #self.players[player] = True
        self.players[player] = (jugador,gameid)
        #self.currentplayer
        #self.currentplayer += 1 ## Asignamos un numero a cada jugador
        
        #self.SendPlayers()
        #print "players", [p for p in self.players]

    def DelPlayer(self, player):
        print "Deleting Player" + str(player.addr)
        try:
            for i in range(len(self.games)):
                if self.players[player][1] == self.games[i].gameid:
                    
                    if self.players[player][0] == 0: ## Se desconecta jugador 0
                        self.games[i].player1['playerid'].Send({"action": "finish", "finish": True})
                    else:
                        self.games[i].player0['playerid'].Send({"action": "finish", "finish": True})
                    
                    print "La partida "+str(self.games[i].gameid)+" ha sido eliminada"
                    #del self.games[i] ## Elimina el juego de memoria
                    self.activegames -= 1

            del self.players[player]
            #print "Numero de partidas activas: "+str(len(self.players))
        except:
            print "Error al eliminar la partida"
            #self.SendPlayers()
        

    def SendPlayers(self):
        print "sendplayer"
        #self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})

    def SendToAll(self, data):
        # Se lo envia a todos los jugadores
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            #sleep(0.0001)
            sleep(0.1)

class Server_intro(Frame):
    # Esta clase abre la ventana para poder meter los valores tipo GUI
    def __init__(self, master=None):
        self.root = Tk()
        self.root.title('CARD GAME')
        self.root.resizable(False,False) # Horizontal y vertical
        self.root.geometry("207x460")
        Frame.__init__(self, master)

        try:
            current_folder = os.path.dirname(os.path.abspath(__file__))
        except NameError:  # We are the main py2exe script, not a module
            import sys
            current_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
            
        images_folder = current_folder+'\images'+'\\'
        sounds_folder = current_folder+'\sounds'+'\\'
        self.root.iconbitmap(images_folder+ICON) # Icono de la intro

        photo = PhotoImage(file=images_folder+INTRO_PHOTO)
        w = Label(self.root, image=photo)
        w.photo = photo
        w.grid(row=0, column=0,columnspan=3, sticky=W+E+N+S, padx=5, pady=5)

        self.lablhost = Label(text="Server").grid(row=1, column=0, padx=5, sticky=W)
        self.lablport = Label(text="Port").grid(row=2, column=0, padx=5, sticky=W)

        # Colocar los text box
        self.host = Entry() ## entry Host
        self.host.grid(row=1, padx=5, column=1,columnspan=2)
        self.port = Entry() ## entry Port
        self.port.grid(row=2, padx=5, column=1,columnspan=2)

        # Colocar los botones
        self.okbutton = Button(self.root, text="OK", command=self.on_button)
        self.okbutton.grid(row=3, column=0, columnspan=2, padx=15, sticky="nsew")
        self.exitbutton = Button(self.root, text="Salir", command=self.salir)
        self.exitbutton.grid(row=3, column=2, padx=15,sticky="nsew")

        self.hostvar = StringVar()
        self.portvar = IntVar()
        # Valores por defecto
        self.hostvar.set("localhost")
        self.portvar.set(7000)
        
        # Poner los valores por defecto
        self.host["textvariable"] = self.hostvar
        self.port["textvariable"] = self.portvar
        
    def on_button(self):
        try:
            print "Server: "+self.hostvar.get()+': '+str(self.portvar.get())
            host = self.hostvar.get()
            port = self.portvar.get()
            if not isUp(host):
                tkMessageBox.showerror("Error","No se alcanza el Host: "+host)
                #print "No se alcanza el Host: "+host
            else:
                self.root.destroy()        
        except:
            ## Mensaje de error en la entrada de parametros
            tkMessageBox.showwarning("Warning","Usage host:port. Ej: localhost:31425")
            #print "Usage host:port. Ej: localhost:31425"
    def salir(self):
        exit()

# COMIENZO DEL SERVIDOR
# Ventana de entrada
#input_values = Server_intro()
#input_values.mainloop()

# Se lanza el server esperando usuarios que se conecten
#s = MyServer(localaddr=(host, int(port)))
#s.Launch()

# get command line argument of server, port
if len(sys.argv) != 2:
   print "Usage:", sys.argv[0], "host:port"
   print "e.g.", sys.argv[0], "localhost:31425"
else:
   host, port = sys.argv[1].split(":")
   s = MyServer(localaddr=(host, int(port)))
   s.Launch()