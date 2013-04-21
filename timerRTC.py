#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Avril 2013 - Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# librairie personnelle contenant une classe implémentant timer RTC 
from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..

import os,sys

import serial # communication serie
import re # module pour analyse de chaîne avec expressions régulières


class timerRTC: # classe implémentant gestion timer temps réel
  	
	def __init__(self): # constructeur principal de la classe 
		#self.data = []
		self.etat=False  # variable d'état du timer - true/false actif/inactif
		self.interval=0 # variable intervalle entre 2 événements en secondes 
		self.maxCompt=0 # variable nombre événements max 
		self.compt=0 # variable nombre événements survenus depuis début comptage
		self.debut=0 # variable unixtime de debut
		self.last=0 # variable unixtime dernier événement
  
		# les différents attributs sont accessibles avec nomobjet.etat, etc... 

	# ---- initialisation Timer avec intervalle et limite ------ 
	def start(self,intervalIn, maxComptIn=None):
		self.interval=intervalIn # intervalle entre 2 événements EN SECONDES !!
		
		if maxComptIn==None:self.maxCompt=0 # nombre d'évènements infinis
		else: self.maxCompt=maxComptIn # nombre d'évènements voulus - durée = (n-1) x delai
		
		self.compt=0 # initialise comptage au démarrage
		self.etat=True # active le timer

	# ----- stoppe le timer sans modifier les paramètres actuels --- 
	def stop(self):
		self.etat=False # désactive le Timer sans modifier les paramètres courants

	# ----- stoppe le timer sans modifier les paramètres actuels --- 
	def restart(self):
		self.etat=True # ré-active le Timer sans modifier les paramètres courants

	#---- info timer ---------
	def status(self, indexIn=None): # la fonction renvoie un String correspondant aux infos sur le Timer RTC
		
		if indexIn==None: strOut="Infos Timer : " # chaîne 
		else: strOut="Infos Timer "+str(indexIn)+" : "
		
		if self.etat==True: strOut=strOut+"Timer actif"+" | "
		else: strOut=strOut+"Timer inactif"+" | "
		
		strOut=strOut+"intervalle="+str(self.interval)+" | "
		strOut=strOut+"limite comptage="+str(self.maxCompt)+" | "
		strOut=strOut+"comptage actuel="+str(self.compt)+" | "
		strOut=strOut+"debut="+str(self.debut)+" | "
		strOut=strOut+"dernier="+str(self.last)+" | "
		
		return(strOut) # renvoie chaine

	# ------ routine de gestion du timer ---- à appeler à partir timer intervalle régulier
	def service(self, unixtimeIn, userFuncIn, indexIn):
		
		if self.etat==True: # si le timer est actif
			if self.compt==0: # si premier passage  
				self.debut=unixtimeIn # mémorise début
				self.last=unixtimeIn # initialise last
				self.compt=1 # incrémente compteur
          
				userFuncIn(indexIn) # appelle la fonction passée en pointeur avec l'argument voulu 
			
			# fin si premier passage
		
			else: # si compt >=1 = passages suivants
				
				if unixtimeIn-self.last>=self.interval: # si l'intervalle du timer s'est écoulé
					
					print(" Intervalle timer "+str(indexIn) + " écoulé.");
					
					self.compt=self.compt+1 # incrémente compteur
					self.last=unixtimeIn # RAZ last          
					
					userFuncIn(indexIn) # appelle la fonction passée en pointeur avec l'argument voulu 
					
					if self.maxCompt!=0 and self.compt>=self.maxCompt:
						print(">>>>>>>>>>>>>>>>>< Desactivation timer <<<<<<<<<<<<<<<<")
						self.etat=0 # stoppe le timer si nombre max atteint et si pas infini (timer[maxCompt]!=0)
					#fin si comptMax atteint
           
				# fin if intervalle écoulé
            
			# fin else compt>=1
      
		# fin si timer ON 
	
	# fin service()		
	
