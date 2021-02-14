#!/usr/bin/env python
# coding: utf-8

# In[2]:

import math
import random as rand


#sphere    -100,100
def h1(root,message):
    result=0
    for i in range(message.D):
        result+=pow(root.space[i],2)
    return result

#Elliptic -100,100
def h2(root,message):
    result=0
    for i in range(message.D):
        result+= pow(10.0,6.0*i/(message.D-1))*pow(root.space[i],2)
    return result

#SumSquare -10,10
def h3(root,message):
    result=0
    for i in range(message.D):
        result+=(i+1)*root.space[i]*root.space[i]
    return result

#SumPower -1,1
def h4(root,message):
    result=0.0
    for i in range(message.D):
        a=abs(root.space[i])
        result+=pow(a,i+2)
    return result

#Schwefel 2.22  -10,10
def h5(root,message):
    tmp1=0
    tmp2=1
    for i in range(message.D):
        temp=abs(root.space[i])
        tmp1+=temp
        tmp2*=temp
    return tmp1+tmp2

#Schwefel 2.21 -100,100
def h6(root,message):
    result = abs(root.space[0])
    for i in range(message.D):
        if abs(root.space[i])>result:
            result=abs(root.space[i])
    return result

#Step  -100,100
def h7(root,message):
    result=0
    for i in range(message.D): 
        result+=pow(math.floor(root.space[i]+0.5),2)
    return result 

#Exponential  -10,10
def h8(root,message):
    result=0
    for i in range(message.D):
        result+=0.5*root.space[i]
    result=pow(math.e,result)
    return result

#Quartic   -1.28,1.28
def h9(root,message):
    result=0
    for i in range(message.D):
        result+=(i+1.0)*pow(root.space[i],4)
    result=result+rand.uniform(0,1)
    return result

#Rosenbrock    -5,10
def h10(root,message):
    result=0
    tmp1=0
    tmp2=0
    for i in range(message.D-1):
        tmp1=100*(root.space[i]*root.space[i]-root.space[i+1])*(root.space[i]*root.space[i]-root.space[i+1])
        tmp2=(root.space[i]-1)*(root.space[i]-1)
        result+=tmp1+tmp2
    return result

#     #Rastrigin        -5.12,5.12
def h11(root,message):
    result=0
    for i in range(message.D):
        result+=(root.space[i]*root.space[i]-10*math.cos(2*math.pi*root.space[i])+10)
    return result

#NCRastrigin   -5.12,5.12
def h12(root,message):
    result=0
    sol1=[0.0 for i in range(message.D)]
    for i in range(message.D):
        if abs(root.space[i])<0.5:
            sol1[i]=root.space[i]
        else:
            a=(int(2*root.space[i]+0.5))
            sol1[i]=a/2.0
        result+=(sol1[i]*sol1[i]-10*math.cos(2*math.pi*sol1[i])+10)
    return result

#Griewank   -600,600
def h13(root,message):
    result=0
    temp1=0.0
    temp2=1.0
    for i in range(message.D):
        temp1+=(root.space[i]*root.space[i])/4000.0
        temp2*=math.cos(root.space[i]/math.sqrt(i+1.0))
    result=temp1-temp2+1
    return result

#Schwefel  2.26
def h14(root,message):
    result=0
    for i in range(message.D):
        result+=(-1*root.space[i])*math.sin(math.sqrt(abs(root.space[i])))
    result=-1*result
    return result

#Ackley -50,50
def h15(root,message):
    result = 0
    temp1 = 0.0
    temp2 = 0.0
    for i in range(message.D):
        temp1 += root.space[i]*root.space[i]
        temp2 += math.cos(2*math.pi*root.space[i])
    temp1/=float(message.D)
    temp1=-0.2*math.sqrt(temp1)
    temp1=-20*math.exp(temp1)
    temp2/=float(message.D)
    temp2=math.exp(temp2)
    result=temp1-temp2+20+math.exp(1.0)
    return result

#Penalized 1  -100,100
def h16(root,message):
    x=[0.0 for i in range(message.D)]
    result=0
    temp1=0
    temp2=0
    for i in range(message.D):
        x[i]=1.0+(root.space[i]+1)/4.0
        if root.space[i]>10:
            temp1=100*pow(root.space[i]-10,4)
        else:
            if root.space[i]<-10:
                temp1=100*pow(-root.space[i]-10,4)
            else:
                temp1=0
        temp2+=temp1
    for i in range(message.D-1):
        result+=(x[i]-1)*(x[i]-1)*(1+10*math.sin(math.pi*x[i+1])*math.sin(math.pi*x[i+1]))
    result=math.pi/message.D*(10*math.sin(math.pi*x[0])*math.sin(math.pi*x[0])+result+(x[message.D-1]-1)*(x[message.D-1]-1))+temp2
    return result

#Penalized 1  -100,100
def h17(root,message):
    f1=0.0
    f2=0.0
    value=0
    u=[0.0 for i in range(message.D)]
    for i in range(message.D):
        if root.space[i]>5:
            u[i] = 100*pow(root.space[i]-5, 4)
        if root.space[i]<-5:
            u[i]=100*pow((-root.space[i]-5), 4)
        if root.space[i]>=-5 and root.space[i]<=5:
            u[i]=0
        f1=f1+u[i]
    for i in range(message.D-1):
        f2=f2+pow(root.space[i]-1,2)*(1+pow(math.sin(3*math.pi*root.space[i+1]),2))
    f2 = f2 + pow(math.sin(3*math.pi*root.space[0]),2)+pow(root.space[message.D-1]-1,2)*(1+pow(math.sin(2*math.pi*root.space[message.D-1]),2))
    value = 0.1*f2 + f1
    return value

#Alpine  -10,10
def h18(root,message):
    result=0.0
    for i in range(message.D):
        result+=abs(root.space[i]*math.sin(root.space[i])+0.1*root.space[i])
    return result

#Levy  -10,10
def h19(root,message):
    result=0
    for i in range(message.D-1):
        result+=pow(root.space[i]-1,2)*(1+pow(math.sin(3*math.pi*root.space[i+1]),2))
    result=result+pow(math.sin(3*math.pi*root.space[1]),2)
    result=result+abs(root.space[message.D-1]-1)*(1+pow(math.sin(3*math.pi*root.space[message.D-1]),2))
    return result

#Weierstrass  -1,1
def h20(root,message):
    a=0.5
    b=3
    kmax=20
    result=0
    temp1=0
    temp2=0
    for i in range(message.D):
        for j in range(kmax):
            temp1+=pow(a,j)*math.cos(2*math.pi*pow(b,j)*(root.space[i]+0.5))

    for j in range(kmax):
        temp2+=pow(a,j)*math.cos(2*math.pi*math.pow(b,j)*(0.5))
    result=temp1-message.D*temp2
    return result


#Himmelblau  -5,5
def h21(root,message):
    result=0
    for i in range(message.D):
        result+=pow(root.space[i],4)-16*root.space[i]*root.space[i]+5*root.space[i]
    result=1.0/message.D*result
    return result

#Michalewicz  0,PI
def h22(root,message):
    result=0
    for i in range(message.D):
        a=math.sin((i+1)*root.space[i]*root.space[i]/math.pi)
        result+=math.sin(root.space[i])*pow(a,20)
    return -1*result




