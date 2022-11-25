import cli
import sys
import pygad
import cv2 as cv
import numpy as np
import image_ops


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

# Load images

target_img = cv.imread(cli.ARGS.TARGET_IMG_FILE)

canvas_img = (cv.imread(cli.ARGS.CANVAS_IMG_FILE)
              if cli.ARGS.CANVAS_IMG_FILE
              else image_ops.color_like(target_img, (255, 255, 255)))

if canvas_img.shape != target_img.shape:
    sys.exit("Canvas image and target image must be the same size!")

# GA parameters

generations = 128
population_size = 32

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
    #print("Starting GA...");
    pass

def on_stop(ga_instance, last_population_fitness):
    #print("Stopping GA...");
    pass

def on_generation(ga_instance):
    #print("Generation " + str(ga_instance.generations_completed) + " finished")
    pass

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
    cv.waitKey(1)

cv.imshow("Output", canvas_img)
cv.waitKey()
