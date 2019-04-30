import prefix_compression as com
import imageQuality as iq
import time
import cv2
import numpy as np
import os
np.set_printoptions(threshold= 0.1)

def main():
    inputFileName = "../data/4.2.07.tiff"
    #inputFileName = "4.2.02.tiff"
    outputFileName = str(com.blockSize) + "-" + str(com.numberOfClusters) + "-" + str(com.s)
    res = open("../results/single_run_results_prefixspan_256_pepper.csv", "w")
    res.write(
        "BlockSize,k,Alpha,ClusteringTime,MiningTime,EncodingTime,CompressionTime,DecompressionTime,ClusterTableSize,CodeTableSize,EncodedImageSize,CompressedSize,ActualSize,JPEG Size,GIF Size,JPEG Cr,GIF Cr,Our Cr,CRP Actual,CRP JPEG,CRP GIF,PSNR,MSE,NormalisedCrossRelation,MaxDiff,AvgDiff,NormalisedAbsoluteError,StructuralContent\n")
    # res = open("s_results.csv", "a")
    image = com.imread(inputFileName)
    (com.rows, com.columns) = com.getImageSize(inputFileName)
    print str(com.blockSize) + "-" + str(com.numberOfClusters) + "-" + str(com.s)
    com.minimumSupport = (com.s * com.rows) / 100.0
    com.numberOfBlocks = (com.rows * com.columns) / (com.blockSize * com.blockSize)
    oTS = time.time()
    cTS = time.time()
    com.runAllClusteringParallel()
    cTE = time.time()
    print "Clustering done"
    clusteringTime = cTE - cTS
    com.runClusterEncodingParallel()
    print "Cluster Encoding Done"
    mTS = time.time()
    com.minerParallel()
    mTE = time.time()
    print "Mining Done"
    mineTime = mTE - mTS
    com.huffEncodeParallel()
    print "Huffman Encoding Done"
    coTS = time.time()
    com.Compressor()
    coTE = time.time()
    print "Encoding Done"
    compressTime = coTE - coTS
    oTE = time.time()
    totalCompressionTime = oTE - oTS
    print "Compression Done"
    dTS = time.time()
    com.Decoder()
    print "Decoding Done"
    com.runClusterDecodingInParallel()
    dTE = time.time()
    decompressionTime = dTE - dTS
    print "Decompression Done"
    com.reconstruct(com.rows, com.columns, outputFileName)
    ClTableSize = (3 * com.numberOfBlocks * (com.nob(com.numberOfClusters) + 8) * com.numberOfClusters) / 8000.0   # doubt
    coTableSize = os.stat("redCodetable.txt").st_size + os.stat("greenCodetable.txt").st_size + os.stat("blueCodetable.txt").st_size
    coTableSize = ((coTableSize / (6 * 1.0))) / 1000.0                     # doubt
    compressedImageSize = os.stat("redCompressed.txt").st_size + os.stat(
        "greenCompressed.txt").st_size + os.stat("blueCompressed.txt").st_size
    compressedImageSize = ((compressedImageSize / 8 * 1.0)) / 1000.0  #doubt
    totalSize = ClTableSize + coTableSize + compressedImageSize


    # Image Quality Measures

    output = cv2.imread(outputFileName + ".bmp",1).astype(float)
    input = cv2.imread(inputFileName).astype(float)
    #declare variable for each image quality measurement and assign it to zero
    mse = 0
    norm_cor = 0
    max_diff = 0
    avg_diff = 0
    nor_abs_error = 0
    str_con = 0
    psnr = 0
    for i in range(0,3):
        psnr += iq.PSNR(input[i],output[i])
        mse += iq.mean_square_error(input[i],output[i])
        norm_cor += iq.normalised_cross_relation(input[i],output[i])
        max_diff +=iq.maximal_difference(input[i],output[i])
        avg_diff += iq.average_difference(input[i],output[i])
        nor_abs_error += iq.normalised_absolute_error(input[i],output[i])
        str_con += iq.structural_content(input[i],output[i])
    mse /= 3
    norm_cor /= 3
    max_diff /= 3
    avg_diff /= 3
    nor_abs_error /= 3
    str_con /= 3
    psnr /= 3
    ActualSize = 2042.355
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
            OurCr) + "," + str(CRPActual) + "," + str(CRPJPEG) + "," + str(CRPGIF) + "," + str(psnr) + "," + str(mse) +
            "," + str(norm_cor) + "," + str(max_diff) + "," + str(avg_diff) + "," + str(nor_abs_error) + "," +
            str(str_con) + "\n")
    filelist = [f for f in os.listdir(".") if f.endswith(".txt")]
    for f in filelist:
        os.remove(f)
    res.close()



if __name__ == "__main__":
    com.blockSize = 32
    com.numberOfClusters = 8
    com.s =
    main()
