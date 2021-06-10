import os
import xml.etree.ElementTree as ET
import math
import re
import json
rootdir_topics="./topics"
dirlist=["./disk_AP_XML","./disk_ZF_XML","./disk_WSJ_XML","./disk_DOE_XML","./disk_FR_XML"]
word_dic={}#单词的倒排索引字典
query_id=[]#query的docid
query={}#query的内容
doc_filename={}#获取全部的文档名和文档长度
word_freq={}
score={}

def getDocLength(dirname,filename):
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

def loadDic():
	print("loaddic")
	f_dic=open("inverted_index.json",encoding='utf-8')
	word_list=json.load(f_dic)
	for word in word_list:
		word_dic[word[0]]=word[1]

	f_dic.close()

	f1_dic=open("docLength.json",encoding='utf-8')
	doc_filename=json.load(f1_dic)
	f1_dic.close()
	print(len(doc_filename))

	return doc_filename

def loadQuery():
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
		for w in test.split():
			wDoc = 0
			if w in word_dic.keys():
				for d, freq in word_dic[w].items():
					wDoc = wDoc + freq
			else:
				wDoc=1
			word_freq[w]=wDoc
		query[s1.text.replace("Number:","").strip()]=test.split()

def getUnigram(title,words,T):
	print('getunigram')
	docDic={}
	for doc,doc_len in doc_filename.items():
		p=1
		for word in words:
			if word in word_dic.keys():
				if doc in word_dic[word]:
					pwd1=word_dic[word][doc]*1.0/doc_len
				else:
					pwd1=0
			else:
				pwd1=0
			p=p*(0.9*pwd1+(1-0.9)*(word_freq[word]/T))
		docDic[doc]=p
	score[title]=docDic

if __name__ == '__main__':
	doc_filename=loadDic()
	T=0
	for doc,doc_len in doc_filename.items():
		T=T+doc_len
	print(len(doc_filename))
	loadQuery()
	for title,words in query.items():
		print(title)
		getUnigram(title,words,T)
	f = open('10152130138_Unigram.res', 'w')
	for key,value in score.items():
		valueSort=sorted(value.items(),key=lambda d:d[1],reverse=True)#按照score倒序
		t=0
		for key1, value1 in valueSort:
			if t<1000:
				f.write(key+' '+'0'+' '+key1+' '+str(t)+' '+str(value1)+' '+'10152130138_dingwanning_unigram'+'\n')
				t=t+1
	f.close()
