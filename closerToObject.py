import cv2
import numpy as np


from imageProcess import *
from Object import *
from graspObject import *

#TODO 46. satirda bir fonksiyon var onu hallet.
# o fonksiyonun adi daha once getMoveToApproachTarget idi simdi getTargetAngle oldu.
# daha once degree return oluyordu artik radian return ediliyor.

#Find Target Object which be reached.
#--------------------------------------------------------------------------------------------
def getTargetObject(contours):
    objects = []
    for i in range (0,len(contours)):
            area = cv2.contourArea( contours[i] )
            
            if (area>6000): ##<-recognize object if area greater than 6000
                newObject = Object(contours[i])
                objects.append(newObject)



    if (len(objects)==0):
        return None
    else:
        target = objects[0]
        for i in range (0, len(objects)):
            obj = objects[i]
            
            if (obj.area>20000 and obj.cy>250 and obj.height<280):#Give priority to small objects
                target = obj
                break
            
            elif obj.area > target.area: #Choose object with larger area(mean closer object)
                target = obj
        return target
#--------------------------------------------------------------------------------------------    


#Find what should Nao do to approach target
#Use this function when object founded
#-------------------------------------------    
def getTargetAngle(obj):
    if(obj==None):
        return None

    xPoint = obj.cx    
    angle = horizontalAngleBetweenRobotAndPixel(xPoint)

        
    if (xPoint>(320-25)) and (xPoint<(320+25)):
        return 0 #means go forward
    else:
        return angle
#--------------------------------------------


#This function calls when nao reach its target
#Return true if there is an object in front of nao
#-------------------------------------------------------------------
def youReachTarget(frame):

    objectSeenInBottom = False
    objectSeenInMiddle = False

    cutFrame_Bottom    = frame[450:480, 0:640]
    contours_Bottom = processImage(cutFrame_Bottom, LOWERBLUE, UPPERBLUE, CONTOURS)
    if(len(contours_Bottom)==0):
        objectSeenInBottom = False
    else:
        maxContour = getMaxContour (contours_Bottom)
        area = cv2.contourArea( maxContour )    
        if area>2000 : objectSeenInBottom = True
        else         : objectSeenInBottom = False

    cutFrame_Middle = frame[300:400, 300:375]
    contours_Middle = processImage(cutFrame_Middle, LOWERBLUE, UPPERBLUE, CONTOURS)
    if(len(contours_Middle)==0):
        objectSeenInMiddle = False
    else:
        maxContour = getMaxContour (contours_Middle)
        area = cv2.contourArea( maxContour )    
        if area>2000 : objectSeenInMiddle = True
        else         : objectSeenInMiddle = False

    if(objectSeenInBottom and objectSeenInMiddle):
        return True
    else:
        return False
    
#-------------------------------------------------------------------
