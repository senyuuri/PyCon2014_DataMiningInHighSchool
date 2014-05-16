# PyCon ACPC 2014
# Zhan Yuli

import time
import pdb
import glob
import os
from subject_match import *
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import itertools

#pdb.set_trace()

# linked list structure
# Student - Subject1 - Subject2 -....
#             |          |
#           Score1     Score1
#             |
#           Score2
#             |
#            ...TypeError: 'int' object is not iterable


class Student(object):
    def __init__(self, sid, cls):
        self.__sid = sid
        self.__cls = cls
        self.__sub = None

    def addSubject(self, sub):
        self.__sub = sub

    def getSubject(self):
        return self.__sub

    def getSid(self):
        return self.__sid

    def getClass(self):
        return self.__cls
        

class Subject(object):
    def __init__(self, code):
        self.__code = code
        self.__score = []
        self.__alevel = None
        self.__next = None

    def addNext(self, node):
        self.__next = node

    def addScore(self, score):
        self.__score.append(score)

    def addAlevel(self, alevel):
        self.__alevel = alevel

    def getScore(self):
        return self.__score

    def getAlevel(self):
        return self.__alevel

    def getNext(self):
        return self.__next

    def getCode(self):
        return self.__code


# print everything
def traverseToFile(data):
    fout = open("output.txt","w")
    for st in data:
        fout.write(st.getSid() + " " + st.getClass()+"\n")
        #print(st.getSid(),st.getClass())
        subject = st.getSubject()
        while subject:
            #print("Code:",subject.getCode()," Result:",subject.getScore())
            #print("    Alevel:",subject.getAlevel())
            fout.write("Code: "+subject.getCode()+" Result: "+",".join(subject.getScore())+"\n")
            if subject.getAlevel()!= None:
                fout.write("    Alevel:"+subject.getAlevel()+"\n")
            subject = subject.getNext()
            
    fout.close()

def traverse(data,subcode):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_zticks((20,17.5,15,12.5,10,5,0))
    ax.set_zticklabels(("A","B","C","D","E","S","U"))
    ax.set_yticks((0,1,2,3,4,5))
    ax.set_yticklabels(("y5 midyr","y5 promo","y6 mct","y6 jct","y6 prelim","A level "))
    ax.set_xlabel("Student")
    ax.set_ylabel("Examination")
    ax.set_zlabel("Result")
    count = 0
    for st in data:
        count += 1
        index = ["A","B","C","D","E","S","U"]
        subject = st.getSubject()
        while subject:
            if subject.getCode() == subcode:
                  scores = subject.getScore()
                  y = []
                  for s in scores:
                      if s and s != " " and s != "\n":
                          y.append(grade2num[s.replace("(","").replace(")","")[0]])
                  if subject.getAlevel() != None:
                      y.append(grade2num[subject.getAlevel()])
                  x = range(len(y))
                  #z = len(y)*[int(st.getSid()[1:])]
                  z = len(y) * [count]
                  #print(subject.getAlevel())
                  if subject.getAlevel() == "A":
                      ax.plot(z,x,y,"b")
                  else:
                      #if y[0] != 20:
                      pass
                      ax.plot(z,x,y,"r")
            subject = subject.getNext()
    plt.show()

def sortAsc(data,subcode):
    index = ["A","B","C","D","E","S","U"]
    container = 7*[0]
    for st in data:
        subject = st.getSubject()
        while subject:
            if subject.getCode() == subcode:
                agrade = subject.getAlevel()
                if agrade!= None:
                    idx = index.index(agrade)
                    if container[idx] != 0:
                        container[idx].append(st)
                    else:
                        container[idx] = [st]
            subject = subject.getNext()
    result = []
    for i in container:
        if i != 0:
            for item in i:
             result.append(item)
    return result

def grade3D(data,subcode):
    data = sortAsc(data,subcode)
    traverse(data,subcode)

# find subject by subject name
def findSubject(data,sub):
    pass

# find student by sid
def findStudent(data,sid):
    pass
    
# initialisation
# ranking point coversion
grade2num = {"A":20,
             "B":17.5,
             "C":15,
             "D":12.5,
             "E":10,
             "S":5,
             "U":0,}
stinfo = []
st_list = []
start = time.time()
# data point counter
counter = 0
directory = "dhs"
files = os.path.join(directory,"*.csv")
print(glob.glob(files)[:-1])

