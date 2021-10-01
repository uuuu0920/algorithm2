import random
import math
import copy
import matplotlib.pyplot as plt
import numpy as np
import testfunction
import time

class AOA():
    def __init__(self,pop_size,dimension,max_iter,lower,upper,c3,c4):
        self.c1 = 2
        self.c2 = 6
        self.u =0.9
        self.l = 0.1
        
        self.pop_size=pop_size
        self.dimension=dimension
        self.max_iter = max_iter
        self.upper= upper
        self.lower= lower
        self.c3=c3
        self.c4=c4
        
        self.x = np.zeros((self.pop_size,self.dimension))
        self.x_value = np.zeros(self.pop_size)
        self.den = np.zeros((self.pop_size,self.dimension))
        self.vol = np.zeros((self.pop_size,self.dimension))
        self.acc = np.zeros((self.pop_size,self.dimension))
        
        self.best_x=[]
        self.best_x_value=0
        self.best_x_index=0
        self.best_den=[]
        self.best_vol=[]
        self.best_acc=[]
        self.acc_norm=[]


    def initialize (self):
        self.x = self.lower + (np.random.rand(self.pop_size,self.dimension)*(self.upper - self.lower))
        for i in range(self.pop_size):
            
            #--------------------------------------------------
            self.x_value[i] = testfunction.testfunction11(self.x[i])
        self.den = np.random.rand(self.pop_size,self.dimension)
        self.vol = np.random.rand(self.pop_size,self.dimension)
        self.acc = self.lower + (np.random.rand(self.pop_size,self.dimension)*(self.upper - self.lower))
        self.acc_norm = np.copy(self.acc)
        
        self.best_x_index= np.argmin(self.x_value)
        self.best_x_value = self.x_value[self.best_x_index]
        self.best_x = np.copy(self.x[self.best_x_index])
        self.best_den = np.copy(self.den[self.best_x_index])
        self.best_vol = np.copy(self.vol[self.best_x_index])
        self.best_acc = np.copy(self.acc[self.best_x_index])
        
    def main(self):
        x_fitline = []
        y_fitline= []
        for iter in range(self.max_iter):
            TF = math.exp( (iter-self.max_iter)/self.max_iter ) #Eq.(8)
            if TF >1:
                TF=1
                          
            d= math.exp( (self.max_iter-iter)/self.max_iter ) -(iter/self.max_iter)
            self.acc=np.copy(self.acc_norm)
            
            acc_temp = np.random.rand(self.pop_size,self.dimension)
            for i in range(self.pop_size): #Exploitation phase
                
                self.den[i] = self.den[i] + (np.random.rand(self.dimension) *(self.best_den - self.den[i]))
                self.vol[i] = self.vol[i] + (np.random.rand(self.dimension) *(self.best_vol - self.vol[i]))
                
                if TF < 0.5:
                    random_select = random.randint(0, self.pop_size-1)
                    acc_temp[i] = ( self.den[random_select] - (self.vol[random_select]*self.acc[random_select]) ) / (self.den[i] *self.vol[i])
                else:
                    acc_temp[i] = (self.best_den - (self.best_vol * self.best_acc) ) / (self.den[i] *self.vol[i])
                    
            self.acc_norm = 0.1 + 0.9*( (acc_temp -acc_temp.min()) / (acc_temp.max()-acc_temp.min()) )
            
            
            new_x = np.copy(self.x)
            for i in range(self.pop_size): #Update position
                if TF<0.5:
                    for j in range(self.dimension):
                        
                        random_select = random.randint(0, self.pop_size-1)
                        new_x[i][j] = self.x[i][j] + ( self.c1*random.random()*self.acc_norm[i][j]*d*(self.x[random_select][j] - self.x[i][j]) )
                else:
                    for j in range(self.dimension):
                        
                        p=(2*random.random())-self.c4
                        T = self.c3*TF
                        if T>1:
                            T=1
                        if p <0.5:
                            new_x[i][j] = self.best_x[j] + (self.c2 * random.random() *self.acc_norm[i][j]*d*((T*self.best_x[j])-self.x[i][j]))

                            
                        else:
                            new_x[i] = self.best_x[j] - (self.c2 * random.random() *self.acc_norm[i][j]*d*((T*self.best_x[j])-self.x[i][j]))

            
            new_x =np.clip(new_x,self.lower,self.upper)
                      
                        
            new_x_value = np.zeros(self.pop_size) 
     
            for i in range(self.pop_size):
                
                #-----------------------------------------------------------------------
                new_x_value[i] = testfunction.testfunction11(new_x[i])
            
                if new_x_value[i] < self.x_value[i]:
                    self.x_value[i] = np.copy(new_x_value[i])
                    self.x[i] = np.copy(new_x[i])      

            if np.min(new_x_value) < self.best_x_value:
                
                self.best_x_index= np.argmin(self.x_value)
                self.best_x_value = self.x_value[self.best_x_index]
                self.best_x = np.copy(self.x[self.best_x_index])
                self.best_den = np.copy(self.den[self.best_x_index])
                self.best_vol = np.copy(self.vol[self.best_x_index])
                self.best_acc = np.copy(self.acc[self.best_x_index])     
            
            x_fitline.append(iter)
            y_fitline.append(self.best_x_value)
        plt.plot(x_fitline,  y_fitline)
        plt.show()
            
            
            
        
pop_size = 30
dimension=30
max_iter=500
lower=-600
upper=600
c3=2
c4=0.5

time_start =time.time()
cal_value=[]
for qq in range(30):
    print("第",qq,"圈")
    random.seed(qq)
    np.random.seed(qq)
    solver = AOA(pop_size,dimension,max_iter,lower,upper,c3,c4)
    solver.initialize()
    
    solver.main()
    print(solver.best_x_value)
    
    cal_value.append(solver.best_x_value)
    #print(solver.best_x)

print("標",cal_value.index( min(cal_value) ))    
print("30次平均值",sum(cal_value) / len(cal_value))
print("最小值",min(cal_value))    

time_end =time.time()
print("花費時間",time_end-time_start)


