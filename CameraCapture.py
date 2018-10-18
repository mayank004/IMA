import cv2
import pyttsx3
import numpy as np
from minimal_object_detection_lib import MinimalObjectDetector

cameraId = 0
cap = cv2.VideoCapture(cameraId)

detector = MinimalObjectDetector()
detector.Initialize()

engine = pyttsx3.init()
engine.setProperty("rate", 120)

i = 0
while True:
    _, frame = cap.read()
    i += 1

    if i == 50:
        i = 0

        # Excluding person with distinct elements
        labels = []
        frame_rgb = np.copy(frame)
        result = detector.Process(frame_rgb)

        for i in range(len(result)):
            label = result[i]['label']
            if label != 'person':
                labels.append(label)

        labels = list(set(labels))

        print(labels)

        lineCount = 1
        if len(labels) > 0:
            for j in range(len(labels)):
                cv2.putText(frame, labels[j], (50, 50 * lineCount), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                lineCount += 1

        cv2.imshow('frame', frame)

        if len(labels) > 0:
            for j in range(len(labels)):
                engine.say("I can see " + labels[j])
                engine.startLoop()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()