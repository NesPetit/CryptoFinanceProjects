import random
import numpy as np
import matplotlib.pyplot as plt
import time
from statistics import mean



# INPUT
# n : number of attack cycles belonging to N+
# q : relative hashrate belonging to [0;0.5]
# z : safety threshold set by the seller --> number of confirmation 
# a : maximum delay allowed by the attacker on the official blockchain 
# k : number of block premined by the attacker at the beginning of his attack 
# bitcoinValue : coinbase belonging to R+

# OUTPUT 
# The objective is to plot the attacker's profitability curve as a function of q (his proportion)
# For n, a, k, z fixed  
class DoubleSpending:

    # Initialisation
    def __init__(self, **inputVar):
        self.n = inputVar['numberCycles']
        self.q = inputVar['relativeHashrate']
        self.z = inputVar['numberConfirmation']
        self.a = inputVar['maximumDelay']
        self.k = inputVar['numberBlockPremined'] # We consider that for the satoshi attack k=1
        self.amount = inputVar['amount']
        self.bitcoinReward = inputVar['bitcoinReward']
        self.bitcoinValue = inputVar['bitcoinValue']

        self.officialChain = 0
        self.DSA_Chain = 0
        self.mean_DSA_Chain = 0
        self.mean_officialChain = 0

        self.time = 600 * self.z # second    
        self.miningTime = 600 # seconds

        self.profitAttacker = 0 # dollar
        self.profitMiners = 0

    # Simulation - DoubleSpending attack 
    def Simulation(self):
        for i in range(self.n):
            self.officialChain = 0 
            self.DSA_Chain = self.k
            #Tant que le seuil de tolerence est respecté et tant qu'on n'a pas depassé le seuil de securité alors on incremente
            while (self.officialChain - self.DSA_Chain) < self.a and self.officialChain <= self.z and self.DSA_Chain <= self.z:
                #On tire un random
                r1 = random.uniform(0,1)
                #Si ce random est inf à q alors on incremente la chaine de l'attaquant 
                if r1 < self.q:
                    self.DSA_Chain += 1
                #Sinon celle de l'honnete
                else: 
                    self.officialChain += 1

            #Si la simulation reussi pour l'attaquant
            if self.DSA_Chain > self.officialChain:
                self.profitAttacker += self.amount + self.bitcoinReward * self.bitcoinValue * self.DSA_Chain #En dollar

            self.profitMiners += self.bitcoinReward * self.bitcoinValue * self.officialChain #En dollar

            self.mean_officialChain += self.officialChain
            self.mean_DSA_Chain += self.DSA_Chain

        self.mean_officialChain = self.mean_officialChain / self.n
        self.mean_DSA_Chain = self.mean_DSA_Chain / self.n



#### TEST WITH INPUT DATA ####
def testDoubleSpendAttackInputData():
    n = int(input("Number cycle : "))
    q = float(input("Relative hashrate : "))
    z = int(input("Number confirmation : "))
    a = int(input("Maximum delay : "))
    k = int(input("Number block premined : "))
    amount = float(input("amount of double spending"))
    bitcoinReward = int(input("Bitcoin Reward : "))
    bitcoinValue = float(input("Bitcoin value : "))

    inputVariables = {'numberCycles':n, 'relativeHashrate':q, 'numberConfirmation':z,'maximumDelay':a, 'numberBlockPremined':k, 'amount':amount,'bitcoinReward':bitcoinReward, 'bitcoinValue':bitcoinValue}
    return inputVariables


#### AUTOMATIC TEST ####
def testDoubleSpendAttackAutomaticData():
    inputVariables = {'numberCycles':1000, 'relativeHashrate':0.3, 'numberConfirmation':8, 'maximumDelay':5, 'numberBlockPremined':1, 'amount':0.1,'bitcoinReward':6.25, 'bitcoinValue':30000}
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
    new = DoubleSpending(**data)
    new.Simulation()
    time = timeConverter(new.time)
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
    print('officialChain (mean):', new.mean_officialChain, end=' units\n')
    print('DSA_Chain (mean):', new.mean_DSA_Chain, end=' units\n')
    print('reward of the attacker :', new.profitAttacker / new.n, end=' dollars\n\n')

    return new

#### Display graphic #### 
def createGraphic(data): 

    x = np.arange(0.0, 0.51, 0.01)
    y = []
    for i in x:
        data['relativeHashrate'] = i
        new = DoubleSpending(**data)
        new.Simulation()
        if new.profitMiners == 0.0: #Evite les divisions par 0 dans les cas ou le miner ne gagne rien
            y.append(1.0)
            print("ok")
        else:
            #print(new.profitAttacker)
            y.append((new.profitAttacker / new.n) / (new.profitMiners / new.n))


    # DISPLAY THE GRAPHIC
    curbX = np.array(x)
    curbY = np.array(y)
    #print(curbY)
    lab = "n = " + str(new.n) + " ; a = " + str(new.a) + " ; k = " + str(new.k) + " ; z = " + str(new.z)
    col = 'red'
    #plt.plot(curbX, curbY, label=label[i])
    plt.plot(curbX, curbY, label = lab, color=col)
    plt.legend() # Ajout de la légende

    plt.title('Revenue of the double spend attack')
    plt.xlim(0,0.5)           # Echelle sur l'axe des x
    plt.xlabel('Pool size')         # Nom de la grandeur en abscisse
    plt.ylabel('Rate of revenue')         # Nom de la grandeur en ordonnée

    plt.show()

def pause():
    input("Press the <ENTER> key to continue...")


#### MENU ####
ans=True
data = []
while ans:
    print ("""
    1.Create a graphic of the reward of the double spend attack according to the proportion of attackers with default data
    2.Create a graphic of the reward of the double spend attack according to the proportion of attackers with input data  
    3.Exit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1":
      data = testDoubleSpendAttackAutomaticData()
      new = displayData(data)
      createGraphic(data)
      pause()
    elif ans=="2":
      data = testDoubleSpendAttackInputData()
      new = displayData(data)
      createGraphic(data)
      pause()
    elif ans=="3":
      print("\n Goodbye")
      import sys
      sys.exit(0)
    elif ans !="":
      print("\n Not Valid Choice Try again") 