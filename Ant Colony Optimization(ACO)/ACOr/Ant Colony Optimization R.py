import random
import math
import copy
import matplotlib.pyplot as plt
import numpy as np
import testfunction
import time

class ACOR():
    def __init__(self,pop_size,dimension,max_iter,lower,upper,q,z):

        
        self.pop_size=pop_size
        self.dimension=dimension
        self.max_iter = max_iter
        self.upper= upper
        self.lower= lower
        self.q = q
        self.z = z
      
        self.x = np.zeros((self.pop_size,self.dimension+1))
        
        self.gsw = np.zeros(self.pop_size)
        self.total_gsw = np.zeros(self.pop_size)

        self.best_x = np.zeros(self.dimension)
        self.best_x_value= 0

    def initialize (self):
        self.x = self.lower + (np.random.rand(self.pop_size,self.dimension+1)*(self.upper - self.lower))
        
        for i in range(self.pop_size):
            
            #--------------------------------------------------
            self.x[i][-1] = testfunction.testfunction1(self.x[i][:-1])
            self.gsw[i] = 1/(self.q * self.pop_size* math.sqrt(2*math.pi)) * math.exp( -0.5*((i+1-1)**2)   / (2*(self.q**2)*(self.pop_size**2))  )         
            #------------------------------------------------------       
        self.x = self.x[self.x[:,-1].argsort()]
        self.total_gsw = self.gsw / np.sum(self.gsw)

    def selector(self,total_gsw):
        r= random.random()
        C= np.cumsum(total_gsw)
        for i in range(len(total_gsw)):
            if C[i] >= r:
                return i

    def main (self):
        for iter in range(self.max_iter):
            sigma = np.zeros((self.pop_size,self.dimension))
            mu = np.copy(self.x[:,:-1])

            for i in range(self.pop_size):
                d = np.zeros(self.dimension)
                for j in range(self.pop_size):
                    d= d+abs(mu[i]-mu[j])
                sigma[i] = self.z*d/(self.pop_size-1)

            
            new_x = np.zeros((self.pop_size,self.dimension+1))
            

            for i in range(self.pop_size):
                for j in range(self.dimension):
                    sel = self.selector(self.total_gsw)

                    new_x[i][j] = mu[sel][j] + random.random()*sigma[sel][j]
            new_x = np.clip(new_x,self.lower,self.upper)


            for i in range(self.pop_size):

                new_x[i][-1] = testfunction.testfunction1(new_x[i][:-1])
            

            new_x = np.vstack((self.x,new_x))
            new_x = new_x[new_x[:,-1].argsort()]
            new_x = new_x[:self.pop_size][:]

            self.best_x = new_x[0][:-1]
            self.best_x_value = new_x[0][-1]


        print(self.best_x_value)


#-------------------------------------------------------------------------

pop_size = 300
dimension=30
max_iter=500
lower=-100
upper=100
q = 0.06
z = 0.85


time_start =time.time()
cal_value=[]
for qq in range(1):
    print("第",qq,"圈")
    random.seed(qq)
    np.random.seed(qq)
    solver = ACOR(pop_size,dimension,max_iter,lower,upper,q,z)
    solver.initialize()
    solver.main()
    cal_value.append(solver.best_x_value)

print("標",cal_value.index( min(cal_value) ))    
print("30次平均值",sum(cal_value) / len(cal_value))
print("最小值",min(cal_value))    

time_end =time.time()
print("花費時間",time_end-time_start)

 

