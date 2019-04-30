import time
import heapq
import os
import math
# from pylab import plot,show
# from numpy import vstack,array
# from numpy.random import rand
from scipy.cluster.vq import kmeans, vq
from PIL import Image
from multiprocessing import Process
import numpy as np
import cv2
from collections import defaultdict
import numpy as np
import imageQuality as iq

np.set_printoptions(threshold=0.1)


def nob(n):
    return int(math.log(n, 2)) + 1


def doubling_range(start, stop):
    while start < stop:
        yield start
        start <<= 1


class Node(object):
    def __init__(self, pairs, frequency):
        # print pairs
        self.pairs = pairs
        self.frequency = frequency

    def __repr__(self):
        return repr(self.pairs) + ", " + repr(self.frequency)

    def merge(self, other):
        total_frequency = self.frequency + other.frequency
        for p in self.pairs:
            p[1] = "1" + p[1]
        for p in other.pairs:
            p[1] = "0" + p[1]
        new_pairs = self.pairs + other.pairs
        return Node(new_pairs, total_frequency)

    def __lt__(self, other):
        return self.frequency < other.frequency


def imread(imageFile):
    # read image
    currentImage = Image.open(imageFile)
    image = currentImage.load()
    [rows, columns] = currentImage.size
    redFile = open("redFile.txt", "w")
    greenFile = open("greenFile.txt", "w")
    blueFile = open("blueFile.txt", "w")
    for i in range(0, rows):
        redFile.write("\n")
        greenFile.write("\n")
        blueFile.write("\n")
        for j in range(0, columns):
            redFile.write(str(image[i, j][0]) + " ")
            greenFile.write(str(image[i, j][1]) + " ")
            blueFile.write(str(image[i, j][2]) + " ")
    redFile.close()
    blueFile.close()
    greenFile.close()


# Return (rows,columns)
def getImageSize(imageFile):
    currentImage = Image.open(imageFile)
    return currentImage.size


def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h // nrows, nrows, -1, ncols)
            .swapaxes(1, 2)
            .reshape(-1, nrows, ncols))


