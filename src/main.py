import cli
import cv2 as cv
from genetic_artist import GeneticArtist
from multiprocessing import Process, Queue


def show_progress(image_queue: Queue):
    while True:
        if not image_queue.empty():
            image = image_queue.get()
            if image is None:
                break
            cv.imshow('Output', image)
        cv.waitKey(10)
    cv.waitKey()


if __name__ == '__main__':
    # Create genetic artist
    genetic_artist = GeneticArtist(cli.ARGS.TARGET_IMG_FILE, cli.ARGS.STROKE_IMG_DIR,
                                   canvas_img_path=cli.ARGS.CANVAS_IMG_FILE,
                                   config_file_path=cli.ARGS.GENETIC_ARTIST_CONFIG_FILE)

    # Create image queue and display process
    image_queue = Queue()
    display_process = Process(target=show_progress, args=(image_queue,))

    # Add blank canvas to image queue and start display process
    image_queue.put(genetic_artist.get_image())
    display_process.start()

    # Run genetic artist for n strokes
    for _ in range(32):
        genetic_artist.draw_stroke()
        image_queue.put(genetic_artist.get_image())

    # End display process
    image_queue.put(None)
    display_process.join()
