import glob
import sys
import pygad
import cv2 as cv
import numpy as np
import image_ops

class GeneticArtistException(Exception):
    """Exception raised for errors from a GeneticArtist object

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=''):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class NonMatchingCanvasSize(GeneticArtistException):
    """Exception raised when the target image and the canvas do not have the same size"""

    def __init__(self):
        super().__init__('The canvas and the target image must be the same size')


class EmptyStrokeImgList(GeneticArtistException):
    """Exception raised when the provided stroke image directory has no valid images

    Attributes:
        stroke_img_dir_path -- path to the stroke image directory
    """

    def __init__(self, stroke_img_dir_path: str):
        super().__init__(f'No stroke images were found in {stroke_img_dir_path}')

class ImageNotFoundError(GeneticArtistException):
    """Exception raised when an image is not found

    Attributes:
        file_path -- path to the missing image
    """

    def __init__(self, file_path: str):
        super().__init__(f'Image \'{file_path}\' not found')


class GeneticArtist:
    def __init__(self, target_img_path: str, stroke_img_dir_path: str, canvas_img_path: str = None):
        # Define instance variables
        self.target_img: np.array
        self.canvas_img: np.array
        self.stroke_img_list: list[np.array] = []

        # Load target image
        self.target_img = cv.imread(target_img_path)
        if self.target_img is None:
            raise ImageNotFoundError(target_img_path)

        # Store stroke images
        stroke_img_dir_ls = glob.glob(f'{stroke_img_dir_path}/*')
        for file in stroke_img_dir_ls:
            read_img = cv.imread(file)
            if read_img is not None:
                self.stroke_img_list.append(read_img)
        if len(self.stroke_img_list) == 0:
            raise EmptyStrokeImgList(stroke_img_dir_path)

        # Store canvas image if specified or create blank canvas image otherwise
        if canvas_img_path:
            self.canvas_img = cv.imread(canvas_img_path)
            if self.canvas_img is None:
                raise ImageNotFoundError(target_img_path)
        else:
            self.canvas_img = image_ops.color_like(self.target_img)