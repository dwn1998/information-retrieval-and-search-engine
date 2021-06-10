# encoding=utf8
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import xml.etree.ElementTree as ET
import nltk
import math
import re

import os

docDir=['./docs.training/topics_raw_docs','./docs.tesing/topics_raw_docs']
queryDir=['./2017TAR/training/extracted_data','./2017TAR/testing/extracted_data']


trainFolder=[]#训练集的doc文件夹名,即对应的query文件的名字
testFolder=[]#测试集的doc文件夹名,也是对应的query的名字
 
trainQrels={}#记录每个querylabel1的docname
stopwords=[]
trainQrels={}
def getStopword():
	f=open('stopword.txt')
	for line in f:
		stopwords.extend(line.strip('\n').split())
	f.close()
def loadQrelsDoc():
	f=open('qrel_abs_train')
	for line in f.readlines():
		lineList=line.split()
		if lineList[0] in trainQrels.keys():
			if lineList[-1]=='1':
				test=trainQrels[lineList[0]]
				test.append(lineList[-2])
				trainQrels[lineList[0]]=test
		else:
			if lineList[-1]=='1':
				test=[]
				test.append(lineList[-2])
				trainQrels[lineList[0]]=test

def outputFile(tfidfSort,bm25Sort,queryname):
	print('output')
	f=open('10152130138_丁婉宁_train','a')

	bm25KeyList=[]
	bmDic={}

	for key,value  in bm25Sort:
		bmDic[key]=value
		bm25KeyList.append(key)
	tfidfIndex=0

	for key,value in tfidfSort:
		tfidfIndex=tfidfIndex+1
		keylist=key.replace('.xml',"")
		keyIndex = bm25KeyList.index(key) + 1
		bmS = bmDic[key]


		if keylist in trainQrels[queryname]:

			print(keylist + '  1\n')
			writeStr=str(queryname) +' '+str(keylist)+' '+str(value)+' ' +str(tfidfIndex)+' '+str(bmS)+' '+str(keyIndex)+' 1\n'
		else:


			writeStr = str(queryname) + ' ' + str(keylist) + ' ' + str(value) + ' ' + str(tfidfIndex) + ' ' + str(bmS)+ ' ' + str(keyIndex) + ' 0\n'
		f.write(writeStr)
	f.close()

def tokenization(str_test):
	word_token=[]
	for i in range(len(str_test)):
		if str_test[i]==None:
			word_token.append("None")
		elif re.findall(r'\S', str_test[i]):

			word_token.append(nltk.word_tokenize(str_test[i])[0])
	return word_token

def stopword(str_test):
	test=[]
	for word in str_test:
		if word in stopwords:
			continue
		else:
			test.append(word)
	return test

def lemmatization(str_test):
	test=[]
	lemmatizaer=WordNetLemmatizer()
	for i in range(len(str_test)):
		if str_test[i]=="None":
			continue
		else:
			test.append(lemmatizaer.lemmatize(str_test[i]))
	return test

def stemmed(str_test):

	test=[]
	porter_stemmer = PorterStemmer()  
	for word in str_test:
		test.append(porter_stemmer.stem(word))
	return test

def loadQuery(foldername):
	testList=[]
	f=open(queryDir[0]+'/'+foldername+'.title')
	test=''
	for words in f:

		test=test+' '+words

	while '_' in test or '`' in test or '.' in test or '-' in test or '!' in test or ';' in test or ',' in test or '$' in test or '//' in test or '/' in test or '{' in test or '}' in test or '*' in test or '#' in test or '^' in test or '|' in test or '~' in test or '=' in test or '\'' in test or '+' in test or ':' in test or '?' in test or 'CD' in test:
		test = test.replace('CD',"").replace("_", "").replace('`', "").replace(".", "").replace('-', "").replace("!","").replace(";","").replace(",", "").replace("$", "").replace("//", "").replace('/', "").replace('{', "").replace('}',"").replace('*',"").replace('^', "").replace("|", "").replace('~', "").replace('=', "").replace('\'', "").replace('+',"").replace(':',"").replace('?', "")
	
	for word in test.split():
		if re.findall(r'\d+', word) or test == "":
			continue
		else:
			testList.append(word)

	text_token=tokenization(testList)
	text_stopword=stopword(text_token)
	text_lemmatize=lemmatization(text_stopword)
	query=stemmed(text_lemmatize)
	return query

