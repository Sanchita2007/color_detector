import numpy as np
import cv2

def get_limits(color):
    c = np.uint8([[color]])  # Convert BGR to HSV
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Extract Hue value

    # Define HSV ranges for primary colors
    if np.array_equal(color, [0, 0, 255]):  # Red in BGR
        lowerLimit1 = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit1 = np.array([10, 255, 255], dtype=np.uint8)
        lowerLimit2 = np.array([170, 100, 100], dtype=np.uint8)
        upperLimit2 = np.array([180, 255, 255], dtype=np.uint8)
        return (lowerLimit1, upperLimit1), (lowerLimit2, upperLimit2)  #2 ranges for red

    elif np.array_equal(color, [0, 255, 0]):  # Green
        lowerLimit = np.array([40, 100, 100], dtype=np.uint8)
        upperLimit = np.array([80, 255, 255], dtype=np.uint8)

    elif np.array_equal(color, [255, 0, 0]):  # Blue
        lowerLimit = np.array([100, 100, 100], dtype=np.uint8)
        upperLimit = np.array([130, 255, 255], dtype=np.uint8)

    elif np.array_equal(color, [0, 255, 255]):  # Yellow
        lowerLimit = np.array([20, 100, 100], dtype=np.uint8)
        upperLimit = np.array([30, 255, 255], dtype=np.uint8)

    elif np.array_equal(color, [0, 0, 0]):  # Black
        lowerLimit = np.array([0, 0, 0], dtype=np.uint8)
        upperLimit = np.array([180, 255, 30], dtype=np.uint8)

    elif np.array_equal(color, [255, 255, 255]):  # White
        lowerLimit = np.array([0, 0, 200], dtype=np.uint8)
        upperLimit = np.array([180, 30, 255], dtype=np.uint8)

    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return (lowerLimit, upperLimit)
