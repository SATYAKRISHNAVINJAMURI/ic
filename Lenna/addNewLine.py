r = open("newBlueCluster.txt","w")
with open("blueCluster.txt") as g:
	for line in g:
		r.write(line.rstrip()+"\n\n")