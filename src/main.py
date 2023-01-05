import time

import cli
import cv2 as cv
from genetic_artist import GeneticArtist
from multiprocessing import Process, Queue


class NoMoreImages:
    pass


def show_progress(window_name: str, image_queue: Queue):
    _LOOP_WAIT = 50

    image = image_queue.get()
    while image is not None:
        cv.imshow(window_name, image)
        cv.waitKey(_LOOP_WAIT)
        image = image_queue.get()

    while cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE) and cv.waitKey(_LOOP_WAIT) & 0xFF != 27:
        # Wait for window to get closed or ESC key to be pressed
        pass

    cv.destroyAllWindows()


if __name__ == '__main__':
    # Create genetic artist
    genetic_artist = GeneticArtist(cli.ARGS.TARGET_IMG_FILE, cli.ARGS.STROKE_IMG_DIR,
                                   canvas_img_path=cli.ARGS.CANVAS_IMG_FILE,
                                   config_file_path=cli.ARGS.CONFIG_FILE)

    # Create image queue and display process
    image_queue = Queue()
    display_process = Process(target=show_progress, args=('Output', image_queue))

    # Add blank canvas to image queue and start display process
    image_queue.put(genetic_artist.get_image())
    display_process.start()

    start = time.time()

    # Run genetic artist
    for _ in range(cli.ARGS.ITERATIONS):
        genetic_artist.draw_stroke()
        image_queue.put(genetic_artist.get_image())

    print("Time: ", time.time() - start, " seconds")

    # Store final image
    genetic_artist.store_image(cli.ARGS.OUTPUT_FILE)

    # End display process
    image_queue.put(None)
    display_process.join()
