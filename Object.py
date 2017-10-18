import cv2
import numpy as np



#Object is class which present detected object.
#----------------------------------------------
class Object:
	area = 0
	cx   = 0 # X point of center of mass
	cy   = 0 # Y point of center of mass
	height = 0 # height of contour
	width = 0  # width of contour
	contours = None

	def __init__(self,a,x,y,h,w):#Create object by given each parameters.
		self.area = a
		self.cx   = x
		self.cy   = y
		self.height = h
		self.width  = w

	def __init__(self,contour): #Create object by given contour.
		self.area   = cv2.contourArea( contour )
		if self.area < 6000 : #It is not object if it is too small
			self.area = None
			self.cx   = None
			self.cy   = None
			self.height = None
			self.width  = None
			self.contour= None
		else:
			M           = cv2.moments(contour)
			self.cx     = int(M['m10']/M['m00'])
			self.cy     = int(M['m01']/M['m00'])
			x,y,w,h     = cv2.boundingRect(contour)
			self.height = h
			self.width  = w
			self.contour=contour
#----------------------------------------------

#Type of Object -> it is big if area>50000
#Use this function when reach the target
# ->if it is big -> call help
# ->if it is small-> carry it out of line        
#----------------------------------------
def typeOfObject(Object):
	if(Object.area > 50000):
		return "big"
	else:
		return "small"        
#----------------------------------------
