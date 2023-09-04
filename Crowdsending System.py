import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import requests #Para obtener la imagen de la URL
import math
import firebase_admin
from firebase_admin import credentials,db
from sort import *

url = 'http://192.168.1.5/1600x1200.jpg'

model = YOLO("yolov8l.pt")

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

totalCount = 0

# Configura las credenciales de Firebase (descarga el archivo JSON de configuración desde tu consola de Firebase)
cred = credentials.Certificate('C:\\TFE\\Scripts TFE\\6. Firebase\\archivo JSON.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://eg25-e9e49-default-rtdb.firebaseio.com'})

while True:

    response = requests.get(url)
    img_array = np.array(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    
    results = model(img, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100

            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "person" and conf > 0.2:
                currentArray = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, currentArray))

        resultsTracker = tracker.update(detections)

        for result in resultsTracker:
            x1, y1, x2, y2, person_id = result
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
		
            # Visuals(rectangle)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(230,216,173))
            cvzone.putTextRect(img, f' {int(person_id)}', (max(0, x1), max(35, y1)),
                               scale=2, thickness=2, offset=10)

            cx, cy = x1 + w // 2, y1 + h // 2

            # Update highest ID
            if person_id > totalCount:
                totalCount = person_id

		#Subir valor a Firebase
                
    # Referencia a la ubicación en la base de datos donde deseas almacenar totalCount
    ref = db.reference('/')

    # Sube el valor de totalCount a la base de datos
    ref.update({'totalCount': totalCount})

    cv2.putText(img, f'Count: {int(totalCount)}', (150, 100), cv2.FONT_HERSHEY_PLAIN, 7, (190, 123, 1), 8)

    cv2.imshow("Image", img)

    cv2.waitKey(1)




