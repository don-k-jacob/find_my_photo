import cv2
import numpy as np
from authentication import authenticate

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

def search_images(folder_id, detected_face):
    service = authenticate()
    query = f"'{folder_id}' in parents and mimeType='image/jpeg'"
    results = service.files().list(q=query,fields="nextPageToken, files(id, name)").execute()
    images = results.get("files", [])
    for image in images:
        image_id = image.get("id")
        image_file = service.files().get_media(fileId=image_id)
        image_data = image_file.execute()
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            face_from_image = gray[y:y+h, x:x+w]
            result = cv2.matchTemplate(detected_face, face_from_image, cv2.TM_CCOEFF_NORMED)
            if result >= 0.7:
                print(f'Image {image.get("name")} contains the same face')
            else:
                print(f'Image {image.get("name")} does not contain the same face')

def take_selfie_and_search():
    take_picture()
    detected_face = detect_face("selfie.jpg")
    search_images("your_folder_id", detected_face)
