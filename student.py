# PyCon ACPC 2014
# Zhan Yuli

class St(object):
    "Indivial student data model"
    
    def __init__(self,name,cls):
        self.__name = name
        self.__class = cls
        self.__chs = []
        self.__math = []
        self.__eng = []
        self.__bio = []
        self.__phy = []
        self.__chem = []
        self.__his = []
        self.__geog = []
        self.__overall = []
        # classification parameter - 1 (pass)
        self.__result = -1
        # classification parameter - 2 (final result)
        self.__final = -1

    def add_chs(self,chs):
        self.__chs.append(chs)

    def add_math(self,math):
        self.__math.append(math)

    def add_eng(self,eng):
        self.__eng.append(eng)

    def add_bio(self,bio):
        self.__bio.append(bio)

    def add_phy(self,phy):
        self.__phy.append(phy)

    def add_chem(self,chem):
        self.__chem.append(chem)

    def add_his(self,his):
        self.__his.append(his)

    def add_geog(self,gs):
        self.__geog.append(gs)

    def add_overall(self,overall):
        self.__overall.append(overall)

    def set_classification(self,cla):
        self.__result = cla

    def set_final(set,f):
        self.__final = f
    
    def show_chs(self):
        return self.__chs

    def show_math(self):
        return self.__math

    def show_eng(self):
        return self.__eng

    def show_bio(self):
        return self.__bio

    def show_phy(self):
        return self.__phy

    def show_chem(self):
        return self.__chem

    def show_his(self):
        return self.__his

    def show_geog(self):
        return self.__geog

    def show_overall(self):
        return self.__overall

    def get_name(self):
        return self.__name

    def get_class(self):
        return self.__class
    
    def get_classification(self):
        return self.__result
    
    def get_final(self):
        return self.__final
        
