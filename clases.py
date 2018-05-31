import pygame
import globals
import random

class Button_scr:
	hovered = False

	def __init__(self,screen,image0,image1,pos):
		self.image0 = pygame.transform.scale(image0,(80,50))
		self.image1 = pygame.transform.scale(image1,(80,50))
		self.pos = pos
		self.screen = screen
		self.set_rect()
		self.draw()

	def draw(self):
		self.screen.blit(self.image1 if self.hovered else self.image0,self.pos)

	def set_rect(self):
		if self.hovered:
			self.rect = self.image1.get_rect()
		else:
			self.rect = self.image0.get_rect()
		self.rect.topleft = self.pos         		
				
class Text_scr:
	hovered = False

	def __init__(self,screen,text,pos,font,flash,color):
		self.text = text
		self.pos = pos
		self.font = font
		self.screen = screen
		self.flash = flash # Indica si es un texto flash
		self.color = color ## Define el color del texto inicialmente
		self.set_rect()
		self.draw()
		
	def draw(self):
		self.set_rend()
		self.screen.blit(self.rend,self.rect)

	def set_rend(self):
		self.rend = self.font.render(self.text,True,self.get_color())
			
	def get_color(self):
		if not self.flash:
			return self.color

		if self.hovered:
			#return (255,255,255)
			return self.color
		else:
			return (0,0,0) ## Es el color del texto ACTIVO
			
	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos                    
				   
class Card_scr:
	def __init__(self,screen,carta,pos):
		self.carta = carta
		self.pos = pos
		img =  pygame.image.load(globals.images_folder+carta.image)
		self.obj = pygame.transform.rotozoom(img,0,0.3) ## Carta normal
		self.objh = pygame.transform.rotozoom(img,0,0.265) ## Carta hangar
		self.objz = pygame.transform.rotozoom(img,0,0.8) ## Carta zoom
		self.objzt = pygame.transform.rotozoom(img,0,0.7) ## Carta zoom tripulante de nave
		self.screen = screen
		self.lock = False
		self.set_rect()
		self.draw()

	def draw(self):
		self.screen.blit(self.obj,self.pos)
	def draw_h(self):
		self.screen.blit(self.objh,self.pos) ## Carta en hangar
	def draw_t(self,pos):
		self.screen.blit(self.objzt,pos) ## Carta zoom de tripulacion
	def effect(self):
		i = 0
		while True:
			self.obj.set_alpha(i)
			self.screen.blit(self.obj,self.pos)
			pygame.time.delay(100)
			if i == 32:
				break
			i +=1
	def zoom(self):
		self.screen.blit(self.objz,(650,200))
	def zoom_v2(self):
		self.screen.blit(self.objz,(150,200))
	def set_rect(self):
		self.rect = self.obj.get_rect()
		self.rect.topleft = self.pos                    

class Frame_scr:
	def __init__(self,screen,image,pos,tipo,bando):
#		self.image = image
		self.pos = pos
		self.bando = bando
		self.obj = image
		self.screen = screen
		self.tipo = tipo
		self.set_rect()
		#self.draw()

	def draw(self):
		self.screen.blit(self.obj,self.pos)

	def set_rect(self):
		self.rect = self.obj.get_rect()
		self.rect.topleft = self.pos         

class Carta:
	def __init__(self,cardid,image,tipo,bando,nombre,nactions,valor):
		self.id = cardid
		self.image = image
		self.tipo = tipo ## Tipo de carta
		self.bando = bando ## Bando 'R' rebeldes o 'I' imperio
		self.nombre = nombre ## Nombre o descripcion
		self.jugada = False ## Indica si se ha jugado
		self.nactions = nactions ## Num de acciones que puede realizar esta carta
		self.valor = valor ## Indica el valor de la carta para evaluar quien gana la partida
		self.modificador = False ## Indica si esta carta modifica parametros globales de defensa o ataque

	def setup(self,ata,defensa,evasion):
		self.ata = ata
		self.defensa = defensa
		self.evasion = evasion # Indica el indice de evasion ante un ataque % de probabilidad de librarse del mismo

class Tropa(Carta):
	tripulante = False
	def set_tripulante(self,nave_ataque,nave_defensa,nave_evasion,dirige,reataque):
		self.tripulante = True # Me dice si puede llegar a ser tripulante de una nave
		self.en_nave = False ## Me dice si esta de tripulante en una nave. Por defecto no
		self.dirige = dirige # Indica si puede dirigir una nave
		self.nave_ata = nave_ataque ## Poder de ataque que aplica a una nave
		self.nave_def = nave_defensa ## Poder de defensa que aplica a una nave
		self.nave_evasion = nave_evasion ## Poder de evasion que aplica a una nave
		self.reataque = reataque ## Indica si cuando se posiciona aplica un poder adicional de ataque de la nave

	def set_terrain(self,defensa, ataque):
		# Esta funcion fija los modificadores de terreno de una carta a las tropas
		self.modificador = True
		self.terrain_def = defensa
		self.terrain_ata = ataque

	def modify_param_terrain(self,defensa,ataque):
		# Aplica los valores de terreno de la carta
		defensa += self.terrain_def
		ataque += self.terrain_ata

		return defensa, ataque

	def modify_param_nave(self,card):
		# Aplica valores a la nave donde se posicione
		card.carta.defensa += self.nave_def
		card.carta.ata += self.nave_ata
		card.carta.evasion += self.nave_evasion

		return card

class Nave(Carta):
	def set_param_nave(self,tripulacion_max,max_dirige):
		self.tripulacion_max = tripulacion_max ## Tripulacion  maxima de la nave
		self.tripulacion = 0 # Numero de tripulantes actuales
		self.max_dirige = max_dirige ## Maximo numero de dirigentes
		self.dirigentes = 0 ## Num de dirigentes actuales en la nave