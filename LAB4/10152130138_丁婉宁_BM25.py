import os
import xml.etree.ElementTree as ET
import math
import re
import json
rootdir_topics="./topics"
dirlist=["./disk_AP_XML","./disk_ZF_XML","./disk_WSJ_XML","./disk_DOE_XML","./disk_FR_XML"]
word_dic={}#单词的倒排索引字典
word_doc_freq={}#包含该单词的文档数
query_id=[]#query的docid
query=[]#query的内容
key=[]#倒排字典的单词数
doc_filaname={}#获取全部的文档名和文档长度
score={}

#获取document文档的信息
def getDocLength(dirname,filename):
	print('getdocument')

	if filename != '.DS_Store':
		xmldoc = ET.parse(dirname + '/'+filename)
		for doc in xmldoc.findall('DOC'):
			doc_list=[]
			for s1 in doc.findall('TEXT'):

				if s1.text==None:
					doc_list.append('')
				else:
					for word in s1.text.split():
						while '_' in word or '`' in word or '.' in word or '-' in word or '!' in word or ';' in word or ',' in word or '$' in word or '//' in word or '/' in word or '{' in word or '}' in word or '*' in word or '#' in word or '^' in word or '|' in word or '~' in word or '=' in word or '\'' in word or '+' in word or ':' in word or '?' in word:
							word = word.replace("_", "").replace('`', "").replace(".", "").replace('-', "").replace("!","").replace(";", "").replace(",", "").replace("$", "").replace("//", "").replace('/', "").replace('{',"").replace('}', "").replace('*', "").replace('^', "").replace("|", "").replace('~', "").replace('=',"").replace('\'', "").replace('+', "").replace(':', "").replace('?', "")
						if re.findall(r'\d+', word) or word == "":
							continue
						doc_list.append(word)
			for s2 in doc.findall('DOCNO'):
				docno=s2.text
			doc_filaname[docno]=len(doc_list)
def loadDocument(dirname):
	for parent,dirnames,filenames in os.walk(dirname):
		for e in filenames:
			getDocLength(dirname,e)
			print(e)

def loadQuery():
	print('query')
	xmldoc = ET.parse('topics_new.xml')
	for doc in xmldoc.findall('top'):
		test=''
		for s1 in doc.findall('num'):
			query_id.append(s1.text.replace("Number:","").strip())
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
		query.append(test.split())
def loadDic():
	print('loaddic')
	f_dic=open("inverted_index.json",encoding='utf-8')
	word_list=json.load(f_dic)
	for word in word_list:
		word_dic[word[0]]=word[1]
	for e in word_dic.keys():
		key.append(e)
def getBM25(words,doc_id):
	scoreArr={}
	for file in doc_filaname.keys():
		s=0
		for word in words:
			if word in word_doc_freq.keys():
				idf=math.log((N-word_doc_freq[word]+0.5)/(word_doc_freq[word]+0.5))
			else:
				idf = math.log((N - 0+ 0.5) / (0+ 0.5))
			if word in word_dic.keys():
				if file in word_dic[word].keys():
					freq = word_dic[word][file]
					s = s + idf * freq * 2.5 / (freq + 1.5 * (0.25 + 0.75 * doc_filaname[file] / avgLen))
			else:
				s= s + 0
		scoreArr[file]=s
	score[doc_id]=scoreArr
if __name__ == '__main__':
	loadQuery()
	loadDic()
	for dirname in dirlist:
		loadDocument(dirname)
	count = 0
	for doc in doc_filaname:
		count=count+doc_filaname[doc]
	for key,value in word_dic.items():
		word_doc_freq[key]=len(word_dic[key])
	N = len(doc_filaname)
	print(N)
	print(count)
	avgLen=count/N
	for i in range(len(query)):
		print(query_id[i])
		getBM25(query[i],query_id[i])
	f = open('10152130138_丁婉宁_BM25.res', 'w')
	for key,value in score.items():
		valueSort=sorted(value.items(),key=lambda d:d[1],reverse=True)#按照score倒序
		t=0
		for key1, value1 in valueSort:
			if t<200:
				f.write(key+' '+'0'+' '+key1+' '+str(t)+' '+str(value1)+' '+'10152130138_BM25'+'\n')
				t=t+1
	f.close()


