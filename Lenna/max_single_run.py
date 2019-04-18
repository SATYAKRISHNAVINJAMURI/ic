import max_compression as com
import time
import numpy as np
import os
np.set_printoptions(threshold= 0.1)

def main():
    res = open("max_single_results.csv", "w")
    res.write(
        "BlockSize,k,Alpha,ClusteringTime,MiningTime,EncodingTime,CompressionTime,DecompressionTime,ClusterTableSize,CodeTableSize,EncodedImageSize,CompressedSize,ActualSize,JPEG Size,GIF Size,JPEG Cr,GIF Cr,Our Cr,CRP Actual,CRP JPEG,CRP GIF\n")
    # res = open("s_results.csv", "a")
    image = com.imread("4.2.02.tiff")
    (com.rows, com.columns) = com.getImageSize("4.2.02.tiff")
    print str(com.blockSize) + "-" + str(com.numberOfClusters) + "-" + str(com.s)
    com.minimumSupport = (com.s * com.rows) / 100.0
    com.numberOfBlocks = (com.rows * com.columns) / (com.blockSize * com.blockSize)
    oTS = time.clock()
    cTS = time.clock()
    com.runAllClusteringParallel()
    cTE = time.clock()
    print "Clustering done"
    clusteringTime = cTE - cTS
    com.runClusterEncodingParallel()
    print "Cluster Encoding Done"
    mTS = time.clock()
    com.miner()
    mTE = time.clock()
    print "Mining Done"
    mineTime = mTE - mTS
    com.huffEncodeParallel()
    print "Huffman Encoding Done"
    coTS = time.clock()
    com.Compressor()
    coTE = time.clock()
    print "Encoding Done"
    compressTime = coTE - coTS
    oTE = time.clock()
    totalCompressionTime = oTE - oTS
    print "Compression Done"
    dTS = time.clock()
    com.Decoder()
    com.runClusterDecodingInParallel()
    dTE = time.clock()
    decompressionTime = dTE - dTS
    print "Decompression Done"
    com.reconstruct(com.rows, com.columns, str(com.blockSize) + "-" + str(com.numberOfClusters) + "-" + str(com.s))
    ClTableSize = (3 * com.numberOfBlocks * (com.nob(com.numberOfClusters) + 8) * com.numberOfClusters) / 8000.0
    coTableSize = os.stat("redCodetable.txt").st_size + os.stat("greenCodetable.txt").st_size + os.stat("blueCodetable.txt").st_size
    coTableSize = ((coTableSize / (6 * 1.0))) / 1000.0
    compressedImageSize = os.stat("redCompressed.txt").st_size + os.stat(
        "greenCompressed.txt").st_size + os.stat("blueCompressed.txt").st_size
    compressedImageSize = ((compressedImageSize / 8 * 1.0)) / 1000.0 - 40

    totalSize = ClTableSize + coTableSize + compressedImageSize

    ActualSize = 786.6
    JPEGSize = 404
    GIFSize = 226
    OurCr = ActualSize / totalSize
    JPEGCr = ActualSize / JPEGSize
    GIFCr = ActualSize / GIFSize
    CRPActual = ((ActualSize - totalSize) * 100) / ActualSize
    CRPJPEG = ((JPEGSize - totalSize) * 100) / JPEGSize
    CRPGIF = ((GIFSize - totalSize) * 100) / GIFSize
    res.write(
        str(com.blockSize) + "," + str(com.numberOfClusters) + "," + str(com.s) + "," + str(clusteringTime) + "," + str(
            mineTime) + "," + str(compressTime) + "," + str(totalCompressionTime) + "," + str(
            decompressionTime) + "," + str(ClTableSize) + "," + str(coTableSize) + "," + str(
            compressedImageSize) + "," + str(totalSize) + "," + str(ActualSize) + "," + str(
            JPEGSize) + "," + str(GIFSize) + "," + str(JPEGCr) + "," + str(GIFCr) + "," + str(
            OurCr) + "," + str(CRPActual) + "," + str(CRPJPEG) + "," + str(CRPGIF) + "\n")
    filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
    for f in filelist:
        os.remove(f)
    res.close()



if __name__ == "__main__":
    com.blockSize = 32
    com.numberOfClusters = 8
    com.s = 10
    main()
