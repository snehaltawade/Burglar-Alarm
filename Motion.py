# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 10:52:48 2018

@author: DTAWADE
"""
import threading

import os
import glob

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from twilio.rest import Client

from tkinter import *
from tkinter import messagebox
from pygame import mixer

import cv2, time, pandas
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets


def Images():
    class Ui_scrolltest(object):
        def setupUi(self, scrolltest):
            scrolltest.setObjectName("scrolltest")
            scrolltest.resize(1400, 1000)
            self.verticalLayout = QtWidgets.QVBoxLayout(scrolltest)
            self.verticalLayout.setObjectName("verticalLayout")
            self.scrollArea = QtWidgets.QScrollArea(scrolltest)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setObjectName("scrollArea")
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 363, 449))
            self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

            self.verticalLayout_2.setObjectName("verticalLayout_2")

            path = (r'''C:\Users\kaust\OneDrive\Desktop\project\project1''')

            for filename in glob.glob(os.path.join(path, '*.png')):
                self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
                self.label.setText("")
                self.label.setPixmap(QtGui.QPixmap(filename))
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("label")
                self.verticalLayout_2.addWidget(self.label)

            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.verticalLayout.addWidget(self.scrollArea)
            self.label_3 = QtWidgets.QLabel(scrolltest)
            self.label_3.setAlignment(QtCore.Qt.AlignCenter)
            self.label_3.setObjectName("label_3")
            self.verticalLayout.addWidget(self.label_3)

            self.retranslateUi(scrolltest)
            QtCore.QMetaObject.connectSlotsByName(scrolltest)

        def retranslateUi(self, scrolltest):
            _translate = QtCore.QCoreApplication.translate
            scrolltest.setWindowTitle(_translate("scrolltest", "scrolltest"))
            self.label_3.setText(_translate("scrolltest",
                                            "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">DETECTION OUTPUT</span></p></body></html>"))

    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        scrolltest = QtWidgets.QWidget()
        ui = Ui_scrolltest()
        ui.setupUi(scrolltest)
        scrolltest.show()
        sys.exit(app.exec_())

def email_send():
    fromaddr = "cameraunlimited856@gmail.com"
    toaddr = Email_.get()
    print(toaddr)
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Your house has been infiltrated"

    # string to store the body of the mail
    body = "The Photo of the house infiltrate"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent

    filename = "opencv.png"
    attachment = open(r'''C:\Users\kaust\OneDrive\Desktop\project\project1\opencv8.png''', "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "Cam@1111")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)
    # terminating the session
    s.quit()


def msg_siren():
    mixer.init()
    mixer.music.load('C:/Users/kaust/Downloads/police_siren.mp3')
    mixer.music.play()

    accountSid = "AC5eb04f88755498ca975d12fd6882a600"
    authToken = "aa0655edcf4da0a75be7d5692b0e0e3d"
    twilioClient = Client(accountSid, authToken)
    myTwilioNumber = "+1 (530) 322-8390"
    destCellPhone = Phone.get()
    message = Message_.get()

    myMessage = twilioClient.messages.create(body=message, from_="+1 (530) 322-8390", to="+919284921938")


def hello():
    flag = 30
    flag1 = 0
    flag2 = 375
    i = 0
    h = 0
    # Assigning our static_back to None
    static_back = None

    # List when any moving object appear
    motion_list = [None, None]

    # Time of movement
    time = []

    # Initializing DataFrame, one column is start
    # time and other column is end time
    df = pandas.DataFrame(columns=["Start", "End"])

    # Capturing video
    video = cv2.VideoCapture(0)

    # Infinite while loop to treat stack of image as video
    while True:
        # Reading frame(image) from video
        check, screenshot = video.read()
        frame = screenshot
        blur = cv2.blur(screenshot, (1, 1))
        # Initializing motion = 0(no motion)
        motion = 0

        # Converting color image to gray_scale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Converting gray scale image to GaussianBlur
        # so that change can be find easily
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # In first iteration we assign the value
        # of static_back to our first frame
        if static_back is None:
            static_back = gray
            continue

        # Difference between static background
        # and current frame(which is GaussianBlur)
        diff_frame = cv2.absdiff(static_back, gray)

        # If change in between static background and
        # current frame is greater than 30 it will show white color(255)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # Finding contour of moving object
        (_, cnts, _) = cv2.findContours(thresh_frame.copy(),
                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            motion = 1

            if flag == 0:
                cv2.imwrite('opencv' + str(i) + '.png', blur)
                i = i + 1
                flag = 30
            flag = flag - 1

            if flag1 == 0:
                threading.Thread(target=msg_siren).start()
                flag1 = flag1 + 1
            if flag2 == 0:
                threading.Thread(target=email_send).start()
                flag2 == 375
            flag2 = flag2 - 1

            (x, y, w, h) = cv2.boundingRect(contour)
            # making green rectangle arround the moving object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            h = h + 1
        # Appending status of motion
        motion_list.append(motion)

        motion_list = motion_list[-2:]

        # Appending Start time of motion
        if motion_list[-1] == 1 and motion_list[-2] == 0:
            time.append(datetime.now())

        # Appending End time of motion
        if motion_list[-1] == 0 and motion_list[-2] == 1:
            time.append(datetime.now())

        # Displaying image in gray_scale
        cv2.imshow("Gray Frame", gray)

        # Displaying the difference in currentframe to
        # the staticframe(very first_frame)
        cv2.imshow("Difference Frame", diff_frame)

        # Displaying the black and white image in which if
        # intencity difference greater than 30 it will appear white
        cv2.imshow("Threshold Frame", thresh_frame)

        # Displaying color frame with contour of motion of object
        cv2.imshow("Color Frame", frame)

        key = cv2.waitKey(1)
        # if q entered whole process will stop
        if key == ord(' '):
            mixer.quit()
            static_back = None
            flag1 = 0

        if key == ord('q'):
            # if something is movingthen it append the end time of movement
            if motion == 1:
                time.append(datetime.now())
            break

    # Appending time of motion in DataFrame
    for i in range(0, len(time), 2):
        df = df.append({"Start": time[i], "End": time[i + 1]}, ignore_index=True)

    # Creating a csv file in which time of movements will be saved
    df.to_csv("Time_of_movements.csv")

    video.release()
    print(h)
    # Destroying all the windows

    cv2.destroyAllWindows()


def clicked():
    if Phone.get() == "+919284921938" and Pass.get() == "admin":
        app = Tk()
        canvas= Canvas(app,width=500,height=500 ,bg="#0aafd1")
        canvas.pack()
        box=canvas.create_rectangle(25,75,250,475,fill="#f2cf21")
        app.title("Home Security System")
        app.geometry('500x500')
        app.configure(background='black')
        msgbutt5 = Button(app, text="start", relief=RAISED, bg="white", fg="black",borderwidth=10 ,font="ARIAL 15 italic",
                          command=hello)
        msgbutt5.place(x=150, y=150, anchor="center")
        msgbutt7 = Button(app, text="Show Images", relief=RAISED, bg="white", fg="black",borderwidth=10 , font="ARIAL 15 italic",
                          command=Images)
        msgbutt7.place(x=150, y=250, anchor="center")
        msgbutt6 = Button(app, text="quit", relief=RAISED, bg="white", fg="black",borderwidth=10 , font="ARIAL 15 italic",
                          command=app.destroy)
        msgbutt6.place(x=150, y=350, anchor="center")
        #whiteline=canvas.create_line(20,15,15,250,fill="white",width=5)
        whiteline=canvas.create_line(20,20,475,20,fill="white",width=5)
        whiteline=canvas.create_line(35,35,460,35,fill="white",width=3)

        app.mainloop()
    else:
        messagebox.showerror("invalid", "invalid input")

root = Tk()
root.title("Enter Security Credentials")
canvas= Canvas(root,width=950,height=750 ,bg="#a60de8")
canvas.pack()
box=canvas.create_rectangle(20,150,450,700,fill="#21e0cd")
whiteline=canvas.create_line(20,20,975,20,fill="#edde12",width=10)
#whiteline=canvas.create_line(35,35,700,35,fill="white",width=3)

root.geometry('1000x800')
root.configure(background='#f7c318')
#print("sentense===="+m)
msgbutt = Button(root, text="submit", relief=RAISED, bg="white", fg="black", font="ARIAL 15 bold", borderwidth=20,command=clicked)
msgbutt.place(x=550, y=600, anchor="center")

thelabel = Label(root, fg="white", bg="orange", font="ARIAL 25 bold", text="Admin Details:-")
thelabel.place(x=50, y=200, anchor="w")

thelabel = Label(root, fg="#edde12", bg="#a60de8", font="ARIAL 40 bold", text="WELCOME !!!")
thelabel.place(x=400, y=75, anchor="w")

thelabel = Label(root, fg="white", bg="orange", font="ARIAL 20 italic", text="Phone no:-")
thelabel.place(x=50, y=300, anchor="w")

thelabel = Label(root, fg="white", bg="orange", font="ARIAL 20 italic", text="Email ID:-")
thelabel.place(x=50, y=400, anchor="w")

thelabel = Label(root, fg="white", bg="orange", font="ARIAL 20 italic", text="Password:-")
thelabel.place(x=50, y=500, anchor="w")

thelabel = Label(root, fg="white", bg="orange", font="ARIAL 20 italic", text="Message:-")
thelabel.place(x=50, y=600, anchor="w")

Phone = Entry(root, width=30)
Phone.place(x=310, y=300, anchor="center")

Email_ = Entry(root,width=40)
Email_.place(x=320, y=400, anchor="center")

Pass = Entry(root, width=30, show="*")
Pass.place(x=310, y=500, anchor="center")

Message_ = Entry(root, width=30)
Message_.place(x=310, y=600, anchor="center")

root.mainloop()
