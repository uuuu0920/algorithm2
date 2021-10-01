import random
import math
import copy
import matplotlib.pyplot as plt
import xlrd
import time
#random.seed(5)


class PSO():
    def __init__(self,popSize,city,cityPosition):
        self.popSize=popSize
        self.city=copy.deepcopy(city)
        self.cityPosition=copy.deepcopy(cityPosition)
        self.path=[] #各城市間距離矩陣
        self.v=[] 
        self.vi=[]

        
        self.solution = [] #當前解
        self.solutionValue=[] #當前解值
        self.individualBestSolution = [] #個人最佳解
        self.individualBestSolutionValue = [] #個人最佳解值

        
        self.globalBestSolution= [] #群體最佳解
        self.globalBestSolutionValue= [] #群體最佳解值
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
            #random.seed(i)
            solution = copy.deepcopy(city)            
            random.shuffle(solution)
            
            
            self.solutionValue.append(self.testFunction1(solution,self.path)) 
            self.solution.append(solution)
            self.individualBestSolution.append(solution)
            
            
            #設置初始速度
            v=[]
            for j in range(random.randint(1,3)): 
                v.append(random.sample(range(1, len(self.city)), 2))

            self.v.append(v) 
            

            


        self.individualBestSolutionValue=copy.copy(self.solutionValue)            
        self.globalBestSolutionValue=min(self.solutionValue)
        self.globalBestSolution=self.individualBestSolution[self.solutionValue.index(min(self.solutionValue))]
            
    def move(self):

        for i in range(popSize):
            

            w_probability =random.random()
            c1_probability = random.uniform(0,1-w_probability)
            c2_probability =1-w_probability-c1_probability
            totalV=[]
            #w*v
            w=round(w_probability*len(self.v[i]))
            if w != 0:
                #position=random.randint(0, len(self.v[i])-w)                
                for j in range(w):
                    totalV.append(self.v[i][j])
            
            
                     
         
            #(pb-xid)
            current=copy.deepcopy(self.solution[i])
            individualV=[]
            for j in range(len(current)):
                if current[j] != self.individualBestSolution[i][j]:
                     temp=current.index(self.individualBestSolution[i][j])
                     current[j],current[temp]=current[temp],current[j]
                     individualV.append([j,temp])


            #c1*(pb-xid)
            c1=round(c1_probability*len(individualV))
            if c1 != 0:
                #position=random.randint(0, len(individualV)-c1) 
                for j in range(c1):
                    totalV.append(individualV[j])
            
            
            #(gb-xid)
            current=copy.deepcopy(self.solution[i])
            
            globalV=[]
            for j in range(len(current)):
                if current[j] != self.globalBestSolution[j]:
                     temp=current.index(self.globalBestSolution[j])
                     current[j],current[temp]=current[temp],current[j]
                     globalV.append([j,temp])
                     
            #c2*(gb-xid)
            c2=round(c2_probability*len(globalV))
            if c2 != 0:     
                #position=random.randint(0, len(globalV)-c2)
                for j in range(c2):
                    totalV.append(globalV[j])
                    
            
            self.vi.append(totalV)
            

            for j in range(len(totalV)):
                self.solution[i][totalV[j][0]],self.solution[i][totalV[j][1]] = self.solution[i][totalV[j][1]],self.solution[i][totalV[j][0]]

                

        
    def update(self):
        for i in range(popSize):

            self.solutionValue[i]=self.testFunction1(self.solution[i],self.path)

            
            if self.solutionValue[i] < self.individualBestSolutionValue[i]:
                
                self.individualBestSolution[i]=copy.copy(self.solution[i])
                self.individualBestSolutionValue[i]=self.solutionValue[i]
                
                if self.solutionValue[i]<self.globalBestSolutionValue:
                    self.globalBestSolutionValue=self.solutionValue[i]
                    self.globalBestSolution=copy.copy(self.solution[i])            
        
    def map (self):
        a= copy.deepcopy(self.globalBestSolution)
        a.append(a[0])
        map_x=[]
        map_y=[]
        print(self.cityPosition[city.index(a[0])])
        for i in range (len(a)):
            map_x.append(self.cityPosition[self.city.index(a[i])][0])
            map_y.append(self.cityPosition[self.city.index(a[i])][1])
        plt.plot(map_x,  map_y)
        plt.show()

            



#-------------------------------主程式--------------------
iteration=500
popSize=30

workbook=xlrd.open_workbook("TSP51.xlsx")  #文件路径
worksheet=workbook.sheet_by_index(0)    
cityPosition=[]
city=[]
for i in range(worksheet.nrows):
    cityPosition.append(worksheet.row_values(i))
    city.append(cityPosition[i][0])
    cityPosition[i].pop(0)



cognitionFactor=1
socialFactor=1
loop_x=list()
loop_y=list()
count=0



global_value = 50000000
global_x=[]    
global_fitline=[]

run_time=[]
time_start =time.time()
for qq in range(30):
    print(qq)
    loop_x=list()
    loop_y=list()
    count=0

    random.seed(i)
    solver =PSO(popSize,city,cityPosition)     
    solver.distance()    
    solver.initialize()
    
    
    loop_x.append(0)
    loop_y.append(solver.globalBestSolutionValue)
    #print(loop_y)
    
    for i in range(iteration):
        count=count+1
        loop_x.append(time)
        #print("第",time,"圈")
        solver.move()
        solver.update()
    
        #print( "最小值為",solver.globalBestSolutionValue)
        loop_y.append(solver.globalBestSolutionValue)
        
    if solver.globalBestSolutionValue < global_value:
        global_value =solver.globalBestSolutionValue
        global_x = copy.deepcopy(solver.globalBestSolution)
        global_fitline =copy.deepcopy(loop_y)
        
        
    #solver.map()
    global_x.append(global_x[0])
    map_x=[]
    map_y=[]
    for i in range (len(global_x)):
        map_x.append(cityPosition[city.index(global_x[i])][0])
        map_y.append(cityPosition[city.index(global_x[i])][1])
    plt.plot(map_x,  map_y)
    plt.xlabel('PSO_route')
    plt.show()        
        
    #plt.plot(loop_x,  global_fitline)
    #plt.xlabel('PSO_fitline')
    #plt.show()
    
    print(global_value)
    run_time.append(global_value)
time_end =time.time()

print( "標",run_time.index( min(run_time) ) )

print("平均值", sum(run_time)/len(run_time))
print("最小值", min(run_time))


print("花費時間",time_end-time_start)

