import cv2
import numpy as np


def binarize(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Adaptive threshold handles
    # uneven lighting and shadows.
    scanned = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        15
    )

    # Remove tiny noise
    kernel = np.ones(
        (2, 2),
        np.uint8
    )

    scanned = cv2.morphologyEx(
        scanned,
        cv2.MORPH_OPEN,
        kernel
    )

    return scanned
