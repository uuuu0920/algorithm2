import random
import math
import copy
import sys
import matplotlib.pyplot as plt
import numpy as np

import testfunction


class SMO():
    def __init__(self,pop_size , dimension , lower , upper, MG , GLL , LLL , pr):
        self.pop_size = pop_size
        self.dimension = dimension
        self.lower = lower
        self.upper = upper
        self.MG = MG
        self.GLL = GLL
        self.LLL = LLL
        self.pr = pr
        
        self.group=1
        
        self.x =[]
        self.x_value =[]
        self.x_fitness =[]
        self.prob =[]
        
        self.local_leader =[]
        self.local_leader_value =[]
        
        self.global_leader =[]
        self.global_leader_value = 0
        
        self.global_leader_count=0
        self.local_leader_count=[0]*self.group
        
    def initialize(self):
        for g in range(self.group):
            x_value=[]
            x_group=[]
            for i in range(self.pop_size):
                x=[]

                for j in range(self.dimension):
                    
                    x.append(self.lower + random.random()*(self.upper - self.lower))
                x_value.append( testfunction.testfunction11( x ))
                
                x_group.append(x)
            self.x_value.append(x_value)
            self.x_fitness.append(fitness_function(x_value))
            self.x.append(x_group)

            
            
        for g in range(self.group):

            self.local_leader_value.append(min(self.x_value[g]))
            self.local_leader.append(self.x[g] [self.x_value[g].index( min(self.x_value[g]) ) ])
        self.global_leader_value = min(self.local_leader_value)
        self.global_leader = copy.deepcopy(self.local_leader[self.local_leader_value.index( min(self.local_leader_value) )])
            
    def local_leader_phase(self):

        for g in range(self.group):
            for i in range(len(self.x[g])):
                
                    
                new_x=[]
                new_x_value=0
                random_num=random.randint(0,len(self.x[g])-1)
                while random_num == i:
                    random_num=random.randint(0,len(self.x[g])-1) 
                for j in range(self.dimension):
                    if random.random()>=self.pr:
                        new_x.append(self.x[g][i][j] + (random.random()*(self.local_leader[g][j] - self.x[g][i][j])) + (-1+(2*random.random()))*(self.x[g][random_num][j] - self.x[g][i][j])  )
                    else:
                        new_x.append(self.x[g][i][j])
                    
                new_x_value=testfunction.testfunction11( new_x )
                if new_x_value< self.x_value[g][i]:
                    self.x_value[g][i] = new_x_value
                    self.x[g][i] = copy.deepcopy(new_x)
       
        self.prob=[]             
        for g in range(self.group):
            prob = []
            for i in range(len(self.x[g])):
                prob.append(0.9 * (self.x_fitness[g][i] / max(self.x_fitness[g]) ) +0.1)
            self.prob.append(prob)
            
    def global_leader_phase(self):

        for g in range(self.group):
            for i in range(len(self.x[g])):
                if random.random() < self.prob[g][i]:

                    
                    new_x=copy.deepcopy(self.x[g][i])
                    new_x_value=0  
                    selected = random.sample(range(self.dimension), random.randint(1, self.dimension))
                                      
                    random_num=random.randint(0,len(self.x[g])-1)
                    while random_num == i:
                        random_num=random.randint(0,len(self.x[g])-1) 
                    for j in selected:
                        new_x[j] =self.x[g][i][j] + (random.random()*(self.global_leader[j] - self.x[g][i][j])) + ((-1+(2*random.random()))*(self.x[g][random_num][j] - self.x[g][i][j]))  
                        
                    new_x_value=testfunction.testfunction11( new_x )
                    if new_x_value< self.x_value[g][i]:
                        self.x_value[g][i] = new_x_value
                        self.x[g][i] = copy.deepcopy(new_x)
                        
    def global_learning_phase(self):
        x_value_min=[]
        x_min=[]
        for g in range(self.group):
            x_value_min.append(min(self.x_value[g]))
            x_min.append(self.x[g][self.x_value.index(self.x_value[g] )])

        
        
        
        new_GL_value = min(x_value_min)
        if new_GL_value < self.global_leader_value:
            self.global_leader_count =0
            self.global_leader_value = min(x_value_min)
            self.global_leader = copy.deepcopy(x_min[x_value_min.index(min(x_value_min))])
        else:
            self.global_leader_count +=1

    def local_learning_phase(self):

        for g in range(self.group):
            new_LL_value = min(self.x_value[g])
            if new_LL_value < self.local_leader_value[g]:
                self.local_leader_count[g] =0
                self.local_leader_value[g] = min(self.x_value[g])
                self.local_leader[g] = self.x[g][self.x_value[g].index(min(self.x_value[g]))]
            else:
                self.local_leader_count[g] +=1   
                    
    def local_leader_decision_phase(self):
        for g in range(self.group):
            if self.local_leader_count[g] ==self.LLL:

                self.local_leader_count[g] = 0
                for i in range(len(self.x[g])):
                    for j in range(self.dimension):
                        if random.random() >= self.pr:
                            self.x[g][i][j] = self.lower + (random.random() *(self.upper - self.lower))
                        else:
                            random_num=random.randint(0,len(self.x[g])-1)
                            while random_num == i:
                                random_num=random.randint(0,len(self.x[g])-1) 
                            self.x[g][i][j] = self.x[g][i][j] + (random.random()*(self.global_leader[j] - self.x[g][i][j])) + (random.random()*(self.x[g][random_num][j] - self.local_leader[g][j]))
                            
                            
    def global_leader_decision_phase(self):
        if self.global_leader_count == self.GLL:
            self.global_leader_count=0      
            if self.group < self.MG:

                new_x=[]
                new_x_value=[]
                new_x_fitness =[]

                
                
                for g in range(self.group):
                    for i in range(len(self.x[g])):
                        new_x.append(self.x[g][i])
                        new_x_value.append(self.x_value[g][i])
                        new_x_fitness.append(self.x_fitness[g][i])
                        
                self.group+=1
                
                self.local_leader_count=[0]*self.group
                self.x =[]
                self.x_value =[]
                self.x_fitness =[]
                
                one = math.floor( self.pop_size/self.group )
                for g in range(self.group):
                    if g==self.group-1:
                        self.x.append(new_x[one*g:])
                        self.x_value.append(new_x_value[one*g:])
                        self.x_fitness.append(new_x_fitness[one*g:])

                    else:
                        self.x.append(new_x[one*g:one*(g+1)])
                        self.x_value.append(new_x_value[one*g:one*(g+1)])
                        self.x_fitness.append(new_x_fitness[one*g:one*(g+1)])
                        
                        
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
                new_x_fitness =[]
            
                for g in range(self.group):
                    for i in range(len(self.x[g])):
                        new_x.append(self.x[g][i])
                        new_x_value.append(self.x_value[g][i])
                        new_x_fitness.append(self.x_fitness[g][i])
                        
                self.group=1     
                
                self.local_leader_count=[0]*self.group
                self.x =[]
                self.x_value =[]
                self.x_fitness =[]                    
                
                self.x.append(new_x)
                self.x_value.append(new_x_value)
                self.x_fitness.append(new_x_fitness)
                
                self.local_leader_value=[]
                self.local_leader=[]
                for g in range(self.group):
                    
                    self.local_leader_value.append(min(self.x_value[g]))
                    self.local_leader.append( self.x[g][  self.x_value[g].index(min(self.x_value[g])  )] )
                    

                self.global_leader_value = min(self.local_leader_value)
                self.global_leader= copy.deepcopy(self.local_leader[ self.local_leader_value.index(min(self.local_leader_value)) ])
      
