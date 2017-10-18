import cv2
import numpy as np

from math import *

from imageProcess import *



def lineDetector(frame):

	frameLeft = frame[380:480, 160:320]
	frameRight= frame[380:480, 320:480]

	contoursLeft = processImage(frameLeft ,LOWERYELLOW,UPPERYELLOW,CONTOURS)
	contoursRight= processImage(frameRight,LOWERYELLOW,UPPERYELLOW,CONTOURS)
    
    
	thereisLineAtLeftSide = False
	for i in range (0,len(contoursLeft)):
		area = cv2.contourArea( contoursLeft[i] ) 
		if area >=500:
			thereisLineAtLeftSide = True
    
	thereisLineAtRightSide = False
	for i in range (0,len(contoursRight)):
		area = cv2.contourArea( contoursRight[i] ) 
		if area >=200:
			thereisLineAtRightSide = True
           

	whereIsLine = None
	if (thereisLineAtLeftSide and thereisLineAtRightSide):
		whereIsLine = "frontside"
	elif thereisLineAtLeftSide:
		whereIsLine = "leftside"
	elif thereisLineAtRightSide:
		whereIsLine = "rightside"
	else:
		whereIsLine = None 
    
	return whereIsLine


def getAngleToAvoidObstacle(frame):
	cuttenFrame = frame[315:350, 115:550]

	contours = processImage(cuttenFrame,LOWERBLUE, UPPERBLUE, CONTOURS)
	if (len(contours)==0):
		return 0
	else:
		maxContour = getMaxContour(contours)
		area = cv2.contourArea( maxContour )
		if(area<100):
			return 0
		else:
			turningOrientation = None
			xPoint = None
			x,y,w,h = cv2.boundingRect(maxContour)
			absLeft = abs(210-x) #210 is middle point of width of cuttenFrame
			absRight= abs(210-(x+w))
			
			if(absLeft < absRight):
				turningOrientation = 'L'
				xPoint = absLeft
			else:
				turningOrientation = 'R'
				xPoint = absRight

			height = 210 * (3**(0.5))
			hypo    =  ((xPoint**2)+(height**2))**(0.5)

			cosAlpha = ((xPoint**2)-(height**2)-(hypo**2))/(-2*height*hypo)
			alpha    = degrees(acos(cosAlpha))
			
			turningAngle = (30-alpha)+10 #10 degree for guarantee
			
			if(turningOrientation=='L'):
				return radians(turningAngle)
			else:
				return -radians(turningAngle)
