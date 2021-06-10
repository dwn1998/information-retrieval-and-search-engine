# -*- coding: UTF-8 -*-
import os
import xml.etree.ElementTree as ET
import re
import json

from numpy import*
rootdir_topics="./topics"
dirlist=["./disk_AP_XML","./disk_ZF_XML","./disk_WSJ_XML","./disk_DOE_XML","./disk_FR_XML"]
word_dic={}#单词的倒排索引字典
word_doc_freq={}#包含该单词的文档数
key=[]#倒排字典的单词数

doc_filaname={}#获取全部的文档名和文档长度

query_id={}#query的docid和文档的长度
query={}#query的内容和词频

qrel_dic={} #标准答案的每个query的相关文档
myres_dic={} #检索结果的每个query的文档
Cor_dic={} #检索结果的每个query的相关的文档
Uncor_dic={}#检索结果的每个query的不相关的文档

matQueDic={}#所有query的tfidf矩阵

newSeVector={}#更新后的查询向量

score={}#新查询的余弦相似度

def loadResDic():
	#原始检索结果
	print("loadresdic")
	f_myres=open('BM25Search.res')
	j=0
	for line in f_myres:
		if j%200<50:
			test=line.split()
			test1=[]
			if test[0] in myres_dic.keys():
				test1=myres_dic[test[0]]
			test1.append(test[2])
			myres_dic[test[0]]=test1
		j=j+1
	#标准答案相关检索结果
	for i in range(5):
		f_qrel=open("qrels_for_disk12/qrels.151-200.disk1.disk2.part"+str(i+1))
		for line in f_qrel:
			test=line.split()
			test1=[]
			if test[0] in qrel_dic.keys() and test[3]=='1':
				test1=qrel_dic[test[0]]
			if test[3]=="1":
				test1.append(test[2])
				qrel_dic[test[0]]=test1
	#相关和不相关
	for key,value in myres_dic.items():
		for filename in value:
			if filename in qrel_dic[key]:
				test=[]
				if key in Cor_dic.keys():
					test=Cor_dic[key]
				test.append(filename)
				Cor_dic[key]=test
			else:
				test1=[]
				if key in Uncor_dic.keys():
					test1=Uncor_dic[key]
				test1.append(filename)
				Uncor_dic[key]=test1

def loadDic():
	print("loaddic")
	f_dic=open("inverted_index.json",encoding='utf-8')
	word_list=json.load(f_dic)
	for word in word_list:
		word_dic[word[0]]=word[1]
	for e in word_dic.keys():
		key.append(e)
	f_dic.close()
	f1_dic=open("docLength.json",encoding='utf-8')
	doc_filaname=json.load(f1_dic)
	f1_dic.close()
	return doc_filaname
def loadQuery():
	print('loadquery')
	xmldoc = ET.parse('topics_new.xml')
	i=0
	for doc in xmldoc.findall('top'):
		print(i)
		i=i+1
		t_dic={}
		test=''
		for s2 in doc.findall('desc'):
			test=test+' '+s2.text.replace("Descript :","").strip()
		for s3 in doc.findall('narr'):
			test=test+' '+s3.text.replace("Narr :","").strip()
		for s4 in doc.findall('title'):
			test=test+' '+s4.text.replace("Topic :","").strip()
		while '_' in test or '`' in test or '.' in test or '-' in test or '!' in test or ';' in test or ',' in test or '$' in test or '//' in test or '/' in test or '{' in test or '}' in test or '*' in test or '#' in test or '^' in test or '|' in test or '~' in test or '=' in test or '\'' in test or '+' in test or ':' in test or '?' in test:
			test = test.replace("_", "").replace('`', "").replace(".", "").replace('-', "").replace("!","").replace(";","").replace(",", "").replace("$", "").replace("//", "").replace('/', "").replace('{', "").replace('}',"").replace('*',"").replace('^', "").replace("|", "").replace('~', "").replace('=', "").replace('\'', "").replace('+',"").replace(':',"").replace('?', "")
		if re.findall(r'\d+', test) or test == "":
			continue
		for word in test.split():
			if word in t_dic.keys():
				t_dic[word]=t_dic[word]+1
			else:
				t_dic[word]=1
		for s1 in doc.findall('num'):
			test_docid=s1.text.replace("Number:","").strip()
			query_id[test_docid]=len(test.split())
			query[test_docid]=t_dic
