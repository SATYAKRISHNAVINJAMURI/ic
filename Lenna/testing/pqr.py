import imageQuality as iq
import cv2



def doubling_range(start, stop):
    while start < stop:
        yield start
        start <<= 1


def ss():
    res = open("image_quality.csv","w")
    tiff_ex = ["airplane","zelda","scene"]
    tif_ex = ["baboon","lena"]
    jpg_ex = ["barbara","high_parrot","high_tiger","medical","medical2"]
    for inputFileName in tiff_ex:
        conv = inputFileName
        res.write(conv + "\n")
        orig = "../../data/" + conv + ".tiff"
        for blockSize in doubling_range(32, 257):
            for numberOfClusters in range(8, 33, 4):
                for s in range(10, 51, 20):
                    inputFileName = "../../results/new/" + conv  + "/" + conv +  ".tiff_" + str(blockSize) + "-" + str(numberOfClusters) + "-" + str(s) + ".bmp"
                    input = cv2.imread(orig)
                    output = cv2.imread(inputFileName)
                    input = input.astype(float)
                    print inputFileName
                    output = output.astype(float)
                    result = 0
                    for i in range(0, 3):
                        result += iq.normalised_absolute_error(input[:, :, i], output[:, :, i])

                    result /= 3
                    res.write(str(result))
                    res.write("\n")
        res.write("\n\n\n")








    for inputFileName in tif_ex:
        conv = inputFileName
        res.write(conv + "\n")
        orig = "../../data/" + conv + ".tif"
        for blockSize in doubling_range(32, 257):
            for numberOfClusters in range(8, 33, 4):
                for s in range(10, 51, 20):
                    inputFileName = "../../results/new/" + conv  + "/" + conv +  ".tif_" + str(blockSize) + "-" + str(numberOfClusters) + "-" + str(s) + ".bmp"
                    input = cv2.imread(orig)
                    output = cv2.imread(inputFileName)
                    input = input.astype(float)
                    print inputFileName
                    output = output.astype(float)
                    result = 0
                    for i in range(0, 3):
                        result += iq.normalised_absolute_error(input[:, :, i], output[:, :, i])

                    result /= 3
                    res.write(str(result))
                    res.write("\n")
        res.write("\n\n\n")







    for inputFileName in jpg_ex:
        conv = inputFileName
        res.write(conv + "\n")
        orig = "../../data/" + conv + ".jpg"
        for blockSize in doubling_range(32, 257):
            for numberOfClusters in range(8, 33, 4):
                for s in range(10, 51, 20):
                    inputFileName = "../../results/new/" + conv  + "/" + conv +  ".jpg_" + str(blockSize) + "-" + str(numberOfClusters) + "-" + str(s) + ".bmp"
                    input = cv2.imread(orig)
                    output = cv2.imread(inputFileName)
                    input = input.astype(float)
                    print inputFileName
                    output = output.astype(float)
                    result = 0
                    for i in range(0, 3):
                        result += iq.normalised_absolute_error(input[:, :, i], output[:, :, i])

                    result /= 3
                    res.write(str(result))
                    res.write("\n")
        res.write("\n\n\n")

    res.close()




ss()