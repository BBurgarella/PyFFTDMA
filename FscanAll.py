import math
import os
import sys
import csv
import getopt
import numpy as np
import matplotlib.pyplot as plt

###############################################################
#  Définition des listes de fréquence, température et essais  #
###############################################################

C1 = 180
C2 = 900
Tref = 160
ListN = [10]
NbChargements = 5
ListEssais = [10,20]
ListFreq = [0.1, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4,12.8]
ListTemp = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]

print('La liste des N est : '+str(ListN)+'\n')
rep = input('Voulez-vous la changer ?\nTapez "0" pour non et "1" pour oui.\nRéponse : ')

if rep == '1':
    
    ListN = []
    i=1
    while rep == '1':
        
        N = int(input('Terme en position '+str(i-1)+': N'))
        ListN.append(N)
        i+=1
        rep = input('\nVoulez-vous rajouter un terme ?\nRéponse :')
    print('\nLa liste des N est la suivante : '+str(ListN))

print('\nLe nombre de chargements est : '+str(NbChargements)+'\n')

rep = input('Voulez vous le changer ?\nTapez "0" pour non et "1" pour oui.\nRéponse : ')

if rep == '1':
    
    NbChargements = int(input('Veuillez saisir le nombre de chargements :'))
    print("\nLe nombre de chargements choisi est : "+str(NbChargements)+"\n")

print("\nLa liste des essais est :\n"+str(ListEssais)+"\n")
rep = input('Voulez-vous la changer ?\nTapez "0" pour non et "1" pour oui.\nRéponse : ')

if rep == "1":
    
    ListEssais = []
    i=1
    while rep == '1':
        
        essai = int(input("\nEssai "+str(i)+" : "))
        ListEssais.append(essai)
        i+=1
        rep = input('Voulez-vous rajouter un essai ?\nTapez "0" pour non et "1" pour oui.\nRéponse : ')
    print("\nLa liste des essais générée est la suivante : \n"+str(ListEssais))


print("\nLa liste des fréquences est :\n"+str(ListFreq)+"\n")
rep = input('Voulez-vous la changer ?\nTapez "0" pour non et "1" pour oui.\nRéponse : ')

if rep == "1":
    
    Nbmin=float(input("Fréquence minimale : "))
    Nbmax=float(input("Fréquence maximale : "))   
    ListFreq = [Nbmin]
    i=0
    while (2*ListFreq[i] <= Nbmax):
        ListFreq.append(2*ListFreq[i])
        i+=1
    print("\nLa liste de fréquences générée est la suivante : \n"+str(ListFreq))

print("\nLa liste des températures est :\n"+str(ListTemp)+"\n")
rep = input('Voulez-vous la changer ?\nTapez "0" pour non et "1" pour oui.\nRéponse : ')

if rep == "1":  
    Tmin=int(input("Température minimale : "))
    Tmax=int(input("Température maximale : "))
    Pas=int(input("Pas : "))
    ListTemp = [Tmin]
    i=0
    while ListTemp[i]+Pas <= Tmax :
        ListTemp.append(ListTemp[i]+Pas)
        i+=1  
    print("\nLa liste de températures générée est la suivante : \n"+str(ListTemp)+"\n")



####################################################################
#   Traitement en fréquence et en température pour chaque essai    #
####################################################################

