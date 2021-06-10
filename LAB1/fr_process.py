#!/usr/bin/python
# coding=utf-8 ##以utf-8编码储存中文字符
from xml.dom.minidom import parse
from nltk.stem import WordNetLemmatizer
import xml.dom.minidom
import xml.etree.ElementTree as ET
import nltk
import re
import sys
import codecs
import os
import gzip 
stopwords=[]
docno_fr=[]
docid_fr=[]
text_fr=[]
fr=[]
rootdir1_fr="./disk12/disk1/FR"
rootdir2_fr="./disk12/disk2/FR"
class PorterStemmer:
    def __init__(self):
        self.b = ""  # buffer for word to be stemmed
        self.k = 0
        self.k0 = 0
        self.j = 0   # j is a general offset into the string

    def cons(self, i):
        if self.b[i] == 'a'or self.b[i] == 'e'or self.b[i] == 'i'or self.b[i] == 'o'or self.b[i] == 'u':
            return 0
        if self.b[i] == 'y':
            if i == self.k0:
                return 1
            else:
                return (not self.cons(i - 1))
        return 1

    def m(self):
        n = 0
        i = self.k0
        while 1:
            if i > self.j:
                return n
            if not self.cons(i):
                break
            i = i + 1
        i = i + 1
        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.cons(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1
            while 1:
                if i > self.j:
                    return n
                if not self.cons(i):
                    break
                i = i + 1
            i = i + 1

    def vowelinstem(self):
        for i in range(self.k0, self.j + 1):
            if not self.cons(i):
                return 1
        return 0

    def doublec(self, j):
        if j < (self.k0 + 1):
            return 0
        if (self.b[j] != self.b[j-1]):
            return 0
        return self.cons(j)

    def cvc(self, i):
        if i < (self.k0 + 2) or not self.cons(i) or self.cons(i-1) or not self.cons(i-2):
            return 0
        ch = self.b[i]
        if ch == 'w'or ch == 'x'or ch == 'y':
            return 0
        return 1

    def ends(self, s):
        length = len(s)
        if s[length - 1] != self.b[self.k]: # tiny speed-up
            return 0
        if length > (self.k - self.k0 + 1):
            return 0
        if self.b[self.k-length+1:self.k+1] != s:
            return 0
        self.j = self.k - length
        return 1

    def setto(self, s):
       
        length = len(s)
        self.b = self.b[:self.j+1] + s + self.b[self.j+length+1:]
        self.k = self.j + length

    def r(self, s):
      
        if self.m() > 0:
            self.setto(s)

    def step1ab(self):
        if self.b[self.k] == 's':
            if self.ends("sses"):
                self.k = self.k - 2
            elif self.ends("ies"):
                self.setto("i")
            elif self.b[self.k - 1] != 's':
                self.k = self.k - 1
        if self.ends("eed"):
            if self.m() > 0:
                self.k = self.k - 1
        elif (self.ends("ed") or self.ends("ing")) and self.vowelinstem():
            self.k = self.j
            if self.ends("at"):   self.setto("ate")
            elif self.ends("bl"): self.setto("ble")
            elif self.ends("iz"): self.setto("ize")
            elif self.doublec(self.k):
                self.k = self.k - 1
                ch = self.b[self.k]
                if ch == 'l'or ch == 's'or ch == 'z':
                    self.k = self.k + 1
            elif (self.m() == 1 and self.cvc(self.k)):
                self.setto("e")

    def step1c(self):
       
        if (self.ends("y") and self.vowelinstem()):
            self.b = self.b[:self.k] + 'i'+ self.b[self.k+1:]
    def step2(self):
        
        if self.b[self.k - 1] == 'a':
            if self.ends("ational"):   self.r("ate")
            elif self.ends("tional"):  self.r("tion")
        elif self.b[self.k - 1] == 'c':
            if self.ends("enci"):      self.r("ence")
            elif self.ends("anci"):    self.r("ance")
        elif self.b[self.k - 1] == 'e':
            if self.ends("izer"):      self.r("ize")
        elif self.b[self.k - 1] == 'l':
            if self.ends("bli"):       self.r("ble") # --DEPARTURE--
            # To match the published algorithm, replace this phrase with
            #   if self.ends("abli"):      self.r("able")
            elif self.ends("alli"):    self.r("al")
            elif self.ends("entli"):   self.r("ent")
            elif self.ends("eli"):     self.r("e")
            elif self.ends("ousli"):   self.r("ous")
        elif self.b[self.k - 1] == 'o':
            if self.ends("ization"):   self.r("ize")
            elif self.ends("ation"):   self.r("ate")
            elif self.ends("ator"):    self.r("ate")
        elif self.b[self.k - 1] == 's':
            if self.ends("alism"):     self.r("al")
            elif self.ends("iveness"): self.r("ive")
            elif self.ends("fulness"): self.r("ful")
            elif self.ends("ousness"): self.r("ous")
        elif self.b[self.k - 1] == 't':
            if self.ends("aliti"):     self.r("al")
            elif self.ends("iviti"):   self.r("ive")
            elif self.ends("biliti"):  self.r("ble")
        elif self.b[self.k - 1] == 'g': # --DEPARTURE--
            if self.ends("logi"):      self.r("log")
        # To match the published algorithm, delete this phrase
    def step3(self):
        
        if self.b[self.k] == 'e':
            if self.ends("icate"):     self.r("ic")
            elif self.ends("ative"):   self.r("")
            elif self.ends("alize"):   self.r("al")
        elif self.b[self.k] == 'i':
            if self.ends("iciti"):     self.r("ic")
        elif self.b[self.k] == 'l':
            if self.ends("ical"):      self.r("ic")
            elif self.ends("ful"):     self.r("")
        elif self.b[self.k] == 's':
            if self.ends("ness"):      self.r("")

    def step4(self):
        if self.b[self.k - 1] == 'a':
            if self.ends("al"): pass
            else: return
        elif self.b[self.k - 1] == 'c':
            if self.ends("ance"): pass
            elif self.ends("ence"): pass
            else: return
        elif self.b[self.k - 1] == 'e':
            if self.ends("er"): pass
            else: return
        elif self.b[self.k - 1] == 'i':
            if self.ends("ic"): pass
            else: return
        elif self.b[self.k - 1] == 'l':
            if self.ends("able"): pass
            elif self.ends("ible"): pass
            else: return
        elif self.b[self.k - 1] == 'n':
            if self.ends("ant"): pass
            elif self.ends("ement"): pass
            elif self.ends("ment"): pass
            elif self.ends("ent"): pass
            else: return
        elif self.b[self.k - 1] == 'o':
            if self.ends("ion") and (self.b[self.j] == 's'or self.b[self.j] == 't'): pass
            elif self.ends("ou"): pass
            # takes care of -ous
            else: return
        elif self.b[self.k - 1] == 's':
            if self.ends("ism"): pass
            else: return
        elif self.b[self.k - 1] == 't':
            if self.ends("ate"): pass
            elif self.ends("iti"): pass
            else: return
        elif self.b[self.k - 1] == 'u':
            if self.ends("ous"): pass
            else: return
        elif self.b[self.k - 1] == 'v':
            if self.ends("ive"): pass
            else: return
        elif self.b[self.k - 1] == 'z':
            if self.ends("ize"): pass
            else: return
        else:
            return
        if self.m() > 1:
            self.k = self.j
    def step5(self): 
        self.j = self.k
        if self.b[self.k] == 'e':
            a = self.m()
            if a > 1 or (a == 1 and not self.cvc(self.k-1)):
                self.k = self.k - 1
        if self.b[self.k] == 'l'and self.doublec(self.k) and self.m() > 1:
            self.k = self.k -1
    def stem(self, p, i, j):
        # copy the parameters into statics
        self.b = p
        self.k = j
        self.k0 = i
        if self.k <= self.k0 + 1:
            return self.b 
        self.step1ab()
        self.step1c()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        return self.b[self.k0:self.k+1]

def get_stopword():
    file=open('stopword.txt')
    for line in file:
        stopwords.extend(line.strip('\n').split())
    file.close()

def tokenization(str_test):
    word_token=[]
    for i in range(len(str_test)):
        if str_test[i]==None:
            word_token.append("None")
        else:
            word_token.append(nltk.word_tokenize(str_test[i]))
    return word_token
def stopword(str_test):
    test=[]
    for words in str_test:
        s=words[:]
        for word in words:
            if word in stopwords:
                s=[e for e in s if e!=word]
        test.append(s)
    return test
def lemmatization(str_test):
    test=str_test[:]
    lemmatizaer=WordNetLemmatizer()
    for i in range(len(str_test)):
        for j in range(len(str_test[i])):
            if str_test[i][j]=="None":
                test[i][j]=""
            else:
                test[i][j]=lemmatizaer.lemmatize(str_test[i][j])
    return test
def stemmed(str_test):
    test=[]
    for words in str_test:
        s=[]
        for word in words:
            p=PorterStemmer()
            s.append(p.stem(word,0,len(word)-1))
        test.append(s)
    return test
def fr_getdata(str_dir,filename):
    dir_filename=str_dir+filename
    fr_open=open(dir_filename,"r")
    file=open(dir_filename+".xml","w")
    fr=""
    i=0
  
    test=[]
    for line in fr_open:
        flag=0
  
        test=""
        new_line=line
        if  "</ITAG>" in new_line and "<ITAG" in new_line:
                test=new_line.replace("</ITAG>","")
                new_line=re.sub("<ITAG.*\d>","",test)
                flag=1
        if "<ITAG" in new_line:
                new_line=re.sub("<ITAG.*\d>","",new_line)
                flag=1
        if "</ITAG>" in new_line:
                new_line=new_line.replace("</ITAG>","")
                flag=1
        if "<FTAG" in new_line and "</FTAG>" in new_line:
                test=new_line.replace("</FTAG>","")
                new_line=re.sub("<FTAG.*\d>","",test)
                flag=1
        if "<FTAG" in new_line:
                new_line=re.sub("<FTAG.*\d>","",new_line)
                flag=1
        if "</FTAG>" in new_line:
                new_line=new_line.replace("</FTAG>","")
                flag=1
           
        while "<T2>" in new_line or "</T2>" in new_line or "<T4>" in new_line or "</T4>" in new_line or"<T3>" in new_line or "</T3>" in new_line or"<NOTE>" in new_line or "</NOTE>" in new_line or "@" in new_line or "&" in new_line or"#" in new_line or "$" in new_line:
          
            new_line=new_line.replace("<T2>","").replace("</T2>","").replace("<T4>","").replace("</T4>","").replace("<NOTE>","").replace("</NOTE>","").replace("<T3>","").replace("</T3>","").replace("@","").replace("&","").replace("$","").replace("#","").replace("$","")
        
        if i==0:
            file.write("<document>\n"+new_line)
        else:
            file.write(new_line)
        i=i+1
    file.write("\n</document>")
    file.close()
    fr_open.close()

    xmldoc = ET.parse(dir_filename+".xml")
    for e in xmldoc.findall('DOC'):
        for s1 in e.findall('DOCNO'):
            docno_fr.append(s1.text.strip())
        for s2 in e.findall('DOCID'):
            docid_fr.append(s2.text.strip())
        for s7 in e.findall('TEXT'):
            text_fr.append(s7.text)   
    fr_processing(str_dir,filename)

def write_file_fr(text,str_dir,filename):
    t=0
    dir_filename=str_dir+filename
    xmldoc = ET.parse(dir_filename+".xml")
    for e in xmldoc.findall('DOC'):
        for s7 in e.findall('TEXT'):
            s7.text=" ".join(text[t])
        for s2 in e.findall('DOCNO'):
            s2.text="".join(docno_fr[t])
        t=t+1
    xmldoc.write(dir_filename+"_new.xml")
    fr=[]
    test=[]
    docno=[]
    file=open(dir_filename+"_new.xml")
    #分割文件
    flag_text=0 
    flag_docno=0
    flag_docid=0
    i=0
    for line in file:
        if "</DOC>" in line:
            test.append(line)
            fr.append(test)
            i=i+1
            test=[]
            flag_text=0
        elif "<DOC>" in line:
            test.append(line)
        elif "<DOCNO>" in line and "</DOCNO>" in line:
            test.append(line)
        elif "<DOCNO>" in line:
            test.append(line)
            flag_docno=1
        elif "</DOCNO>" in line :
            test.append(line)
            flag_docno=0
        elif flag_docno==1:
            test.append(line)
        elif "<DOCID>" in line and "</DOCID>" in line:
            test.append(line)
        elif "<DOCID>" in line:
            test.append(line)
            flag_docid=1
        elif "</DOCID>" in line :
            test.append(line)
            flag_docid=0
        elif flag_docid==1:
            test.append(line)
        elif "<TEXT>" in line:
            flag_text=1
            test.append(line)
        elif "</TEXT>" in line:
            flag_text=0
            test.append(line)
        elif flag_text==1:
            test.append(line)
        else:
            continue
    s=0
    for words in fr:
        query="".join(docno_fr[s])
        file_test=open('./XML_FR/'+query+".xml",'w')
        word="".join(words)
        file_test.write(word)
        s=s+1
        file_test.close()
    file.close()
def fr_processing(str_dir,filename):
    text_token=tokenization(text_fr)
    text_stopword=stopword(text_token)
    text_lemmatize=lemmatization(text_stopword)
    text=stemmed(text_lemmatize)
    write_file_fr(text,str_dir,filename)
    
if __name__ == '__main__':
    filename1=[]
    filename2=[]
    filename=[]
    get_stopword()
    for parent,dirnames,filenames in os.walk(rootdir1_fr):
        for e in filenames:
            filename1.append(e.replace(".gz",""))
    for word in filename1:
        f_name=word
        g_file=gzip.GzipFile(rootdir1_fr+'/'+word+".gz")
        open("./disk_FR/"+f_name,"w+").write(g_file.read().decode("utf8","ignore"))
        g_file.close()
    for parent,dirnames,filenames in os.walk(rootdir2_fr):
        for e in filenames:
            filename2.append(e.replace(".gz",""))
    for word in filename2:
        f_name=word
        g_file=gzip.GzipFile(rootdir2_fr+'/'+word+".gz")
        open("./disk_FR/"+f_name,"w+").write(g_file.read().decode("utf8","ignore"))
        g_file.close()

    for parent,dirnames,filenames in os.walk("./disk_FR"):
        for e in filenames:
            filename.append(e)
            fr_getdata("./disk_FR/",e)
            docno_fr=[]
            text_fr=[]
            docid_fr=[]
            


   