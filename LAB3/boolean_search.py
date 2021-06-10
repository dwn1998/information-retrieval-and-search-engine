import json
from numpy import*
import xml.etree.ElementTree as ET
import os
rootdir_ap="./XML_AP"
rootdir_zf="./XML_ZF"
rootdir_wsj="./XML_WJS"
rootdir_doe="./XML_DOE"
rootdir_fr="./XML_FR"
key=[]
doc_filename=[]
query_word=[]
word_dic={}
flag=-1
def loadDic():
    f_dic=open("inverted_index.json",encoding='utf-8')
    word_list=json.load(f_dic)
    for word in word_list:
        word_dic[word[0]]=word[1]
    for e in word_dic.keys():
        key.append(e)
def getDocName(str_dir,filename):
    dirfilename = str_dir+'/' + filename
    if filename != '.DS_Store':
        xmldoc = ET.parse(dirfilename)
        for e in xmldoc.findall('DOC'):
            for s1 in e.findall('DOCNO'):
                doc_filename.append(s1.text.strip())
def loadFileName():
    for parent,dirnames,filenames in os.walk(rootdir_ap):
        for e in filenames:
            getDocName(rootdir_ap,e)

    for parent,dirnames,filenames in os.walk(rootdir_zf):
        for e in filenames:
            getDocName(rootdir_zf, e)

    for parent,dirnames,filenames in os.walk(rootdir_doe):
        for e in filenames:
            getDocName(rootdir_doe, e)

    for parent,dirnames,filenames in os.walk(rootdir_wsj):
        for e in filenames:
            getDocName(rootdir_wsj, e)

    for parent,dirnames,filenames in os.walk(rootdir_fr):
        for e in filenames:
            getDocName(rootdir_fr, e)

def makeMatrix(word):
    word_array=[0]*len(doc_filename)
    i=0
    word_key=[]
    for key in word_dic[word].keys():
        word_key.append(key)
    for doc in doc_filename:
        if doc in word_key:
            word_array[i]=1
        else:
            word_array[i]=0
        i=i+1
    return word_array
def operatorAnd(word1,word2,search_result):
    arr=[0]*len(doc_filename)
    if word1:
        arr1 = makeMatrix(word1)
        arr2 = makeMatrix(word2)
        for i in range(len(arr1)):
            arr[i] = arr1[i] & arr2[i]
    else:
        arr2 = makeMatrix(word2)
        for i in range(len(arr2)):
            arr[i] = search_result[i] & arr2[i]
    return arr
def operatorOr(word1,word2,search_result):
    arr=[0]*len(doc_filename)
    if word1:
        arr1 = makeMatrix(word1)
        arr2 = makeMatrix(word2)
        for i in range(len(arr1)):
            arr[i] = arr1[i]|arr2[i]
    else:
        arr2 = makeMatrix(word2)
        for i in range(len(arr2)):
            arr[i] = search_result[i] | arr2[i]
    return arr
def operatorNot(word1,word2,search_result):
    arr = [0] * len(doc_filename)
    if word1:
        arr1 = makeMatrix(word1)
        arr2 = makeMatrix(word2)
        if flag==1:
            for i in range(len(arr1)):
                arr[i] = arr1[i] & ~arr2[i]
            return arr
        elif flag==0:
            for i in range(len(arr1)):
                arr[i] = arr1[i] | ~arr2[i]
            return arr
    else:
        arr1 = makeMatrix(word1)
        arr2 = makeMatrix(word2)
        if flag==1:
            for i in range(len(arr1)):
                arr[i] = search_result[i] & ~arr2[i]
            return arr
        elif flag==0:
            for i in range(len(arr1)):
                arr[i] = arr1[i] | ~arr2[i]
            return arr

def getBooleanSearch(search_word):
    search_list=[]
    word1=''
    word2=''
    logical_operator=''
    search_result = [0] * len(doc_filename)
    for e in search_word.split():
        search_list.append(e)
    for i in range(len(search_list)):
        if i%2==1:
            logical_operator=search_list[i]
        if i==0:
            word1=search_list[i]
        if i%2==0 and i!=0:
            word2=search_list[i]
            print(word1,word2,logical_operator)
            if logical_operator=='and':
                search_result=operatorAnd(word1,word2,search_result)
            elif logical_operator=='or':
                search_result=operatorOr(word1,word2,search_result)
            elif logical_operator=='not':
                search_result=operatorNot(word1,word2,search_result)
    return search_result
if __name__ == '__main__':
    loadDic()
    loadFileName()
    while(True):
        query_word = input("请输入查询语句：")
        if query_word == "quit":
            break
        result = getBooleanSearch(query_word)
        for i in range(len(result)):
            if result[i] == 1:
                print(doc_filename[i])



