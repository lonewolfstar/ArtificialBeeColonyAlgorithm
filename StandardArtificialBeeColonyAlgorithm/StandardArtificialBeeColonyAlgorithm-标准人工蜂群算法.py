#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""导包"""
import math
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import ObjectiveFunctionSet as function#自定义测试函数库
from matplotlib.pyplot import MultipleLocator


# In[2]:


class BeeColony:
    """蜜源信息"""
    space=[]
    tureValue=0
    fitnessValue=0
    selectionPro=0
    notUpdateNum=0
    
    def __init__(self,message):
        self.space=[float for i in range(message.D)]
    
    def setSpace(self,i,value):
        self.space[i]=value
            
    def setTureValue(self,tureValue):
        self.tureValue=tureValue
        
    def setFitnessValue(self,fitnessValue):
        self.fitnessValue=fitnessValue
        
    def setSelectionPro(self,selectionPro):
        self.selectionPro=selectionPro
    
    def setNotUpdateNum(self,notUpdateNum):
        self.notUpdateNum=notUpdateNum


# In[3]:


class ParameterInformation:
    """参数信息"""
    D=0
    SN=0
    limit=0
    foodNum=0
    maxIterateNum=0
    minBoundary=0
    maxBoundary=0
    resultNum=0
    functionId=0
    
    def __init__(self,SN,limit,functionId,minBoundary,maxBoundary,D,maxIterateNum,resultNum):
        self.D=D
        self.SN=SN
        self.limit=limit
        self.foodNum=int(SN/2)
        self.functionId=functionId
        self.maxIterateNum=maxIterateNum
        self.minBoundary=minBoundary
        self.maxBoundary=maxBoundary
        self.resultNum=resultNum
        
    def setNowIterateNum(self,nowIterateNum):
        self.nowIterateNum=nowIterateNum


# In[4]:


def getTureValue(root,message):
    """获取目标函数真实值"""
    switcher = {
        1:function.h1,
        2:function.h2,
        3:function.h3,
        4:function.h4,
        5:function.h5,
        6:function.h6,
        7:function.h7,
        8:function.h8,
        9:function.h9,
        10:function.h10,
        11:function.h11,
        12:function.h12,
        13:function.h13,
        14:function.h14,
        15:function.h15,
        16:function.h16,
        17:function.h17,
        18:function.h18,
        19:function.h19,
        20:function.h20,
        21:function.h21,
        22:function.h22
    }
    return switcher.get(message.functionId)(root,message)


# In[5]:


def getFitnessValue(value):
    """获取蜜源适应值"""
    result=0;
    if value>=0:
        result=1/(value+1)
    else:
        result=1+abs(value)
    return result


# In[6]:


def initNectarSource(NectarSource,BestNectarSource,message):
    """初始化蜜源"""
    for i in range(message.foodNum):
        for j in range(message.D):
            NectarSource[i].setSpace(j,rand.uniform(message.minBoundary,message.maxBoundary))
            BestNectarSource.setSpace(j,NectarSource[0].space[j])
        NectarSource[i].setTureValue(getTureValue(NectarSource[i],message))
        NectarSource[i].setFitnessValue(getFitnessValue(NectarSource[i].tureValue))
        NectarSource[i].setSelectionPro(0)
        NectarSource[i].setNotUpdateNum(0)
        
    #初始化最优蜜源    
    BestNectarSource.setTureValue(NectarSource[0].tureValue)


# In[7]:


def copy(NectarSource,b,message):
    """复制信息"""
    for i in range(message.D):
        NectarSource.setSpace(i,b.space[i])
    NectarSource.setTureValue(b.tureValue)
    NectarSource.setFitnessValue(b.fitnessValue)


# In[8]:


def preserveTheBestNectarSource(NectarSource,BestNectarSource,message):
    """保存全局最优蜜源"""
    for i in range( message.foodNum):
        if BestNectarSource.tureValue> NectarSource[i].tureValue:
            copy(BestNectarSource,NectarSource[i],message)


# In[9]:


def employmentBeesBehavior(NectarSource,message):
    """雇佣蜂行为"""
    for i in range(message.foodNum):
        change=int(rand.uniform(0,message.D))
        while 1:
            k=int(rand.uniform(0,message.foodNum))
            if k!=i:
                break
        R=rand.uniform(-1,1)
        V=BeeColony(message)
        copy(V,NectarSource[i],message)
            
        #雇佣蜂搜索蜜源
        V.setSpace(change,(NectarSource[i].space[change]
                         +R*(NectarSource[i].space[change]
                             -NectarSource[k].space[change])))
        if V.space[change]<message.minBoundary:
            V.setSpace(change,message.minBoundary)
        if V.space[change]>message.maxBoundary:
            V.setSpace(change,message.maxBoundary)
        V.setTureValue(getTureValue(V,message))
        V.setFitnessValue(getFitnessValue(V.tureValue))
        message.setNowIterateNum(message.nowIterateNum+1)
            
        #贪婪选择
        if V.tureValue<NectarSource[i].tureValue:
            copy(NectarSource[i],V,message)
            NectarSource[i].setNotUpdateNum(0)
        else:
            NectarSource[i].setNotUpdateNum(NectarSource[i].notUpdateNum+1)


