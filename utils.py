#!/usr/bin/python
# -*- coding: utf-8 -*-

# par X. HINAULT - Avril 2013 - Tous droits réservés
# GPLv3 - www.mon-club-elec.fr

# librairie personnelle contenant des fonctions python utiles
from PyQt4.QtGui import *
from PyQt4.QtCore import *  # inclut QTimer..

import os,sys

import serial # communication serie
import re # module pour analyse de chaîne avec expressions régulières


  #========== analyse de chaine ========================= 
	
#---- test instruction string ------ 
def testInstructionString (chaineRefIn,chaineTestIn, debugIn):
	# Les paramètres reçus par la fonction sont :
	# chaineTestIn : chaîne à trouver
	# chaineRefIn : chaine entière à tester
	# debugIn : flag pour message de débug
	
	# cast paramètres reçus 
	str(chaineTestIn)
	str(chaineRefIn)
	bool(debugIn)
	
	if (debugIn): print(chaineTestIn)
	if (debugIn): print(chaineRefIn)
	if (debugIn): print(debugIn)
	
	posRef=len(chaineTestIn)# position de référence pour analyse (xxx) 
	if (debugIn): print("posRef= "+str(posRef))
	
	paramString=None # le String reste "none" tant que pas initialisé par =""

	if (debugIn): print(chaineRefIn[0:posRef]) 

	if chaineRefIn[0:posRef]==chaineTestIn : # si reçoit l'instruction chaineTest(
 
		if (debugIn): print("Racine reconnue : "+str(chaineTestIn)) 

		paramString=chaineRefIn[posRef:len(chaineRefIn)-1] # extrait la chaine de caractere recue en parametre 
		if (debugIn): print(paramString) # affiche la chaine de caractere
 
		if chaineRefIn[len(chaineRefIn)-1:len(chaineRefIn)]==")" : # si fermeture parenthèse = instruction valide
		
			if (debugIn) : print(")") # affiche
			if (debugIn) : print("Instruction valide !") # affiche
			return(paramString) # renvoie true si instruction valide 
	
		#fin si fermeture parenthèse
	
		else: # si parenthese absente 
		
			if (debugIn) : print("Instruction invalide !") # affiche
			return(0) # renvoie null 
				
		# fin else
	
	# fin si recoit chaineTest(
	
	else : # si pas bonne chaine Test présente
		
		if (debugIn) : print(".") # affiche
		return(0) # renvoie null si instruction invalide
	  
	# fin else 

#-- fin testInstructionString

