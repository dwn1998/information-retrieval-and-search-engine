#!/usr/bin/python
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
import json
import os
from collections import Counter
docno=[]
text=[]
dict_test={}
my_dict=[]
rootdir_ap="./XML_AP"
rootdir_zf="./XML_ZF"
rootdir_wsj="./XML_WSJ"
rootdir_doe="./XML_DOE"
rootdir_fr="./XML_FR"
def getdata(str_dir,filename):
    dirfilename=str_dir+'/'+filename
    xmldoc = ET.parse(dirfilename)
    for e in xmldoc.findall('DOC'):
        test=""
        for s1 in e.findall('DOCNO'):
            docno.append(s1.text.strip())
        for s7 in e.findall('TEXT'):
            if s7.text==None:
                continue
            else:
                test=test+s7.text
        text.append(test)   
    create_inverted_index()
def create_inverted_index():
    print("create")
    test={}
    i=0
    for words in text:
        for word in words.split():
            if word==';' or word==',' or word=='$' or word=='//' or word=='/' or word=='{' or word=='}':
                continue
            if word in dict_test:
                    if docno[i] in dict_test[word]:
                         dict_test[word][docno[i]]=dict_test[word][docno[i]]+1
                    else:
                        dict_test[word][docno[i]]=1
            else:
                test[docno[i]]=1
                dict_test[word]=test
                test={}
        i=i+1
def add_invert():
    dict_final=my_dict[0]
    for word in my_dict[1:]:
        for key1 in word:
            if key1 in dict_final:
                dict_final[key1]=dict(Counter(dict_final[key1])+Counter(word[key1]))
            else:
                dict_final[key1]=word[key1]

    dict_sorted=sorted(dict_final.items(),key=lambda d:d[0])

    file_write = open("inverted_index.json", 'w')
    i = 0
    for word in dict_sorted:
        jsobj = json.dumps(word[1])
        if i == 0:
            file_write.write('{ "' + word[0] + '" :' + jsobj + ',')
        else:
            file_write.write('"' + word[0] + '" :' + jsobj + ',')
        i = i + 1
    file_write.write('}')
    file_write.close()
if __name__ == '__main__':
    print("my")
    for parent,dirnames,filenames in os.walk(rootdir_ap):
        for e in filenames:
            print(e)
            getdata(rootdir_ap,e)
            docno=[]
            text=[]
    my_dict.append(dict_test)
    dict_test={}

    for parent,dirnames,filenames in os.walk(rootdir_zf):
        for e in filenames:
            print(e)
            getdata(rootdir_zf,e)
            docno=[]
            text=[]
    my_dict.append(dict_test)
    dict_test={}

    for parent,dirnames,filenames in os.walk(rootdir_doe):
        for e in filenames:
            print(e)
            getdata(rootdir_doe,e)
            docno=[]
            text=[]
    my_dict.append(dict_test)
    dict_test={}

    for parent,dirnames,filenames in os.walk(rootdir_wsj):
        for e in filenames:
            print(e)
            getdata(rootdir_wsj,e)
            docno=[]
            text=[]
    my_dict.append(dict_test)
    dict_test={}

    for parent,dirnames,filenames in os.walk(rootdir_fr):
        for e in filenames:
            print(e)
            getdata(rootdir_fr,e)
            docno=[]
            text=[]
    my_dict.append(dict_test)
    add_invert()
    print("#")