# In[10]:


def roulette(NectarSource,message):
    """通过轮盘赌得到选择概率"""
    max= NectarSource[0].fitnessValue
    for i in range( message.foodNum):
        if max< NectarSource[i].fitnessValue:
            max= NectarSource[i].fitnessValue
    for i in range( message.foodNum):
         NectarSource[i].setSelectionPro((0.9* NectarSource[i].fitnessValue/(1.0*max))+0.1)


# In[11]:


def followingBeesBehavior(NectarSource,message):
    """跟随蜂行为"""
    t=0
    i=0
    while t<message.foodNum:
        r=rand.uniform(0,1)
        if r<= NectarSource[i].selectionPro:
            change=int(rand.uniform(0, message.D))
            while 1:
                k=int(rand.uniform(0, message.foodNum))
                if k!=i:
                    break
            R=rand.uniform(-1,1)
            V=BeeColony(message)
            copy(V,NectarSource[i],message)
            
            #跟随蜂搜索蜜源
            V.setSpace(change,(NectarSource[i].space[change]
                             +R*(NectarSource[i].space[change]
                                 -NectarSource[k].space[change])))
            if V.space[change]<message.minBoundary:
                V.setSpace(change,message.minBoundary)
            if V.space[change]>message.maxBoundary:
                V.setSpace(change,message.maxBoundary)
            V.setTureValue(getTureValue(V,message))
            V.setFitnessValue(getFitnessValue(V.tureValue))
            message.setNowIterateNum(message.nowIterateNum+1)

            if V.tureValue<NectarSource[i].tureValue:
                copy(NectarSource[i],V,message)
                NectarSource[i].setNotUpdateNum(0)
            else:
                NectarSource[i].setNotUpdateNum(NectarSource[i].notUpdateNum+1)
            t+=1
        i=(i+1)%message.foodNum


# In[12]:


def scouterBeesBehavior(NectarSource,message):
    """侦查蜂行为"""
    index=0
    notUpdateNum= NectarSource[0].notUpdateNum
    for i in range(message.foodNum):
        if notUpdateNum< NectarSource[i].notUpdateNum:
            notUpdateNum= NectarSource[i].notUpdateNum
            index=i
    if notUpdateNum> message.limit:
        for i in range(message.D):
             NectarSource[index].setSpace(i,rand.uniform(message.minBoundary,message.maxBoundary))
        NectarSource[index].setTureValue(getTureValue(NectarSource[index],message))
        NectarSource[index].setFitnessValue(getFitnessValue(NectarSource[index].tureValue))
        NectarSource[index].setSelectionPro(0)
        NectarSource[index].setNotUpdateNum(0)


# In[13]:


def draw(Y,maxIterateNum):
    '''画出收敛图'''
    x = np.linspace(0, maxIterateNum,maxIterateNum)
    plt.figure(num = 1, figsize=(8, 5))# num表示的是编号，figsize表示的是图表的长宽
    plt.yscale('log')#设置纵坐标的缩放
    x_major_locator=MultipleLocator(maxIterateNum/10)#把x轴的刻度间隔设置为100，并存在变量里
    ax=plt.gca()#ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)#把x轴的主刻度设置为100的倍数

    l1,=plt.plot(x, Y,color='black',  # 线条颜色
             linewidth = 1.5,  # 线条宽度
             linestyle='-',  # 线条样式
             label='algorithm1')
    plt.show()


# In[18]:


def run(message,testNum):
    """算法逻辑控制"""
    NectarSource=[BeeColony(message) for i in range(message.foodNum)]
    BestNectarSource=BeeColony(message)
    resultCollection=[0 for i in range(int(message.maxIterateNum/message.SN))]
    
    sum=0
    for i in range(testNum):
        j=0
        message.setNowIterateNum(0)
        initNectarSource(NectarSource,BestNectarSource,message)
        preserveTheBestNectarSource(NectarSource,BestNectarSource,message)
        while(message.nowIterateNum<message.maxIterateNum):
            employmentBeesBehavior(NectarSource,message)
            roulette(NectarSource,message)
            followingBeesBehavior(NectarSource,message)
            preserveTheBestNectarSource(NectarSource,BestNectarSource,message)
            scouterBeesBehavior(NectarSource,message)
            resultCollection[j]=BestNectarSource.tureValue
            j+=1
        sum+=BestNectarSource.tureValue
    mean=sum/(1.0*testNum)
    print("Standard Artificial BeeColony Algorithm-标准人工蜂群算法")
    print("The average of the optimal results of function",message.functionId,": ",mean)
    draw(resultCollection,int(message.maxIterateNum/message.SN))
    return resultCollection


# In[15]:


