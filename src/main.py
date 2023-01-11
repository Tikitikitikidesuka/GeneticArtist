import toml
from pathlib import Path
from pydantic import ValidationError
import genetic_artist_config


def interrupt_program(before_exit=None):
    print("Interrupted!")
    print("Terminating")

    if before_exit:
        before_exit()

    exit(1)


# Make queue statically typed with a class which contains an image
# or a message like LasImage or ProgramEnd

try:
    import cli
    import signal
    import cv2 as cv
    from multiprocessing import Process, Queue, Event
    from genetic_artist import GeneticArtist, GeneticArtistException
except KeyboardInterrupt:
    interrupt_program()


# Not very good function ahead... Remember to fix it sometime
# If the artist is faster than the loop wait time Keyboard interrupts will not work
def show_progress_process(window_name: str, image_queue: Queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    loop_wait = 50
    image = image_queue.get()
    while image is not None:
        cv.imshow(window_name, image)
        cv.waitKey(loop_wait)
        if not image_queue.empty():
            image = image_queue.get()

    while cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE) and cv.waitKey(loop_wait) & 0xFF != 27:
        pass

    cv.destroyAllWindows()


def run_genetic_artist(genetic_artist: GeneticArtist, image_queue: Queue = None, verbose=False):
    if image_queue:
        image_queue.put(genetic_artist.get_image())

    for iteration in range(cli.ARGS.ITERATIONS):
        genetic_artist.draw_stroke()

        if verbose:
            print("Stroke number %d finished" % iteration)

        if image_queue:
            image_queue.put(genetic_artist.get_image())

    if image_queue:
        image_queue.put(None)


def store_genetic_artist_result(genetic_artist: GeneticArtist, output_file: str, verbose=False):
    if verbose:
        print("Storing the final image into %s..." % output_file)

    try:
        genetic_artist.store_image(output_file)
    except GeneticArtistException as exception:
        print(exception.message)
        return

    if verbose:
        print("Image stored successfully")


def main():
    if cli.ARGS.VERBOSE:
        print("Creating the genetic artist...")

    # Load configuration
    try:
        toml_data = toml.loads(Path(cli.ARGS.CONFIG_FILE).read_text())
    except FileNotFoundError as exception:
        print(f"Config file \'{exception.filename}\' not found")
        exit(1)

    try:
        config: genetic_artist_config.Configuration = genetic_artist_config.Configuration.parse_obj(toml_data)
    except ValidationError as exception:
        print(f"Config file exception: {exception}")
        exit(1)

    # Create the Genetic Artist
    try:
        genetic_artist = GeneticArtist(cli.ARGS.TARGET_IMG_FILE, cli.ARGS.STROKE_IMG_DIR, config,
                                       canvas_img_path=cli.ARGS.CANVAS_IMG_FILE)
    except GeneticArtistException as exception:
        print(exception.message)
        exit(1)

    if cli.ARGS.VERBOSE:
        print("Genetic artist created successfully")
        print("Starting the drawing process...")

    if not cli.ARGS.NO_GUI:
        image_queue = Queue()
        display_process = Process(name='DisplayProcess', target=show_progress_process, args=('Output', image_queue))
        display_process.start()

        try:
            run_genetic_artist(genetic_artist, image_queue=image_queue, verbose=cli.ARGS.VERBOSE)
            store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)
        except KeyboardInterrupt:
            def interrupt_func():
                if display_process.is_alive():
                    image_queue.put(None)
                display_process.join()

                store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)

            interrupt_program(interrupt_func)

        if cli.ARGS.VERBOSE:
            print("\nProcess finished successfully")
            print("Press ESC on the preview window to close it")

        display_process.join()

    else:
        try:
            run_genetic_artist(genetic_artist, verbose=cli.ARGS.VERBOSE)
            store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)
        except KeyboardInterrupt:
            def interrupt_func():
                store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)

            interrupt_program(interrupt_func)

        if cli.ARGS.VERBOSE:
            print("\nProcess finished successfully")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        interrupt_program()
