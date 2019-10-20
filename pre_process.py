# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 01:35:52 2019

@author: Tiha
"""

import cv2
import argparse
import numpy as np
img=cv2.imread('braille_scan.jpg',0)

#inverting the image
img=255-img
#thresholding - a process of comparing each pixel value with threshold value
ret,thresh=cv2.threshold(img,120,255,cv2.THRESH_BINARY)
#blur the image
blur=cv2.blur(thresh,(5,5))
#numpy.ones() responsible for returning an array with provided data types with ones
k=np.ones((5,5),np.uint8)
#erode()(Morphological Operation)helps in removing the internal noise in the image.Erosion is a technique for shrinking figures.
erosion=cv2.erode(blur,k,iterations=1)


ret,thresh2=cv2.threshold(erosion,12,255,cv2.THRESH_BINARY)
k=np.ones((3,2),np.uint8)
#dilate It is making objects expand.
mask=cv2.dilate(thresh2,k,iterations=1)

rows,cols=mask.shape
cv2.imwrite('mask.jpg',mask)



#cropping
refPt=[] 
cropping =False
def click_and_crop(event,x,y,flags,param):
    global refPt,cropping
    #if left mouse button clicked cropping started
    if event==cv2.EVENT_LBUTTONDOWN:
        refPt=[(x,y)]
        cropping=True
        #cropping done
    elif event==cv2.EVENT_LBUTTONUP:
        #mouse click is released and cropping operation is completed
        refPt.append((x,y))
        cropping=False
        
        cv2.rectangle(mask,refPt[0],refPt[1],(255,255,255),2)
        cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        cv2.resizeWindow('imae',rows,cols)
        cv2.imshow("image",mask)
clone=mask.copy()
cv2.namedWindow("image",cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',rows,cols)
cv2.setMouseCallback("image",click_and_crop)#setup the mouse callback function


#keep looping until the 'q' key is pressed

while True:
    #display the image and wait for a keypress
    cv2.namedWindow("image",cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image',rows,cols)
    cv2.imshow('image',mask)
    key=cv2.waitKey(1) 
    
    #'r' key is used to reset the cropping region
    if key== ord("r"):
        image=clone.copy()
    #if 'c' key is used to break the loop
    elif key==ord("c"):
        break


#if there are reference points,then crop the region of interest from the image and didsplay it
 
if len(refPt)==2:
    roi=clone[refPt[0][1]:refPt[1][1],refPt[0][0]:refPt[1][0]]
    cv2.imwrite('roi.jpg',roi)
    
     
            
            
    cv2.namedWindow("ROI",cv2.WINDOW_NORMAL)
    cv2.resizeWindow('ROI',refPt[0][1]-refPt[1][1],refPt[0][0]-refPt[1][0])
    cv2.imshow("ROI",roi) 
                  
cv2.waitKey(0)
cv2.destroyALLWindows()


        