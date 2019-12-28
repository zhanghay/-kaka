#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np 
def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def createC1(dataSet):
    C1=[]  #C1是个列表 
    for transaction in dataSet:
        for item in transaction:
            if  [item] not in C1:
                C1.append([item]) #逐项加入单个物品，重复的不加
    C1.sort()
    #return C1
    return list(map(frozenset,C1))# 注意  frozenset 可作为字典建值使用 set不行

def scanD(D,Ck,minSupport):
    ssCnt={}#字典 
    #print (type(ssCnt))
    for tid in D:
        for can in Ck:
            if can.issubset(tid):#判断集合can的每一项元素是否在tid中
                ssCnt[can]=ssCnt.get(can,0)+1
    numItems=float(len(D))
    retList=[]  #满足支持度的
    supportData={}
    for key in ssCnt:
        support =ssCnt[key]/numItems
        if support >=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData#  可以的列表 和 每个的 支持度


# In[4]:


dataSet=loadDataSet()  #加载数据集
print(dataSet)
print(type(dataSet))   #列表


# In[5]:


C1=createC1(dataSet)
print(C1)


# In[6]:


D=list(map(set,dataSet))
print(D)   
print(map(set,dataSet))#不加list() 


# In[7]:


L1,suppData=scanD(dataSet,C1,0.5)
print(L1)
print(suppData)


# In[12]:


def aprioriGen(Lk,k):
    retList=[]  #空列表
    lenLk=len(Lk) #LK长度  项集的个数 传入 
    for i in range(lenLk): #遍历
        for j in range(i+1,lenLk): #从下一个到结束
            L1=list(Lk[i])[:k-2];
            L2=list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()            
            if L1==L2:            # 到倒数第二项都一样才求并集    巧妙保证了并集不重复   可通过实验证明
                retList.append(Lk[i]|Lk[j]) #并集操作，生成组合项集
    return retList

def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet)
    D=list(map(set,dataSet))
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while (len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)           #in：项集的列表 k项集元素个数{0}、{1}、{2} out：Ck {0，1}、{0、2}、{1，2}
        Lk,supK=scanD(D,Ck,minSupport)    #从Ck中筛选出满足min的Lk ---- Ck待选的项集列表
        supportData.update(supK)    #update？？？？？？？？？
        L.append(Lk)     #满足的添加到L
        k+=1               #K自增1
    return L,supportData


# In[13]:


L,suppDate=apriori(dataSet)
print(L)  #包含的项数从低到高


# In[14]:


print(L[0])


# In[27]:


print(L[1],L[2],L[3])
print (suppDate)


# In[23]:


C1=aprioriGen(L[0],2)   #是几？？嘿嘿
print(C1)
print(aprioriGen(L[0],1))
print(aprioriGen(L[0],3))
print(aprioriGen(L[1],3))
print(aprioriGen(L[1],4))
print(aprioriGen(L[1],2))  #通过实验  显然：


# In[24]:


"""
关联分析
一个元素可否推导出其他元素
量化：可信度
在P发生时P并H同时发生---概率论
如果2能推出013那么有2就能推出3 但是2推不出013 那么 有2不一定推不出3
如果有2推不出3那么2推不出013  

如果有a推出B那么有a的超集就能推出B的子集
如果A推不出b那么A的子集就不能推出b的超集

"""


# In[41]:


#计算可信度

def calcConf(freqSet,H,supportData,br1,minConf=0.7):
    prunedH=[]
    for conseq in H:#遍历H并计算各个的可信度
        conf=supportData[freqSet]/supportData[freqSet-conseq]#读取supportData方便计算可信度
        if conf>=minConf:#如果成立
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

#多于两个就合并


def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m=len(H[0])
    if (len(freqSet)>(m+1)):
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if(len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)
   
 #主函数
 #输入：3
#项集列表、数据集字典(值和对应的支持度)、阈值
    #前两个是apriori的输出
    #从多元素的集合开始构建
    #

def generateRules(L,supportData,minConf=0.7):  
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if (i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList


# In[42]:


L,suppData=apriori(dataSet,0.5)
rules=generateRules(L,suppData,0.7)
print(rules)





# In[ ]:
def main():
    mushDatSet=[line.split() for line in open ('mushroom.dat').readlines()]
    L,suppData=apriori(mushDatSet,0.3)
    for item in L[1]:
        if item.intersection('2'):
            print(item)


# In[ ]:
main()




# In[ ]:




