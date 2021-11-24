from __future__ import print_function
from picamera.array import PiRGBArray
from threading import Thread
from definitions import ROOT_DIR
import os, io, cv2, numpy, time, imutils
import logLogger, notification, picamera
import argparse

class Stream:
    def __init__(self, resolution=(320, 240), framerate=16):
        self.cam = picamera.PiCamera()
        self.frame = None
        self.running = True
        self.cam.resolution = resolution
        self.cam.framerate = framerate
        self.capture = PiRGBArray(self.cam, resolution)
        self.stream = self.cam.capture_continuous(self.capture, "bgr", True)

    def start(self):
<<<<<<< HEAD
        Thread(self.new).start #start new thread for stream
=======
        Thread(target=self.new, args=()).start()
>>>>>>> 62265caba8d8c88f8f8ae70429c08c3ea034b604
        return self

    def stop(self):
        self.running = False
        
    def read(self):
        return self.frame
        
    def new(self):
        for f in self.stream:
            self.frame = f.array
            self.capture.truncate(0)
            
            #cleanup when cam shuts down
            if self.running == False:
                self.stream.close()
                self.capture.close()
                self.cam.close()
                return
    
def runPiCam():
    print('runs picam method')
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num-frames", type=int, default=100,
        help="frames for test")
    ap.add_argument("-d", "--display", type=int, default=-1,
        help="Whether or not frames should be displayed")
    args = vars(ap.parse_args())

    def singleThread():
        camera = picamera.PiCamera()
        camera.resolution = (320, 240)
        camera.framerate = 16

        capture = PiRGBArray(camera, size=(320, 240))
        stream = camera.capture_continuous(capture, "bgr", True)

        time.sleep(2.0)
        fps = imutils.video.FPS().start()

        for (i, f) in enumerate(stream):
            frame = f.array
            frame = imutils.resize(frame, width=400)
    
            if args["display"] > 0:
                cv2.imshow("Frame",frame)
                cv2.waitKey(1)

            capture.truncate(0)
            fps.update()
                 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cleanUp(fps, stream, capture, camera)
    
    # multithreaded video stream viewer
    def multiThread():
        stream = Stream().start()
        time.sleep(2.0)
        fps = imutils.video.FPS().start()
       
        while True:
            frame = stream.read()
            frame = imutils.resize(frame, width=400)
<<<<<<< HEAD
            cv2.imshow("multi", frame)
=======
            #cv2.imshow("MultiThreaded", frame)
            
>>>>>>> 62265caba8d8c88f8f8ae70429c08c3ea034b604
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break 

        stream.stop()

    def cleanUp(fps, stream, capture, camera):
        fps.stop()
        cv2.destroyAllWindows()
        stream.close()
        capture.close()
        camera.close()
    
    multiThread()











def getImageFromPiCam():
    try:
        import  picamera
    except:
        os.kill
    stream = io.BytesIO()

    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')

    #Convert the picture into a numpy array
    buff = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8)

    #Now creates an OpenCV image
    return process(cv2.imdecode(buff, 1),'piCam ')


def process(frame, method):
        cascPath = "/cascades/faces.xml"
        #print(ROOT_DIR)
        cascade = cv2.CascadeClassifier(ROOT_DIR + cascPath)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = cascade.detectMultiScale(gray, 1.1, 5)

        cv2.imshow('video feed', frame)

        k = cv2.waitKey(10)

        if len(faces) > 0:
            logLogger.writeToLog(method , "Found " + str(len(faces))+ " face(s)")
            save(frame, method, faces)
            getImageFromPiCam()
        
        if k == -1:
            getImageFromPiCam()

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

    notification.notification(fileName, filePath)

    if os.path.isfile(filePath) == True:
       logLogger.writeToLog(method, " wrote file " + ('result_%s.jpg'%i)) 
    else:
       logLogger.writeToLog('ERROR IN: ' + method, ("FAILED to write file " + ('result_%s.jpg'%i) + 'CDW is: ' + cde )) 

#getImageFromPiCam()
#runPiCam()