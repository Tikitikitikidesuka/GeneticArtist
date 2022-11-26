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
    def __init__(self, target_img_path: str, stroke_img_dir_path: str, canvas_img_path: str = None,
                 config_file_path: str = None):
        # Define instance variables
        self._target_img: np.array
        self._canvas_img: np.array
        self._stroke_img_list: list[np.array] = []

        # Load target image
        self._target_img = cv.imread(target_img_path)
        if self._target_img is None:
            raise ImageNotFoundError(target_img_path)

        # Store stroke images
        stroke_img_dir_ls = glob.glob(f'{stroke_img_dir_path}/*')
        for file in stroke_img_dir_ls:
            read_img = cv.imread(file)
            if read_img is not None:
                self._stroke_img_list.append(read_img)
        if len(self._stroke_img_list) == 0:
            raise EmptyStrokeImgList(stroke_img_dir_path)

        # Store canvas image if specified or create blank canvas image otherwise
        if canvas_img_path:
            self._canvas_img = cv.imread(canvas_img_path)
            if self._canvas_img is None:
                raise ImageNotFoundError(target_img_path)
        else:
            self._canvas_img = image_ops.color_like(self._target_img, (255, 255, 255))

        # Setup genetic algorithm
        # genes -> [stroke x position, stroke y position, stroke scale, stroke rotation]
        self._gene_space = [range(0, self._target_img.shape[1] + 1),
                            range(0, self._target_img.shape[0] + 1),
                            {'low': 0.1, 'high': 10.0},
                            {'low': 0.0, 'high': 360.0}]
        self._ga_instance = pygad.GA(num_generations=32,
                                     fitness_func=lambda g, gidx: self._fitness_function(g, gidx),
                                     sol_per_pop=32,
                                     num_parents_mating=10,
                                     num_genes=len(self._gene_space),
                                     parallel_processing=8,
                                     gene_space=self._gene_space)

    def _image_from_gene(self, gene):
        canvas = self._canvas_img.copy()

        # Get the target image's average color inside the stroke area
        mask = np.zeros((self._target_img.shape[0], self._target_img.shape[1]), np.uint8)
        cv.circle(mask, (int(gene[0]), int(gene[1])), int(gene[2] * 64), (255, 255, 255), -1)
        mean_color = cv.mean(self._target_img, mask=mask)

        # Draw
        cv.circle(canvas, (int(gene[0]), int(gene[1])), int(gene[2] * 64), mean_color, -1)

        return canvas

    def _fitness_function(self, gene, gene_idx):
        diff = image_ops.image_difference(self._target_img, self._image_from_gene(gene))
        return 1.0 / diff if diff != 0 else float('inf')

    def draw_circle(self):
        print("Circle")
        self._ga_instance.run()
        solution, solution_fitness, solution_idx = self._ga_instance.best_solution()
        self._canvas_img = self._image_from_gene(solution)
