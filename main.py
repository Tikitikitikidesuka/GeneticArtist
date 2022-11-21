import sys
import pygad
import cv2 as cv
import numpy as np

def image_difference(img_a, img_b):
    return cv.norm(img_a, img_b, cv.NORM_L2)


# Cli parameters

if len(sys.argv) < 2:
    sys.exit("Usage:\npython main.py target_img <canvas_img>")

target_img_dir = sys.argv[1]
canvas_img_dir = sys.argv[2] if len(sys.argv) > 2 else None

# Load images

target_img = cv.imread("assets/" + target_img_dir)

canvas_img = cv.imread("assets/" + canvas_img_dir) if canvas_img_dir else np.full_like(target_img, (255, 255, 255))
if (canvas_img.shape != target_img).all():
    sys.exit("Canvas image and target image must be the same size!")






# GA parameters

fitness_function = lambda gene, gene_idx : 1.0 / image_difference(target_img, image_from_gene(canvas_img, gene))

# genes -> [stroke x position, stroke y position, scale, stroke rotation]
gene_space = [range(0, target_img.shape[1] + 1),
              range(0, target_img.shape[0] + 1),
              {"low": 0.33, "high": 3.0},
              {"low": 0.0, "high": 360.0}]

def on_start(ga_instance):
    print("Starting GA...");

def on_stop(ga_instance, last_population_fitness):
    print("Stopping GA...");

#ga_instance = pygad.GA(num_generations=num_generations...







# Tests

cv.imshow("XD", canvas_img)
cv.waitKey()