def loadXmlText(filename,docdir,foldername):
	print(docdir+'/'+foldername+'/'+filename)
	if filename.endswith('.xml'):
		xmldoc=ET.parse(docdir+'/'+foldername+'/'+filename)
	else:
		os.rename(docdir+'/'+foldername+'/'+filename,docdir+'/'+foldername+'/'+filename+'.xml')
		xmldoc = ET.parse(docdir + '/' + foldername + '/' + filename + '.xml')

	test=''
	for MedlineCitation in xmldoc.findall('MedlineCitation'):
		for article in MedlineCitation.findall('Article'):

			for journal in article.findall('Journal'):

				for title in journal.findall('Title'):

					test = test + ' ' + title.text
			for a in article.findall('Abstract'):
				for abstract in a.findall('AbstractText'):

					if abstract.text==None:
						for s in abstract.findall('AbstractText'):
							test = test + ' ' + s.text
					else:
						test = test + ' ' + abstract.text

	testList=[]

	i=0
	for word in test.split():

		if re.findall(r'\d+', word) or word  == "":
			continue
		while '_' in word or '`' in word or '.' in word or '-' in word or '!' in word or ';' in word or ',' in word or '$' in word or '//' in word or '/' in word or '{' in word or '}' in word or '*' in word or '#' in word or '^' in word or '|' in word or '~' in word or '=' in word or '\'' in word or '+' in word or ':' in word or '?' in word:
			word = word.replace("_", "").replace('`', "").replace(".", "").replace('-', "").replace("!", "").replace(
				";",
				"").replace(
				",", "").replace("$", "").replace("//", "").replace('/', "").replace('{', "").replace('}', "").replace(
				'*',
				"").replace(
				'^', "").replace("|", "").replace('~', "").replace('=', "").replace('\'', "").replace('+', "").replace(
				':',
				"").replace(
				'?', "").replace("#","")
		testList.append(word)

	text_token=tokenization(testList)
	text_stopword=stopword(text_token)
	text_lemmatize=lemmatization(text_stopword)
	text=stemmed(text_lemmatize)

	return text


def getTfIdf(query,wordDir,N,docLength):
	wordDocFreq={}
	score={}

	for key,value in wordDir.items():
		wordDocFreq[key]=len(value)
	for doc in docLength.keys():
		s=0
		for word in query:
			if word in wordDocFreq.keys():
				idf=math.log(N/wordDocFreq[word])
			else:
				idf=0
			if word in wordDir.keys():
				if doc in wordDir[word].keys():
					freq=wordDir[word][doc]/docLength[doc]
					s=s+idf*freq
				else:
					s=s+0
		score[doc]=s
	return score


def getBM25(query,wordDir,N,docLength):
	wordDocFreq={}
	score={}
	for key,value in wordDir.items():
		wordDocFreq[key]=len(value)
	count=0
	for doc in docLength.keys():
		count=count+docLength[doc]
	avgLen=count/N

	for doc in docLength.keys():
		s=0
		for word in query:
			if word in wordDocFreq.keys():
				idf=math.log((N-wordDocFreq[word]+0.5)/(0+0.5))
			else:
				idf=math.log((N-0+0.5)/(0+0.5))
			if word in wordDir.keys():
				if doc in wordDir[word].keys():
					freq=wordDir[word][doc]
					s=s+idf*freq*2.5/(freq+1.5*(0.25+0.75*docLength[doc]/avgLen))
		score[doc]=s
	return score



def loadDocument(foldername,docdir,query):
	docLength={}#文档长度
	wordDir={}#倒排索引，word是key
	N=0

	for root,dirs,files in os.walk(docdir+'/'+foldername):
		count=0
		for file in files:
			if file.endswith('.gz'):
				continue
			else:
				count=count+1
		for file in files:
			if file=='.DS_Store':
				continue
			if file.endswith('.gz'):
				continue
			else:

				N=N+1
				if re.findall(r'\d+', file):
					text=loadXmlText(file,docdir,foldername)
					docLength[file]=len(text)
					wordFreq={}
					for word in text:
						if word in wordDir:
							if file in wordDir[word]:
								wordDir[word][file]=wordDir[word][file]
							else:
								wordDir[word][file]=1
						else:
							test={}
							test[file]=1
							wordDir[word]=test

	scoreTfIdf=getTfIdf(query,wordDir,N,docLength)
	scoreBM25=getBM25(query,wordDir,N,docLength)



	tfidfSort=sorted(scoreTfIdf.items(),key=lambda d:d[1],reverse=True)
	bm25Sort=sorted(scoreBM25.items(),key=lambda d:d[1],reverse=True)

	outputFile(tfidfSort,bm25Sort,foldername)

def fileFolder():
	for dirname in docDir:
		for dir in os.listdir(dirname):
			if dir=='.DS_Store':
				continue
			if dirname=='./docs.training/topics_raw_docs':
				trainFolder.append(dir)
			else:
				testFolder.append(dir)
	print(trainFolder)
	print(testFolder)

if __name__ == '__main__':
	f = open('10152130138_丁婉宁_train', 'a')
	f.write('queryname' + ' document' + ' tfidf' + ' tfidfRank' + ' bm25' + ' bm25Rank' + ' label\n')
	f.close()
	fileFolder()
	getStopword()
	loadQrelsDoc()
	print(trainQrels)
	i=0
	for foldername in trainFolder:
		print(i,len(trainFolder),foldername)
		i=i+1
		query=loadQuery(foldername)
		loadDocument(foldername,docDir[0],query)

