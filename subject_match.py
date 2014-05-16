# PyCon ACPC 2014
# Zhan Yuli
# match different subject code between school results and alevel results
# *ignore H3 subjects, assume all H3s don't change
f1 = open("dhs/5_y6prelim.csv","r")
f2 = open("dhs/6_y6alevel.csv","r")

sub1 = set()
sub2 = set()
line = f1.readline()
while line:
    line = line.split(",")
    for l in line:
        if l and l[0] == "H" and l not in sub1 and l[:2]!="H3":
            sub1.add(l)
    line = f1.readline()
    
line = f2.readline()
while line:
    line = line.split(",")
    for l in line:
        if l and l[0] == "H" and l[:2] !="H3":
            temp = l.replace("(","").replace(")","")[:-1]
            if temp not in sub2:
                sub2.add(temp)
    line = f2.readline()

#print(sub1)
#print(sub2)

auto_match = {}
for a in sub1:
    match = False
    for b in sub2:
        if a[:4] == b[:4]:
            #print("Match",a,b)
            match = True
            auto_match[b] = a
    if not match:
        pass
        #print("No match",a)
    match = True

manual_match = {"H2CP":"H2COMP",
                "H2JP":"H2JAPANESE",
                "H2HS":"H2HIST",
                "H1HS":"H1HIST",
                "PW":"H1PW",
                "GP":"H1GP",
                "H2CSC":"H2 CSC",
                "H1CSC":"H1 CSC",}

sub_match = auto_match.copy()
sub_match.update(manual_match)
#print("Subject Match:")
#print(sub_match)
f1.close()
f2.close()