for csv_file in glob.glob(files)[:-1]:
    print("Preprocessing ", csv_file)
    with open(csv_file,"r") as input_file:
        line = input_file.readline()
        while line:
            line = line.split(",")
            counter += len(line)
            # if new student
            if line[0] not in st_list:
                #print("New student ",line[0])
                st_list.append(line[0])
                tempSt = Student(line[0],line[1])
                tempSb = Subject(line[2])
                tempSb.addScore(line[3].replace("(","").replace(")","")[0])
                tempSt.addSubject(tempSb)
                for i in range(4,len(line),2):
                    if line[i] and line[i+1] and line[i+1]!="\n":
                        newSb = Subject(line[i])
                        newSb.addScore(line[i+1].replace("(","").replace(")","")[0])
                        tempSb.addNext(newSb)
                        tempSb = newSb
                stinfo.append(tempSt)
            # append result to existing record
            else:
                # find record index by sid
                index = st_list.index(line[0])
                # retrive student record
                tempSt = stinfo[index]
                nextSub = tempSt.getSubject()
                for i in range(2,len(line),2):
                    if line[i] and line[i+1] and line[i+1] != "\n":
                        #print("i: line[i]",line[i])
                        found = False
                        while nextSub:
                            # if subject code match
                            #print(nextSub.getCode())
                            if line[i] and line[i] == nextSub.getCode():
                                if line[i+1]:
                                    nextSub.addScore(line[i+1].replace("(","").replace(")","")[0])
                                found = True
                                break
                            else:
                                nextSub = nextSub.getNext()
                        if not found:
                            # locate end of linked list
                            nextSub = tempSt.getSubject()
                            while nextSub.getNext()!= None:
                                nextSub = nextSub.getNext()
                            #print(nextSub.getCode())
                            # subject combination changed
                            #print("Subject changed:",line[0],)
                            newSub = Subject(line[i])
                            if line[i+1]:
                                newSub.addScore(line[i+1].replace("(","").replace(")","")[0])
                            nextSub.addNext(newSub)                                       
                    # initialise to first subject
                    nextSub = tempSt.getSubject()
            line = input_file.readline()

# Add alevel result
#a_file = open("dhs/6_y6alevel.csv","r")
with open("dhs/6_y6alevel.csv","r") as input_file:
    line = input_file.readline()
    while line:
        line = line.split(",")
        counter += len(line)
        # if new student
        if line[0] not in st_list:
            print(line[0]+" Warning: historical record not found")
        # append result to existing record
        else:
            # find record index by sid
            index = st_list.index(line[0])
            # retrive student record
            tempSt = stinfo[index]
            nextSub = tempSt.getSubject()
            for i in range(2,len(line)):
                # non-H3 subjects
                if line[i] and len(line[i]) != 1 and line[i][:2]!="H3":
                    #print("i: line[i]",line[i])
                    found = False
                    while nextSub:
                        # if subject code match
                        #print(nextSub.getCode())
                        # covert Alevel code to school code
                        aCode = line[i][:-3]
                        #print(len(line[i]),line[i],aCode)
                        if not aCode.isdigit():
                        #print(aCode)
                            sCode = sub_match[aCode]
                        if line[i] and sCode == nextSub.getCode():
                            result = line[i][-2]
                            nextSub.addAlevel(result)
                            found = True
                            break
                        else:
                            nextSub = nextSub.getNext()
                    if not found:
                        print(line[0],line[i],"Warning: first time taking the subject?")
                        # add new node
                        # locate end of linked list
                        nextSub = tempSt.getSubject()
                        while nextSub.getNext()!= None:
                            nextSub = nextSub.getNext()
                            sCode = sub_match[line[i][:-3]]
                            result = line[i][-2]
                            newSub = Subject(sCode)
                            newSub.addAlevel(result)
                        nextSub.addNext(newSub)                                       

                        
                # H3 subjects
                elif line[i] and len(line[i]) != 1:
                    found = False
                    while nextSub:
                        #çprint(line[i],nextSub.getCode())
                        if line[i] and nextSub.getCode()[:2]=="H3":
                            result = line[i][-2]
                            nextSub.addAlevel(result)
                            found = True
                            break
                        else:
                            nextSub = nextSub.getNext()
                    if not found:
                        pass
                        #print(line[0]+"Warning: first time taking the H3 subject?")
                    
                # initialise to first subject
                nextSub = tempSt.getSubject()
        line = input_file.readline()

print("Time cost:",time.time() - start)

grade3D(stinfo,"H2CHEM")
#grade3D(stinfo,"H2COMP")
#grade3D(stinfo,"H2ECONS")
print(len(stinfo))
print(counter)
