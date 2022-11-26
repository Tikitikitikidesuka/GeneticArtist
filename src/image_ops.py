import cv2 as cv
import numpy as np


def color_like(reference_img: np.array, color: tuple[int, int, int]):
    return np.full_like(reference_img, color)


def image_difference(img_a, img_b):
    return cv.norm(img_a, img_b, cv.NORM_L2)