#--------------- testInstructionLong : test si instruction de la forme instruction(xxx, xxx, xxx, xxx, xxx) ou moins ------------
def testInstructionLong(chaineIn, chaineRacineIn, debugIn): # fonction reçoit chaine à analyser et la racine à utiliser - reconnaît fonction racine(**,**, ..,**)
	# le nombre de paramètres attendus... sera analysé secondairement
	
	args=None # valeur par défaut de args 
	flagRacine=False # drapeau racine OK 
	
	chaineRacineIn=chaineRacineIn[:-1] # enlève la parenthèse à la racine reçue
	
	#self.textEditTraceAnalyseChaine.setText(QString.fromUtf8("Chaine à analyser : " + chaineIn)) # trace analyse chaine
	if debugIn: print("Chaine à analyser : " + chaineIn)

	#result=re.findall(r'^.*\((.*)\).*$',chaineIn) # extrait ** de la chaine au format --(**) si la chaîne est au format valide  
	result=re.findall(r'^.*\((.*)\)$',chaineIn) # extrait ** de la chaine au format --(**) si la chaîne est au format valide  
	#self.textEditTraceAnalyseChaine.append(str(len(result)) + QString.fromUtf8(" chaine valide")) # trace analyse chaine 
	if debugIn: print(str(len(result)) + " chaine valide")

	#racine=re.findall(r'^(.*)\(.*\).*$',chaineIn) # extrait ** de la chaine au format **(--) si la chaîne est au format valide  
	#racine=re.findall(r'^(.*)\(.*\)',chaineIn) # extrait ** de la chaine au format **(--) si la chaîne est au format valide  
	racine=re.findall(r'^(.*)\(.*\)',chaineIn) # extrait ** de la chaine au format **--) si la chaîne est au format valide  
	#self.textEditTraceAnalyseChaine.append(str(len(racine)) + QString.fromUtf8(" racine valide")) # trace analyse chaine 
	if debugIn: print(str(len(racine)) + " racine valide")
	
	
	#-- analyse racine --		
	if len(racine)==1:
		#self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Racine reçue : ")+ racine[0]) # trace analyse chaine 
		if debugIn: print("Racine reçue : "+ racine[0])
					
		if racine[0] == str(chaineRacineIn): 
			#self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Racine reçue conforme"))# trace analyse chaine 
			if debugIn: print("Racine reçue conforme")
			flagRacine=True # flag racine OK
		else:
			#self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Racine reçue non conforme"))# trace analyse chaine 
			if debugIn: print("Racine reçue non conforme")
		# fin else

	# fin if
					
	if len(result)==1 and flagRacine: # si une seule chaine valide détectée et que la racine OK 
		#self.textEditTraceAnalyseChaine.append(QString.fromUtf8(result[0])) # trace analyse chaine : affiche la chaine des arguments
		#self.textEditTraceAnalyseChaine.append(QString.fromUtf8("Paramètres reçus :")) # trace analyse chaine : affiche la chaine des arguments
		if debugIn: print("Paramètres reçus :")
		args=result[0].split(',') # récupère la liste des arguments séparés par une parenthèse
		#self.textEditTraceAnalyseChaine.append(QString.fromUtf8(str(args))) # trace analyse chaine : affiche la liste des arguments
		if debugIn: print(str(args))
		
		# boucle sans l'indice
		#for valeur in args: # défile les arguments de la liste
			#self.textEditTraceAnalyseChaine.append(QString.fromUtf8(str(valeur))) # trace analyse chaine : affiche la liste des arguments
		
		print len(args) # debug
		print args
		
		# boucle avec indice
		if len(args): # si il y a au moins 1 argument numérique... 
			for i in range(0,len(args)): # défile indice args - attention range c'est valeur de départ, nombre de valeur donc range(0,3) défile de 0 à 2 !
				if str(args[i]).isalnum():
					valeur=int(args[i])
					#self.textEditTraceAnalyseChaine.append(QString.fromUtf8(str(valeur))) # trace analyse chaine : affiche la liste des valeurs int des arguments 
					if debugIn: print(str(valeur))
				else:args=None # si l'un des éléments n'est pas numérique - repasse args à None 
				
			
		
	
	return args # renvoie la liste des arguments - None si pas d'arguments
	
	# pour tester en Terminal Python 
	# analyse de la chaine 
		#chaine="CAN(123,122,121)"
		# result=re.findall(r'^.*\((.*)\)',chaine) # extrait --(**)
		# result=re.findall(r'^.*\((.*,.*,.*)\)',chaine) # extrait --(*,*,*) = 3 paramètres 
		# sub=result[0].split(',') 
		# print sub
		# => 123, 122, 121
		# print len(sub)
		# => 3
		# print int(sub[0])
		# => 123

	
	
#--------- fonctions pour les fichiers -------------
def getContentDir(pathIn):
	
	QString.fromUtf8(pathIn) # chemin reçu 
		
	#-- ouverture du répertoire et récupération du contenu - fonctions PyQt
	myDir=QDir(pathIn) # définit objet répertoire
	filesList=myDir.entryList() # liste des entrées... = liste du contenu 
	#filesList=myDir.entryList(["*.*"], QDir.Files, QDir.Name) # liste des entrées... avec filtres 
	#filesList=myDir.entryList(["*.txt"], QDir.Files, QDir.Name) # liste des entrées... avec filtres 
	# ici que les fichier triés par nom - filtre *.txt
	
	# QStringList QDir.entryList (self, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
	# QStringList QDir.entryList (self, QStringList nameFilters, Filters filters = QDir.NoFilter, SortFlags sort = QDir.NoSort)
	
	# les filtres possibles http://pyqt.sourceforge.net/Docs/PyQt4/qdir.html#Filter-enum
	# classement possibles : http://pyqt.sourceforge.net/Docs/PyQt4/qdir.html#SortFlag-enum
	
	contentOut="" # chaine de contenu
			
	for fileName in filesList: # défile les noms des fichiers..
		print fileName +"\t"+str(QFileInfo(pathIn+"/"+fileName).size())+"\t Octets " # affiche le fichier + tab + taille
		contentOut=contentOut+fileName+"\t"+str(QFileInfo(pathIn+"/"+fileName).size())+"\t Octets \n" # ajoute ligne saut de ligne 

	#self.textEdit.setText("") # efface le champ texte 	
	return(contentOut) # renvoie la chaîne de contenu
	
