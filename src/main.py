import cli
import cv2 as cv
from src.genetic_artist import GeneticArtist

genetic_artist = GeneticArtist(cli.ARGS.TARGET_IMG_FILE, cli.ARGS.STROKE_IMG_DIR,
                               canvas_img_path=cli.ARGS.CANVAS_IMG_FILE,
                               config_file_path=cli.ARGS.GENETIC_ARTIST_CONFIG_FILE)

for _ in range(32):
    genetic_artist.draw_circle()
    cv.imshow('Output', genetic_artist._canvas_img)
    cv.waitKey(10)

cv.imshow("Output", genetic_artist._canvas_img)
cv.waitKey()

"""
def on_start(ga_instance):
    # print("Starting GA...");
    pass


def on_stop(ga_instance, last_population_fitness):
    # print("Stopping GA...");
    pass


def on_generation(ga_instance):
    # print("Generation " + str(ga_instance.generations_completed) + " finished")
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
"""
