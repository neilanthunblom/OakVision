from piCam import Stream
import io
import sys
import os
import time
import cv2
import numpy
import pathlib
import logLogger
import notification
import piCam
import imutils


global image

ROOT_DIR = str(pathlib.Path(__file__).parent.absolute())

def main():
    #checks system platform to determine camera protocall
    if sys.platform == "darwin":
        getImageFromMacOs()
    elif sys.platform == "linux":
        runPiCam()

def runPiCam():
    method = 'piCam'
    cascPath = "/cascades/faces.xml"
    cascade = cv2.CascadeClassifier(ROOT_DIR + cascPath)

    try:
        import picamera
    except:
        try:
            os.system("pipenv install requests")
        except:
            pass

    stream = piCam.Stream().start()
    time.sleep(1.0)
    runDetection = True
    count=0
    frameSinceDetect = 1024
    totalFrameOneSecondAgo = 0
    totalFrame = 0
    frameRate = 0
    st = time.clock()
    t = st

    while runDetection:
        #print('hits while')
        totalFrame += 1
        print('new time', time.perf_counter)
        print('tiem', time.clock())
        if st - t < 10.0:
            if time.clock() - t > 1.0:
                frameRate = totalFrameOneSecondAgo - totalFrame
                print('framerate ',  frameRate, 'time', t)
                t = time.clock()
                totalFrameOneSecondAgo = frameRate
            frameRate = frameRate / totalFrame

        frameSinceDetect += 1
        frame = stream.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, 1.1, 5)

        cv2.imshow('video feed', frame)

        if cv2.waitKey(50) & 0xFF == ord('q'):
            print(count)
            stream.stop()
            runDetection = False
        
        if len(faces) > 0 and frameSinceDetect > 128:
            frameSinceDetect = 0
            count+=1
            print(str(len(faces)))
            #logLogger.writeToLog(method , " Found " + str(len(faces))+ " face(s)")
            #save(frame, method, faces)




def getImageFromMacOs():
    cascPath = "/cascades/faces.xml"
    cascade = cv2.CascadeClassifier(cascPath)

    video_capture = cv2.VideoCapture(0)

    while cv2.waitKey(1) & 0xFF != ord('q'):
        # get each frame
        frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Video', frame)

    # done, release capture
    video_capture.release()
    cv2.destroyAllWindows()


def save(frame, method, faces):
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    cdw = os.path.join(ROOT_DIR + '/out')
    i = 0
    #incriment through photoname and select next avail name.
    while os.path.exists(os.path.join(cdw , 'result_%s.jpg'%i)):
        i += 1
    #write edited image to dir
    fileName = ('result_%s.jpg'%i)
    filePath = os.path.join(cdw, fileName)
    
    cv2.imwrite(filePath, frame)

    if os.path.isfile(filePath) == True:
       logLogger.writeToLog(method, " wrote file " + ('result_%s.jpg'%i))
       notification.notify(fileName, filePath)
    else:
       logLogger.writeToLog('ERROR IN: ' + method, ("FAILED to write file " + ('result_%s.jpg'%i) + 'CDW is: ' + cdw )) 

main()
