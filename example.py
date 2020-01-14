#!/usr/bin/python3
import cv2
import numpy as np
import iris

# Set up the sliders
iris.slider("hue", 0, 255)
iris.slider("sat", 0, 255)
iris.slider("val", 0, 255)

# Add a video stream
iris.stream("http://10.15.40.100:5801/stream.jpg")

# You can add as many as you want, it organizes into a 3xN grid.
# iris.stream("http://10.15.40.100:5801/stream.jpg")
# iris.stream("http://10.15.40.100:5801/stream.jpg")
# iris.stream("http://10.15.40.100:5801/stream.jpg")

cap = cv2.VideoCapture(0)

# Spawn a new thread with the web server
iris.serve(host='0.0.0.0', port=8012)

if not cap.isOpened():
    print("Unable to read camera feed")

while True:
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the values by name consisting of [high, low]
    hue = iris.get("hue")
    sat = iris.get("sat")
    val = iris.get("val")

    lower = np.array([hue[0], sat[0], val[0]])
    higher = np.array([hue[1], sat[1], val[1]])

    mask = cv2.inRange(hsv, lower, higher)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    if ret:
        # cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        # cv2.imshow("res", res)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()
