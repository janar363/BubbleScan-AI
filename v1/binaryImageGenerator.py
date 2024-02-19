import os
import cv2

def generateBinaryImage(sourceFolder, destFolder):

    # geting all image files names form source file
    files = os.listdir(sourceFolder)

    # Creating output folder 
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)

    # for each file
    for file in files:
        # read and convert image to gray scale image
        originalImg = cv2.imread(sourceFolder+file)
        grayscaleImg = cv2.cvtColor(originalImg, cv2.COLOR_BGR2GRAY)

        outputImg = grayscaleImg.copy()

        # is not valid returns true if current position is not inside the image
        def is_not_valid(pos):
            if 0 <= pos[0] < grayscaleImg.shape[0] and 0 <= pos[1] < grayscaleImg.shape[1]: return False
            return True
            
        directions = [(-1, 0), (-1, 1),(0, 1),(1, 1) ,(1, 0), (1, -1),(0, -1), (-1, -1)]
        
        for rid in range(grayscaleImg.shape[0]):
            for cid in range(grayscaleImg.shape[1]):
                # min pixel value initalized with current pixel value
                min_pix = grayscaleImg[rid][cid]

                # for each direction check if pixel in that direction is less than min pixel
                # if yes update min pixel value
                for direction in directions:
                    if is_not_valid((rid+direction[0], cid+direction[1])): continue

                    if grayscaleImg[rid+direction[0]][cid+direction[1]] < min_pix:
                        min_pix = grayscaleImg[cid+direction[0]][cid+direction[1]]


                outputImg[rid][cid] = 255 if min_pix < 90 else 0

        cv2.imwrite(destFolder+file, outputImg)


generateBinaryImage('exampleScans/', 'binaryExampleScans/')