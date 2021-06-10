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
key=[]#倒排字典的单词数
doc_filaname={}#获取全部的文档名和文档长度
score={}

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
				docno=s2.text.strip()
			doc_filaname[docno]=len(doc_list)
def loadDocument(dirname):
	print('loaddocument')
	for parent,dirnames,filenames in os.walk(dirname):
		for e in filenames:
			print(e)
			getDocLength(dirname,e)

def loadDic():
	print('loaddic')
	f_dic=open("inverted_index.json",encoding='utf-8')
	word_list=json.load(f_dic)
	for word in word_list:
		word_dic[word[0]]=word[1]

def loadQuery():
	print('loadquery')
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
		query[s1.text.replace("Number:","").strip()]=test.split()

def getUnigram(title,words):
	docDic={}
	for doc,doc_len in doc_filaname.items():
		p=1
		for word in words:
			if doc in word_dic[word]:
				pwd1=word_dic[word][doc]*1.0/doc_len
			else:
				pwd1=1

			wDoc=0
			for d,freq in word_dic[word].items():
				wDoc=wDoc+freq

			p=p*(0.9*pwd1+(1-0.9)*(wDoc/len(doc_filaname)))
		docDic[doc]=p
	score[title]=docDic

if __name__ == '__main__':
	loadDic()
	loadQuery()
	for dirname in dirlist:
		loadDocument(dirname)

	for title,words in query.items():
		print(title)
		getUnigram(title,words)
	f = open('10152130138_Unigram.res', 'w')
	for key,value in score.items():
		valueSort=sorted(value.items(),key=lambda d:d[1],reverse=True)#按照score倒序
		t=0
		for key1, value1 in valueSort:
			if t<500:
				f.write(key+' '+'0'+' '+key1+' '+str(t)+' '+str(value1)+' '+'10152130138_dingwanning_unigram'+'\n')
				t=t+1
	f.close()
