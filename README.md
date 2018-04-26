# PyFFTDMA
PyFFTDMA is a series of python programs written by Boris Burgarella during his PhD.
The objective is to have a fully python handled full field homogenization model

Depdencies:
- CraFT (http://craft.lma.cnrs-mrs.fr/)

PyFFTDMA is divided in two main components:
Main.py --> takes care of the RVE generation and the CraFT calls
FScanAll --> Post-treat the CraFT results and calls ShiftcalculatorFFV4

the Main.Py can be configured thanks to the code at its very bottom, with this part of the code:

The filename variable determines the name of the material file for CraFT, you can use any name you like since this craft will be configured 
to use this name.

Mu and Eta are the material configuration variables, you can specify any number of mu and eta as you, they correspond to the 
Shear modulus and the viscosity of each branches.

the CoefPowerLaw is a CraFT parameter, you need to give as many coefficient as the number of branch you want in your model
to when this parameter is 1, the branch is a maxewll branch

The RVE generation parameters are gathered in the VER class
- the first parameter is the fiber volume ratio
- the second gives the number of fiber to be placed in the RVE
- the third one gives N the orientation distribution parameter
- The fourth gives elongation ratio of the inclusions
- The fith the resolution
- the last one is a seed for the random variables in the generation

The DMA is handled by the DMA class
a DMA is defined by:
  - A scan type (Frequency or temperature): "F" for frequency, "T" for a temperature scan
  - A frequency sample in the form of a list [F0,Ffin,Multiplication between two points]
  - A Material (see the material class in the code)
  - An RVE (See definition above)

```
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
```

The FscanAll.py file is used to post treat the CraFT results, it is configures through this code:
```
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
```

C1 and C2 are the parameters for the shift factors
Tref is the reference temperature
ListN is the list of N (the orientation distribution parameter)
NbChargement should remain equal to 5 since nothing is implemented to change
The other different lists defines the cases that will be post-treated
