from numpy import *
import operator

def file2matrix(filename):
    fr=open(filename)
    arrayofLines=fr.readlines()
    numberofLine=len(arrayofLines)
    returnMat=zeros((numberofLine,3))#前三个有效,另一维度置为3
    classLabelVector=[]
    index=0
    for line in arrayofLines:
        line=line.strip()#截取去掉回车
        listFromLine=line.split('\t')#以\t将其分为列表
        returnMat[index,:]=listFromLine[0:3]#取前三个
        classLabelVector.append(int(listFromLine[-1]))#将列表得最后一列给向量,
                                                    #-1值告诉是倒数第一个,去掉int//int限定转为int型而非字符串
        index+=1
    return returnMat,classLabelVector



def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))#0-matrix
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))#行m次,列不变
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals


def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels
    
def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistance=sqDiffMat.sum(axis=1)
    distance=sqDistance**0.5
    sortedDistance=distance.argsort()
    classCount={}
    for i in range(k):
        votelabel=labels[sortedDistance[i]]
        classCount[votelabel]=classCount.get(votelabel,0)+1
    sortedClassCount=sorted(classCount.items(),
            key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]


def datingClassTest():
    hoRatio=0.10
    datingDataMat,labs=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)#注意ranges不要和range重名
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errorCount=0.0
    for i in range(numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],
            labs[numTestVecs:m],3)
        print("近邻结果:%d','实际结果:%d"\
            %(classifierResult,labs[i]))
        if classifierResult!=labs[i]:
            errorCount+=1.0
    print('总错误率:%f'%(errorCount/float(numTestVecs)))

def raw_input(str):
    dataIn=input(str)
    return dataIn
def classifyPerson():
    resultList=['不是','一点','大概率']
    percentTats=float(raw_input('游戏时间'))
    ffmile=float(raw_input('每年飞行里程'))
    icecream=float(raw_input('每年冰激凌食用升数'))
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals=autoNorm(datingDataMat)
    inArr=array([ffmile,percentTats,icecream])
    classifierResult=classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print("是%d"+resultList[classifierResult -1])