def unblockshaped(arr, h, w):
    n, nrows, ncols = arr.shape
    return (arr.reshape(h // nrows, -1, nrows, ncols)
            .swapaxes(1, 2)
            .reshape(h, w))


def clustering(i, string, y):
    z = y[i].reshape(1, blockSize * blockSize).astype(float)
    centroids, _ = kmeans(z[0], numberOfClusters)
    # print centroids
    k = 0;
    redCluster = open(string + "Cluster" + str(i) + ".txt", "w")
    with open(string + "ClusterTable" + str(i) + ".txt", "w") as redClusterTable:
        for identifier in centroids:
            redClusterTable.write(str(k))
            redClusterTable.write(" " + str(identifier) + "\n");
            k = k + 1
        redClusterTable.close()
    idx, _ = vq(z[0], centroids)
    c = 1
    a = list()
    for cid in idx:
        redCluster.write(str(cid) + " ")
        a.append(cid)
        c = c + 1
        if (c == blockSize + 1):
            redCluster.write("\n")
            c = 1;
    redCluster.close()


def runParallelClustering(string):
    red = []
    with open(string + "File.txt") as redFile:
        y = redFile.read()
        for m in y.split():
            red.append(int(m))
        redFile.close()
    redarray = np.asarray(red);
    redarray = redarray.reshape(rows, columns)
    y = blockshaped(redarray, blockSize, blockSize)
    proc = []
    for i in range(0, numberOfBlocks):
        p = Process(target=clustering, args=(i, string, y,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def runAllClusteringParallel():
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=runParallelClustering, args=(string,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def clusterEncoding(string):
    final = []
    for i in range(0, numberOfBlocks):
        with open(string + "Cluster" + str(i) + ".txt", "r") as s:
            i = s.read()
            k = []
            for m in i.split():
                k.append(int(m))
            s.close()
        k = np.asarray(k)
        k = k.reshape(blockSize, blockSize)
        final.append(k)
    final = np.asarray(final)
    p = unblockshaped(final, rows, columns)
    with open(string + "ClusterEncoded.txt", "w") as w:
        for i in range(0, rows):
            for m in p[i]:
                w.write(str(m) + " ")
            w.write("\n")
        w.close()


def runClusterEncodingParallel():
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=clusterEncoding, args=(string,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()



def frequent_rec(patt,mdb,db,frequentPatterns):  # mdb has line number as key and column number as value and count as second element of the list
    pattern_len = len(patt)
    if (pattern_len > 0):  # adding pattern to result if and only if len > 1 becoz single length sequences are already added
        key = ""
        for k in patt:
            key += " " + k
        key += " "
        frequentPatterns[pattern_len][key] = mdb[1]  # get frequency
        if pattern_len > 2:
            for key2 in frequentPatterns[pattern_len - 1].keys():
                if key2 in key:
                    frequentPatterns[pattern_len - 1].pop(key2,None)


    occurs = defaultdict(list)  # note the position of each item.6
    # Iterating for next value in each line and finding their support
    for (i, pos) in mdb[0].items():
        line = db[i]  # GET LINE
        j = [x + 1 for x in pos]
        for val in j:
            if val >= columns:
                continue
            else:
                l = occurs[line[val]]
                dic = defaultdict(list)
                if len(l) == 0:
                    dic[i] = [val]
                    # dic[i] = np.where(line == str(id))[0]
                    l.append(dic)
                    l.append(1)
                else:
                    l[0][i].append(val)
                    # if first value in the  line increment
    # pop infrequent patterns
    for (c, newmdb) in occurs.items():
        newmdb[1] = len(newmdb[0].keys())
        if newmdb[1] >= minimumSupport:
            frequent_rec(patt + [c], newmdb,db,frequentPatterns)



def miner(string):
    db = []
    string_db = []
    # Reading data base as list in db and " " + line + " " in string_db
    with open(string + "ClusterEncoded.txt", "r") as file:
        for line in file:
            db.append(line.replace("\n", '').lstrip().rstrip().split())
            string_db.append(" " + line.replace('\n', '').replace("  ", " ").rstrip().lstrip() + " ")
        file.close()
    frequentPatterns = {}
    for i in range(1, columns + 1):
        frequentPatterns[i] = {}  # initialization of patterns.

    # adding all one lenght sequences
    for i in range(0, numberOfClusters):
        key = " " + str(i) + " "
        frequentPatterns[1][key] = 0

    # starting with one length sequence
    occurs = defaultdict(list)
    for id in range(0, numberOfClusters):
        id = str(id)
        dic = {}
        count = 0
        for i in range(len(db)):
            line = np.array(db[i])
            dic[i] = list(np.where(line == id)[0])
            if len(dic[i]) != 0:
                count += 1
            else:
                del dic[i]
        l = occurs[id]
        l.append(dic)
        l.append(count)

    # possibility for paralellization
    for (c, values) in occurs.items():
        frequent_rec([c], values, db, frequentPatterns)  # iterates from 0 to total rows i,e 0 to 511

        # print db

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


def minerParallel():
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=miner, args=(string,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def huffman_codes(s):
    freq = []
    i = 0
    table = []
    with open(s, "r") as s:
        for line in s:
            x = line.replace("\n", '').rstrip().split('-')
            table.append(Node([[x[0], '']], int(x[1])))
        s.close()
    heapq.heapify(table)
    while len(table) > 1:
        first_node = heapq.heappop(table)
        second_node = heapq.heappop(table)
        new_node = first_node.merge(second_node)
        heapq.heappush(table, new_node)
    return dict(table[0].pairs)


def huffEncode(string):  # changes made
    s = open(string + "Codetable.txt", "w")
    x = huffman_codes(string + "Patterns.txt")
    for i in x.keys():
        s.write(i + "-" + x[i] + "\n")
    s.close()


def huffEncodeParallel():  # changes made
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=huffEncode, args=(string,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def huffmanEncoder(string):
    codetable = {}
    with open(string + "Codetable.txt", "r") as ct:
        for line in ct:
            (pattern, code) = line.replace("\n", "").split("-")
            codetable[pattern] = code
        ct.close()

    codeTableItems = codetable.items()
    sortedCodeTable = sorted(codeTableItems, key=lambda s: len(s[0]))
    reversedSortedCodeTable = list(reversed(sortedCodeTable))
    # print reversedSortedCodeTable[0][0]
    codes = []
    for item in reversedSortedCodeTable:
        codes.append(item[0])

    # print codetable

    redEncoding = open(string + "Compressed.txt", "w")
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


def Compressor():
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=huffmanEncoder, args=(string,))
        p.start()
        proc.append(p)

    for p in proc:
        p.join()


def huffmanDecoder(string):
    codeTable = {}
    with open(string + "Codetable.txt", "r") as ct:
        for line in ct:
            (pattern, code) = line.replace("\n", "").split("-")
            codeTable[code] = pattern
        ct.close()

    redDecomp = open(string + "HuffmanDecoded.txt", "w")
    with open(string + "Compressed.txt", "r") as rc:
        count = 0
        for line in rc:
            count += 1
            # print line
            line.replace('\n', '')
            currentLine = ""
            codes = line.split();
            for code in codes:
                currentLine = currentLine + " " + codeTable[code]
            redDecomp.write(currentLine.rstrip().lstrip() + "\n")
        rc.close()
    redDecomp.close()


def Decoder():  # changes made.
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=huffmanDecoder, args=(string,))
        p.start()
        proc.append(p)

    for p in proc:
        p.join()

    # for string in ['red','green','blue']:
    #     huffmanDecoder(string)


def clusterDecoding(string):
    final = []
    with open(string + "HuffmanDecoded.txt", "r") as s:
        m = s.read()
        for ch in m.split():
            final.append(int(ch))
        s.close()
    final = np.asarray(final);
    final = final.reshape(rows, columns)
    y = blockshaped(final, blockSize, blockSize)
    val = {}
    for i in range(0, numberOfBlocks):
        val[i] = {}
        with open(string + "ClusterTable" + str(i) + ".txt", "r") as s:
            for line in s:
                mat = line.strip().split(" ")
                val[i][int(mat[0])] = float(mat[1])
            s.close()
    newFinal = []
    for i in range(0, numberOfBlocks):
        newY = y[i].reshape(1, blockSize * blockSize)
        yNew = []
        for element in newY[0]:
            yNew.append(val[i][int(element)])
        yNew = np.asarray(yNew)
        yNew = yNew.reshape(blockSize, blockSize)
        newFinal.append(yNew)
    newFinal = np.asarray(newFinal)
    shapedNewFinal = unblockshaped(newFinal, rows, columns)
    with open(string + "Decompressed.txt", "w") as w:
        for i in range(0, rows):
            for m in shapedNewFinal[i]:
                w.write(str(m) + " ")
            w.write("\n")
        w.close()


def runClusterDecodingInParallel():
    proc = []
    for string in ["red", "green", "blue"]:
        p = Process(target=clusterDecoding, args=(string,))
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def reconstruct(rows, columns, fileName):
    data = np.zeros((rows, columns, 3), dtype=np.uint8)
    print data.shape

    i = 0;
    j = 0;
    with open("redDecompressed.txt", "r") as rc, open("dummy.txt", "w") as d:
        for line in rc:
            j = 0
            for character in line.strip().split(" "):
                data[j, i, 0] = float(character)
                d.write(str(data[j, i, 2]) + " ")
                j = j + 1;
            i = i + 1
            d.write("\n")
        d.close()

    i = 0;
    j = 0;
    with open("greenDecompressed.txt", "r") as gc, open("dummy1.txt", "w") as d:
        for line in gc:
            j = 0
            for character in line.strip().split(" "):
                data[j, i, 1] = float(character)
                d.write(str(data[j, i, 1]) + " ")
                j = j + 1;
            d.write("\n")
            i = i + 1
        d.close()

    i = 0;
    j = 0;
    with open("blueDecompressed.txt", "r") as bc, open("dummy2.txt", "w") as d:
        for line in bc:
            j = 0
            for character in line.strip().split(" "):
                data[j, i, 2] = float(character)
                d.write(str(data[j, i, 0]) + " ")
                j = j + 1;
            i = i + 1
            d.write("\n")
        d.close()
    img = Image.fromarray(data)
    img.save(fileName + '.bmp')


def main():
    res = open("high_parrot_results.csv", "a")
    res.write(
        "BlockSize,k,Alpha,ClusteringTime,MiningTime,EncodingTime,CompressionTime,DecompressionTime,ClusterTableSize,CodeTableSize,EncodedImageSize,CompressedSize,ActualSize,JPEG Size,GIF Size,JPEG Cr,GIF Cr,Our Cr,CRP Actual,CRP JPEG,CRP GIF,PSNR,MSE,NormalisedCrossRelation,MaxDiff,AvgDiff,NormalisedAbsoluteError,StructuralContent\n")
    global blockSize, numberOfClusters, s, rows, columns, numberOfBlocks, minimumSupport
    #images_data = ["scene.tiff","airplane.tiff","medical.jpg","medical2.jpg","high_parrot.jpg","high_tiger.jpg","high_road.jpg"]
    images_data = ["high_parrot.jpg"]
    for inputFileName in images_data:
        res.write(inputFileName + '\n')
        conv = inputFileName
        inputFileName = "../data/" + inputFileName
        for blockSize in doubling_range(128, 513):
            for numberOfClusters in range(8, 33, 4):
                for s in range(10, 71, 20):
                    outputFileName = conv + "_" + str(blockSize) + "-" + str(numberOfClusters) + "-" + str(s)
                    image = imread(inputFileName)
                    (rows, columns) = getImageSize(inputFileName)
                    print str(blockSize) + "-" + str(numberOfClusters) + "-" + str(s)
                    minimumSupport = (s * rows) / 100.0
                    numberOfBlocks = (rows * columns) / (blockSize * blockSize)
                    oTS = time.time()
                    cTS = time.time()
                    runAllClusteringParallel()
                    cTE = time.time()
                    print "Clustering done"
                    clusteringTime = cTE - cTS
                    runClusterEncodingParallel()
                    print "Cluster Encoding Done"
                    mTS = time.time()
                    minerParallel()
                    mTE = time.time()
                    print "Mining Done"
                    mineTime = mTE - mTS
                    huffEncodeParallel()
                    print "Huffman Encoding Done"
                    coTS = time.time()
                    Compressor()
                    coTE = time.time()
                    print "Encoding Done"
                    compressTime = coTE - coTS
                    oTE = time.time()
                    totalCompressionTime = oTE - oTS
                    print "Compression Done"
                    dTS = time.time()
                    Decoder()
                    print "Decoding Done"
                    runClusterDecodingInParallel()
                    dTE = time.time()
                    decompressionTime = dTE - dTS
                    print "Decompression Done"
                    reconstruct(rows, columns, outputFileName)
                    ClTableSize = (3 * numberOfBlocks * (
                                nob(numberOfClusters) + 8) * numberOfClusters) / 8000.0
                    coTableSize = os.stat("redCodetable.txt").st_size + os.stat("greenCodetable.txt").st_size + os.stat(
                        "blueCodetable.txt").st_size
                    coTableSize = ((coTableSize / (6 * 1.0))) / 1000.0
                    compressedImageSize = os.stat("redCompressed.txt").st_size + os.stat(
                        "greenCompressed.txt").st_size + os.stat("blueCompressed.txt").st_size
                    compressedImageSize = ((compressedImageSize / 8 * 1.0)) / 1000.0 - 40
                    totalSize = ClTableSize + coTableSize + compressedImageSize

                    # Image Quality Measures

                    output = cv2.imread(outputFileName + ".bmp", 1).astype(float)
                    input = cv2.imread(inputFileName).astype(float)
                    # declare variable for each image quality measurement and assign it to zero
                    mse = 0
                    norm_cor = 0
                    max_diff = 0
                    avg_diff = 0
                    nor_abs_error = 0
                    str_con = 0
                    psnr = 0
                    for i in range(0, 3):
                        psnr += iq.PSNR(input[i], output[i])
                        mse += iq.mean_square_error(input[i], output[i])
                        norm_cor += iq.normalised_cross_relation(input[i], output[i])
                        max_diff += iq.maximal_difference(input[i], output[i])
                        avg_diff += iq.average_difference(input[i], output[i])
                        nor_abs_error += iq.normalised_absolute_error(input[i], output[i])
                        str_con += iq.structural_content(input[i], output[i])
                    mse /= 3
                    norm_cor /= 3
                    max_diff /= 3
                    avg_diff /= 3
                    nor_abs_error /= 3
                    str_con /= 3
                    psnr /= 3
                    ActualSize = 786.6
                    JPEGSize = 404
                    GIFSize = 226.03
                    OurCr = ActualSize / totalSize
                    JPEGCr = ActualSize / JPEGSize
                    GIFCr = ActualSize / GIFSize
                    CRPActual = ((ActualSize - totalSize) * 100) / ActualSize
                    CRPJPEG = ((JPEGSize - totalSize) * 100) / JPEGSize
                    CRPGIF = ((GIFSize - totalSize) * 100) / GIFSize
                    res.write(
                        str(blockSize) + "," + str(numberOfClusters) + "," + str(s) + "," + str(
                            clusteringTime) + "," + str(
                            mineTime) + "," + str(compressTime) + "," + str(totalCompressionTime) + "," + str(
                            decompressionTime) + "," + str(ClTableSize) + "," + str(coTableSize) + "," + str(
                            compressedImageSize) + "," + str(totalSize) + "," + str(ActualSize) + "," + str(
                            JPEGSize) + "," + str(GIFSize) + "," + str(JPEGCr) + "," + str(GIFCr) + "," + str(
                            OurCr) + "," + str(CRPActual) + "," + str(CRPJPEG) + "," + str(CRPGIF) + "," + str(
                            psnr) + "," + str(mse) +
                        "," + str(norm_cor) + "," + str(max_diff) + "," + str(avg_diff) + "," + str(
                            nor_abs_error) + "," +
                        str(str_con) + "\n")
                    filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
                    for f in filelist:
                        os.remove(f)
        res.write("\n\n\n\n\n\n\n")
    res.close()


if __name__ == "__main__":
    main()


