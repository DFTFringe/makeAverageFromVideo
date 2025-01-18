
import numpy as np
import cv2

fnm = 'DSC_0087.MOV'
vd = cv2.VideoCapture(fnm)

success, image = vd.read()
sumImg = image[:,:,1] * 1. 

count=1
while success:
    success, image = vd.read()
    if success:
        count += 1
        sumImg += image[:,:,1] * 1.

avgImg = sumImg / (count * 1.)
sumImg *= 0.

vd.release()

vd = cv2.VideoCapture(fnm)

success, image = vd.read()
sumImg = image[:,:,1] * 1. - avgImg

count=1
while success:
    success, image = vd.read()
    if success:
        count += 1
        sumImg += image[:,:,1] * 1. - avgImg 
        if count % 100 == 0:
            sumImg -= np.min(sumImg)
            sumImg *= 255./np.max(sumImg) 
            cv2.imwrite(str(count)+'_avg.png', sumImg.astype(np.uint8))
            sumImg *= 0.

vd.release()

