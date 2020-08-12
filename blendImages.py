from PIL import Image, ImageDraw, ImageFilter
import cv2
import numpy as np

def nothing(x):
    pass

def changeImageSize(maxWidth, maxHeight, image):

    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage

image1 = Image.open("./Fire_001.png")
image2 = Image.open('./Label_1.png').resize(image1.size)
mask = Image.open('./Label_1.png').convert('L').resize(image1.size)

# image1 = Image.open("./lena.jpg")
# image2 = Image.open('./horse.png').resize(image1.size)
# mask = Image.open('./horse.png').convert('L').resize(image1.size)

image1 = changeImageSize(300, 300, image1)
image2 = changeImageSize(300, 300, image2)
mask = changeImageSize(300, 300, mask)

mask1 = mask.copy()

cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)

# create trackbars for color change
cv2.createTrackbar('Transparency','image',0,255,nothing)

result = Image.composite(image2, image1, mask1)

while(1):
    mask1 = mask.copy()
    cv2.imshow('image', np.array(result))
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    
    transparency = cv2.getTrackbarPos('Transparency','image')

    pixels2 = mask1.load() # create the pixel map


    for i in range(mask1.size[0]): # for every pixel:
        for j in range(mask1.size[1]):
            if pixels2[i,j] == (255):
                # change to black if not red
                pixels2[i,j] = (transparency)

    result = Image.composite(image2, image1, mask1)
