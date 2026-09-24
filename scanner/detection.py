import cv2
import numpy as np


def preprocess_for_detection(image):
    """
    Create an edge image suitable for document detection.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Reduce noise
    gray = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    # Canny edges
    edges = cv2.Canny(
        gray,
        30,
        120
    )

    # Connect broken edges
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (9, 9)
    )

    edges = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )

    return gray, edges


def find_page(image):
    """
    Detect the largest document-like quadrilateral.
    """

    gray, edges = preprocess_for_detection(
        image
    )

    height, width = gray.shape

    image_area = height * width

    # Find external contours
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        raise ValueError(
            "No contours detected."
        )

    # Largest contours first
    contours = sorted(
        contours,
        key=cv2.contourArea,
        reverse=True
    )

    # Look through many contours
    for contour in contours[:100]:

        area = cv2.contourArea(
            contour
        )

        # Ignore very small objects
        if area < image_area * 0.02:
            continue

        perimeter = cv2.arcLength(
            contour,
            True
        )

        # Try several approximation values
        for epsilon in [
            0.01,
            0.015,
            0.02,
            0.025,
            0.03,
            0.04,
            0.05,
            0.06,
            0.08,
        ]:

            approx = cv2.approxPolyDP(
                contour,
                epsilon * perimeter,
                True
            )

            if len(approx) == 4:

                points = approx.reshape(
                    4,
                    2
                ).astype(np.float32)

                if cv2.isContourConvex(
                    approx
                ):

                    return points

    raise ValueError(
        "Document/page could not be detected."
    )


def get_debug_images(image):
    """
    Return intermediate images for debugging.
    """

    gray, edges = preprocess_for_detection(
        image
    )

    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    # Otsu threshold
    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return {
        "gray": gray,
        "edges": edges,
        "adaptive": adaptive,
        "otsu": otsu,
    }
