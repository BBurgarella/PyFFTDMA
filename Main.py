# -*- coding: utf-8 -*-

import os
import math
import numpy as np
import sys
import getopt
import subprocess

##########################################
#          Définitions des classes       #
##########################################

class VER:
    """ un VER est défini par trois variables physiques, et une informatique:
            - Vf, Taux de fibre
            - NbF, Nombre de fibres
            - N, coefficient de dispertion d'orientation
            - Ratio d'allongement des fibres
            ||||||||||||||||||||||||||||||||||||||||||||
            - Résolution du VER (Pixel cube)
            - Générateur de process aléatoire """
            
    def __init__(self,Vf,NbF,N,Elong,Resolution,RandomSeed):
        self.Vf = Vf
        self.NbF = NbF
        self.N = N
        self.Elong = Elong
        self.Resolution = Resolution
        self.RandomSeed = RandomSeed
        
    def GenerateVER(self):
        command = "./bin/whiskers -n "+str(self.NbF)+" -e "+str(self.Elong)+" -f "+str(self.Vf)+" -s "
        command = command+str(self.RandomSeed)+" -o VERTEST.txt -T "+str(self.Resolution)
        command = command+"x"+str(self.Resolution)+"x"+str(self.Resolution)+" -x "+str(self.N)+" -y "+str(self.N)
        os.system(command)
        command = "./bin/place_whiskers -x VERTEST.txt -o VER_"+str(self.Vf)+"_"+str(self.N)+" -n "+str(self.Resolution)
        command = command+"x"+str(self.Resolution)+"x"+str(self.Resolution)+" -T "+str(self.Resolution)+"x"+str(self.Resolution)+"x"+str(self.Resolution)
        os.system(command)
        command = "./bin/i3dtovtk VER_"+str(self.Vf)+"_"+str(self.N)
        os.system(command)
    
        
class mat402:
    """ reprise du code du matériaux 403 pour l'adapter au 402"""

    def __init__(self,Mu,Eta,CoefPowerLaw,PoissonMatrix,C1C2,ThermalExp,Tg,T0,matfilename):
        self.Mu = Mu
        self.Eta = Eta
        self.CoefPowerLaw = CoefPowerLaw
        self.PoissonMatrix = PoissonMatrix
        self.C1C2 = C1C2
        self.ThermalExp = ThermalExp
        self.Tg = Tg
        self.T0 = T0
        self.matfilename = matfilename
        
    def GenerateMatFile(self,MatNumber,Temp):
        """ fonction générant le fichier .mat pour CraFT, il suffit de donner le nom du fichier
        et cette fonction crée le fichier mat 403 correspondant le numéro identifiant le materiau dans 
        craft sera "MatNumber" """
        FileName = self.matfilename
	aT = float(10**((-float(C1C2[0])*(Temp-float(C1C2[2])))/(float(C1C2[1])+Temp-float(C1C2[2]))))
        file = open(FileName,"w+")
        file.write("#This file was automatically generated \n#thanks to a python script developped by Boris Burgarella, this material is loaded at a temperature of:\n# "+str(Temp)+" degrees C\n")
        file.write("#------------------------------------------\n"+"#aT = "+str(aT)+"\n"+"#-------------------------------------\n")
        file.write("# Mat. #"+str(MatNumber)+" is a power law Elastic Visco-Plastic material\n")
        file.write(str(MatNumber)+" 402 \n")
        file.write("# Shear Modulus\n")
        file.write(str(Mu)+"\n")
        file.write("# Poisson Coefficient\n#T nu\n")
        file.write(str(self.PoissonMatrix[0][0])+" "+str(self.PoissonMatrix[0][1])+"\n"+str(self.PoissonMatrix[1][0])+" "+str(self.PoissonMatrix[1][1])+"\n")
        file.write("#------------------------------------------\n")  
        file.write("# parameters for the yield stress:\n")
        file.write(str(C1C2[0])+" "+str(C1C2[1])+"\n")
        file.write("# Reference Temperature\n")
        file.write(str(Temp)+"\n")
        file.write("# Exponent of the power law\n")
        file.write(str(CoefPowerLaw)+"\n")
        file.write("# Eigen frequency\n")
        file.write(str(float(Mu)/((float(Eta))*aT))+"\n")
        file.write("#---------------------------------------------------------\n")
        file.write("# parameters of the thermal expansion\n")
        file.write("# alpha1\n")
        file.write(str(self.ThermalExp[0])+"\n")
        file.write("# alpha2\n")
        file.write(str(self.ThermalExp[1])+"\n")
        file.write("# Tg\n")
        file.write(str(self.Tg)+"\n")
        file.write("# T0\n")
        file.write(str(self.T0)+"\n")
        file.write("#------------------------------------------------------------------\n# Mat. #1 est la Fibre\n1 10\n# isotrope\n1\n# young\n70000\n# Poisson\n0.22\n#-------------------------------------------------------------------")
        file.close()
        
        
