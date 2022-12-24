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
