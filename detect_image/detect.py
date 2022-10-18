"""
├── yolo
│   ├── labels.txt
│   ├── yolov4-tiny.cfg
│   ├── yolov4-tiny.weights
├── people.jpg
├── people_out.jpg
├── street.jpg
├── street_out.jpg
├── video.mp4
├── video_out.avi
├── yolo_image.py
└── yolo_video.py
 if program cant find yolo folder in main folder it will crash."""
# example usage: python yolo_image.py -i street.jpg -o output.jpg
import argparse
import time
import glob

import cv2
import numpy as np

def create_json(classes, class_id, confidence):
    confidencePorcent = confidence * 100
    confidenceFormatted = round(confidencePorcent, 2)
    infoProdutos = {"produto": classes[class_id], "precisao": confidenceFormatted}
    return infoProdutos

def detect(imgpath):

    CONFIDENCE_THRESHOLD = 0.7
    NMS_THRESHOLD = 0.4

    weights = glob.glob("detect_image/yolo/*.weights")[0]
    labels = glob.glob("detect_image/yolo/*.txt")[0]
    cfg = glob.glob("detect_image/yolo/*.cfg")[0]

    lbls = list()
    with open(labels, "r") as f:
        lbls = [c.strip() for c in f.readlines()]

    nn = cv2.dnn.readNetFromDarknet(cfg, weights)
    nn.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    nn.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    layer = nn.getLayerNames()
    layer = [layer[i - 1] for i in nn.getUnconnectedOutLayers()]

    image = cv2.imread(imgpath)
    assert image is not None, f"Image is none, check file path. Given path is: {imgpath}"

    (H, W) = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 1 / 255, (416, 416), swapRB=True, crop=False)
    nn.setInput(blob)
    start_time = time.time()
    layer_outs = nn.forward(layer)
    end_time = time.time()

    boxes = list()
    confidences = list()
    class_ids = list()

    for output in layer_outs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONFIDENCE_THRESHOLD:
                box = detection[0:4] * np.array([W, H, W, H])
                (center_x, center_y, width, height) = box.astype("int")

                x = int(center_x - (width / 2))
                y = int(center_y - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

    if len(idxs) > 0:
        json = []
        for i in idxs.flatten():
            json.append(create_json(lbls, class_ids[i], confidences[i]))
        return json
    else:
        return {"error": "Não foi reconhecido nenhum produto!"}
