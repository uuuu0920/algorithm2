import random
import math
import copy
import matplotlib.pyplot as plt
import xlrd


class PSO():
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
        offSpring=[]
        
        for i in range(crossOverTime):
            
            #第一條染色體
                interval1=0
                interval2=self.fitnessValue[0]
                hit=random.random()
                selectX=[]
                selectY=[]
                
                for j in range(len(self.fitnessValue)):
                    if j == len(self.fitnessValue)-1:
                        if hit > interval1 and hit < interval2:
                            selectX=copy.deepcopy(self.solution[j])
                    else:
                        
                        if hit > interval1 and hit < interval2:
                            selectX=copy.deepcopy(self.solution[j])
                        
                        interval1=interval1+self.fitnessValue[j]
                        interval2=interval2+self.fitnessValue[j+1]
                print(selectX)
            #第二條染色體
                selectY=copy.deepcopy(selectX)
                
                while selectY == selectX:
                    interval1=0
                    interval2=self.fitnessValue[0]
                    hit=random.random()
                    for j in range(len(self.fitnessValue)):
                        if j == len(self.fitnessValue)-1:
                            if hit > interval1 and hit < interval2:
                                selectY=copy.deepcopy(self.solution[j])
                        else:
                            
                            if hit > interval1 and hit < interval2:
                                selectY=copy.deepcopy(self.solution[j])
                            
                            interval1=interval1+self.fitnessValue[j]
                            interval2=interval2+self.fitnessValue[j+1]      
                print(selectY)
                
                #交配
                selectX2=copy.deepcopy(selectX)
                selectY2=copy.deepcopy(selectY)
                #child x
                child_x=[]
                selectCity= random.sample(selectX,1)
                selectCity= selectCity[0]
                print(selectCity)
                child_x.append(selectCity)
                
                while len(selectX)>0:
                    selectX.index(selectCity)
                    
                    
                    
                    
            
                    
                
            
        
        
        
            
        
        
#------
iteration=1
popSize=3
crossOverRate=0.9
mutationRate=0.01

workbook=xlrd.open_workbook("TSP.xlsx")  #文件路径
worksheet=workbook.sheet_by_index(0)    
cityPosition=[]
city=[]
for i in range(worksheet.nrows):
    cityPosition.append(worksheet.row_values(i))
    city.append(cityPosition[i][0])
    cityPosition[i].pop(0)

loop_x=list()
loop_y=list()
time=0



solver =PSO(popSize,city,cityPosition,crossOverRate,mutationRate)     
solver.distance()    
solver.initialize()
solver.roulette()
solver.crossOver()
#print(solver.solutionValue)
#print(solver.fitnessValue)
#while solver.globalBestSolutionValue >30:




plt.plot(loop_x,  loop_y)
plt.show()