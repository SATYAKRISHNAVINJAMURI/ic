def miner(numberOfClusters, columns, minimumSupport):
    string = "green"
    redFile = []
    with open(string+"ClusterEncoded.txt", "r") as r:
        for line in r:
            line = line.replace("\n","")
            redFile.append(" "+line+" ")
        r.close()
    # print redFile
    #Find all one length sequences
    frequentPatterns = {}
    currentLength = 1
    frequentPatterns[currentLength] = {}
    for i in range(0,numberOfClusters):
        cKey = " "+str(i)+" "
        for eachLine in redFile:
            if(cKey in eachLine):
                if(cKey in frequentPatterns[currentLength].keys()):
                    frequentPatterns[currentLength][cKey] = frequentPatterns[currentLength][cKey] + 1
                else:
                    frequentPatterns[currentLength][cKey] = 1
    # print frequentPatterns
    #Enumerate length 2 frequent sequences
    currentLength = 2
    frequentPatterns[currentLength] = {}
    for key1 in frequentPatterns[currentLength-1].keys():
        for key2 in frequentPatterns[currentLength-1].keys():
            newKey = key1.rstrip()+key2
            frequentPatterns[currentLength][newKey] = 0
    for eachKey in frequentPatterns[currentLength].keys():
        for line in redFile:
            if(eachKey in line):
                frequentPatterns[currentLength][eachKey] = frequentPatterns[currentLength][eachKey] + 1
    for key in frequentPatterns[currentLength].keys():
        if(frequentPatterns[currentLength][key]<minimumSupport):
            frequentPatterns[currentLength].pop(key, None)
    currentLength = currentLength + 1
    # print frequentPatterns
    #Enumerate all frequent sequences
    for i in range(currentLength, columns+1):
        # print i
        # if(len(frequentPatterns[i].keys())!=0):
        frequentPatterns[i] = {}
        #Generate the i-length keys
        for key1 in frequentPatterns[i-1].keys():
            for key2 in frequentPatterns[i-1].keys():
                mkey1 = key1.lstrip().rstrip().split(" ")
                mkey2 = key2.lstrip().rstrip().split(" ")
                if(mkey1[1:len(mkey1)]==mkey2[0:len(mkey2)-1]):
                    key2Split = key2.lstrip().rstrip().split(" ")
                    newKey = key1+key2Split[len(key2Split)-1]+" "
                    frequentPatterns[i][newKey] = 0;
        # print "Loop"
        #Find the support of each i-length key
        for line in redFile:
            for eachKey in frequentPatterns[i].keys():
                if(eachKey in line):
                    frequentPatterns[i][eachKey] = frequentPatterns[i][eachKey] + 1

        #Pop all sequences that don't satisfy the minimum support threshold
        for key in frequentPatterns[i].keys():
            if(frequentPatterns[i][key]<minimumSupport):
                frequentPatterns[i].pop(key, None)

        #Pop all non closed sequences
        for key1 in frequentPatterns[i].keys():
            for key2 in frequentPatterns[i-1].keys():
                if((key2 in key1) and (frequentPatterns[i][key1] == frequentPatterns[i-1][key2])):
                    frequentPatterns[i-1].pop(key2, None)

    allKeys = []
    allFrequentPatterns = {}
    for i in range(1, columns+1):
        for key in frequentPatterns[i].keys():
            allKeys.insert(0,key.lstrip().rstrip())
            allFrequentPatterns[key.lstrip().rstrip()] = 0
            # print key+"---"+str(frequentPatterns[i][key])

    #By this time all frequent sequences are generated
    '''*********************************************'''
    #Find the modified frequency of each sequence
    for line in redFile:
        # print "x"
        for key in allKeys:
            # print key
            key = " " + key + " "
            if (key in line):
                allFrequentPatterns[key.lstrip().rstrip()] += line.count(key)
                while (key in line):
                    line = line.replace(key, ' ')

        # print line
    finalKeys = open(string +"Patterns.txt","w")
    finalLength = 0
    for eachKey in allKeys:
        if(allFrequentPatterns[eachKey]!=0):
            finalKeys.write(eachKey.lstrip().rstrip()+"-"+str(allFrequentPatterns[eachKey])+"\n")
            finalLength = finalLength + (len(eachKey.lstrip().rstrip().split(" "))*allFrequentPatterns[eachKey])
    print finalLength
    finalKeys.close()


if __name__ == "__main__":
    miner(8,32,51.2)