def interrupt_program(before_exit=None):
    print("Interrupted!")
    print("Terminating")

    if before_exit:
        before_exit()

    exit(1)


try:
    import cli
    import signal
    import cv2 as cv
    from multiprocessing import Process, Queue, Event
    from genetic_artist import GeneticArtist, GeneticArtistException
except KeyboardInterrupt:
    interrupt_program()


# Not very good function ahead... Remember to fix it sometime
def show_progress_process(window_name: str, image_queue: Queue):
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    loop_wait = 50
    image = image_queue.get()
    while image is not None:
        cv.imshow(window_name, image)
        cv.waitKey(loop_wait)
        if not image_queue.empty():
            image = image_queue.get()

    while not cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE) and cv.waitKey(loop_wait) & 0xFF != 27:
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

    try:
        genetic_artist = GeneticArtist(cli.ARGS.TARGET_IMG_FILE, cli.ARGS.STROKE_IMG_DIR,
                                       canvas_img_path=cli.ARGS.CANVAS_IMG_FILE,
                                       config_file_path=cli.ARGS.CONFIG_FILE)
    except GeneticArtistException as exception:
        print(exception.message)
        exit(1)

    if cli.ARGS.VERBOSE:
        print("Genetic artist created successfully")
        print("Starting the drawing process...")

    if not cli.ARGS.NO_GUI:
        image_queue = Queue()
        display_process = Process(name='DisplayProcess', target=show_progress_process, args=('Output', image_queue))

        try:
            display_process.start()
            run_genetic_artist(genetic_artist, image_queue=image_queue, verbose=cli.ARGS.VERBOSE)
            store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)
            display_process.join()
        except KeyboardInterrupt:
            def interrupt_func():
                if display_process.is_alive():
                    image_queue.put(None)
                display_process.join()

                store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)

            interrupt_program(interrupt_func)

    else:
        try:
            run_genetic_artist(genetic_artist, verbose=cli.ARGS.VERBOSE)
            store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)
        except KeyboardInterrupt:
            def interrupt_func():
                store_genetic_artist_result(genetic_artist, cli.ARGS.OUTPUT_FILE, verbose=cli.ARGS.VERBOSE)

            interrupt_program(interrupt_func)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        interrupt_program()
