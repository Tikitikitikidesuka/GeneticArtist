import cv2 as cv
import numpy as np

def color_like(reference_img: np.array, color: tuple[int, int, int]):
    return np.full_like(reference_img, color)