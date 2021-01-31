import random
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import interpolate

# INPUT
# n : number of attack cycles belonging to R+
# q : relative hashrate belonging to [0;0.5]
# gamma : the ratio of honest miners that choose to mine on the pool’s block belonging to [0;1]
# bitcoinValue : coinbase belonging to R+
# bitcoinReward : no. of bitcoin for each block mined belonging to R+
class SelfishMining:

    # Initialisation
    def __init__(self, **inputVar):
        self.n = inputVar['numberCycles']
        self.q = inputVar['relativeHashrate']
        self.gamma = inputVar['gamma']

        self.honestChain = 0 # unit
        self.selfishChain = 0 # unit
        self.officialChain = 0 # unit
        self.orphanBlocks = 0 # unit
        self.delta = 0 # advance of selfish miners on honests'ones

        self.time = 0 # second    
        self.miningTime = 600 # seconds
        self.timeUpdate = 0 # second

        self.bitcoinValue = inputVar['bitcoinValue']
        self.bitcoinReward = inputVar['bitcoinReward']
        self.miningReward = self.bitcoinValue * self.bitcoinReward # dollars
        self.profitSelfishMining = 0 # dollar

    # Simulation 1 - Mining classic 
    def Simulation1(self):
        while(self.officialChain < self.n):

            r1 = random.uniform(0,1)
            
            # Update variables
            self.update()
                
            # If selfish miner solve the block
            if(r1 < self.q):
                self.selfishChain += 1

                # Beginning of the attack
                self.Simulation2()

            # If honest miner solve the block in first
            else:
                self.officialChain += 1

    
    # Simulation 2 - SelfishMining Attack
    def Simulation2(self):
        while(self.selfishChain != 0 and self.officialChain <= self.n):
            r2 = random.uniform(0,1)

            # If selfish miner solve the block in first
            if(r2 < self.q):
                self.selfishChain += 1
            else:
                self.honestChain +=1 
                # Update variables
                self.update()

                # Difference between selfish and honest chain
                if(self.delta == 0):
                    
                    if(r2 < self.q):
                        self.selfishChain += 1
                        self.officialChain += self.selfishChain
                        self.profitSelfishMining += self.miningReward * self.selfishChain
                        self.orphanBlocks += self.honestChain
                        self.selfishChain = self.honestChain = 0

                    else:
                        self.officialChain += 1

                        r3 = random.uniform(0,1)
                        # if the ratio of honest miners choose to mine on the pool’s block
                        if(r3 <= self.gamma):
                            self.officialChain += self.selfishChain
                            self.profitSelfishMining += self.miningReward * self.selfishChain
                            self.orphanBlocks += self.honestChain-1
                            self.selfishChain = self.honestChain = 0
                        else:
                            self.officialChain += self.honestChain
                            self.selfishChain = self.honestChain = 0

                # Difference between selfish and honest chain
                elif(self.delta == 1):
                    self.officialChain += self.selfishChain
                    self.profitSelfishMining += self.miningReward * self.selfishChain
                    self.orphanBlocks += self.honestChain
                    self.selfishChain = self.honestChain = 0

                elif(self.delta == -1):
                    self.officialChain += self.honestChain
                    self.orphanBlocks += self.selfishChain
                    self.selfishChain = self.honestChain = 0


    def update(self):
        # Updating the difficulty
        if(self.officialChain % 2016 == 0 and self.officialChain != 0):
            self.miningTime = self.miningTime * ((2016 * 600) / self.timeUpdate)
            self.timeUpdate = 0

        # Updating time 
        self.time += self.miningTime
        self.timeUpdate += self.miningTime

        # Updating delta
        self.delta = self.selfishChain - self.honestChain

#### TEST WITH INPUT DATA ####
def testSelfishMiningInputData():
    n = int(input("numberCycle : "))
    q = float(input("relativeHashrate : "))
    gamma = float(input("gamma : "))
    bitcoinValue = int(input("bitcoinValue : "))
    bitcoinReward = float(input("bitcoinReward : "))
    inputVariables = {'numberCycles':n, 'relativeHashrate':q, 'gamma':gamma,'bitcoinValue':bitcoinValue,'bitcoinReward':bitcoinReward}
    return inputVariables


#### AUTOMATIC TEST ####
def testSelfishMiningAutomaticData():
    inputVariables = {'numberCycles':1000, 'relativeHashrate':0.4, 'gamma':0,'bitcoinValue':10000,'bitcoinReward':6}
    return inputVariables

