from numpy import * 
import pandas as pd  
import statsmodels.api as sm
import pylab as pl  
import numpy as np 
opts = {'alpha': 0.001, 'maxIter': 100}
trainFeatures=[]
trainFlag=[]
testFeatures=[]
resultMy=[]
resultM={}
testFile=[]
resS={}
def loadTrainData():

	f=open('10152130138_丁婉宁_train')
	i=0
	for line in f.readlines():
		if i==0:
			i=i+1
			continue
		else:
			lineList=line.split()
			# test=[float(e) for e in lineList[2:]]
			# # if test[0]==0 or test[2]==0:
			# # 	continue
			# # else:
			test=[]
			test.append(lineList[3])
			test.append(lineList[5])
			trainFeatures.append(test)
			trainFlag.append(lineList[-1])
		i=i+1
	f.close() 

def loadTestData():

	f=open('10152130138_丁婉宁_test')
	i=0
	for line in f.readlines():
		if i==0:
			i=i+1
			continue
		else:
			lineList=line.split()
			file=[word for word in lineList[0:2]]
			test=[float(e) for e in lineList[2:]]
			testFile.append(file)
			testFeatures.append(test[:])
		i=i+1
	f.close()

# calculate the sigmoid function
# def sigmoid(inX):
# 	print('sigmoid')
# 	return 1.0 / (1 + exp(-inX))

# def logRegModel(train_x, train_y, opts):
# 	print('logRegModel')
# 	numSamples, numFeatures = shape(train_x)
# 	alpha = opts['alpha']
# 	maxIter = opts['maxIter']
# 	weights = ones((numFeatures, 1))
# 	for k in range(maxIter):
# 		for i in range(numSamples):
# 			print(k,maxIter,i,numSamples)
# 			output = sigmoid(train_x[i, :] * weights)
# 			error = train_y[i, 0] - output
# 			weights = weights + alpha * train_x[i, :].transpose() * error
# 	return weights
#库函数逻辑回归
def logreRression(features,flag):

	logit=sm.Logit(flag,features)
	model=logit.fit()
	resR=model.predict(testFeatures)

	return resR
#MYlogistic model
# def predictLogModel(weights,train_x):
# 	print('predictLogModel')
# 	resM=[]
# 	numSamples, numFeatures = shape(train_x)
# 	for i in range(numSamples):
# 		p=sigmoid(test_x[i,:]*weights)
# 		print(p)
# 		resM.append(p)
# 	return resM
def outputFile(result):
	i=0
	test=''
	dicOffi={}
	dicTest={}
	f=open('10152130138_丁婉宁.res','w')
	for file in testFile:
		if test==file[0]:
			dicTest[file[1]]=result[i]
		else:
			if i!=0:
				dicOffi[test]=dicTest
				dicTest={}
			test=file[0]
			dicTest[file[1]]=result[i]
		i=i+1
	for key,value in dicOffi.items():
		valueSort =sorted(value.items(),key=lambda d:d[1],reverse=True)
		for key1,value1 in valueSort:
			f.write(str(key)+' '+str(key1)+' '+str(value1)+"\n")
	getEvalution(dicOffi)

def getEvalution(dicOffi):
	fS=open('./2017_test_qrels/qrel_abs_test.txt')
	for line in fS.readlines():
		lineList=line.split()
		if lineList[0] in resS.keys():
			if lineList[-1]=='1':
				test=resS[lineList[0]]
				test.append(lineList[-2])
				resS[lineList[0]]=test
		else:
			if lineList[-1]=='0':
				test=[]
				test.append(lineList[-2])
				resS[lineList[0]]=test
	MAP=0
	for key,value in dicOffi.items():
		valueSort =sorted(value.items(),key=lambda d:d[1],reverse=True)
		t=0
		keyList=valueSort.keys()
		for i in range(len(resS[key])):
			t=t+i/((keyList.index(resS[key][i]))+1)
		MAP=MAP+t/(i+1)
	MAP=MAP/(len(dicOffi.keys()))


if __name__ == '__main__':
	loadTrainData()
	loadTestData()

	# trainFeatMat=mat(trainFeatures).transpose()
	# trainFeatArray=array(trainFeatMat)

	# for i in range(len(trainFeatArray)):
	# 	dataMax=max(trainFeatArray[i])
	# 	dataMin=min(trainFeatArray[i])
	# 	data=dataMax-dataMin
	# 	for j in range(len(trainFeatArray[i])):	
	# 		trainFeatArray[i][j]=trainFeatArray[i][j]/data
	# trainX=mat(trainFeatArray).transpose()
	# trainY=mat(trainFlag).transpose()

	# testFeatMat=mat(testFeatures).transpose()
	# testFeatArray=array(testFeatMat)
	# for i in range(len(testFeatArray)):
	# 	dataMax=max(testFeatArray[i])
	# 	dataMin=min(testFeatArray[i])
	# 	data=dataMax-dataMin
	# 	for j in range(len(testFeatArray[i])):
	# 		testFeatArray[i][j]=testFeatArray[i][j]/data
	# testX=mat(testFeatArray).transpose()

	modelR=logreRression(trainFeatures,trainFlag)
	outputFile(modelR)
	# modelWeights=logRegModel(trainX,trainY,opts)
	# myPredict=predictLogModel(modelWeights,testX)





