import cv2
import numpy as np

import math

from Object import *



#yPoint     : Row Number of Pixel
#knownAngle : Angle between bottom range of camera and y axis of robot.
def verticalAngleBetweenRobotAndPixel(yPoint,knownAngle):
	alpha = 47.64 #Field of view: given by Aldebaran.	
	alpha_half = alpha/2.0

	knownAngle = math.degrees(knownAngle)
	knownAngle = 90-knownAngle

	beta = 90.0 - alpha_half

	k = 240.0/math.sin(math.radians(alpha_half))
	
	a = ((yPoint**2)+(k**2)-2*k*yPoint*math.cos(math.radians(beta))) ** (0.5)

	t = 480-yPoint

	cos_aci = ((t**2)-(a**2)-(k**2)) / (-2*a*k)

	aci = math.degrees(math.acos(cos_aci))

	araaci = knownAngle-alpha_half

	toplam_aci = aci + araaci

	return math.radians(toplam_aci)

#xPoint: Column Number of Pixel
def horizontalAngleBetweenRobotAndPixel(xPoint) :
	k = 320.0/math.sin(math.radians(30.49))	
	
	a = ((xPoint**2)+(k**2)-2*k*xPoint*math.cos(math.radians(58.06))) ** (0.5)
	
	cosAlpha = ((xPoint**2)-(k**2)-(a**2)) / (-2.0*k*a)

	Alpha =   math.degrees(math.acos(cosAlpha))

	Alpha = 30.48 - Alpha

	return math.radians(Alpha)



#targetHeight is real height of object (not contour height)
# gets coordinates according to BottomCamera
#-----------------------------------------------------
def coordinatesOfTargetObject(cameraPosition6D, targetObject, targetHeight):
	if(targetObject==None):
		return None

	else:
		cameraHeight = cameraPosition6D[2]
		angle        = cameraPosition6D[4]
			
		cnt = targetObject.contour

		top = tuple(cnt[cnt[:,:,1].argmin()][0])

		print [top[0],top[1]]

		verticalAngle   = verticalAngleBetweenRobotAndPixel(top[1],angle) 
		horizontalAngle = horizontalAngleBetweenRobotAndPixel(top[0]) 
	
		verticalDistance   = tan(verticalAngle)  * (cameraHeight-targetHeight)

		horizontalDistance = tan(horizontalAngle)* verticalDistance


		x = verticalDistance
		y = horizontalDistance
		z = targetHeight

		return [x,y,z]
#-----------------------------------------------------

# Return (X,Y) point of bottom of object.
#Use this function when getting closer to small object in order to grasp.
#---------------------------------------------------------------------------------------------
def getXYPointsOfObject(cameraPosition6D, targetObject, targetHeight, targetRadius):
	topCoordinates = coordinatesOfTargetObject(cameraPosition6D, targetObject,targetHeight)
	
	x = x + cameraPosition6D[0]-( 2*targetRadius) #X coordinate is verticalDistance + x coordinate of bottomCamera
	
	y = y + cameraPosition6D[1] #Y coordinate is horizontalDistance + y coordinate of bottomCamera


	return [x,y]
#--------------------------------------



