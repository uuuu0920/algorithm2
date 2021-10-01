import random
import math
import copy
import matplotlib.pyplot as plt
import numpy as np
import testfunction
import time

class PSO():
    def __init__(self,popSize,dimension,upper,lower,cognitionFactor,socialFactor):
        self.popSize= popSize
        self.dimension= dimension
        self.upper= upper
        self.lower= lower
        self.cognitionFactor=cognitionFactor
        self.socialFactor=socialFactor
        
        self.solution = np.zeros((self.popSize,self.dimension)) #當前解
        self.solutionValue=np.zeros(self.popSize) #當前解值
        self.individualBestSolution = np.zeros((self.popSize,self.dimension)) #個人最佳解
        self.individualBestSolutionValue = np.zeros(self.popSize) #個人最佳解值
        self.velocity=np.zeros((self.popSize,self.dimension)) #速度
        
        self.globalBestSolution= np.zeros(self.dimension) #群體最佳解
        self.globalBestSolutionValue= [] #群體最佳解值
        

      
    def initialize (self):
        self.solution = 50 + (np.random.rand(self.popSize,self.dimension)*50)
        for i in range(self.popSize):
            self.solutionValue[i] = testfunction.testfunction11(self.solution[i])
        self.individualBestSolution=np.copy(self.solution)
        self.individualBestSolutionValue = np.copy(self.solutionValue)

        
        self.globalBestSolutionValue = self.individualBestSolutionValue.min()
        self.globalBestSolution = np.copy(self.individualBestSolution[np.argmin(self.individualBestSolutionValue)])

    def move_gbest(self):
        self.velocity=0.72894 * (self.velocity+   (   self.cognitionFactor*np.random.rand(self.popSize,self.dimension)*(self.individualBestSolution-self.solution)   )  +  (   self.socialFactor*np.random.rand(self.popSize,self.dimension)*(self.globalBestSolution -self.solution)   )     )
        self.solution = self.solution + self.velocity
        
    def update(self):
        for i in range(self.popSize):
            self.solutionValue[i] = testfunction.testfunction11(self.solution[i])

            
            if self.solutionValue[i] < self.individualBestSolutionValue[i]:
                self.individualBestSolutionValue[i] = self.solutionValue[i]
                self.individualBestSolution[i] = np.copy(self.solution[i])
                
        if np.min(self.individualBestSolutionValue) < self.globalBestSolutionValue:
            self.globalBestSolutionValue = np.min(self.individualBestSolutionValue)
            self.globalBestSolution = self.individualBestSolution[np.argmin(self.individualBestSolutionValue)]


            

popSize= 30
dimension= 30
iteration=500
lower= -600
upper= 600
time_start =time.time()
cal_value=[]
for qq in range(1):
    
    x=np.arange(iteration+1)

    gbest=[]
    cognitionFactor=2.05
    socialFactor=2.05
    random.seed(qq)
    np.random.seed(qq)
    solver= PSO(popSize,dimension,upper,lower,cognitionFactor,socialFactor)
    solver.initialize()
    gbest.append(solver.globalBestSolutionValue)
    #print(solver.globalBestSolutionValue)
    for i in range(iteration):
        solver.move_gbest()
        solver.update()
        gbest.append(solver.globalBestSolutionValue)
    print(solver.globalBestSolutionValue)
    
    plt.plot(x,gbest,label="lbest")
    plt.xlabel('PSO')
    plt.show()
    cal_value.append(solver.globalBestSolutionValue)
# =============================================================================
# print("標",cal_value.index( min(cal_value) ))    
# print("30次平均值",sum(cal_value) / len(cal_value))
# print("最小值",min(cal_value))    
# 
# time_end =time.time()
# print("花費時間",time_end-time_start)
# =============================================================================
