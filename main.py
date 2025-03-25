
import os
import cv2
import pickle

import cvzone
import face_recognition
import numpy as np
import time  as t# Thêm import thư viện time

import firebase_admin
from firebase_admin import credentials, db
from firebase_admin import storage
from datetime import datetime, date, timedelta

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendacerealtime-f55c9-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendacerealtime-f55c9.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 500)
cap.set(4, 380)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    img = cv2.imread(os.path.join(folderModePath, path))
    img = cv2.resize(img, (325, 605))  # Resize img to match the size of the region in imgBackground
    imgModeList.append(img)


# Load the encoding file
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")

modeType = 0 #display active 1.png
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgResized = cv2.resize(img, (500, 380))  # Resize img to match the size of the region in imgBackground

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[220:220 + 380, 97:97 + 500] = imgResized
    imgBackground[52:52 + 605, 703:703 + 325] = imgModeList[modeType]
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match index", matchIndex)
            if matches[matchIndex]:
                # print("Known face detected ")
                # print(studentIds[matchIndex])
                # print(faceLoc)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

                # print(x1, y1,x2,  y2 , x1)

                # Không cần thay đổi tỷ lệ kích thước vì imgResized đã là 500x380
                bbox = (10 + x1, 100 + y1, x2 - x1, y2 - y1)
                # print(int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
                # Chuyển đổi tọa độ bbox thành kiểu số nguyên
                bbox = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]

                if counter == 0:
                    counter = 1
                    modeType = 1 #display infor (2.png)
            # if not any(matches):
            #     modeType = 4
        if counter != 0:
            if counter ==1:
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                #Get the image form the storage
                blob = bucket.get_blob(f'Images/{id}.jpg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                # Thay đổi kích thước của imgStudent sao cho phù hợp với kích thước của vùng trên imgBackground
                #update data of attendance
                # datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                lastAttendanceDate = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S").date()
                currentDate = date.today()

                # secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                # print(secondsElapsed)
                if lastAttendanceDate < currentDate:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    '''
                    one_day_delta = timedelta(days=1)
                    # # Lấy ngày hôm qua
                    yesterday = datetime.now() - one_day_delta
                    # # Format ngày hôm qua dưới dạng chuỗi "YYYY-MM-DD HH:MM:SS"
                    yesterday_str = yesterday.strftime("%Y-%m-%d %H:%M:%S")
                    # # Set thời gian điểm danh trước đó là hôm qua
                    ref.child('last_attendance_time').set(yesterday_str)
                    '''
                else:
                    modeType = 3 # already marked (4.png)
                    counter = 0
                    imgBackground[52:52 + 605, 703:703 + 325] = imgModeList[modeType]
                    # t.sleep(5)

            if modeType !=3 :
                if 10 < counter < 20:
                    modeType = 2 #displays the "marked" (3.png)

                imgBackground[52:52 + 605, 703:703 + 325] = imgModeList[modeType]

                if counter<= 10:

                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (750, 108),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)

                    cv2.putText(imgBackground, str(id), (840, 480),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (835, 553),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (800, 620),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (50, 50, 50), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (950, 620),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (50, 50, 50), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (325-w) //2
                    cv2.putText(imgBackground, str(studentInfo['name']), (700 + offset, 410),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    #rộng trước dài sau
                    imgBackground[145:145 + 216, 757:757 + 216] = imgStudent
                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[52:52 + 605, 703:703 + 325] = imgModeList[modeType]
        # if modeType == 4:
        #     imgBackground[52:52 + 605, 703:703 + 325] = imgModeList[modeType]
        #     counter = 0
        #     modeType = 0
        #     studentInfo = []
        #     imgStudent = []
    else:
        modeType = 0
        counter = 0
    cv2.imshow("FaceAttendance", imgBackground)
    cv2.waitKey(1)
