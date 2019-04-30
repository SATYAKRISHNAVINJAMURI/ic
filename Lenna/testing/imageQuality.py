import numpy as np
import cv2


def mean_square_error(im1,im2):
    (M,N) = im1.shape
    diff = (im1 - im2) * (im1 - im2)
    res = sum(sum(diff))
    res /= N
    return res

def PSNR(im1,im2):
    return 10 * np.log((255 * 255)/mean_square_error(im1, im2))

def normalised_cross_relation(im1,im2):
    (M, N) = im1.shape
    sum_diff = sum(sum(im1-im2))
    sum_sq = sum(sum(im1 * im1))
    return sum_diff/sum_sq

def average_difference(im1,im2):
    (M,N) = im1.shape
    diff = sum(sum(im1 - im2))
    return diff/(M*N)

def structural_content(im1,im2):
    (M,N) = im1.shape
    sum_sq1 = sum(sum(im1 * im1))
    sum_sq2 = sum(sum(im2 * im2))
    return sum_sq1/sum_sq2

def maximal_difference(im1,im2):
    (M,N) = im1.shape
    return np.amax(np.absolute(im1 - im2))


def O(im):
    im1 = np.zeros(im.shape)
    (M,N) = im.shape
    for j in range(0,M):
        for k in range(0,N):
            if (k+1) < N and (j+1) < M and (k-1) >=  0 and (j-1) >= 0:
                im1[j][k]= im[j+1][k] + im[j-1][k] + im[j][k+1] + im[j][k-1] - (4 * im[j][k])
            else:
                if(j+1) >= M:
                    j1 = j
                else:
                    j1 = j + 1
                if(k+1) >= M:
                    k1 = k
                else:
                    k1 = k + 1
                if(j-1) >= 0:
                    j2 = j - 1
                else:
                    j2 = 0
                if(k - 1) >= 0:
                    k2= k - 1
                else:
                    k2 = 0
                im1[j][k] = im[j1][k] + im[j2][k] + im[j][k1] + im[j][k2] - (4 * im[j][k])
    return im1

def laplace_mean_squar_error(im1,im2):
    o1 = O(im1)
    print o1
    o2 = O(im2)
    print o2
    diff = sum(sum(o1 - o2))
    print sum(sum(o1 - o2,1))
    sum_sq = sum(sum(o1 * o1))
    return diff/sum_sq



def normalised_absolute_error(im1,im2):
    diff = np.absolute(sum(sum(im1 - im2)))
    sum1 = np.absolute(sum(sum(im1)))
    return diff/sum1







if __name__ == "__main__":
    # l1 = [[1,2,3],[2,3,4],[3,4,5]]
    # l2 = [[3,4,5],[5,6,7],[4,5,6]]
    # l1 = [[1,3,5],[78,76,79],[89,34,848]]
    # l2 = [[3,65,98],[5,63,7],[4,5,43]]
    # for i in range(0,3):
    #     for j in range(0,3):
    #         im1[i,j] = l1[i][j]
    #
    # for i in range(0,3):
    #     for j in range(0,3):
    #         im2[i,j] = l2[i][j]


    input = cv2.imread("4.2.02.tiff")
    output = cv2.imread("32-8-10.bmp")
    input = input.astype(float)
    output = output.astype(float)
    res = 0
    for i in range(0,3):
        res += normalised_absolute_error(input[:,:,i],output[:,:,i])

    res /= 3
    print res

