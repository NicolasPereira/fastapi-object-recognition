import cv2
import numpy as np
classes = None

def create_json(classes, class_id, confidence):
    confidencePorcent = confidence * 100
    confidenceFormatted = round(confidencePorcent, 2)
    infoProdutos = {"produto": classes[class_id], "precisao": confidenceFormatted}
    return infoProdutos

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i- 1] for i in net.getUnconnectedOutLayers()]

    return output_layers

def detect(foto): 
    image = cv2.imread(foto)
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    produtos = []
    with open('yolov3.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])


    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        produtos.append(create_json(classes, class_ids[i], confidences[i]))
    resultados = produtos.copy()
    produtos.clear()
    return resultados