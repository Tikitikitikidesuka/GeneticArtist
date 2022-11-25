import sys
import pygad
import cv2 as cv
import image_ops

class GeneticArtist:
    def __init__(self, target_img_path, stroke_img_dir_path, canvas_img_path = None):
        self.target_img = cv.imread(target_img_path)

        if canvas_img_path:
            self.canvas_img = cv.imread(canvas_img_path)
            if self.canvas_img.shape != self.target_img.shape:
                sys.exit("Canvas image and target image must be the same size!")
        else:
            self.canvas_img = image_ops.color_like(self.target_image)