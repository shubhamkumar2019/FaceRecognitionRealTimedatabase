import cv2
import os
import face_recognition
import pickle

#importing the students Images
folderPath='Images'
pathList=os.listdir(folderPath)               #List of file names in the folderModePath
imgList=[]
studentIds=[]

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    #we want the id also if we type print(path)-123455.png but we only want 123456 ie id
    #print(os.path.splitext(path)[0])   # adding [0] will only give first word before dot
    studentIds.append(os.path.splitext(path)[0])     # Add id to studentids list
print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)

encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")

