import random
import math
import copy
import matplotlib.pyplot as plt
random.seed(5)

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
    
    def testfunction2(self,x):
        value1=0
        value2=abs(x[0])
        for i in x:
            value1 = value1 + abs(i)
        for i in range(1,len(x)):
            value2= value2 *abs(x[i])
        return value1+value2

    def testfunction3(self,x):
        value1=0
        value2=0
        for i in range(len(x)):
            
            value2=value2+(value1**2)
            value1=0
            for j in range(i):
                value1=value1+x[j]
        return value2
    
    def testfunction4(self,x):
        value=copy.deepcopy(x)
        for i in range(len(value)):
            value[i]=abs(value[i])
        return max(value)
    
    def testfunction5(self,x):
        value=0
        for i in range(len(x)-1):
            value=value + (100* ((x[i]**2)-x[i+1]) **2 + (1-x[i])**2)
        return value
    
    def testfunction6(self,x):
        value=0
        for i in x:
            value= value + (i+0.5)**2
            
        return value
    
    def testfunction7(self,x):
        value=0
        for i in range(len(x)):
            value=value+ i*x[i]**4 
        return value+ random.random()
    
    def testfunction8(self,x):
        value=0
        for i in x:
            value= value + (-i) * math.sin(abs(i)**0.5)
        return value
        
    def testfunction9(self,x):
        value=0
        for i in x:
            value=value+ ((i**2)-(10*math.cos(2*math.pi*i)) +10)
            
        return value
    
    def testfunction10(self,x):
        value=0
        value1=0
        value2=0
        for i in x:
            value1=value1+ i**2
            value2=value2+ math.cos(2*math.pi*i)
        value= -20*math.exp(-0.2*math.sqrt((1/len(x))*value1)) - math.exp((1/len(x))*value2) + 20 + math.e
            
        return value 
    
    def testfunction11(self,x):
        value=0
        value1=0
        value2=x[0]
        for i in x:
            value1=value1+ i**2
        for i in range(1,len(x)+1):
            value2= value* math.cos(x[i-1]/math.sqrt(i))
        value2=value2/x[0]
        value= 1+ ((1/4000)*value1) - value2
            
        return value 
        
    def initialize (self):
        
        for i in range(self.popSize):
            random.seed(i)
            solution = []
            for j in range(self.dimension):
                solution.append(self.lower+(random.random()*(self.upper-self.lower)))
            self.solution.append(solution)
            self.individualBestSolution.append(solution)
            
            #-------------------------------------------------------------------------
            self.solutionValue.append(self.testfunction11(solution))
            
        self.individualBestSolutionValue=copy.copy(self.solutionValue)
            
        self.globalBestSolutionValue=min(self.solutionValue)
        self.globalBestSolution=self.individualBestSolution[self.solutionValue.index(min(self.solutionValue))]
    
    def move(self):
        for i in range(self.popSize):
            c1=self.cognitionFactor*random.random()
            c2=self.socialFactor*random.random()
            for j in range(self.dimension):
                v= (random.random()*self.velocity[i][j])+c1*(self.individualBestSolution[i][j]-self.solution[i][j])+ c2*(self.globalBestSolution[j]-self.solution[i][j])
                self.velocity[i][j]=v
                self.solution[i][j]=self.solution[i][j]+v
                
                if self.solution[i][j]<lower:
                    self.solution[i][j]=lower
                elif self.solution[i][j]>upper:
                    self.solution[i][j]=upper
            
    def update(self):
        for i in range(popSize):
            
            #---------------------------------------------------------------------------
            self.solutionValue[i] =self.testfunction11(self.solution[i])


            if self.solutionValue[i] < self.individualBestSolutionValue[i]:
                
                self.individualBestSolution[i]=copy.copy(self.solution[i])
                self.individualBestSolutionValue[i]=self.solutionValue[i]
                
                if self.solutionValue[i]<self.globalBestSolutionValue:
                    self.globalBestSolutionValue=self.solutionValue[i]
                    self.globalBestSolution=copy.copy(self.solution[i])



#-------------------------------主程式--------------------
popSize= 30
dimension= 30
iteration=500
lower= -600
upper= 600


cognitionFactor=0.5
socialFactor=0.5
loop_x=list()
loop_y=list()



solver =PSO(popSize,dimension,upper,lower,cognitionFactor,socialFactor)         
solver.initialize()
print(solver.solution)
print(solver.globalBestSolutionValue)


loop_x.append(0)
loop_y.append(solver.globalBestSolutionValue)
for i in range(iteration):
    loop_x.append(i+1)
    print("第",i+1,"圈")
    solver.move()
    solver.update()
    print("最小值為:" ,solver.globalBestSolutionValue)
    loop_y.append(solver.globalBestSolutionValue)

plt.plot(loop_x,  loop_y)
plt.xlabel('PSO')
plt.show()