def getDocVector(words,name):
	test=[]
	for word in words:
		if word in word_doc_freq.keys():
			idf = math.log(N / word_doc_freq[word])
		else:
			idf = 0
		if word in word_dic.keys():
			if name in word_dic[word].keys():
				freq = word_dic[word][name] / doc_filaname[name]
				test.append(idf * freq)
			else:
				test.append(0)
		else:
			test.append(0)
	return test


def getQueVector():
	print('queryVector')
	for title,word_f in query.items():
		print ('queryVector'+title)
		test=[]
		for word in word_f.keys():
			tf=word_f[word]/query_id[title]
			if word in word_doc_freq.keys():
				idf=math.log(N/(word_doc_freq[word]+1))
			else:
				idf=math.log(N/1)
			test.append(tf*idf)
		matQueDic[title]=test

def getRocchio():
	print('rocchio')
	for title,vector in matQueDic.items():
		print("rocchio"+title)
		if title in Cor_dic:
			Dr=len(Cor_dic[title])
			Dnr = len(Uncor_dic[title])

			Drv = mat([0 for i in range(len(query[title].keys()))])

			Dnrv = mat([0 for i in range(len(query[title].keys()))])
			for file in Cor_dic[title]:
				docvector = getDocVector(query[title].keys(), file.strip())
				print(query[title].keys())
				print(len(docvector))
				Drv = Drv + mat(docvector)
			for file in Uncor_dic[title]:
				docvector = getDocVector(query[title].keys(), file.strip())
				Dnrv = Dnrv + mat(docvector)
			new_v = mat(matQueDic[title]) + 0.75 * (1 / Dr) * Drv - 0.15 * (1 / Dnr) * Dnrv
			newSeVector[title] = new_v.tolist()[0]
		else:
			Dnr=len(Uncor_dic[title])
			Dnrv=mat([0 for i in range(len(query[title].keys()))])
			for file in Uncor_dic[title]:
				docvector=getDocVector(query[title].keys(),file)
				Dnrv=Dnrv+mat(docvector)
			new_v=mat(matQueDic[title])-0.15*(1/Dnr)*Dnrv
			newSeVector[title]=new_v.tolist()[0]
def getRelDoc(words):
	print('getreldoc')
	file=[]
	for word in words:
		if word in word_dic:
			for f in word_dic[word].keys():
				if f in file:
					continue
				else:
					file.append(f)
	print(len(file))
	return file
def makeNewSearch(words,num):
	print('newsearch')
	scoreArr = {}
	for file in doc_filaname.keys():
		vectorList=[]
		flag=0
		for word in words.keys():
			if word in word_doc_freq.keys():
				idf = math.log(N / word_doc_freq[word])
			else:
				idf = 0
			if word in word_dic.keys():
				if file in word_dic[word].keys():
					freq = word_dic[word][file] / doc_filaname[file]
					vectorList.append(idf * freq)
					flag=1
				else:
					vectorList.append(0)
			else:
				vectorList.append(0)
		if flag==0:
			continue
		t = 0
		t1 = 0
		t2 = 0
		for i in range(len(words)):
			t = t + newSeVector[num][i] * vectorList[i] * 1.0
			t1 = t1 + newSeVector[num][i]** 2 * 1.0
			t2 = t2 + vectorList[i] ** 2 * 1.0
		scoreArr[file] =t/(math.sqrt(t1)*math.sqrt(t2))*1.0
	score[num] = scoreArr
if __name__ == '__main__':
	doc_filaname=loadDic()
	count=0
	for doc in doc_filaname:
		count=count+doc_filaname[doc]
	for key,value in word_dic.items():
		word_doc_freq[key]=len(word_dic[key])
	N = len(doc_filaname)
	loadQuery()
	loadResDic()
	getQueVector()
	getRocchio()
	for num,words in query.items():
		print(num)
		makeNewSearch(words,num)
	f = open('newSearch.res', 'w')
	for key,value in score.items():
		valueSort=sorted(value.items(),key=lambda d:d[1],reverse=True)#按照score倒序
		t=0
		for key1, value1 in valueSort:
			if t<100:
				f.write(key+' '+'0'+' '+key1+' '+str(t)+' '+str(value1)+' '+'10152130138dingwanningRF'+'\n')
				t=t+1
	f.close()

					



