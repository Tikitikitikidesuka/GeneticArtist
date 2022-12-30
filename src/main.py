import cli
import cv2 as cv
from src.genetic_artist import GeneticArtist

genetic_artist = GeneticArtist(cli.ARGS.TARGET_IMG_FILE, cli.ARGS.STROKE_IMG_DIR,
                               canvas_img_path=cli.ARGS.CANVAS_IMG_FILE,
                               config_file_path=cli.ARGS.GENETIC_ARTIST_CONFIG_FILE)

for _ in range(256):
    try:
        genetic_artist.draw_stroke()
        cv.imshow('Output', genetic_artist._canvas_img)
        cv.waitKey(1)
    except:
        cv.waitKey(1);

cv.waitKey()
