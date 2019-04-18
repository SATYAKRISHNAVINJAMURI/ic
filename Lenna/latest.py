import numpy as np
import time
import os
import math
import cv2;
from scipy.cluster.vq import kmeans,vq
from PIL import Image
from multiprocessing import Process
np.set_printoptions(threshold= 0.1)


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
    image = cv2.imread(imageFile,1)
    (rows,columns,channels) = image.shape





def main():
    global  blockSize,numberOfClusters,s;
    blockSize = 32;
    numberOfClusters = 8;
    s = 10;
    imread("4.2.02.tiff");






if __name__ == "__main__":
    main()