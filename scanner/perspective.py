import cv2
import numpy as np


def order_points(points):

    rect = np.zeros(
        (4, 2),
        dtype=np.float32
    )

    # Top-left + bottom-right
    total = points.sum(axis=1)

    rect[0] = points[np.argmin(total)]
    rect[2] = points[np.argmax(total)]

    # Top-right + bottom-left
    difference = np.diff(
        points,
        axis=1
    ).ravel()

    rect[1] = points[np.argmin(difference)]
    rect[3] = points[np.argmax(difference)]

    return rect


def warp_page(image, points):

    rect = order_points(points)

    tl, tr, br, bl = rect

    width_top = np.linalg.norm(tr - tl)
    width_bottom = np.linalg.norm(br - bl)

    max_width = int(
        max(width_top, width_bottom)
    )

    height_left = np.linalg.norm(bl - tl)
    height_right = np.linalg.norm(br - tr)

    max_height = int(
        max(height_left, height_right)
    )

    destination = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype=np.float32)

    matrix = cv2.getPerspectiveTransform(
        rect,
        destination
    )

    warped = cv2.warpPerspective(
        image,
        matrix,
        (max_width, max_height)
    )

    return warped
