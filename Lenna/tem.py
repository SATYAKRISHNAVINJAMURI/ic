codetable = {}
string = "red"
with open(string + "Codetable.txt", "r") as ct:
    for line in ct:
        (pattern, code) = line.replace("\n", "").split("-")
        codetable[pattern] = code

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

        currentLine = currentLine.replace(" ", "").replace("-", " ").rstrip().lstrip()
        redEncoding.write(currentLine + "\n")