def getParameterInformations():
    """自定义测试参数与自定义函数库中函数相对应"""
    m1_1=ParameterInformation(100,50*30,1,-100,100,30,5000*30,10)
    m1_2=ParameterInformation(100,50*100,1,-100,100,100,5000*100,10)

    m2_1=ParameterInformation(100,50*30,2,-100,100,30,5000*30,10)
    m2_2=ParameterInformation(100,50*100,2,-100,100,100,5000*100,10)

    m3_1=ParameterInformation(100,50*30,3,-10,10,30,5000*30,10)
    m3_2=ParameterInformation(100,50*100,3,-10,10,100,5000*100,10)

    m4_1=ParameterInformation(100,50*30,4,-1,1,30,5000*30,10)
    m4_2=ParameterInformation(100,50*100,4,-1,1,100,5000*100,10)

    m5_1=ParameterInformation(100,50*30,5,-10,10,30,5000*30,10)
    m5_2=ParameterInformation(100,50*100,5,-10,10,100,5000*100,10)

    m6_1=ParameterInformation(100,50*30,6,-100,100,30,5000*30,10)
    m6_2=ParameterInformation(100,50*100,6,-100,100,100,5000*100,10)

    m7_1=ParameterInformation(100,50*30,7,-100,100,30,5000*30,10)
    m7_2=ParameterInformation(100,50*100,7,-100,100,100,5000*100,10)

    m8_1=ParameterInformation(100,50*30,8,-10,10,30,5000*30,10)
    m8_2=ParameterInformation(100,50*100,8,-10,10,100,5000*100,10)

    m9_1=ParameterInformation(100,50*30,9,-1.28,1.28,30,5000*30,10)
    m9_2=ParameterInformation(100,50*100,9,-1.28,1.28,100,5000*100,10)

    m10_1=ParameterInformation(100,50*30,10,-5,10,30,5000*30,10)
    m10_2=ParameterInformation(100,50*100,10,-5,10,100,5000*100,10)

    m11_1=ParameterInformation(100,50*30,11,-5.12,5.12,30,5000*30,10)
    m11_2=ParameterInformation(100,50*100,11,-5.12,5.12,100,5000*100,10)

    m12_1=ParameterInformation(100,50*30,12,-5.12,5.12,30,5000*30,10)
    m12_2=ParameterInformation(100,50*100,12,-5.12,5.12,100,5000*100,10)

    m13_1=ParameterInformation(100,50*30,13,-600,600,30,5000*30,10)
    m13_2=ParameterInformation(100,50*100,13,-600,600,100,5000*100,10)

    m14_1=ParameterInformation(100,50*30,14,-500,500,30,5000*30,10)
    m14_2=ParameterInformation(100,50*100,14,-500,500,100,5000*100,10)

    m15_1=ParameterInformation(100,50*30,15,-50,50,30,5000*30,10)
    m15_2=ParameterInformation(100,50*100,15,-50,50,100,5000*100,10)

    m16_1=ParameterInformation(100,50*30,16,-100,100,30,5000*30,10)
    m16_2=ParameterInformation(100,50*100,16,-100,100,100,5000*100,10)

    m17_1=ParameterInformation(100,50*30,17,-100,100,30,5000*30,10)
    m17_2=ParameterInformation(100,50*100,17,-100,100,100,5000*100,10)

    m18_1=ParameterInformation(100,50*30,18,-10,10,30,5000*30,10)
    m18_2=ParameterInformation(100,50*100,18,-10,10,100,5000*100,10)

    m19_1=ParameterInformation(100,50*30,19,-10,10,30,5000*30,10)
    m19_2=ParameterInformation(100,50*100,19,-10,10,100,5000*100,10)

    m20_1=ParameterInformation(100,50*30,20,-1,1,30,5000*30,10)
    m20_2=ParameterInformation(100,50*100,20,-1,1,100,5000*100,10)

    m21_1=ParameterInformation(100,50*30,21,-5,5,30,5000*30,10)
    m21_2=ParameterInformation(100,50*100,21,-5,5,100,5000*100,10)

    m22_1=ParameterInformation(100,50*30,22,0,math.pi,30,5000*30,10)
    m22_2=ParameterInformation(100,50*100,22,0,math.pi,100,5000*100,10)

    switcher = {
            1:m1_1,
            2:m1_2,
            3:m2_1,
            4:m2_2,
            5:m3_1,
            6:m3_2,
            7:m4_1,
            8:m4_2,
            9:m5_1,
            10:m5_2,
            11:m6_1,
            12:m6_2,
            13:m7_1,
            14:m7_2,
            15:m8_1,
            16:m8_2,
            17:m9_1,
            18:m9_2,
            19:m10_1,
            20:m10_2,
            21:m11_1,
            22:m11_2,
            23:m12_1,
            24:m12_2,
            25:m13_1,
            26:m13_2,
            27:m14_1,
            28:m14_2,
            29:m15_1,
            30:m15_2,
            31:m16_1,
            32:m16_2,
            33:m17_1,
            34:m17_2,
            35:m18_1,
            36:m18_2,
            37:m19_1,
            38:m19_2,
            39:m20_1,
            40:m20_2,
            41:m21_1,
            42:m21_2,
            43:m22_1,
            44:m22_2
        }
    return switcher


# In[16]:


#获取参数信息
Parameter=getParameterInformations()


# In[19]:


#测试
for i in range(len(Parameter)):
    if i%2!=0:
        rC1=run(Parameter[i],1)


# In[ ]:




