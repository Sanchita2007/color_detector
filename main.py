import cv2
import numpy as np
from PIL import Image
from util import get_limits  # Imports function from util.py

# Defines colors in BGR format
colors = {
    "red": [0, 0, 255],
    "green": [0, 255, 0],
    "blue": [255, 0, 0],
    "yellow": [0, 255, 255],
    "black": [0, 0, 0],
    "white": [255, 255, 255],
}

# Start detection from index 3
color_index = 3
color_names = list(colors.keys())  # List of color names

cap = cv2.VideoCapture(0)

# Tracking previous bbox for smoothing
prev_bbox = None  

while True:
    ret, frame = cap.read()
    if not ret:
        continue  # Skip if  frame is empty(avoids cv2 error)

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the currently selected color
    color_name = color_names[color_index]
    bgr_value = colors[color_name]
    limits = get_limits(color=bgr_value)

    if isinstance(limits[0], tuple):  # Special case for red (2 HSV ranges)
        lowerLimit1, upperLimit1 = limits[0]
        lowerLimit2, upperLimit2 = limits[1]
        mask1 = cv2.inRange(hsvImage, lowerLimit1, upperLimit1)
        mask2 = cv2.inRange(hsvImage, lowerLimit2, upperLimit2)
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        lowerLimit, upperLimit = limits
        mask = cv2.inRange(hsvImage, lowerLimit, upperLimit)

    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

        #Bbox Stability Enhancements
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        area = (x2 - x1) * (y2 - y1)

        # Ignore small flickering detections
        if area > 500:  # Minimum size threshold (adjustable)
            # Smooth Bbox using previous frame data
            if prev_bbox is not None:
                x1 = int(0.7 * prev_bbox[0] + 0.3 * x1)
                y1 = int(0.7 * prev_bbox[1] + 0.3 * y1)
                x2 = int(0.7 * prev_bbox[2] + 0.3 * x2)
                y2 = int(0.7 * prev_bbox[3] + 0.3 * y2)

            prev_bbox = (x1, y1, x2, y2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr_value, 3)  # Draw Bbox
            cv2.putText(frame, color_name.upper(), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, bgr_value, 2, cv2.LINE_AA)  # Label the detected color

    cv2.putText(frame, f"Press 'n' to switch color: {color_name.upper()}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("n"):  # Switch color when 'n' is pressed
        color_index = (color_index + 1) % len(colors)
        prev_bbox = None  # Reset tracking when switching colors

cap.release()
cv2.destroyAllWindows()