class mat403:
    """ un materiau est défini par N branches, pour lesquelles, on abs  
        N Modules de cisaillement --> Liste à N termes
        N modules de viscosité ---> Liste à N termes
        N Coefficients de loi puissance --> Liste à N termes
        la valeur du coefficient de poisson à deux températures différentes (extrapolation linéaire)
        ---> Matrice    [[T1,nu1]
                        [T2,nu2]]
        un couple C1 C2 pour la loi WLF + température de référence --> Liste [C1,C2,Tref]
        les deux coefficients d'expension thermique [alpha1,alpha2]
        Tg (transition vitreuse ?)
        T0 (Température de départ de l'essai ?)"""

    def __init__(self,MuList,EtaList,CoefPowerLawList,PoissonMatrix,C1C2,ThermalExp,Tg,T0,matfilename):
        self.MuList = MuList
        self.EtaList = EtaList
        self.CoefPowerLawList = CoefPowerLawList
        self.PoissonMatrix = PoissonMatrix
        self.C1C2 = C1C2
        self.ThermalExp = ThermalExp
        self.Tg = Tg
        self.T0 = T0
        self.matfilename = matfilename
        
    def GenerateMatFile(self,MatNumber,Temp):
        """ fonction générant le fichier .mat pour CraFT, il suffit de donner le nom du fichier
        et cette fonction crée le fichier mat 403 correspondant le numéro identifiant le materiau dans 
        craft sera "MatNumber" """
        FileName = self.matfilename
        aT = 10**((-C1C2[0]*(Temp-C1C2[2]))/(C1C2[1]+Temp-C1C2[2]))
        file = open(FileName,"w+")
        file.write("#This file was automatically generated \n#thanks to a python script developped by Boris Burgarella, this material is loaded at a temperature of:\n# "+str(Temp)+" degrees C\n")
        file.write("#------------------------------------------\n")
        file.write("# Mat. #"+str(MatNumber)+" is a power law Elastic Visco-Plastic material\n")
        file.write(str(MatNumber)+" 403 \n")
        file.write("# Nombre de branches\n")
        file.write(str(len(self.MuList))+"\n")
        file.write("# Shear Modulus(i)\n")
        for i in self.MuList:
            file.write(str(i)+"\n")
        file.write("# Poisson Coefficient\n#T nu\n")
        file.write(str(self.PoissonMatrix[0][0])+" "+str(self.PoissonMatrix[0][1])+"\n"+str(self.PoissonMatrix[1][0])+" "+str(self.PoissonMatrix[1][1])+"\n")
        file.write("#------------------------------------------\n")  
        file.write("# parameters for the yield stress:\n")
        file.write(str(C1C2[0])+" "+str(C1C2[1])+"\n")
        file.write("# Reference Temperature\n")
        file.write(str(Temp)+"\n")
        file.write("# Exponent of the power law\n")
        for i in self.CoefPowerLawList:
            file.write(str(i)+"\n")
        file.write("# Eigen frequencies of each branch\n")
        for i in range(len(self.MuList)):
            file.write(str(float(self.MuList[i])/((float(self.EtaList[i]))*aT))+"\n")
        file.write("#---------------------------------------------------------\n")
        file.write("# parameters of the thermal expansion\n")
        file.write("# alpha1\n")
        file.write(str(self.ThermalExp[0])+"\n")
        file.write("# alpha2\n")
        file.write(str(self.ThermalExp[1])+"\n")
        file.write("# Tg\n")
        file.write(str(self.Tg)+"\n")
        file.write("# T0\n")
        file.write(str(self.T0)+"\n")
        file.write("#------------------------------------------------------------------\n# Mat. #1 est la Fibre\n1 10\n# isotrope\n1\n# young\n70000\n# Poisson\n0.22\n#-------------------------------------------------------------------")
        file.close()
        