#### Convert Time to days, hours, minutes... ####
def timeConverter(n):
    sec = min = hour = day = week = 0
    if(n>=60):
        min=n//60
        sec=n%60
        if(min>=60):
            hour=min//60 
            min = min%60
            if(hour>=24):
                day=hour//24
                hour=hour%24
                if(day>=7):
                    week=day//7
                    day=day%7
                else:
                    week=0
            else:
                day=0
        else:
            hour=0 
    else:
        min=0
        sec=n
    return sec, min, hour, day, week

#### Display data ### 
def displayData(data):
    new = SelfishMining(**data)
    new.Simulation1()
    time = timeConverter(new.time)
    revenueRate = new.profitSelfishMining/(new.officialChain*new.bitcoinReward*new.bitcoinValue)
    if(time[4] == 0): 
        print('\ntime :', time[3],'days', time[2],'hours', time[1],'minutes', time[0],'seconds')
    elif(time[3] == 0): 
        print('\ntime :', time[2],'hours', time[1],'minutes', time[0],'seconds')
    elif(time[2] == 0): 
        print('\ntime :', time[1],'minutes', time[0],'seconds')
    elif(time[1] == 0): 
        print('\ntime :', time[0],'seconds')
    else:
        print('\ntime :', time[4],'weeks', time[3],'days', time[2],'hours', time[1],'minutes', time[0],'seconds')
    print('orphanBlocks :', new.orphanBlocks, end=' units\n')
    print('officialChain :', new.officialChain, end=' units\n')
    print('reward :', new.profitSelfishMining, end=' dollars\n')
    print('revenue rate : ', revenueRate, end='\n\n')

#### Launch selfish mining test with all data #### 
def launchSelfishMining(i, j):
    inputVariables = {'numberCycles':2000, 'relativeHashrate':j, 'gamma':i,'bitcoinValue':30000,'bitcoinReward':6.25}
    new = SelfishMining(**inputVariables)
    new.Simulation1()
    return new.profitSelfishMining/(new.officialChain*new.bitcoinReward*new.bitcoinValue)

#### Display graphic #### 
def createGraphic(kmax): 
    label = ['Gamma = 0', 'Gamma = 0.5', 'Gamma = 1', 'Honest Miner']
    col = ['red', 'green', 'blue']
    for i in range(0, 3, 1):
        x = []
        y = []
        for j in range(0, 51, 1):
            x.append(j*0.01)
            moyenneY = k = 0
            if(i == 0):
                while k < kmax:
                    moyenneY +=launchSelfishMining(0, j*0.01)
                    k += 1
                y.append(moyenneY / kmax)
            elif(i == 1):
                while k < kmax:
                    moyenneY +=launchSelfishMining(0.5, j*0.01)
                    k += 1
                y.append(moyenneY / kmax)
            elif(i == 2):
                while k < kmax:
                    moyenneY +=launchSelfishMining(1, j*0.01)
                    k += 1
                y.append(moyenneY / kmax)

        
        # DISPLAY THE GRAPHIC
        curbX = np.array(x)
        curbY = np.array(y)
        
        #plt.plot(curbX, curbY, label=label[i])
        plt.plot(curbX, curbY, label=label[i], color=col[i])
        plt.legend() # Ajout de la légende
    tab1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    plt.plot(tab1,tab1, label=label[3], color='grey')
    plt.legend() # Ajout de la légende
    plt.title('Revenue of SelfishMining strategy')
    plt.xlim(0,0.5)           # Echelle sur l'axe des x
    plt.ylim(0,1)  
    plt.xlabel('Pool size')         # Nom de la grandeur en ordonnée
    plt.ylabel('Relative pool revenue')         # Nom de la grandeur en abscisse

    plt.show()

def pause():
    input("Press the <ENTER> key to continue...")


#### MENU ####
ans=True
data = []
while ans:
    print ("""
    1.Create a graphic of the reward of selfish miners compare to honest miners
    2.Launch a selfish mining test for default data 
    3.Launch a selfish mining test for input data 
    4.Exit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1": 
      print("Please wait few seconds")
      createGraphic(20)
    elif ans=="2":
      data = testSelfishMiningAutomaticData()
      displayData(data)
      pause()
    elif ans=="3":
      data = testSelfishMiningInputData()
      displayData(data)
      pause()
    elif ans=="4":
      print("\n Goodbye")
      import sys
      sys.exit(0)
    elif ans !="":
      print("\n Not Valid Choice Try again") 