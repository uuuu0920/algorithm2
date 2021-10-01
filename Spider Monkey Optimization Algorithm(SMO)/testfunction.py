import math
import copy
import random
def testfunction1(x):
    value=0
    for i in x:
        value = value + (i*i)

    return value

def testfunction2(x):
    value1=0
    value2=abs(x[0])
    for i in x:
        value1 = value1 + abs(i)
    for i in range(1,len(x)):
        value2= value2 *abs(x[i])
    return value1+value2

def testfunction3(x):
    value1=0
    value2=0
    for i in range(len(x)):
        
        value2=value2+(value1**2)
        value1=0
        for j in range(i):
            value1=value1+x[j]
    return value2

def testfunction4(x):
    value=copy.deepcopy(x)
    for i in range(len(value)):
        value[i]=abs(value[i])
    return max(value)

def testfunction5(x):
    value=0
    for i in range(len(x)-1):
        value=value + (100* ((x[i]**2)-x[i+1]) **2 + (1-x[i])**2)
    return value

def testfunction6(x):
    value=0
    for i in x:
        value= value + (i+0.5)**2
        
    return value

def testfunction7(x):
    value=0
    for i in range(len(x)):
        value=value+ i*x[i]**4 
    return value+ random.random()

def testfunction8(x):
    value=0
    for i in x:
        value= value + (-i) * math.sin(abs(i)**0.5)
    return value
    
def testfunction9(x):
    value=0
    for i in x:
        value=value+ ((i**2)-(10*math.cos(2*math.pi*i)) +10)
        
    return value

def testfunction10(x):
    value=0
    value1=0
    value2=0
    for i in x:
        value1=value1+ i**2
        value2=value2+ math.cos(2*math.pi*i)
    value= -20*math.exp(-0.2*math.sqrt((1/len(x))*value1)) - math.exp((1/len(x))*value2) + 20 + math.e
        
    return value 

def testfunction11(x):
    value=0
    value1=0
    value2=x[0]
    for i in x:
        value1=value1+ i**2
    for i in range(1,len(x)+1):
        value2= value2* math.cos(x[i-1]/math.sqrt(i))
    value2=value2/x[0]
    value= 1+ ((1/4000)*value1) - value2
        
    return value 

def testfunction12(x):
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