def fitness_function(x):
    a= copy.copy(x)
    for i in range(len(a)):
        if a[i] >=0:
            a[i] = 1/(1+a[i])
        else:
            a[i] = 1+abs(a[i])
    return a

fitline_x=[]
fitline_y=[]
    
pop_size = 30
dimension = 30
lower = -600
upper = 600


MG = round(pop_size/10)
GLL= round((pop_size*2 - pop_size/2)/3*2)
LLL=dimension*pop_size/10
pr = 0.7

value=[]
for qq in range(30):
    
    print(qq)
    random.seed(qq)
    np.random.seed(qq)
    solver = SMO(pop_size , dimension , lower , upper , MG , GLL , LLL , pr)
    solver.initialize()

    fitline_x.append(0)
    fitline_y.append(solver.global_leader_value)



    for i in range(500):
        #print("迴圈",i)
        solver.local_leader_phase()
    
        solver.global_leader_phase()
    
        solver.global_learning_phase()
    
        solver.local_learning_phase()
        solver.local_leader_decision_phase()
        solver.global_leader_decision_phase()
        #print(solver.global_leader_value)
        fitline_x.append(i+1)
        fitline_y.append(solver.global_leader_value)
    value.append(solver.global_leader_value)
    print(solver.global_leader_value)

print("30次平均值",sum(value) / len(value))
print("最小值",min(value))    
#plt.plot(fitline_x,  fitline_y)
#plt.show()