def writeFile(absoluteFilenameIn, strIn):		
	
	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 
	strIn=str(strIn) # chaine à écrire
	
	if not os.path.isfile(absoluteFilenameIn): return("Echec : Le fichier n'existe pas!") # si le fichier n'existe pas

	myFile = open(absoluteFilenameIn, 'a') # ouverture du fichier en mode écriture append
	#myFile = open(absoluteFilenameIn, 'w') # ouverture du fichier en mode écriture write - efface contenu existant
	# open est une fonction du langage python : http://docs.python.org/2/library/functions.html#open
	# mode peut-être r, w, a (append)		
	myFile.write(strIn) # écrit les données dans le fichier		
	myFile.close() # ferme le fichier 

	return("Ecriture fichier OK"); 
	
def readFile(absoluteFilenameIn):

	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 
	
	#-- ouverture du fichier Ui et récupération du contenu 
	myFile=open(absoluteFilenameIn,"r") # ouvre le fichier en lecture
	myFileContent=myFile.read() # lit le contenu du fichier
	myFile.close() # ferme le fichier - tant que le fichier reste ouvert, il est inacessible à d'autres ressources
	
	#self.textEdit.setText(myFileContent) # copie le contenu dans la zone texte 
	return(myFileContent)
	
def getNumberOfLines(absoluteFilenameIn):

	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 
	
	myFileContent=readFile(absoluteFilenameIn) # récupère le contenu du fichier
	#print myFileContent # debug
	
	lines=myFileContent.count("\n") +1 # comptage du nombre de saut de ligne + 1 et donc de lignes.. !
	# +1 car la ligne courante est une ligne même si pas de saut de ligne..
	print ("Nombre de lignes =" + str(lines))
	
	return(lines)

def getLine(absoluteFilenameIn, lineNumberIn):

	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 
	lineNumberIn=int(lineNumberIn) # numéro de ligne à extraire
	
	myFileContent=readFile(absoluteFilenameIn) # récupère le contenu du fichier
	#print myFileContent # debug
	
	allLines=myFileContent.splitlines() # extrait toutes les lignes
	print(len(allLines))
	print(allLines)
	
	if lineNumberIn<=len(allLines): # si ligne demandée cohérente... 
		line=str(allLines[lineNumberIn-1]) # extrait la ligne voulue - la ligne 1 a l'index 0 
		print ("Ligne à extraire" + line)
		return(line)
	else:
		return("Depassement nombre lignes"); 

def createFile(absoluteFilenameIn):		
	
	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 

	if os.path.isfile(absoluteFilenameIn): return("Echec : Le fichier existe !") # si le fichier existe 

	#self.myFile = open(self.filename, 'a') # ouverture du fichier en mode écriture append
	myFile = open(absoluteFilenameIn, 'w') # ouverture du fichier en mode écriture write - efface contenu existant
	# open est une fonction du langage python : http://docs.python.org/2/library/functions.html#open
	# mode peut-être r, w, a (append)		
	myFile.write("") # écrit les données dans le fichier		
	myFile.close() # ferme le fichier 

	return("Creation fichier OK"); 

def removeFile(absoluteFilenameIn):		
	
	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 

	if not os.path.isfile(absoluteFilenameIn): return("Echec : Le fichier n'existe pas!") # si le fichier existe 
	else : 
		os.remove(absoluteFilenameIn)
		return("Effacement fichier OK !")
		
def sizeFile(absoluteFilenameIn):		
	
	absoluteFilenameIn=str(absoluteFilenameIn) # chemin reçu 

	if not os.path.isfile(absoluteFilenameIn): return("Echec : Le fichier n'existe pas!") # si le fichier existe 
	else : 
		#size=long(os.path.getsize(absoluteFilenameIn))
		size=QFileInfo(absoluteFilenameIn).size() # idem avec fonctions PyQt
		return(size)
