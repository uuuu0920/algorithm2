import random
import math
import copy
import matplotlib.pyplot as plt
import xlrd
import time
import numpy as np

#----------------------------
workbook=xlrd.open_workbook("TSP38.xlsx")  #文件路径
worksheet=workbook.sheet_by_index(0)    
city_position=np.zeros((worksheet.nrows,2))
#city= np.chararray(14)
city=list()
for i in range(worksheet.nrows):
    city.append(worksheet.cell(i,0).value)
    city_position[i][0]=worksheet.cell(i,1).value
    city_position[i][1]=worksheet.cell(i,2).value
city=np.array(city)
#---------------------------------

class AntColonyOptimization:
    def __init__(self,city,city_position,pop_size,pheromone_drop_amount,p,alpha,beta):
        
        self.city = city
        self.city_position= city_position
        self.pop_size = pop_size
        self.pheromone_drop_amount = pheromone_drop_amount
        self.p = p
        self.alpha =alpha
        self.beta= beta
        
        self.x= np.zeros((self.pop_size,len(self.city)),dtype=int)
        self.x_value = np.zeros(self.pop_size)
        self.best_x=np.zeros(len(self.city))
        self.best_x_value =9999999999
        
        self.distance = np.zeros( (len(self.city),len(self.city) ) )
        self.visibility = np.zeros( (len(self.city),len(self.city) ) )
        self.pheromone_map = np.ones((len(self.city),len(self.city)))
        self.candidate = np.zeros((self.pop_size,len(self.city)))
        
    def compute_total_distance(self,x):       
        x_list =list(map(int, x.tolist()))
        total_distance=0
        solution_plus=copy.deepcopy(x_list)   
        solution_plus.append(x_list[0])
        for i in range(len(solution_plus)-1):
            total_distance+=self.distance[solution_plus[i]][solution_plus[i+1]]         
        return total_distance

    def initialize (self):
        for i in range(len(self.city)):
            for j in range(len(self.city)):
                self.distance[i][j] = ((self.city_position[i][0]-self.city_position[j][0])**2 + (self.city_position[i][1]-self.city_position[j][1])**2) **(1/2)
                if i !=j:                   
                    self.visibility[i][j] = 1/self.distance[i][j]
        
    def ant(self):
        for each in range(len(self.x)):
            
            one_solution =np.zeros(len(self.city))
            candidates = [i for i in range(len(self.city))]
            #random choose city as first city 
            current_city = random.choice(candidates)
            one_solution[0] = current_city
            candidates.remove(current_city)
        
            for t in range(1,len(self.city)-1):
                #best
                fitness_list = []
                for i in candidates:
                    fitness = pow(self.pheromone_map[current_city][i],self.alpha)*\
                        pow(self.visibility[current_city][i],self.beta)
                    fitness_list.append(fitness)
                
                total_fitness = sum(fitness_list)
                transition_probability = [fitness/total_fitness for fitness in fitness_list]
                
                hit = random.random()
                
                sum_prob = 0
                for i in range(len(transition_probability)):
                    sum_prob += transition_probability[i]
                    if hit < sum_prob:
                        next_city_id = candidates[i]
                        break
                        
                 
                candidates.remove(next_city_id)
                one_solution[t] = next_city_id
                
                current_city = next_city_id
            one_solution[-1] = candidates.pop()
            self.x[each] = one_solution
            self.x_value[each] = self.compute_total_distance(self.x[each])
            
            if self.x_value[each] < self.best_x_value:
                self.best_x_value = self.x_value[each]
                self.best_x = np.copy(self.x[each])
                
            
    def pheromone(self):
        #evaporate hormones all the path
        self.pheromone_map *= (1-p)
                
        #Add hormones to the path of the ants
        for i in range(len(self.x)):
            for j in range(len(self.x[i])):
                if j == len(self.x[i])-1:
                    self.pheromone_map[ self.x[i][j],self.x[i][0] ] += self.pheromone_drop_amount
                else:
                    
                    self.pheromone_map[ self.x[i][j],self.x[i][j+1] ] += self.pheromone_drop_amount

pop_size = 30
iteration=500
pheromone_drop_amount = 0.003
p = 0.1 #evaporate_rate
alpha = 1 #pheromone_factor
beta = 3 #heuristic_factor
run_time=[]
time_start =time.time()

for qq in range(30):
    print(qq)
    fitness_line_x=[]
    fitness_line_y=[]
    
    random.seed(qq)
    np.random.seed(qq)
    solver = AntColonyOptimization(city,city_position,pop_size,pheromone_drop_amount,p,alpha,beta)
    solver.initialize()
  
    for i in range(iteration):    
        solver.ant()
        solver.pheromone()
        fitness_line_x.append(i)
        fitness_line_y.append(solver.best_x_value)
        
    run_time.append(solver.best_x_value)

    plt.plot(fitness_line_x,  fitness_line_y)
    plt.xlabel('SMO_fitline')
    plt.show()
    
    #----------------------------------------------------
    map_x=[]
    map_y=[]
    best_x_list = solver.best_x.tolist()

    for i in best_x_list:
        map_x.append(city_position[i][0])
        map_y.append(city_position[i][1])
        
    map_x.append(city_position[best_x_list[0]][0])
    map_y.append(city_position[best_x_list[0]][1])
    plt.plot(map_x,  map_y)
    plt.xlabel('ACO_route')
    plt.show()
    #----------------------------------------------------
    ans=[]
    print(best_x_list)
    for i in range(len(best_x_list)) :
        ans.append(city[best_x_list[i]])
    print('最佳路線' , ans)
    print('總長度' , solver.best_x_value)
        

print( "標",run_time.index( min(run_time) ) )
print("平均值", sum(run_time)/len(run_time))
print("最小值", min(run_time))
time_end =time.time()
print("花費時間",time_end-time_start)
#----------------------------------------------------