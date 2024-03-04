def EnhanceBinaryImage(binaryImage):
    
    for itr in range(1, 5):
        print("running itr ", itr)
        outputBinaryImage = binaryImage.copy()

        def is_not_valid(d):
            if 0 <= d[0] < binaryImage.shape[0] and 0 <= d[1] < binaryImage.shape[1]: return False
            return True
        
        directions = [(-1, 0), (-1, 1),(0, 1),(1, 1) ,(1, 0), (1, -1),(0, -1), (-1, -1)]
        for rid in range(binaryImage.shape[0]):
            for cid in range(binaryImage.shape[1]):
                
                # using min fill to fillout improperly bubble answers : higher number of iterations more it fills out
                min_pix = 0
                for direction in directions:
                    if is_not_valid((rid+direction[0], cid+direction[1])): continue

                    if binaryImage[rid+direction[0]][cid+direction[1]] == 255 or  binaryImage[rid][cid] == 255:
                        min_pix = 255
                        break

                outputBinaryImage[rid][cid] = min_pix

        binaryImage = outputBinaryImage

    return outputBinaryImage