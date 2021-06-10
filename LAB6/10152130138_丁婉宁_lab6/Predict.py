from numpy import * 
import pandas as pd  
# import statsmodels.api as sm
import pylab as pl  
import numpy as np 
opts = {'alpha': 0.001, 'maxIter': 100}
trainFeatures=[]
trainFlag=[]
testFeatures=[]
resultMy=[]
resultM={}
testFile=[]

def loadTrainData():
	print('loadTrainData')
	f=open('10152130138_丁婉宁_trainnew')
	i=0
	for line in f.readlines():
		if i==0:
			i=i+1
			continue
		else:
			lineList=line.split()


			test=[float(e) for e in lineList[2:]]

			trainFeatures.append(test[:-1])
			trainFlag.append(test[-1])
		i=i+1
	f.close() 

def loadTestData():
	print('loadTestData')
	f=open('10152130138_丁婉宁_testnew')
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
def sigmoid(inX):
	print('sigmoid')
	return 1.0 / (1 + exp(-inX))

def logRegModel(train_x, train_y, opts):
	print('logRegModel')
	numSamples, numFeatures = shape(train_x)
	alpha = opts['alpha']
	maxIter = opts['maxIter']
	weights = ones((numFeatures, 1))
	for k in range(maxIter):
		for i in range(numSamples):
			print(k,maxIter,i,numSamples)
			output = sigmoid(train_x[i, :] * weights)
			error = train_y[i, 0] - output
			weights = weights + alpha * train_x[i, :].transpose() * error
	return weights
#库函数逻辑回归
def logreRression(features,flag):
	print(features)
	print(flag)
	logit=sm.Logit(flag,features)
	model=logit.fit()
	resR=model.predict(testFeatures)
	print(len(testX))
	print(len(resR))
	return resR
#MYlogistic model
def predictLogModel(weights,train_x):
	print('predictLogModel')
	resM=[]
	numSamples, numFeatures = shape(train_x)
	for i in range(numSamples):
		p=sigmoid(train_x[i,:]*weights)
		print(p[0])
		resM.append(p[0])
	return resM
def outputFile(result):
	i=0
	test=''
	dicOffi={}
	dicTest={}
	f=open('machinePredict','w')
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
		for key1,value2 in valueSort:
			f.write(str(key)+' '+str(key1)+' '+str(value2))
	f.close()
if __name__ == '__main__':
	loadTrainData()
	loadTestData()

	trainFeatMat=mat(trainFeatures).transpose()
	trainFeatArray=array(trainFeatMat)

	for i in range(len(trainFeatArray)):
		dataMax=max(trainFeatArray[i])
		dataMin=min(trainFeatArray[i])
		data=dataMax-dataMin
		for j in range(len(trainFeatArray[i])):	
			trainFeatArray[i][j]=trainFeatArray[i][j]/data
	trainX=mat(trainFeatArray).transpose()
	trainY=mat(trainFlag).transpose()

	testFeatMat=mat(testFeatures).transpose()
	testFeatArray=array(testFeatMat)
	for i in range(len(testFeatArray)):
		dataMax=max(testFeatArray[i])
		dataMin=min(testFeatArray[i])
		data=dataMax-dataMin
		for j in range(len(testFeatArray[i])):
			testFeatArray[i][j]=testFeatArray[i][j]/data
	testX=mat(testFeatArray).transpose()

	# modelR=logreRression(trainFeatures,trainFlag)
	# outputFile(modelR)
	modelWeights=logRegModel(trainX,trainY,opts)
	myPredict=predictLogModel(modelWeights,testX)
	outputFile(myPredict)
	print(myPredict)





