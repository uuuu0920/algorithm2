import random
import math
import copy
import matplotlib.pyplot as plt
import numpy as np
import testfunction
import time

class WOA():
    def __init__(self,pop_size,dimension,max_iter,lower,upper):

        
        self.pop_size=pop_size
        self.dimension=dimension
        self.max_iter = max_iter
        self.upper= upper
        self.lower= lower

        
        self.x = np.zeros((self.pop_size,self.dimension))
        self.x_value = np.zeros(self.pop_size)

        self.best_x=[]
        self.best_x_value=0




    def initialize (self):
        self.x = self.lower + (np.random.rand(self.pop_size,self.dimension)*(self.upper - self.lower))
        for i in range(self.pop_size):
            
            #--------------------------------------------------
            self.x_value[i] = testfunction.testfunction11(self.x[i])
            #------------------------------------------------------

        
        self.best_x_value = np.min(self.x_value)
        self.best_x = np.copy(self.x[np.argmin(self.x_value)])
    def main (self):
        x_fitline = []
        y_fitline= []
        for iter in range(self.max_iter):
            a= 2-iter*((2)/self.max_iter) #a decreases linearly from 2 to 0
            a2 = -1+iter*((-1)/self.max_iter) #-1 to -2
            
            for i in range(self.pop_size):
                A = 2*a*random.random()-a
                C= 2*random.random()
                
                b = 1
                l = (a2-1)*random.random()+1
                
                if random.random() < 0.5:
                    if abs(A) >=1:
                        rand = random.randint(0, self.pop_size-1)
                        self.x[i] = self.x[rand] - A*abs(C*self.x[rand]-self.x[i])
                    else:

                        self.x[i] = self.best_x - A*abs(C*self.best_x-self.x[i])
                else:
                    self.x[i] = abs(self.best_x-self.x[i]) *math.exp(b*l)*math.cos(2*l*math.pi) +self.best_x
                    
                self.x[i] =np.clip(self.x[i],self.lower,self.upper)
                
                #--------------------------------------------------------------
            
                self.x_value[i] = testfunction.testfunction11(self.x[i])
                
                #-----------------------------------------------------------------
                
            if np.min(self.x_value) < self.best_x_value:
                self.best_x_value = np.min(self.x_value)
                self.best_x = np.copy(self.x[np.argmin(self.x_value)])
            
            x_fitline.append(iter)
            y_fitline.append(self.best_x_value)
        plt.plot(x_fitline,  y_fitline)
        plt.show()
            
                

                        
                

        

            
        
pop_size = 30
dimension=30
max_iter=500
lower=-600
upper=600


time_start =time.time()
cal_value=[]
for qq in range(30):
    print("第",qq,"圈")
    random.seed(qq)
    np.random.seed(qq)
    solver = WOA(pop_size,dimension,max_iter,lower,upper)
    solver.initialize()
    
    solver.main()
    #print(solver.best_x_value)
    
    cal_value.append(solver.best_x_value)
    #print(solver.best_x)

print("標",cal_value.index( min(cal_value) ))    
print("30次平均值",sum(cal_value) / len(cal_value))
print("最小值",min(cal_value))    

time_end =time.time()
print("花費時間",time_end-time_start)


