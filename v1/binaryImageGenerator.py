import os
import cv2

def generateBinaryImage(sourceFolder, destFolder):

    files = os.listdir(sourceFolder)

     # Creating output folder 
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)

    for file in files:
        originalImg = cv2.imread(sourceFolder+file)
        grayscaleImg = cv2.cvtColor(originalImg, cv2.COLOR_BGR2GRAY)

        new_gray = grayscaleImg.copy()
        def is_not_valid(d):
            if 0 <= d[0] < grayscaleImg.shape[0] and 0 <= d[1] < grayscaleImg.shape[1]: return False
            return True
            
        dir = [(-1, 0), (-1, 1),(0, 1),(1, 1) ,(1, 0), (1, -1),(0, -1), (-1, -1)]
        for i in range(grayscaleImg.shape[0]):
            for j in range(grayscaleImg.shape[1]):
                min_pix = grayscaleImg[i][j]

                for d in dir:
                    if is_not_valid((i+d[0], j+d[1])): continue

                    if grayscaleImg[i+d[0]][j+d[1]] < min_pix:
                        min_pix = grayscaleImg[i+d[0]][j+d[1]]


                new_gray[i][j] = 255 if min_pix < 90 else 0
        
        # normalization
        # for i in range(grayscaleImg.shape[0]):
        #     for j in range(grayscaleImg.shape[1]):
        #         new_gray[i][j] = 255 if new_gray[i][j] < 100 else 0

        cv2.imwrite(destFolder+file, new_gray)


generateBinaryImage('exampleScans/', 'binaryExampleScans/')