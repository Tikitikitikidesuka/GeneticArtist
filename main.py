import sys
import pygad
import cv2 as cv
import numpy as np


# Helper functions

def image_difference(img_a, img_b):
    return cv.norm(img_a, img_b, cv.NORM_L2)

def image_from_gene(target_img, canvas_img, gene):
    canvas_img = canvas_img.copy()
    
    # Get the target image's average color inside the stroke area
    mask = np.zeros((target_img.shape[0], target_img.shape[1]), np.uint8)
    cv.circle(mask, (int(gene[0]), int(gene[1])), int(gene[2] * 64), (255, 255, 255), -1)
    mean_color = cv.mean(target_img, mask=mask)[:-1]

    cv.circle(canvas_img, (int(gene[0]), int(gene[1])), int(gene[2] * 64), mean_color, -1)

    return canvas_img


# Cli parameters

if len(sys.argv) < 2:
    sys.exit("Usage:\npython main.py target_img <canvas_img>")

target_img_dir = sys.argv[1]
canvas_img_dir = sys.argv[2] if len(sys.argv) > 2 else None


# Load images

target_img = cv.imread(target_img_dir)

canvas_img = cv.imread(canvas_img_dir) if canvas_img_dir else np.full_like(target_img, (255, 255, 255))
if canvas_img.shape != target_img.shape:
    sys.exit("Canvas image and target image must be the same size!")

"""
radius = 32
pos = (1000, 500)

mask = np.zeros((target_img.shape[0], target_img.shape[1]), np.uint8)
cv.circle(mask, pos, radius, (255, 255, 255), -1)
mean_color = cv.mean(target_img, mask=mask)[:-1]

cv.imshow("XD", cv.bitwise_and(target_img, target_img, mask=mask))
cv.waitKey()

cv.circle(mask, pos, radius, mean_color, -1)


print(mean_color)

cv.imshow("XD",mask)
cv.waitKey()

exit()
"""

# GA parameters

generations = 32
population_size = 16

parallel_processing = 8

def fitness_function(gene, gene_idx):
    diff = image_difference(target_img, image_from_gene(target_img, canvas_img, gene))
    return 1.0 / diff if diff != 0 else float("inf")

# genes -> [stroke x position, stroke y position, stroke scale, stroke rotation]
gene_space = [range(0, target_img.shape[1] + 1),
              range(0, target_img.shape[0] + 1),
              {"low": 0.1, "high": 10.0},
              {"low": 0.0, "high": 360.0}]

def on_start(ga_instance):
    print("Starting GA...");

def on_stop(ga_instance, last_population_fitness):
    print("Stopping GA...");

def on_generation(ga_instance):
    print("Generation " + str(ga_instance.generations_completed) + " finished")

for _ in range(1024):
    ga_instance = pygad.GA(num_generations=generations,
                           fitness_func=fitness_function,
                           sol_per_pop=population_size,
                           num_parents_mating=10,
                           num_genes=4,
                           parallel_processing=parallel_processing,
                           gene_space=gene_space,
                           on_start=on_start,
                           on_stop=on_stop,
                           on_generation=on_generation)


    # GA execution

    ga_instance.run()


    # Show result

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    canvas_img = image_from_gene(target_img, canvas_img, solution)

cv.imshow("Output", canvas_img)
cv.waitKey()
