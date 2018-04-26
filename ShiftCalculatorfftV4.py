# -*- coding: utf-8 -*-
import math
import os
import sys
import csv
import getopt
import numpy as np
import matplotlib.pyplot as plt


CraFT = True
Verbose = False
nbT = 5
Sampling = 25
file = open("InstructionFreQ.txt","r")
f = float(file.readline())
#Sampling = float(file.readline())
file.close()
NumCharg = 1

## Matrice Pure ##
VC1 = [0,0,0,1,0,1]

## Cisaillement ##
# VC1 = [0,0,0,1,0,1]
VC2 = [0,0,0,0,1,0]

## Incompressible ##

VI3 = [-0.5,1,-0.5,0,0,0]

##  Sphérique  ##

VS4 = [1,1,1,0,0,0]

V41 = [1,0,1,0,0,0]
V42 = [0,1,0,0,0,0]

## Cas incompressible ##
#VI1 = [-0.5,-0.5,1,0,0,0]
#VI2 = [0.5,-0.5,0,0,0,1]
#VI3 = [0,0,0,1,1,0]
#Incompressible = [VI1,VI2,VI3]

## Cas Compressible ##
#V1 = [0,0,0,1,1,0]
#V2 = [0,0,0,0,0,1]
#V31 = [-0.5,-0.5,0,0,0,0]
#V32 = [0,0,1,0,0,0]
#V4 = [-0.5,-0.5,0,0,0,0]
#V51 = [1,1,0,0,0,0]
#V52 = [0,0,1,0,0,0]
#Compressible = [V1,V2,V31,V4]


path0 = os.path.dirname(os.path.realpath(__file__))
path1 = os.path.dirname(path0)
path2 = os.path.dirname(path1)
path3 = os.path.dirname(path2)
path0 = os.path.basename(path0)
print(path0)
path1 = os.path.basename(path1)
print(path1)
path2 = os.path.basename(path2)
print(path2)
path3 = os.path.basename(path3)
print(path3)

if path0 == "Chargement0" or path1 == "Chargement0" or path2 == "Chargement0" or path3 == "Chargement0":
    VCharg =  VC0
if path0 == "Chargement1" or path1 == "Chargement1" or path2 == "Chargement1" or path3 == "Chargement1":
    VCharg =  VC1
elif path0 == "Chargement2" or path1 == "Chargement2" or path2 == "Chargement2" or path3 == "Chargement2":
    VCharg =  VC2
elif path0 == "Chargement3" or path1 == "Chargement3" or path2 == "Chargement3" or path3 == "Chargement3":
    VCharg =  VI3
elif path0 == "Chargement4" or path1 == "Chargement4" or path2 == "Chargement4" or path3 == "Chargement4":
    VCharg =  V41
elif path0 == "Chargement5" or path1 == "Chargement5" or path2 == "Chargement5" or path3 == "Chargement5":
    VCharg =  V42
    
    
def searchmax(list):
    max = 0
    imax = 0
    for i in range(len(list)):
        if list[i] > max:
            max = list[i]
            print(max)
            imax = i
            print(imax)
    return imax
   
def Scalaire(A,B):
    Somme = 0
    if len(A)==len(B):
        for i in range(len(A)):
            Somme += A[i]*B[i]
    else:
        print("Erreur: A et B ne font pas la même dimension, return 0")
    return Somme

    
def ProdScalVect(Scal,B):
    ReturnVect = []
    for i in range(len(B)):
        ReturnVect.append(B[i]*Scal)
    return ReturnVect  
  
def projection(A,B):
    return ProdScalVect((Scalaire(A,B)/Scalaire(B,B)),B)
    
if CraFT == False:
    with open('data.csv', 'rb') as f:
        reader = csv.reader(f)
        raw_data = list(reader)
    data = []

    for i in raw_data:
        data.append(float(i[0]))

    with open('data2.csv', 'rb') as f:
        reader = csv.reader(f)
        raw_data = list(reader)
    data2 = []
    for i in raw_data:
        data2.append(float(i[0]))
    
############# Comparaison CraFT ####################
if CraFT == True:
    NameFile = "MicroStruct.res"
    FEntry = open(NameFile)
    TableSigma = []
    TableEpsilon = []
    TableTime = []
    CurrentLine = FEntry.readline()

    while len(CurrentLine) > 0:
        if CurrentLine[0] != '#':
            CurrentlineList = CurrentLine.split()
            if len(CurrentlineList) > 0:
                TableEpsilon.append(Scalaire([float(CurrentlineList[5]),float(CurrentlineList[6]),float(CurrentlineList[7]),float(CurrentlineList[8]),float(CurrentlineList[9]),float(CurrentlineList[10])],VCharg))
                TableSigma.append(Scalaire([float(CurrentlineList[11]),float(CurrentlineList[12]),float(CurrentlineList[13]),float(CurrentlineList[14]),float(CurrentlineList[15]),float(CurrentlineList[16])],VCharg))
                TableTime.append(float(CurrentlineList[0]))
        CurrentLine = FEntry.readline()
    FEntry.close()
    print(VCharg)
    print(TableEpsilon)
    Resultats = [[],[],[]]
    Non0Values = []
    data = []
    data2 = []

    for i in range(len(TableTime)):
        Resultats[0].append(TableTime[i])
        Resultats[1].append(TableEpsilon[i])
        Resultats[2].append(TableSigma[i])
    lenght = len(TableTime)    
    debutTraitement = int(lenght-((nbT)*Sampling))
    finTraitement = lenght 
    #data = Resultats[2]
    #data2 = Resultats[1]
    data = Resultats[2][debutTraitement:finTraitement]
    data2 = Resultats[1][debutTraitement:finTraitement]
################ Comparaison CraFT ###########################
fourier = [0,0,0,0,0,0]
print(len(Non0Values))  
fourier = np.fft.fft(data)/np.fft.fft(data2)

if Verbose:
    plt.plot(data)
    plt.plot(data2)
    plt.show()
    
if CraFT == True:
    f = 10*f


    

plt.plot(np.absolute(np.fft.fft(data)))
if Verbose == True:
    plt.show()
nbT = searchmax(np.absolute(np.fft.fft(data)))
print("max = "+str(nbT))
Sigma0 = max(data)
Eps0 = max(data2)
phi =abs(np.angle(fourier[nbT],deg = True))
Ep = abs((Sigma0/(Eps0))*math.cos(np.angle(fourier[nbT])))
Es = abs((Sigma0/(Eps0))*math.sin(np.angle(fourier[nbT])))
file = open("Result.csv","a")
if CraFT == True:
    file.write(str(phi)+" "+str(Ep)+" "+str(Es)+" "+str(f/10)+"\n")
else:
    file.write(str(phi)+" "+str(Ep)+" "+str(Es)+" "+str(f)+"\n")
file.close()


