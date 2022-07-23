import cv2
import numpy as np
import face_recognition
import os
import smtplib
from datetime import datetime

FLAG = 0
OTP = 0
def faceEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def send_mail(to_mail, message, time, date):
    print('mail sent ', to_mail )
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("testingproject5138@gmail.com", "test@2021")

    server.sendmail("testingproject5138@gmail.com", to_mail, message)
    print(456)
    server.quit()
   # return redirect('otp')




def attendance(name, otp_value):
    print('attendance --- ', name)
    print('otp_value --- ', otp_value)
    file_date = datetime.now()
    date_name_new = file_date.strftime('%d/%m/%Y')
    file_date = date_name_new.split('/')
    file_gen = "{}_{}_{}.csv".format(file_date[0], file_date[1], file_date[2])
    with open(file_gen, 'r+') as f:
        #myDataList = f.readlines()
        nameList = []
        to_mail = ""
        ###########TYPE YOUR FRIENDS GMAIL ID'S AND NAME HERE
        person_list = ['prajwal shetty', 'hugh jackman', 'deepika padukone', 'salman khan', 'sharukh khan']
        personNames_parent_mail = ["sneha2917@gmail.com", "prajwal3844@gmail.com", "prajwal4483@gmail.com",
                                   "prajwalshettyme@gmail.com", "tara3844@gmail.com", "prajwalshettyself@gmail.com"]
        '''
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0]) '''
        if name not in nameList:
            time_now = datetime.now()
            tStr = time_now.strftime('%H:%M:%S')
            dStr = time_now.strftime('%d/%m/%Y')
            f.writelines(f'\n{name},{tStr},{dStr}')
            message = "\n{} is present- Entry Time: {}   Date: {}  OTP: {}".format(name, tStr, dStr, otp_value)
            print(message)
            print(name)
            name = name.lower()
            if name == person_list[0]:
                to_mail = personNames_parent_mail[0]
                send_mail(to_mail, message, tStr, dStr)
            if name == person_list[1]:
                to_mail = personNames_parent_mail[1]
                send_mail(to_mail, message, tStr, dStr)
            if name == person_list[2]:
                to_mail = personNames_parent_mail[2]
                send_mail(to_mail, message, tStr, dStr)
            if name == person_list[3]:
                to_mail = personNames_parent_mail[3]
                send_mail(to_mail, message, tStr, dStr)
            if name == person_list[4]:
                to_mail = personNames_parent_mail[4]
                send_mail(to_mail, message, tStr, dStr)

def detect_face(otp_value):
    global FLAG
    time_new = datetime.now()
    date_name = time_new.strftime('%d/%m/%Y')
    time_name = time_new.strftime('%H:%M:%S')
    date_s = date_name.split('/')

    file = "{}_{}_{}.csv".format(date_s[0], date_s[1], date_s[2])

    open(file, 'a').close()



    path = 'C:/Users/Prasheel/Downloads/FaceDetection_V1/FaceDetection_V1/dataset/project/project'
    images = []
    personNames = []
    myList = os.listdir(path)

    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personNames.append(os.path.splitext(cu_img)[0])
    encodeListKnown = faceEncodings(images)
    print('All Encodings Complete!!!')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while_loop_count = 0
    max_loop_count = 100
    while FLAG==0 and while_loop_count<max_loop_count:
        while_loop_count+=1
        ret, frame = cap.read()
        faces = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces, facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personNames[matchIndex].upper()
                print("name is ",name)
                FLAG = 1
                cap.release()
                cv2.destroyAllWindows()
                attendance(name, otp_value)
                break
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)



        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break