class Load:
    def __init__(self):
        self.Type = ''
        self.ModelID = 0
        self.Factor = 0
        self.Direction = [0,0,0,0,0,0]
        self.dt = 0
        self.Tmax = 0
        self.omega = 1
     
    def getLoad(self,Filename):
        File = open(Filename,'r')
        SortieText = File.readlines()
        ListeProps=[0,0,0,0]
        j = 0
        NbB = 1
        for i in SortieText:
            if i[0]	!= '#' and i[0] != ' ':
                SplittedLine = i.split()
                if len(SplittedLine) != 0:
                    if SplittedLine[0] == 'Type':
                        self.Type = SplittedLine[2]
                    if SplittedLine[0] == 'Factor':
                        self.Factor = np.longdouble(SplittedLine[2])
                    if SplittedLine[0] == 'Direction':
                        self.Direction = np.array([np.longdouble(SplittedLine[2]),np.longdouble(SplittedLine[3]),np.longdouble(SplittedLine[4]),np.longdouble(SplittedLine[5]),np.longdouble(SplittedLine[6]),np.longdouble(SplittedLine[7])])
                    if SplittedLine[0] == 'dt':
                        self.dt = np.longdouble(SplittedLine[2])
                    if SplittedLine[0] == 'omega':
                        self.omega = np.longdouble(SplittedLine[2])
                    if SplittedLine[0] == 'Tmax':
                        self.Tmax = np.longdouble(SplittedLine[2])
                    if SplittedLine[0] == 'Model':
                        self.ModelID = np.longdouble(SplittedLine[2])
         
    def __str__(self):
        if self.Type == 'S':
            return "Chargement de type sinusoidal \ndans la direction "+str(self.Direction)+"\navec un facteur "+str(self.Factor)+"\na "+str(self.omega)+"Rad/s \navec dt = "+str(self.dt) 
        if self.Type == 'T':
            return "Chargement de type traction monotone \ndans la direction "+str(self.Direction)+"\navec un facteur "+str(self.Factor)+"\navec dt = "+str(self.dt)         


