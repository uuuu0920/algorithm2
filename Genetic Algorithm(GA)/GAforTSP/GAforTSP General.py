import random
import math
import copy
import matplotlib.pyplot as plt
import xlrd
import time

class GA():
    def __init__(self,popSize,city,cityPosition,crossOverRate,mutationRate):
        self.popSize=popSize
        self.city=copy.deepcopy(city)
        self.cityPosition=copy.deepcopy(cityPosition)
        self.crossOverRate=crossOverRate #交配率
        self.mutationRate=mutationRate #突變率
        
        
        self.path=[] #各城市間距離矩陣        
        self.solution = [] #當前解
        self.solutionValue=[] #當前解值
        self.fitnessValue=[] #適應值  
        self.bestSolution = [] #當前最佳解
        self.bestSolutionValue=[] #當前最佳解值
        
        self.offSpring=[]
        
        
    def testFunction1(self,solution,path):
        totalDistance=0
        solutionPlus=copy.deepcopy(solution)        
        solutionPlus.append(solutionPlus[0])
        for i in range(len(solutionPlus)-1):
            a=self.city.index(solutionPlus[i])
            b=self.city.index(solutionPlus[i+1])
            totalDistance=totalDistance+path[a][b]
            
        return totalDistance

        
    def distance(self): #計算各城市間距離
        #建立二維陣列
        path=[[0]*len(city) for i in range(len(city))]

        #兩點距離
        def between_distance(xs1,xs2,ys1,ys2):
            distance=((xs2-xs1)**2 + (ys2-ys1)**2) **(1/2)
            return distance

        #將兩點距離導入path
        for i in range(len(city)):
            for y in range(len(city)):
                path[i][y]=between_distance(cityPosition[i][0],cityPosition[y][0],cityPosition[i][1],cityPosition[y][1])
        self.path=copy.deepcopy(path)


    def initialize (self):
        for i in range(self.popSize):
            solution = copy.deepcopy(city)
            random.shuffle(solution)
            
            self.solutionValue.append(self.testFunction1(solution,self.path)) 
            self.solution.append(solution)
        self.bestSolution=self.solution[self.solutionValue.index(min(self.solutionValue))]
        self.bestSolutionValue=min(self.solutionValue)
        
    def roulette (self):
        fitnessReverse=[]
        fitness=[]
        fitnessSum=0
        
        for i in range(len(self.solutionValue)):
            fitnessReverse.append(1/self.solutionValue[i])
        fitnessSum=sum(fitnessReverse)
        for i in range(len(self.solutionValue)):
            fitness.append(fitnessReverse[i]/fitnessSum)
        self.fitnessValue=copy.deepcopy(fitness)
        
    def crossOver (self):
        crossOverTime= round(self.crossOverRate*self.popSize)
        self.offSpring=[]
        
        for i in range(crossOverTime):
            hit=random.sample(self.fitnessValue,2)
            parent1 = copy.deepcopy( self.solution[ self.fitnessValue.index( hit[0] ) ] )
            parent2 = copy.deepcopy( self.solution[ self.fitnessValue.index( hit[1] ) ] )

            randomPoint = random.sample(range(len(parent1)) , random.randint(1, len(parent1)-1) )
            randomPoint=sorted(randomPoint)
            child= []
            randomPointReverse= []
          
            for j in range(len(parent1)):
               randomPointReverse.append(j)
            for j in randomPoint:
               randomPointReverse.pop(randomPointReverse.index(j)) 
               parent2.pop( parent2.index( parent1[j] ) )
            

            
            count = 0
            for j in range(len(parent1)):
                
                if  j == randomPoint[count]:
                                       
                    child.append(parent1[j])
                    if count < len(randomPoint)-1:                        
                        count = count+1
                    
                else:
                    child.append(parent2[0])
                    parent2.pop(0)
            self.offSpring.append(child)
    def mutation (self):
        mutationTime=round(self.mutationRate*self.popSize)
        
        for i in range(mutationTime):
            hit = random.sample(self.offSpring, 1)
            hit=hit[0]
            randomPoint = random.sample(range(len(hit)) , 2 )
            randomPoint=sorted(randomPoint)
            snippet = hit[randomPoint[0]:randomPoint[1]]
            snippet.reverse()        
            for j in range(len(snippet)):
                hit[randomPoint[0]+j] = snippet[j]

            self.offSpring.append(hit)
    #--------檢查串列是否重複--------------------       
    def index_of(self,val, in_list):
        try:
            return in_list.index(val)
        except ValueError:
            return -1
        
    def update(self):
        for i in range(len(self.offSpring)):
            
            if  self.index_of(self.offSpring[i],self.solution) == -1:
                offSpringValue=self.testFunction1(self.offSpring[i],self.path)
                
                if offSpringValue < max(self.solutionValue):
                    self.solutionValue.append(offSpringValue)
                    self.solution.append(self.offSpring[i])
                    
                    self.solution.pop( self.solutionValue.index( max(self.solutionValue) ) )
                    self.solutionValue.pop( self.solutionValue.index( max(self.solutionValue) ) )
                    
                    if offSpringValue < self.bestSolutionValue:
                        self.bestSolutionValue = offSpringValue
                        self.bestSolution = copy.deepcopy(self.offSpring[i])
        self.offSpring=[]
        
        
    def map (self):
        a= copy.deepcopy(self.bestSolution)
        a.append(a[0])
        map_x=[]
        map_y=[]
        for i in range (len(a)):
            map_x.append(self.cityPosition[self.city.index(a[i])][0])
            map_y.append(self.cityPosition[self.city.index(a[i])][1])
        plt.plot(map_x,  map_y)
        plt.xlabel('GA_route')
        plt.show()
    
          
        
        
#------
iteration=500
popSize=30
crossOverRate=0.8
mutationRate=0.1

workbook=xlrd.open_workbook("TSP51.xlsx")  #文件路径
worksheet=workbook.sheet_by_index(0)    
cityPosition=[]
city=[]
for i in range(worksheet.nrows):
    cityPosition.append(worksheet.row_values(i))
    city.append(cityPosition[i][0])
    cityPosition[i].pop(0)


run_time=[]
time_start =time.time()
for qq in range(30):
    random.seed(qq)
    
    loop_x=list()
    loop_y=list()
    
    
    solver =GA(popSize,city,cityPosition,crossOverRate,mutationRate)     
    solver.distance()    
    solver.initialize()
    for i in range(iteration):
        
        print(qq,"第",i,"圈")
    
        solver.roulette()
        solver.crossOver()
        solver.mutation()
        solver.update()
        loop_x.append(i)
        loop_y.append(solver.bestSolutionValue)
    
    #print(solver.bestSolutionValue)
    
    
    plt.plot(loop_x,  loop_y)
    plt.xlabel('GA_fitline')
    plt.show()
    
    solver.map()
    run_time.append(solver.bestSolutionValue)
    
print( "標",run_time.index( min(run_time) ) )
print("平均值", sum(run_time)/len(run_time))
print("最小值", min(run_time))
time_end =time.time()
print("花費時間",time_end-time_start)