for n in range(len(ListN)):
    
    print('N'+str(ListN[n])+'\n')
    
    Str = 'move ShiftCalculatorfftV4.py N'+str(ListN[n])
    os.system(Str)
    os.chdir('N'+str(ListN[n]))
    
    for c in range(NbChargements):
        
        print('\tChargement'+str(c+1))
        
        Str = 'move ShiftCalculatorfftV4.py '+'Chargement'+str(c+1)
        os.system(Str)
        
        os.chdir('Chargement'+str(c+1))

        for k in range(len(ListEssais)):
            
            print('\t\t'+str(ListEssais[k]))
            
            Str = "move ShiftCalculatorfftV4.py "+str(ListEssais[k])
            os.system(Str)
            os.chdir(str(ListEssais[k]))
        
            for j in range(len(ListTemp)):
                
                print('\t\t\t'+str(ListTemp[j]))
                
                Str = "move ShiftCalculatorfftV4.py "+str(ListTemp[j])
                os.system(Str)
                os.chdir(str(ListTemp[j]))
                
                Str = "move ShiftCalculatorfftV4.py "+str(ListFreq[0])
                os.system(Str)
                os.chdir(str(ListFreq[0]))
                
                Str = "python3 ShiftCalculatorfftV4.py"
                os.system(Str)
                
                Str = "move ShiftCalculatorfftV4.py ../"+str(ListFreq[1])
                os.system(Str)
                Str = "move Result.csv ../"+str(ListFreq[1])
                os.system(Str)
                os.chdir("../")
                print('\t\t\t\t'+str(ListFreq[0]))
                
                for i in range(len(ListFreq)-1):
                    os.chdir(str(ListFreq[i+1]))
                    Str = "python3 ShiftCalculatorfftV4.py"
                    os.system(Str)
                    print('\t\t\t\t'+str(ListFreq[i+1]))
                    if i != len(ListFreq)-2:
                        Str = "move ShiftCalculatorfftV4.py ../"+str(ListFreq[i+2])
                        os.system(Str)
                        Str = "move Result.csv ../"+str(ListFreq[i+2])
                        os.system(Str)
                    else:
                        Str = "move ShiftCalculatorfftV4.py .."
                        os.system(Str)
                        Str = "move Result.csv Result"+str(j+1)+".csv"
                        os.system(Str)
                        Str = "move Result"+str(j+1)+".csv ../.."
                        os.system(Str)
                    os.chdir("../")
                Str = "move ShiftCalculatorfftV4.py .."
                os.system(Str)
                os.chdir("../")
                
            Str = "move ShiftCalculatorfftV4.py .."
            os.system(Str)
            os.chdir("../")
        
        Str = 'rm Chargement'+str(c+1)
        os.system(Str)
        Str = "move ShiftCalculatorfftV4.py .."
        os.system(Str)
        os.chdir("../")
    
    Str = "move ShiftCalculatorfftV4.py .."
    os.system(Str)
    os.chdir("../")
        
        
        
    
########################################################
#            Traitement des fichiers .csv              #
########################################################

def aTgen(TempList):
    aT = []
    for i in range(len(TempList)):
        aT.append(float(10**((-float(C1)*(TempList[i]-float(Tref)))/(float(C2)+(TempList[i]-float(Tref))))))
    return aT

aT = aTgen(ListTemp)
    
for n in range(len(ListN)):
    os.chdir('N'+str(ListN[n]))
    for c in range(NbChargements):
        os.chdir('Chargement'+str(c+1))
        for k in range(len(ListEssais)):
            os.chdir(str(ListEssais[k]))
            resultat = open("ResultatFinal.csv","a")
            for i in range(len(ListTemp)):
                file = open("Result"+str(i+1)+".csv","r") 
                for j in range(len(ListFreq)):
                    ligne = file.readline()
                    resultat.write(str(ligne.split(" ")[0])+" "+str(ligne.split(" ")[1])+" "+str(ligne.split(" ")[2])+" "+str(ListFreq[j]*float(aT[i]))+"\n")
            resultat.close()
            os.chdir("../")
        os.chdir("../")
    os.chdir("../")


for n in range(len(ListN)):
    os.chdir('N'+str(ListN[n]))
    for c in range(NbChargements):
        os.chdir('Chargement'+str(c+1))
        for k in range(len(ListEssais)):
            essai = ListEssais[k]
            os.chdir(str(essai))
            Str = "move ResultatFinal.csv ResultatFinal"+str(essai)+'C'+str(c+1)+".csv"
            os.system(Str)
            Str = "move ResultatFinal"+str(essai)+'C'+str(c+1)+".csv .."
            os.system(Str)
            os.chdir("../")
            Str = "move ResultatFinal"+str(essai)+'C'+str(c+1)+".csv .."
            os.system(Str)
        os.chdir("../")
    os.chdir("../")


