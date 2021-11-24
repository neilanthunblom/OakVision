from definitions import ROOT_DIR
from ftpretty import ftpretty
from twilio.rest import Client
import secrets
import logLogger
import cv2
import os

logName = 'Notification'

def notify(fileName, filePath):

    def uploadImg():
        try:
            ftp = ftpretty(secrets.sftp_host,secrets.sftp_username,secrets.sftp_password)
            logLogger.writeToLog(logName," authenticated with " + secrets.sftp_username + " to " + secrets.sftp_host)
            ftp.put(filePath,"/MMS_img/" + fileName)
            logLogger.writeToLog(logName," put " + fileName + " to \'oakvision/MMS_img\'")
        except:
            print("faild to connect to ftp")
            logLogger.writeToLog(logName," FAILD to authenticate " + secrets.sftp_username + " at " + secrets.sftp_host)
        
    uploadImg()

def sendNotif(frame):
    account_sid = os.environ[secrets.account_sid]
    auth_token = os.environ[secrets.auth_token]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
            body=('Face Detected view '),
            from_='+17372010005',
            to=secrets.notifcationToPhoneNumber
        )

    print(message.sid)