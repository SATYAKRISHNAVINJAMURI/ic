import cv2
data = ["lena.tif","baboon.tif","barbara.jpg","zelda.tiff","scene.tiff","airplane.tiff","medical.jpg","medical2.jpg","high_parrot.jpg","high_tiger.jpg","high_road.jpg"]

for name in data:
    print name
    input = "../../data/" + name
    img = cv2.imread(input,1)
    print img.shape