class DMA:
    """ Une DMA est définie par:
        - Un type de balayage (Fréquence / Température): "F" pour Fréquence "T" pour température
        - un échantillonage en fréquence: Sous forme de liste [F0,Ffin,Facteur N entre deux points]
        - un materiau (voir classe materiau)
        - un VER  (voir classe VER)"""
        
    def __init__(self,Type,FreQList,TempList,Mat,VER,Load):
        self.Type = Type
        self.F0 = FreQList[0]
        self.TempList = TempList
        self.Ffin = FreQList[1]
        self.FacteurN = FreQList[2]
        self.Load = Load
        self.mat = Mat
        self.VER = VER
    
    def LoadString(self):
        string = ''
        for i in self.Load.Direction:
            string += str(i)+' '
        return string  

    def GenerateInstructionfile(self):
        file = open("MicroStruct2.in",'w+')
        file.write("#file describing the mechanical behavior of the\n#different components of the material\n")
        file.write("Materials = "+str(self.mat.matfilename))
        file.write("\n#Phases\nPhases = Phases.phases\n#Images\n")
        file.write("MicroStructure = VER_"+str(self.VER.Vf)+"_"+str(self.VER.N)+".vtk\n")
        file.write("#Chargement\nLoading = DMA.dat\nTemperature = temp.dat\n# Choix de C0\nC0 = auto\n")
        file.write("#Precision requise\nprecision = 1.E-3\n#Sorties\noutput = MicroStruct.output\nscheme = 0")
        file.close()          
    
    def GenerateLoadFile(self,FreQ,Sampling,NbSin,Eps0):
        CurrentFreq = FreQ
        CurrentPulse = CurrentFreq*2*math.pi
        
        ## Generation des pas de chargement ##
        time = 0
        TableEps = []
        TableTime = []
        CurrentPulse = CurrentFreq*2*math.pi
        T = 1/float(CurrentFreq)
        dt = T/float(Sampling)
        time0 = time
        for i in range(NbSin*Sampling+1):
            TableEps.append(math.sin(CurrentPulse*(time-time0))*Eps0)
            TableTime.append(time)
            time += dt
            
        ## Configuration du fichier de chargement Traction.dat ##
        Tractiof = open("DMA.dat",'w')
        Tractiof.write("#-------------------------------------\n# prescribed strain\nD\n#-------------------------------------\n# loading\n# t direction k\n# 11 22 33 12 13 23\n#- - - - - - - - - - - - - - - - - - -\n")
        for i in range(len(TableTime)):
            if i != 0:
                    DMAstr = ''
                    if math.fabs(TableEps[i]) > 0.0001:
                        DMAstr = str(TableTime[i])+' '+self.LoadString()+' '+str(TableEps[i])+'\n'
                        Tractiof.write(DMAstr)
        Tractiof.close()      

    def RunFreQScan(self):
        self.GenerateInstructionfile("MicroStruct2.in")
        self.mat.GenerateMatFile(0,temp)
        ListFreq = []
        CurrentFreq = self.F0
        while CurrentFreq <= self.Ffin:
            ListFreq.append(CurrentFreq)
            CurrentFreq = CurrentFreq*self.FacteurN
        for f in ListFreq:
            self.GenerateLoadFile(f,100,5,0.05)
            CraftCommand = './bin/craft MicroStruct2.in -v -n 8'
            subprocess.call([CraftCommand], shell = True)
            Command = "mkdir "+str(f)
            os.system(Command)
            Command = "mv MicroStruct.res "+str(f)
            os.system(Command)
            file = open("InstructionFreQ.txt","w")
            file.write(str(f))
            file.close()
            Command = "mv InstructionFreQ.txt "+str(f)
            os.system(Command)

    def RunTempScan(self):
        for temp in self.TempList:
            self.mat.T0 = temp
            file = open("temp.dat","w+")
            file.write("# Loading conditions in temperature\n#\n# time temperature\n")
            file.write("1 "+str(temp)+"\n")
            file.close()
            Command = "mkdir "+str(self.mat.T0)
            os.system(Command)
            self.mat.GenerateMatFile(0,temp)
            ListFreq = []
            CurrentFreq = self.F0
            while CurrentFreq <= self.Ffin:
                ListFreq.append(CurrentFreq)
                CurrentFreq = CurrentFreq*self.FacteurN
            for f in ListFreq:
                self.GenerateLoadFile(f,100,5,0.05)
                CraftCommand = './bin/craft MicroStruct2.in -v -n 8'
                subprocess.call([CraftCommand], shell = True)
                Command = "mkdir "+str(f)
                os.system(Command)
                Command = "mv MicroStruct.res "+str(f)
                os.system(Command)
                file = open("InstructionFreQ.txt","w")
                file.write(str(f))
                file.close()
                Command = "mv InstructionFreQ.txt "+str(f)
                os.system(Command)
                Command = "mv "+str(f)+" "+str(self.mat.T0)
                os.system(Command)
            Command = "mv PEEK.mat"+" "+str(self.mat.T0)
            os.system(Command)
            
        
#####################
#       Main        #
#####################
filename = "PEEK.mat"
Mu = [127.737, 25.5474, 31.0219, 50., 82.8467, 90.8759, 130.292, 122.993,111.314, 85.7664, 54.7445, 8.39416]
Eta = [1000000000000000000,36000,1280,130,18,2,0.3,0.032,0.0025,0.00012,0.00001,0.0000001]
CoefPowerLaw = [1,1,1,1,1,1,1,1,1,1,1,1]
ThermalExp = [0,0]
MatNumber = 0
PoissonMatrix = [[0,0.37],[300,0.37]]
C1C2 = [180,900,160]
Tg = 150
T0 = 21
TestMat = mat403(Mu,Eta,CoefPowerLaw,PoissonMatrix,C1C2,ThermalExp,Tg,T0,"PEEK.mat")
Loadcase = Load()
Loadcase.getLoad("Load.txt")
VERtest = VER(0.2,50,10,10,50,137)
VERtest.GenerateVER() 
TestDMA = DMA('F',[0.1,13,2],[100,110,120,130,140,150,160,170,180,190,200],TestMat,VERtest,Loadcase)
TestDMA.GenerateInstructionfile()
TestDMA.RunTempScan()
