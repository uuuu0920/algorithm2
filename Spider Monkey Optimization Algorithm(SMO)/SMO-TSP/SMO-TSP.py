import random
import math
import copy
import matplotlib.pyplot as plt
import xlrd
import time
class SMO():
    def __init__(self, pop_size , city , city_position , MG , GLL , LLL , pr):
        self.pop_size=pop_size
        self.city=copy.deepcopy(city)
        self.city_position=copy.deepcopy(city_position)
        self.path=[] #各城市間距離矩陣

        self.MG = MG
        self.GLL = GLL
        self.LLL = LLL
        self.pr = pr
        self.group=1
        
        self.x =[]
        self.x_value =[]
        self.original_value=[]
        self.prob =[]
        
        self.local_leader =[]
        self.local_leader_value =[]
        
        self.global_leader =[]
        self.global_leader_value = 0
        
        self.global_leader_count=0
        self.local_leader_count=[0]*self.group
        
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
                path[i][y]=between_distance(city_position[i][0],city_position[y][0],city_position[i][1],city_position[y][1])
        self.path=copy.deepcopy(path)
        
    def initialize (self):
        
        for g in range(self.group):
            total=[]
            total_value=[]
            for i in range(self.pop_size):
                
                x = copy.deepcopy(city)            
                random.shuffle(x)
                
                
                total_value.append(self.testFunction1(x,self.path)) 
                total.append(x)
            self.x.append(total)
            self.x_value.append(total_value)
            self.local_leader_value.append(min(self.x_value[g]))
            self.local_leader.append( self.x[g][ self.x_value[g].index( (min(self.x_value[g])) ) ] )
            
            self.global_leader = copy.deepcopy(self.local_leader[0])
            self.global_leader_value=self.local_leader_value[0]
            
            self.original_value = copy.deepcopy(self.x_value)
            
    def local_leader_phase(self):
        for g in range(self.group):
            for i in range( len(self.x[g]) ):
                if random.random() >= self.pr:
                        
                    
                    ss= []
                    
                    # ss1 (local_leader - x)
                    
                    current=copy.deepcopy(self.x[g][i])                
                    ss1=[]
                    for j in range(len(current)):
                        if current[j] != self.local_leader[g][j]:
                            temp=current.index(self.local_leader[g][j])
                            current[j],current[temp]=current[temp],current[j]
                            ss1.append([j,temp])
                            
                    #random * ss1
                    random_len= round(random.random()*len(ss1))
                    if random_len != 0:
                    #position=random.randint(0, len(individualV)-c1) 
                        for j in range(random_len):
                            ss.append(ss1[j])
    
                    # ss2 (random_x - x)
                    
                    current=copy.deepcopy(self.x[g][i])                
                    ss2=[]
                    random_x = copy.deepcopy( self.x[g][ random.randint(0,len(self.x[g])-1) ] )
                    if random_x ==current:
                        random_x = copy.deepcopy( self.x[g][ random.randint(0,len(self.x[g])-1) ] )
    
                    for j in range(len(current)):
                        if current[j] != random_x:
                            temp=current.index(random_x[j])
                            current[j],current[temp]=current[temp],current[j]
                            ss2.append([j,temp])
                            
                    #random * ss2
                    random_len= round(random.random()*len(ss2))
                    if random_len != 0:
                    #position=random.randint(0, len(individualV)-c1) 
                        for j in range(random_len):
                            ss.append(ss2[j])  
           
                    new_x=copy.deepcopy(self.x[g][i])
                    for j in range(len(ss)):
                        new_x[ss[j][0]],new_x[ss[j][1]] =new_x[ss[j][1]],new_x[ss[j][0]]
                        
                    # Basic SS
                    current=copy.deepcopy(self.x[g][i])                
                    ss=[]
                    for j in range(len(current)):
                        if current[j] != new_x[j]:
                            temp=current.index(new_x[j])
                            current[j],current[temp]=current[temp],current[j]
                            ss.append([j,temp])
    
                            
                    new_x=copy.deepcopy(self.x[g][i])
                    for j in range(len(ss)):
                        new_x[ss[j][0]],new_x[ss[j][1]] =new_x[ss[j][1]],new_x[ss[j][0]]
                        new_x_value = self.testFunction1(new_x,self.path)
                        if new_x_value <self.x_value[g][i]:
                            self.x[g][i] = copy.deepcopy(new_x)
                            self.x_value[g][i] = new_x_value


    def global_leader_phase(self):
        min_cost=[]
        for g in range(self.group):
            min_cost.append(min(self.x_value[g]))
        min_cost=min(min_cost)
        
        for g in range(self.group):
            for i in range(len(self.x[g])):
                if random.random() <= (0.9* (min_cost/self.x_value[g][i])) + 0.1:
                        
                    
                    ss= []
                    
                    # ss1 (global_leader - x)
                    
                    current=copy.deepcopy(self.x[g][i])                
                    ss1=[]
                    for j in range(len(current)):
                        if current[j] != self.global_leader[j]:
                            temp=current.index(self.global_leader[j])
                            current[j],current[temp]=current[temp],current[j]
                            ss1.append([j,temp])
                            
                    #random * ss1
                    random_len= round(random.random()*len(ss1))
                    if random_len != 0:
                    #position=random.randint(0, len(individualV)-c1) 
                        for j in range(random_len):
                            ss.append(ss1[j])
    
                    # ss2 (random_x - x)
                    
                    current=copy.deepcopy(self.x[g][i])                
                    ss2=[]
                    random_x = copy.deepcopy( self.x[g][ random.randint(0,len(self.x[g])-1) ] )
                    if random_x ==current:
                        random_x = copy.deepcopy( self.x[g][ random.randint(0,len(self.x[g])-1) ] )
    
                    for j in range(len(current)):
                        if current[j] != random_x:
                            temp=current.index(random_x[j])
                            current[j],current[temp]=current[temp],current[j]
                            ss2.append([j,temp])
                            
                    #random * ss2
                    random_len= round(random.random()*len(ss2))
                    if random_len != 0:
                    #position=random.randint(0, len(individualV)-c1) 
                        for j in range(random_len):
                            ss.append(ss2[j])  
           
                    new_x=copy.deepcopy(self.x[g][i])
                    for j in range(len(ss)):
                        new_x[ss[j][0]],new_x[ss[j][1]] =new_x[ss[j][1]],new_x[ss[j][0]]
                        
                    # Basic SS
                    current=copy.deepcopy(self.x[g][i])                
                    ss=[]
                    for j in range(len(current)):
                        if current[j] != new_x[j]:
                            temp=current.index(new_x[j])
                            current[j],current[temp]=current[temp],current[j]
                            ss.append([j,temp])
    
                            
                    new_x=copy.deepcopy(self.x[g][i])
                    for j in range(len(ss)):
                        new_x[ss[j][0]],new_x[ss[j][1]] =new_x[ss[j][1]],new_x[ss[j][0]]
                        new_x_value = self.testFunction1(new_x,self.path)
                        if new_x_value <self.x_value[g][i]:
                            self.x[g][i] = copy.deepcopy(new_x)
                            self.x_value[g][i] = new_x_value    
    def update(self):
        for g in range(self.group):
            if min(self.x_value[g]) < self.local_leader_value[g]:
                self.local_leader_count[g] =0
                
                self.local_leader[g] = copy.deepcopy(self.x[g][ self.x_value[g].index(  min(self.x_value[g]) ) ])
                self.local_leader_value[g] = min(self.x_value[g])
            else:
                self.local_leader_count[g] +=1
        
        if min(self.local_leader_value) < self.global_leader_value:
            self.global_leader = copy.deepcopy( self.local_leader [self.local_leader_value.index(min(self.local_leader_value))] )
            self.global_leader_value = min(self.local_leader_value)
            
            self.global_leader_count = 0
            
        else:
            self.global_leader_count +=1

    def decision(self):
        for g in range(self.group):
            if self.local_leader_count[g] > self.LLL:
                
                self.local_leader_count[g] = 0
                
                for i in range(len(self.x[g])):
                    if random.random() >= self.pr:
                        self.x[g][i] = copy.deepcopy(city)
         
                        random.shuffle(self.x[g][i])  
                        self.x_value[g][i]=self.testFunction1(self.x[g][i],self.path)
                    else:
                        ss= []
                        
                        # ss1 (global_leader - x)
                        
                        current=copy.deepcopy(self.x[g][i])                
                        ss1=[]
                        for j in range(len(current)):
                            if current[j] != self.global_leader[j]:
                                temp=current.index(self.global_leader[j])
                                current[j],current[temp]=current[temp],current[j]
                                ss1.append([j,temp])
                                
                        #random * ss1
                        random_len= round(random.random()*len(ss1))
                        if random_len != 0:
                        #position=random.randint(0, len(individualV)-c1) 
                            for j in range(random_len):
                                ss.append(ss1[j])
        
                        # ss2 (x - local_leader)
                        
                        current=copy.deepcopy(self.local_leader[g])                
                        ss2=[]
        
                        for j in range(len(current)):
                            if current[j] != self.x[g][i][j]:
                                temp=current.index(self.x[g][i][j])
                                current[j],current[temp]=current[temp],current[j]
                                ss2.append([j,temp])
                                
                        #random * ss2
                        random_len= round(random.random()*len(ss2))
                        if random_len != 0:
                        #position=random.randint(0, len(individualV)-c1) 
                            for j in range(random_len):
                                ss.append(ss2[j])  
               
                        for j in range(len(ss)):
                            self.x[g][i][ss[j][0]],self.x[g][i][ss[j][1]] =self.x[g][i][ss[j][1]],self.x[g][i][ss[j][0]]                  
                        self.x_value[g][i]=self.testFunction1(self.x[g][i],self.path)
        
        
        if self.global_leader_count > self.GLL:
            self.global_leader_count =0
            if self.group < self.MG:
                new_x=[]
                new_x_value=[]
                for g in range(self.group):
                    for i in range(len(self.x[g])):
                        new_x.append(self.x[g][i])
                        new_x_value.append(self.x_value[g][i])
                self.group+=1
                
                self.local_leader_count=[0]*self.group
                self.x =[]
                self.x_value =[]
                one = math.floor( self.pop_size/self.group )
                for g in range(self.group):
                    if g==self.group-1:
                        self.x.append(new_x[one*g:])
                        self.x_value.append(new_x_value[one*g:])
                    else:
                        self.x.append(new_x[one*g:one*(g+1)])
                        self.x_value.append(new_x_value[one*g:one*(g+1)])
                        
                self.local_leader_value=[]
                self.local_leader=[]
                for g in range(self.group):
                    
                    self.local_leader_value.append(min(self.x_value[g]))
                    self.local_leader.append( self.x[g][  self.x_value[g].index(min(self.x_value[g])  )] )
                    
                self.global_leader_value = min(self.local_leader_value)
                self.global_leader= copy.deepcopy(self.local_leader[ self.local_leader_value.index(min(self.local_leader_value)) ])

            else:
                new_x=[]
                new_x_value=[]
            
                for g in range(self.group):
                    for i in range(len(self.x[g])):
                        new_x.append(self.x[g][i])
                        new_x_value.append(self.x_value[g][i])
                        
                self.group=1     
                
                self.local_leader_count=[0]*self.group
                self.x =[]
                self.x_value =[]                  
                
                self.x.append(new_x)
                self.x_value.append(new_x_value)
                
                self.local_leader_value=[]
                self.local_leader=[]
                for g in range(self.group):
                    
                    self.local_leader_value.append(min(self.x_value[g]))
                    self.local_leader.append( self.x[g][  self.x_value[g].index(min(self.x_value[g])  )] )
                    

                self.global_leader_value = min(self.local_leader_value)
                self.global_leader= copy.deepcopy(self.local_leader[ self.local_leader_value.index(min(self.local_leader_value)) ])
                
            

