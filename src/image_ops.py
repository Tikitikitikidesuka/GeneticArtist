import cv2 as cv
import numpy as np
from numba import jit


def color_like(reference_img: np.array, color: tuple[int, int, int]):
    return np.full_like(reference_img, color)


def image_difference(img_a: np.array, img_b: np.array):
    return cv.norm(img_a, img_b, cv.NORM_L2)


def scale_stroke(stroke_img: np.array, scale: float):
    height, width = stroke_img.shape[:2]
    new_dimensions = (int(width * scale), int(height * scale))
    return cv.resize(stroke_img, new_dimensions)


def rotate_stroke(stroke_img: np.array, angle: float):
    # https://pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    height, width = stroke_img.shape[:2]
    center = (width // 2, height // 2)

    M = cv.getRotationMatrix2D(center, angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    new_width = int((height * sin) + (width * cos))
    new_height = int((height * cos) + (width * sin))

    M[0, 2] += (new_width / 2) - center[0]
    M[1, 2] += (new_height / 2) - center[1]

    return cv.warpAffine(stroke_img, M, (new_width, new_height))


@jit(nopython=True)
def crop_image_by_mask_and_position(target_img: np.array, mask: np.array, position: tuple[int, int]) -> tuple[np.array, np.array]:
    target_height, target_width = target_img.shape[:2]
    height, width = mask.shape[:2]

    xp_diff = 0
    x_pos = position[0] - width // 2
    if x_pos < 0:
        xp_diff = -x_pos
        x_pos = 0

    xl_diff = 0
    x_lim = x_pos + width - xp_diff
    if x_lim > target_width:
        xl_diff = x_lim - target_width
        x_lim = target_width

    yp_diff = 0
    y_pos = position[1] - height // 2
    if y_pos < 0:
        yp_diff = -y_pos
        y_pos = 0

    yl_diff = 0
    y_lim = y_pos + height - yp_diff
    if y_lim > target_height:
        yl_diff = y_lim - target_height
        y_lim = target_height

    mask = mask[yp_diff:height-yl_diff, xp_diff:width-xl_diff]
    target_crop = target_img[y_pos:y_lim, x_pos:x_lim]

    return target_crop, mask


def get_mean_stroke_color(target_img: np.array, stroke_img: np.array, position: tuple[int, int]):
    target_crop, stroke_img = crop_image_by_mask_and_position(target_img, stroke_img, position)
    return cv.mean(target_crop, mask=stroke_img)[:3]


@jit(nopython=True)
def paint_stroke(canvas_img: np.array, stroke_img: np.array, stroke_color: tuple[int, int, int],
                 position: tuple[int, int]) -> np.array:
    output = canvas_img.copy()
    height, width = stroke_img.shape[:2]
    boundy, boundx = canvas_img.shape[:2]
    stroke_color = np.array(stroke_color)

    x_pos = position[0] - width // 2
    y_pos = position[1] - height // 2

    for y in range(height):
        gy = y + y_pos
        if 0 <= gy < boundy:
            for x in range(width):
                gx = x + x_pos
                if 0 <= gx < boundx:
                    background_color = canvas_img[gy, gx]
                    overlay_alpha = stroke_img[y, x] / 255
                    output[gy, gx] = background_color * (1 - overlay_alpha) + stroke_color * overlay_alpha

    return output
