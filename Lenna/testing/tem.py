codetable = {}
string = "red"

with open(string + "Codetable.txt", "r") as ct:
    for line in ct:
        (pattern, code) = line.replace("\n", "").split("-")
        codetable[pattern] = code
    ct.close()

codeTableItems = codetable.items()
sortedCodeTable = sorted(codeTableItems, key=lambda s: len(s[0]))
reversedSortedCodeTable = list(reversed(sortedCodeTable))  # big one first
# print reversedSortedCodeTable[0][0]
codes = []
for item in reversedSortedCodeTable:
    codes.append(item[0])

redEncoding = open(string + "temCompressed.txt", "w")
with open(string + "ClusterEncoded.txt", "r") as rc:
    for line in rc:
        line = " " + line + " "
        currentLine = line
        for key in codes:
            # print codetable[key]
            if (len(key.split(" ")) == 1):
                # print "yes"
                k1 = " " + key + " "
                k2 = " " + key + " "
                if ((k1 in currentLine)):
                    while (k1 in currentLine):
                        currentLine = currentLine.replace(k1, " -" + codetable[key] + "- ")
                    # redEncoding.write("no-"+k1+"$$"+currentLine+"\n")
                elif (k2 in currentLine):
                    while (k2 in currentLine):
                        currentLine = currentLine.replace(k2, " -" + codetable[key] + "- ")
                    # redEncoding.write("no-"+k2+"$$"+currentLine+"\n")
            else:
                # print "no"
                if (" " + key + " " in currentLine):
                    while (" " + key + " " in currentLine):
                        currentLine = currentLine.replace(" " + key + " ", " -" + codetable[key] + "- ")
                    # redEncoding.write("ues "+currentLine+"\n")
                    # print currentLprint currentLineine

        currentLine = currentLine.replace(" ", "").replace("-", " ").replace("\n", " ").replace("  "," ").rstrip().lstrip()
        redEncoding.write(currentLine + "\n")
    rc.close()
redEncoding.close()






codeTable = {}
with open(string + "Codetable.txt", "r") as ct:
    for line in ct:
        (pattern, code) = line.replace("\n", "").split("-")
        codeTable[code] = pattern
    ct.close()

redDecomp = open(string + "temHuffmanDecoded.txt", "w")
with open(string + "temCompressed.txt", "r") as rc:
    count = 0
    for line in rc:
        count+= 1
        # print line
        line.replace('\n','')
        currentLine = ""
        codes = line.split();
        for code in codes:
            currentLine = currentLine + " " + codeTable[code]
        redDecomp.write(currentLine.rstrip().lstrip() + "\n")
    rc.close()
redDecomp.close()


