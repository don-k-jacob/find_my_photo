import cv2
import numpy as np
import os
import shutil
# from authentication import authenticate

def take_picture():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    cv2.imwrite("selfie.jpg", image)
    del(camera)

def detect_face(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
    cv2.imwrite("selfie_with_face.jpg", image)
    return gray

def search_images(folder_path, detected_face):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                image_path = os.path.join(root, file)
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
                for (x, y, w, h) in faces:
                    face_from_image = gray[y:y+h, x:x+w]
                    result = cv2.matchTemplate(detected_face, face_from_image, cv2.TM_CCOEFF_NORMED)
                    if np.any(result >= 0.7):
                        save_matched_image(image_path)
                        print(f'Image {file} contains the same face and saved to matched_images folder')
                    else:
                        print(f'Image {file} does not contain the same face')
                    
def save_matched_image(image_path):
    shutil.copy(image_path, "images/match/")

def take_selfie_and_search():
    take_picture()
    detected_face = detect_face("selfie.jpg")
    print("pic saved")
    search_images("images", detected_face)

take_selfie_and_search()