#----------------------------
workbook=xlrd.open_workbook("TSP51.xlsx")  #文件路径
worksheet=workbook.sheet_by_index(0)    
city_position=[]
city=[]
for i in range(worksheet.nrows):
    city_position.append(worksheet.row_values(i))
    city.append(city_position[i][0])
    city_position[i].pop(0)
#---------------------------------


pop_size = 100
iteration = 500


MG = 5
GLL= 100
LLL=50
pr = 0.1


run_time=[]
time_start =time.time()
for qq in range(30):
    random.seed(qq)
    #print(qq)
    fitness_line_x=[]
    fitness_line_y=[]
    
    solver = SMO(pop_size , city , city_position  , MG , GLL , LLL , pr)
    solver.distance()
    solver.initialize()
    fitness_line_x.append(0)
    fitness_line_y.append(solver.global_leader_value)
    #print(solver.global_leader_value)
    for i in range(iteration):
        print(qq,i)
        solver.local_leader_phase()
        solver.global_leader_phase()
        solver.update()
        solver.decision()
        fitness_line_x.append(i+1)
        fitness_line_y.append(solver.global_leader_value)
    #print(solver.global_leader_value)
    run_time.append(solver.global_leader_value)

    plt.plot(fitness_line_x,  fitness_line_y)
    plt.xlabel('SMO_fitline')
    plt.show()
    
    map_x=[]
    map_y=[]
    for i in range (len(solver.global_leader)):
        map_x.append(city_position[city.index(solver.global_leader[i])][0])
        map_y.append(city_position[city.index(solver.global_leader[i])][1])
        
    map_x.append(city_position[city.index(solver.global_leader[0])][0])
    map_y.append(city_position[city.index(solver.global_leader[0])][1])
    plt.plot(map_x,  map_y)
    plt.xlabel('PSO_route')
    plt.show()  
print( "標",run_time.index( min(run_time) ) )

print("平均值", sum(run_time)/len(run_time))
print("最小值", min(run_time))


time_end =time.time()
print("花費時間",time_end-time_start)