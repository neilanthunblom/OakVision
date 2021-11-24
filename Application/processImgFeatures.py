import cv2.cv2 as cv2
from definitions import ROOT_DIR
def process(image):
    cascPath = "/faces.xml"
    cascade = cv2.CascadeClassifier(ROOT_DIR + cascPath)

    #Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = cascade.detectMultiScale(gray, 1.1, 5)

    print ("Found " + str(len(faces))+ " face(s)")

    #Draw a rectangle around every found face
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    
    return image
