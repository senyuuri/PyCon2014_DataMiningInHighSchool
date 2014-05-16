# PyCon ACPC 2014
# Zhan Yuli
# Code reference
# 1)Peter Harrington - Data Mining in Action

from numpy import *
import matplotlib.pyplot as plt
from dhs_preprocessing import *

grade2num = {"A":20,
             "B":17.5,
             "C":15,
             "D":12.5,
             "E":10,
             "S":5,
             "U":0,}

index = ["A","B","C","D","E","S","U"]


def standRegres(xArr,yArr,sid):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        return
    ws = xTx.I * (xMat.T*yMat)
    return ws

def predict(st,code):
    try:
        subject = st.getSubject()
        while subject:
            if subject.getCode() == code:
                y = [grade2num[x.replace("\n","")] for x in subject.getScore() if x != " " and x!="" and x!="\n"]
                x_graph = range(len(y))
                x_cal = []
                z = len(y) * [int(st.getSid()[1:])]
                for i in range(len(y)):
                    x_cal.append([1.0,i])
                ax.plot(z,x_graph,y,"bo")
                #ax.plot(x_graph,y,"b")
            subject = subject.getNext()
    except KeyError:
        print(st.getSid(),subject.getScore())
    return x_cal, y

def analyse_sub(code,moderation):
    count = 0
    correct = 0
    secMatch = 0
    npolar = 0
    ppolar = 0
    for st in stinfo:
        select = False
        aresult = ""
        sub = st.getSubject()
        while sub:
            if sub.getCode() == code:
                select = True
                aresult = sub.getAlevel()
                break
            sub = sub.getNext()
        if select:
            x, y = predict(st,code)
            ws = None
            if x and y:
            #print(x,y)
                ws = standRegres(x,y,st.getSid())
            if ws != None:
                count += 1
                xMat = mat(x)
                yMat = mat(y)
                yHat = (xMat*ws).getA()
                #xCopy = xMat.copy().getA()
                #ax.plot(len(y) * [int(st.getSid()[1:])],xCopy[:,1],yHat)
                #print("yHat",yHat)
                grad = (yHat[0] - yHat[-1])/(x[0][1]-x[-1][1])
                yinter = y[0] - x[0][1]*grad
                result = 5*grad + yinter
                #moderation
                if moderation:
                    result += moderation
                #print(grad,yinter,result)
                grade = ""
                if result >= 18.75:
                    grade = "A"
                elif result >= 16.25:
                    grade = "B"
                elif result >= 13.75:
                    grade = "C"
                elif result >= 11.25:
                    grade = "D"
                elif result >= 7.5:
                    grade = "E"
                elif result >= 2.5:
                    grade = "S"
                else:
                    grade = "U"
                #print(st.getSid(),"P:",grade,"A:",aresult)
                if aresult:
                    if grade == aresult:
                        correct += 1
                    elif absolute(index.index(grade)-index.index(aresult))==1:
                        correct += 1
                        secMatch += 1
                    if grade > aresult:
                        npolar += -1
                    elif grade < aresult:
                        ppolar += 1
                
                #print(corrcoef(yHat.T, yMat))
    #plt.show()
    #print("Total:",count)
    #print("Correct",correct)
    print(code,"lower:",npolar,"higher",ppolar,"Correct rate:",correct/count*100,"%","secMatch:",secMatch/count*100,"%")
    #print(code,count,"Accuracy",str(correct/count*100)+"%","secMatch:",str(secMatch/count*100)+"%")
    #print(code,str(correct/count*100)+"%")
    return correct/count*100


#sublist = ['H2MATH', 'H1GSC', 'H1BIO', 'H2COMP', 'H1GEO', 'H2FRENCH', 'H2ELIT', 'H1ELIT', 'H1GP', 'H2ECONS', 'H1PW', 'H2MUS', 'H1CL', 'H1ECONS', 'H2HIST', 'H2ART', 'H2GEO', 'H2PHY', 'H1MATH', 'H2CHEM', 'H2BIO', 'H1ART', 'H1PHY', 'H1HIST', 'H1 CSC', 'H2CLL', 'H2 CSC', 'H2JAPANESE', 'H1CHEM']
sublist = ['H2MATH', 'H1GSC', 'H2COMP', 'H2ELIT', 'H1ELIT', 'H1GP', 'H2ECONS', 'H1ECONS', 'H2HIST', 'H2ART', 'H2GEO', 'H2PHY', 'H1MATH', 'H2CHEM', 'H2BIO', 'H1PHY', 'H1HIST',  'H2CLL', 'H2 CSC', 'H1CHEM']
total = 0
fig = plt.figure()
ax = fig.gca(projection='3d')
for s in sublist:
    total += analyse_sub(s,0)
print("Overall accuracy:",total/len(sublist))
#plt.show()
'''


code = "H2CHEM"
for i in range(0,20):
    moderation = i*1.25
    print("M:",moderation)
    analyse_sub(code,moderation)
'''
