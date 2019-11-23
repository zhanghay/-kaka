from math import log
import operator
'''
计算香农熵，返回一个字典，
key是标签（所有的分类），
对应的值是标签出现的次数。
'''
def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}#计数
    for featVec in dataSet:
        currentLabel=featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel]=0#没有-》对应值为零
        labelCounts[currentLabel]+=1
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key])/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

'''
依据某个特征是否等于value，进行划分
将符合条件的加入新列表
并去除已经作为依据的值
'''
def splitDataset(dataset,axis,value):
    retDataSet=[]
    for featVet in dataset:
        if featVet[axis]==value:#向量中第axis个值满足条件：=value
            reducedFeatVec=featVet[:axis]
            reducedFeatVec.extend(featVet[axis+1:])#将向量的第axis个值后的所有值加入
            retDataSet.append(reducedFeatVec)#
    return retDataSet

'''
寻找最佳划分依据特征值
根据熵值减少
'''

def chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1#包含多少特征属性
    baseEntropy=calcShannonEnt(dataSet)#计算香农熵值
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]#导入数据集每个向量的第i个特征值
        uniqueVals=set(featList)#生成各个值互不相同的集合
        newEntropy=0.0
        for value in uniqueVals:#依次以每个特征为依据划分数据集
            subDataSet=splitDataset(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy#比较熵值是否减小
        if (infoGain>bestInfoGain):#减小了
            bestInfoGain=infoGain#第i个特征值是对的
            bestFeature=i
    return bestFeature


'''
处理了所有的特征后
多数表决的方法决定该节点的分类
即使类标签仍然不统一
'''
def majorityCnt(classList):#标签的集合
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)#排序
    return sortedClassCount[0][0]#返回最多的

'''
递归造树
'''


def creatTree(dataSet,labels):#labels:所有特征的名字
    classList=[example[-1] for example in dataSet]#提取标签
    if classList.count(classList[0])==len(classList):#都是同一类的
        return classList[0]
    if len(dataSet[0])==1:#不懂
        return majorityCnt(classList)#投票
    #开始创建树    
    bestFeat=chooseBestFeatureToSplit(dataSet)#选取最好的特征
    bestFeatLabel=labels[bestFeat]
    myTree={bestFeatLabel:{}}#字典变量  包含所有树的信息
    del(labels[bestFeat])#del 删除变量 数据没有删除  https://blog.csdn.net/love1code/article/details/47276683
    featValues=[example[bestFeat] for example in dataSet]
    uniqueVals=set(featValues)#每个值互不相同
    for value in uniqueVals:
        subLabels=labels[:]
        myTree[bestFeatLabel][value]=creatTree(splitDataset\
            (dataSet,bestFeat,value),subLabels)#递归造树
    return myTree