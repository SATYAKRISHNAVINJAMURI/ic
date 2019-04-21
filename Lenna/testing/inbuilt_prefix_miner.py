from pyprefixspan import pyprefixspan
from pprint import pprint


data =     ['0 1 2 3 4',
    '1 1 1 3 4',
    '2 1, 2 2 0',
    '1 1 1 1 2']

string = "green"
minsup = 2
numberOfClusters = 8
string_db = []
with open(string + "ClusterEncoded.txt","r") as file:
    for line in file:
        string_db.append(line.replace('\n','').replace("  "," ").rstrip().lstrip())




p = pyprefixspan(data)
p.setminsup(minsup)

p.run()


print(p.out)
















