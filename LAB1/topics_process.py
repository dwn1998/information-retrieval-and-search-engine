#!/usr/bin/python
from xml.dom.minidom import parse
from nltk.stem import WordNetLemmatizer
import xml.dom.minidom
import xml.etree.ElementTree as ET
import nltk

query_title=[]
query_desc=[]
query_narr=[]
stopwords=[]
title_name=[]


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

def topics_makexml():
    query_open=open('topics.151-200',"r")
    file=open("topics.xml",'w')
    i=0;
    for line in query_open:
        if i==0:
            file.write(line.replace("<top>","<collection>\n<top>").replace("<title>","</num>\n<title>").replace("<desc>","</title>\n<desc>").replace("<narr>","</desc>\n<narr>").replace("</top>","</narr>\n</top>"))
        else:
             file.write(line.replace("<title>","</num>\n<title>").replace("<desc>","</title>\n<desc>").replace("<narr>","</desc>\n<narr>").replace("</top>","</narr>\n</top>"))
        i=i+1  
    file.close()
    file_add=open("topics.xml",'a')
    file_add.write('</collection>')
    file_add.close()
    query_open.close()
def topics_getdata():
    DOMTree = xml.dom.minidom.parse("topics.xml")
    collection = DOMTree.documentElement
    docs = collection.getElementsByTagName("top")
    for doc in docs:
        num = doc.getElementsByTagName('num')[0]
        title = doc.getElementsByTagName('title')[0]
        title_name.append(title.childNodes[0].data.strip('\n').split())
        query_title.append(title.childNodes[0].data)
        desc = doc.getElementsByTagName('desc')[0]
        query_desc.append(desc.childNodes[0].data)
        narr = doc.getElementsByTagName('narr')[0]
        query_narr.append(narr.childNodes[0].data)   
         
def write_file_topics(title,desc,narr):
    i=0
    xmldoc = ET.parse("topics.xml")
    for e in xmldoc.findall('top'):
        for s1 in e.findall('title'):
            s1.text = " ".join(title[i])
        for s2 in e.findall('desc'):
            s2.text = " ".join(desc[i])
        for s3 in e.findall('narr'):
            s3.text = " ".join(narr[i])
        i=i+1
    xmldoc.write("topics_new.xml")
    divided_topics_file()
def divided_topics_file():
    file=open("topics_new.xml")
    topics=[]
    test=[]
    #分割文件
    for line in file:
        if "</top>" in line:
            test.append(line)
            topics.append(test)
            test=[]
        else:
            test.append(line)
    for i in range(len(title_name)):
        title_name[i].remove("Topic:")
        for word in title_name[i]:
            if '/' in word:
                title_name[i].remove(word) 
        i=i+1
    s=0
    for words in topics:
        query=" ".join(title_name[s])
        file_test=open('./disk_TOPICS/'+query+".xml" ,'w')
        word="".join(words)
        file_test.write(word)
        s=s+1
        file_test.close()
def topics_processing():
    title_token=tokenization(query_title)
    title_stopword=stopword(title_token)
    title_lemmatize=lemmatization(title_stopword)
    title=stemmed(title_lemmatize)
    desc_token=tokenization(query_desc)
    desc_stopword=stopword(desc_token)
    desc_lemmatize=lemmatization(desc_stopword)
    desc=stemmed(desc_lemmatize)
    narr_token=tokenization(query_narr)
    narr_stopword=stopword(narr_token)
    narr_lemmatize=lemmatization(narr_stopword)
    narr=stemmed(narr_lemmatize)
    write_file_topics(title,desc,narr)
if __name__ == '__main__':
    get_stopword()
    topics_makexml()
    topics_getdata()
    topics_processing()