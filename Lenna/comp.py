import cv2
import numpy as np

def main():
	im1 = cv2.imread("32-8-10.bmp")
	im2 = cv2.imread("32-8-10max.bmp")

	if(im1.ravel.nonzero(im1.ravel == im2.ravel)):
		print("yes")
	else:
		print("no")


if __name__ == "__main__":
	main()