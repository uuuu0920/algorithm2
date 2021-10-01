import random
import math
import copy
import matplotlib.pyplot as plt
import xlrd
workbook=xlrd.open_workbook("L32.xlsx")  #文件路径
worksheet=workbook.sheet_by_index(0)    
orthogonalArray=[[0]*worksheet.ncols]*worksheet.nrows

for i in range(worksheet.nrows):
    orthogonalArray[i]=worksheet.row_values(i)
roop_value=[]
for roop in range(30):
    
    random.seed(roop)

    class TGA():
        def __init__(self,pop_size,dimension,upper,lower,crossover_rate,mutation_rate):
            self.pop_size=pop_size
            self.dimension=dimension
            self.upper=upper
            self.lower=lower
            self.crossover_rate=crossover_rate
            self.mutation_rate=mutation_rate
            
            self.x=[]
            self.x_value=[]
            self.adaptive_value=[]
            
            self.best_x=[]
            self.best_x_value=0
            
            self.new_x=[]
            self.new_x_value=[]     
            
        
            
        #----------------------testfunction---------------------
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
        
    
        #--------------------------------------------------------
        def initialize (self):
            
            for i in range(self.pop_size):
                random.seed(i)
                x=[]            
                for j in range(self.dimension):
                    x.append(self.lower + (random.random() * (self.upper-self.lower)))
                self.x.append(x)
                
                """------------------------------------------------"""
                self.x_value.append(self.testfunction11(self.x[i]))
                                
            self.best_x=self.x[self.x_value.index(min(self.x_value))]
            self.best_x_value=min(self.x_value)
            
           
            
        def adaptive (self):
            self.adaptive_value=[0]*self.pop_size
            temp_adaptive=[0]*self.pop_size
            
            for i in range(self.pop_size):
                temp_adaptive[i]=1/(1+max(self.x_value)+self.x_value[i])
            for i in range(self.pop_size):
                self.adaptive_value[i]=temp_adaptive[i]/sum(temp_adaptive)
                    
        def crossover(self):
            #-----------------roulette--------------------
            
            crossover_time=round(self.crossover_rate*self.pop_size)
            for i in range(crossover_time):
                #print(i)
                break_point1=0
                break_point2=self.adaptive_value[0]
                hit=[]
                hit_rand=random.uniform(0, sum(self.adaptive_value))
                for j in range(self.pop_size):
                    if hit_rand>break_point1 and hit_rand<=break_point2:
                        hit.append(self.x[j])
                    if j <self.pop_size-1:
                        break_point1=break_point1 + self.adaptive_value[j]
                        break_point2=break_point2 + self.adaptive_value[j+1]
    
                
                hit_num2 = copy.copy(hit[0])
                while hit_num2 == hit[0]:
                    break_point1=0
                    break_point2=self.adaptive_value[0]
                    hit_rand=random.uniform(0, sum(self.adaptive_value))
                    for j in range(self.pop_size):
                        if hit_rand>break_point1 and hit_rand<=break_point2:
                            hit_num2=self.x[j]
                        if j <self.pop_size-1:
                            break_point1=break_point1 + self.adaptive_value[j]
                            break_point2=break_point2 + self.adaptive_value[j+1]  
                hit.append(hit_num2)
                
                #-------------------switch--------------------
                
                rand_breakpoint=random.randint(0,self.dimension-1)
                a=copy.copy(hit[0])
                b=copy.copy(hit[1])
                a[rand_breakpoint]=a[rand_breakpoint]+random.random()*(b[rand_breakpoint]-a[rand_breakpoint])
                b[rand_breakpoint]=lower+random.random()*(upper-lower)
                a[rand_breakpoint+1:],b[rand_breakpoint+1:]=b[rand_breakpoint+1:],a[rand_breakpoint+1:]
                self.new_x.append(a)
                self.new_x.append(b)
                
        def taguchi(self):
            taguchi_time=round((1/2)*self.crossover_rate*self.pop_size)
            for size in range(taguchi_time):
                rand=random.sample(self.new_x, 2) 
                a=copy.copy(rand[0])
                b=copy.copy(rand[1])
                taguchi=list()
                taguchi_value=list()
                for i in range(len(orthogonalArray)):
                    taguchi.append(copy.deepcopy(orthogonalArray[i][0:len(a)]))                
                for i in range(len(taguchi)-1):
                    for j in range(len(taguchi[i])):
                        if (orthogonalArray[i][j]==1.0):
                            taguchi[i][j]=a[j]
                        elif (orthogonalArray[i][j]==2.0):
                            taguchi[i][j]=b[j]
                            
                for i in range(len(taguchi)):
                    
                    """----------------------------------------------------"""
                    taguchi_value.append( self.testfunction11(taguchi[i]) )          
                
                optimalArray=list()   
                for i in range(len(taguchi[i])):
                    E=[0,0]
                    
                    for j in range(len(taguchi)):
                        if (orthogonalArray[j][i]==1.0):
                            E[0]=E[0]+1/(taguchi_value[j]**2)
                        
            
                        elif (orthogonalArray[j][i]==2.0):
                            E[1]=E[1]+1/(taguchi_value[j]**2)
                        
                    if E[0]>E[1]:
                        optimalArray.append(a[i])
                    elif E[1]>=E[0]:
                        optimalArray.append(b[i])
                self.new_x.append(optimalArray)
    
        def mutation(self):
            mutation_time=round(self.mutation_rate*self.pop_size)
            for i in range(mutation_time):
                rand=random.sample(self.new_x, 1)
                hit=rand[0]
                rand=random.sample(range(0,self.dimension), 2)
                hit[rand[0]],hit[rand[1]]=hit[rand[1]],hit[rand[0]]
                
                self.new_x.append(hit)
        #--------檢查串列是否重複--------------------       
        def index_of(self,val, in_list):
            try:
                return in_list.index(val)
            except ValueError:
                return -1
        #----------------------------------------------    
        def update(self):
            new_x=[]
            for i in range(len(self.new_x)):
                if  self.index_of(self.new_x[i],self.x) == -1:
                    new_x.append(self.new_x[i])
            
            for i in range(len(new_x)):
                """--------------------------------------------------------------------"""
                self.new_x_value.append( self.testfunction11(new_x[i]) )
                
                if self.new_x_value[i] <= max(self.x_value):
                    self.x.append(new_x[i])
                    self.x_value.append(self.new_x_value[i])
                    
                    self.x.pop(self.x_value.index(max(self.x_value)))
                    self.x_value.pop(self.x_value.index(max(self.x_value)))
                    
                    if self.new_x_value[i] < self.best_x_value:
                        self.best_x_value= copy.copy(self.new_x_value[i])
                        self.best_x= copy.deepcopy(new_x[i])
            self.new_x_value=[]
            self.new_x=[]
            
    
        
    #---------------------------主程式--------------------------
    pop_size = 30
    dimension = 30
    lower= -600
    upper = 600
    crossover_rate=0.4
    mutation_rate=0.1
    iteration=500
    fitline_x=[]
    fitline_y=[]
    
    solver= TGA(pop_size,dimension,upper,lower,crossover_rate,mutation_rate)
    solver.initialize()
    #print("初始",solver.best_x_value)
    
    
    fitline_x.append(0)
    fitline_y.append(solver.best_x_value)
    
    for i in range(1,iteration+1):
        #print("第",i,"圈")
    
        solver.adaptive()
    
        solver.crossover()
    
        solver.taguchi()
    
        solver.mutation()
       
        solver.update()
        fitline_x.append(i)
        fitline_y.append(solver.best_x_value)
        print("第",roop+1,"次 第",i,"圈")
    roop_value.append(solver.best_x_value)
#plt.plot(fitline_x,  fitline_y)
#plt.xlabel('TGA')
#plt.show()

print("500 Dimension平均值: ",sum(roop_value)/len(roop_value))    