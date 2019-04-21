from collections import defaultdict

string = "green"
minsup = 52
columns = 512
numberOfClusters = 8

db = []
string_db = []


# Reading data base as list in db and " " + line + " " in string_db
with open(string + "ClusterEncoded.txt","r") as file:
    for line in file:
        db.append(line.split())
        string_db.append(" " + line.replace('\n','').replace("  "," ").rstrip().lstrip() + " ")




frequentPatterns = {}
for i in range(1 ,columns + 1):
    frequentPatterns[i] = {}        # initialization of patterns.




# adding all one lenght sequences
for i in range(0,numberOfClusters):
    for line in string_db:
        key = " " + str(i) + " "
        if key in line:
            if key in frequentPatterns[1].keys():
                frequentPatterns[1][key] += 1
            else:
                frequentPatterns[1][key] = 1



    # print db



def frequent_rec(patt, mdb):
    pattern_len = len(patt)
    if(pattern_len > 1):  # adding pattern to result if and only if len > 1 becoz single length sequences are already added
        key = ""
        for k in patt:
            key += " " + k
        key += " "
        frequentPatterns[pattern_len][key] = len(mdb)

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in range(startpos + 1, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j))

    for (c, newmdb) in occurs.items():
        if len(newmdb) >= minsup:
            frequent_rec(patt + [c], newmdb)



frequent_rec([], [(i, -1) for i in range(len(db))])



# Pop all non closed sequences
for key1 in frequentPatterns[i].keys():
    for key2 in frequentPatterns[i - 1].keys():
        if ((key2 in key1) and (frequentPatterns[i][key1] == frequentPatterns[i - 1][key2])):
            frequentPatterns[i - 1].pop(key2, None)



# total = 0
# for i in range(1,5):
#     total += len(frequentPatterns[i].keys())
#     print frequentPatterns[i]
# print(total)

allKeys = []
allFrequentPatterns = {}
for i in range(1, columns + 1):
    for key in frequentPatterns[i].keys():
        allKeys.insert(0, key.lstrip().rstrip())
        allFrequentPatterns[key.lstrip().rstrip()] = 0


# By this time all frequent sequences are generated
'''*********************************************'''
# Find the modified frequency of each sequence
for line in string_db:
    # print "x"
    for key in allKeys:
        # print key
        key = " " + key + " "
        if (key in line):
            allFrequentPatterns[key.lstrip().rstrip()] += line.count(key)
            while (key in line):
                line = line.replace(key, ' ')

    # print line
finalKeys = open(string + "Patterns.txt", "w")
finalLength = 0
for eachKey in allKeys:
    if (allFrequentPatterns[eachKey] != 0):
        finalKeys.write(eachKey.lstrip().rstrip() + "-" + str(allFrequentPatterns[eachKey]) + "\n")
        finalLength = finalLength + (len(eachKey.lstrip().rstrip().split(" ")) * allFrequentPatterns[eachKey])
finalKeys.close()



# total = 0
# for i in range(1,columns + 1):
#     total += len(frequentPatterns[i].keys())
#     print frequentPatterns[i]
# print(total)

