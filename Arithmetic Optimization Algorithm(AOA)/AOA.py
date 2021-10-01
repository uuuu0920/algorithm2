import random
import math
import copy
import sys
import matplotlib.pyplot as plt
roop_value=[]
for roop in range(1):
    
    random.seed(roop)
    class AOA():
        def __init__(self,pop_size,dimension,upper,lower,MOP_max,MOP_min,alpha,mu,iteration):
            self.pop_size = pop_size
            self.dimension = dimension
            self.upper = upper
            self.lower = lower
            self.MOP_max= MOP_max
            self.MOP_min = MOP_min
            self.alpha = alpha
            self.mu =mu
            self.iteration = iteration
            self.begin=0
            self.global_best_value=0
            self.global_best=[]
        
            self.x=[]
            self.x_value =[]
            self.best_x=[]
            self.best_x_value=0        
            self.new_x=[]
            self.new_x_value=0
            
            self.fitline_x=[]
            self.fitline_y=[]
    
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
        
        def testfunction12(self,x):
            a=10
            k=1000
            m=4
            u=[]
            y=[]
            for i in range(1,len(x)+1):
                y.append(1+((x[i-1]+1)/4))
                
                if x[i-1] > a:
                    u.append(k*((x[i-1]-a)**m))
                elif -a <= x[i-1]:
                    u.append(k*(-x[i-1]-a)**m)
                    
                    
            value=0
            value1=0
            value2=sum(u)
            
            for i in range(0,len(x)-1):
                value1=value1+  ((y[i]-1)**2) *(1+ (10*math.sin(math.pi*y[i+1])**2) +value2 )
                
            value= (math.pi/len(x)) * (10*math.sin(math.pi*y[0])) +value1
            return value
    
                            
            return value     
        def initialize (self):
            
            for i in range(self.pop_size):
                #random.seed(i)
                x=[]            
                for j in range(self.dimension):
                    x.append(self.lower + (random.random() * (self.upper-self.lower)))
                self.x.append(x)
                
                #------------------------------------------------
                self.x_value.append(self.testfunction1(self.x[i]))
                    
                
    
            self.best_x=self.x[self.x_value.index(min(self.x_value))]
            self.best_x_value=min(self.x_value)
            
            self.fitline_y.append(self.best_x_value)
            self.fitline_x.append(0)
            self.begin=self.best_x_value
            
    
        #--------檢查串列是否重複--------------------       
        def index_of(self,val, in_list):
            try:
                return in_list.index(val)
            except ValueError:
                return -1
        #----------------------------------------------
    
                    
        def AOA_main(self):
            
            for i in range(1,self.iteration+1):
                print("第",roop,"次 第",i,"圈")
                MOA = self.MOP_min + i *((self.MOP_max-self.MOP_min)/self.iteration)
                MOP = 1-((i**(1/alpha))/(self.iteration**(1/alpha)))
    
                
                
                
                for j in range(self.pop_size):
                    self.new_x = []
                    
                    for k in range(self.dimension):
                        r1= random.random()
                        
                        if r1 > MOA:
                            r2= random.random()
                            if r2 > 0.5: #(*)
                                self.new_x.append(self.best_x[k] * (MOP * ((self.upper-self.lower) *mu +lower)))
                            else: #(/)
                                self.new_x.append((self.best_x[k] / ((MOP+sys.float_info.epsilon)) * ((self.upper-self.lower) *mu +lower)))
                                
                        else:
                            r3 =random.random()
                            if r3 >0.5: #(+)
                                self.new_x.append(self.best_x[k] + (MOP * ((self.upper-self.lower) *mu +lower)))
                            else: #(-)          
                                self.new_x.append(self.best_x[k] -( MOP * ((self.upper-self.lower) *mu +lower)))
                                
                        if self.new_x[k]>self.upper:
                            self.new_x[k] = self.upper
                        elif  self.new_x[k]<lower:    
                            self.new_x[k] = self.lower
    
                    
                    if  self.index_of(self.new_x,self.x) == -1:
                        #-----------------------------------------------------------------------------------------
                        self.new_x_value=self.testfunction1(self.new_x)
    
                    
                        if self.new_x_value < self.x_value[j]:
                            #print("switch",self.x_value[j],self.x[j],self.new_x_value,self.new_x)                    
                            self.x[j]=copy.deepcopy(self.new_x)
                            self.x_value[j]= self.new_x_value
                        
                            if self.new_x_value<self.best_x_value:
                                self.best_x=self.new_x
                                self.best_x_value=self.new_x_value
    
          
                self.fitline_y.append(self.best_x_value)
                self.fitline_x.append(i)
    
                #print("best_x_value",self.best_x_value) 
                
    
    
                
            
            
    pop_size = 30
    dimension = 30
    lower= -100
    upper = 100
    
    MOP_max = 1
    MOP_min = 0.2
    alpha= 5
    mu = 0.499
    iteration =500
    
    solver = AOA(pop_size,dimension,upper,lower,MOP_max,MOP_min,alpha,mu,iteration)
    
    solver.initialize() 
    
    
    #print("best_x_value",solver.best_x_value)      
    solver.AOA_main()
    roop_value.append(solver.best_x_value)
    #print("")
    #print("初始最佳解=",solver.begin)
    
print("500 Dimension平均值: ",sum(roop_value)/len(roop_value))    
    
    #plt.plot(solver.fitline_x,  solver.fitline_y)
    #plt.xlabel('Dimension=30')
    #plt.show()
    
