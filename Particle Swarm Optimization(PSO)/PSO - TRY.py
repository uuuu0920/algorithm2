import random
import math
import copy
import matplotlib.pyplot as plt


class PSO():
    def __init__(self,popSize,dimension,upper,lower,cognitionFactor,socialFactor):
        self.popSize= int(popSize)
        self.dimension= int(dimension)
        self.upper= upper
        self.lower= lower
        self.cognitionFactor=cognitionFactor
        self.socialFactor=socialFactor
        
        self.solution = [] #當前解
        self.solutionValue=[] #當前解值
        self.individualBestSolution = [] #個人最佳解
        self.individualBestSolutionValue = [] #個人最佳解值
        self.velocity=[[0]*dimension for i in range(popSize)] #速度
        
        self.globalBestSolution= [] #群體最佳解
        self.globalBestSolutionValue= [] #群體最佳解值
    def testfunction1(self,x):
        value=0

        for i in x:
            value = value + i**2
        return value
    
 
    def initialize (self):
        
        for i in range(self.popSize):
            solution = []
            for j in range(self.dimension):
                solution.append(  50 + (random.random()*50)  )
                #solution.append(self.lower+(random.random()*(self.upper-self.lower)))
            self.solution.append(solution)
            self.individualBestSolution.append(solution)
            
            #-------------------------------------------------------------------------
            self.solutionValue.append(self.testfunction1(solution))
            #--------------------------------------------------------------------
            
        self.individualBestSolutionValue=copy.copy(self.solutionValue)
            
        self.globalBestSolutionValue=min(self.solutionValue)
        self.globalBestSolution=self.individualBestSolution[self.solutionValue.index(min(self.solutionValue))]
    
    def move(self):
        for i in range(self.popSize):

            for j in range(self.dimension):
                v= self.velocity[i][j] + (self.cognitionFactor*random.random()*(self.individualBestSolution[i][j]-self.solution[i][j]))+ (self.socialFactor*random.random()*(self.globalBestSolution[j]-self.solution[i][j]))
                self.velocity[i][j]=v
                self.solution[i][j]=self.solution[i][j]+v
                    
                if self.solution[i][j]<lower:
                    self.solution[i][j]=lower
                elif self.solution[i][j]>upper:
                    self.solution[i][j]=upper
                  
    def move_gbest(self):
        for i in range(self.popSize):
                

            for j in range(self.dimension):
                v= 0.72984*(self.velocity[i][j] + (self.cognitionFactor*random.random()*(self.individualBestSolution[i][j]-self.solution[i][j]))+ (self.socialFactor*random.random()*(self.globalBestSolution[j]-self.solution[i][j])))
                self.velocity[i][j]=v
                self.solution[i][j]=self.solution[i][j]+v
                    
                """if self.solution[i][j]<lower:
                    self.solution[i][j]=lower
                elif self.solution[i][j]>upper:
                    self.solution[i][j]=upper """
                    
                    
                    
    def move_lbest(self):
        
        for i in range(self.popSize):
            current_best= copy.deepcopy( self.solution [self.solutionValue.index( min(self.solutionValue) ) ])    

            for j in range(self.dimension):
                v= 0.72984*(self.velocity[i][j]+self.cognitionFactor*random.random()*(self.individualBestSolution[i][j]-self.solution[i][j])+ self.socialFactor*random.random()*(current_best[j]-self.solution[i][j]))
                self.velocity[i][j]=v
                self.solution[i][j]=self.solution[i][j]+v
                    
                """if self.solution[i][j]<lower:
                    self.solution[i][j]=lower
                elif self.solution[i][j]>upper:
                    self.solution[i][j]=upper"""
                    
                  
    def update(self):
        for i in range(popSize):
            
            #---------------------------------------------------------------------------
            self.solutionValue[i] =self.testfunction1(self.solution[i])
            #---------------------------------------------------------------------

            if self.solutionValue[i] < self.individualBestSolutionValue[i]:
                
                self.individualBestSolution[i]=copy.copy(self.solution[i])
                self.individualBestSolutionValue[i]=self.solutionValue[i]
                
                if self.solutionValue[i]<self.globalBestSolutionValue:
                    self.globalBestSolutionValue=self.solutionValue[i]
                    self.globalBestSolution=copy.copy(self.solution[i])



#-------------------------------主程式--------------------
popSize= 50
dimension= 30
iteration=300000
lower= -100
upper= 100
origin_value=[]
lbest_value=[]
gbest_value=[]

aa=[]

for qq in range(1): #執行30次

    random.seed(1)
    
    cognitionFactor=2.05
    socialFactor=2.05
    loop_x=list()
    loop_y=list()
      
    solver =PSO(popSize,dimension,upper,lower,cognitionFactor,socialFactor)         
    solver.initialize()
   
    loop_x.append(0)
    loop_y.append(solver.globalBestSolutionValue)
    for i in range(iteration):
        loop_x.append(i+1)
        print("origin 第",qq,"次第",i+1,"圈")
        solver.move()
        solver.update()

        loop_y.append(solver.globalBestSolutionValue)
#------------------------------------Gbest------------------------------------------------------
    random.seed(2)

    loop_y_gbest=list()    
    solver_gbest=PSO(popSize,dimension,upper,lower,cognitionFactor,socialFactor)    
    solver_gbest.initialize()

    loop_y_gbest.append(solver_gbest.globalBestSolutionValue)
    
    for i in range(iteration):

        print("gbest 第",qq,"次第",i+1,"圈")
        solver_gbest.move_gbest()
        solver_gbest.update()

        loop_y_gbest.append(solver_gbest.globalBestSolutionValue)
        
        
#---------------------------------------Lbest------------------------------------------------

    random.seed(qq)

    loop_y_lbest=list()    
    solver_lbest=PSO(popSize,dimension,upper,lower,cognitionFactor,socialFactor)    
    solver_lbest.initialize()


    loop_y_lbest.append(solver_lbest.globalBestSolutionValue)
    
    for i in range(iteration):
        
        print("lbest 第",qq,"次第",i+1,"圈")
        solver_lbest.move_lbest()
        solver_lbest.update()

        loop_y_lbest.append(solver_lbest.globalBestSolutionValue)
    
    origin_value.append(solver.globalBestSolutionValue)
    gbest_value.append(solver_gbest.globalBestSolutionValue)
    lbest_value.append(solver_lbest.globalBestSolutionValue)
    
          
    plt.plot(loop_x,  loop_y,label="origin")
    plt.plot(loop_x,loop_y_gbest,label="gbest")
    plt.plot(loop_x,loop_y_lbest,label="lbest")
    plt.xlabel('PSO')
    plt.legend()
    plt.savefig("testfunction1-.png")
    plt.show()
print(solver_gbest.globalBestSolution)    
print("origin 30次迴圈 平均值: ",sum(origin_value)/len(origin_value))  
print("origin 30次迴圈 最小值: ",min(origin_value)) 
print() 
print("gbest 30次迴圈 平均值: ",sum(gbest_value)/len(gbest_value))  
print("gbest 30次迴圈 最小值: ",min(gbest_value))  
print()
print("lbest 30次迴圈 平均值: ",sum(lbest_value)/len(lbest_value))  
print("lbest 30次迴圈 最小值: ",min(lbest_value))  