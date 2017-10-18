import cv2
import numpy as np


#Process a given cv2 image and return its transforms that specified by "mode" parameter.
#-------------------------------------------------------------------------------------
CONTOURS = 0
CLOSING  = 1
THRESH   = 2
HSV      = 3

LOWERBLUE = 100 #Use this range to detect objects
UPPERBLUE = 140

LOWERYELLOW = 90 #Use this range to detect security line
UPPERYELLOW = 105

def processImage(img, lowerHue, upperHue, mode):
	
                
                # Convert BGR to HSV
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                if mode==3: return hsv
                
		# Define range of color in HSV
                #IMPORTANT: RGB - BGR
                
                lower_color = np.array([lowerHue,50,50])
                upper_color = np.array([upperHue,255,255])
                
                # Threshold the HSV image to get only blue(actually red in real world) colors
                thresh = cv2.inRange(hsv, lower_color, upper_color)
		if mode==2: return thresh
 
                # Image closing
		kernel = np.ones((5,5),np.uint8)
                closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
		if mode==1: return closing

                # Find contours
                contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		if mode==0 or True  : return contours
#--------------------------------------------------------------------------------------------
		

#Convert naoImage to CV2 Image
#Important: OPENCV2 use BGR color space instead of RGB. So R-value and B-value are permutated.
#--------------------------------------------------------------------------------------------			
def convert_NAOImg2CV2Img(naoImage):
	if(naoImage != None):
		image = (np.reshape(np.frombuffer(naoImage[6], dtype='%iuint8' % naoImage[2]), (naoImage[1], naoImage[0], naoImage[2])))
		return image
	else:
		return None
#--------------------------------------------------------------------------------------------		



#Get the counter which have maximum area
#---------------------------------------
def getMaxContour(contours):
	maxContour = None
	maxArea    = -1
	for i in range (0,len(contours)):
		tempContour = contours[i]
		tempArea    = cv2.contourArea( tempContour )
		if (tempArea > maxArea):
			maxContour = tempContour
	return maxContour
#---------------------------------------
