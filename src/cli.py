import os
import argparse
from argparse import ArgumentParser
from pathvalidate import is_valid_filename


def is_valid_path(arg: str) -> bool:
    return os.path.exists(arg)


def is_valid_file(arg: str) -> str:
    if not is_valid_path(arg) or not os.path.isfile(arg):
        raise argparse.ArgumentTypeError("Unable to locate the file %s" % arg)

    return arg


def is_valid_new_filepath(arg: str) -> str:
    head, tail = os.path.split(arg)
    if head and not os.path.exists(head):
        raise argparse.ArgumentTypeError("Directory %s does not exist" % head)
    if not is_valid_filename(tail):
        raise argparse.ArgumentTypeError("%s is not a valid filename" % tail)

    return arg


def is_valid_directory(arg: str) -> str:
    if not is_valid_path(arg) or not os.path.isdir(arg):
        raise argparse.ArgumentTypeError("Unable to locate the directory %s" % arg)

    return arg


def is_positive_non_zero_int(arg: str) -> int:
    try:
        arg_num = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Value must be an integer larger than zero. The provided value was %s" % arg)

    if arg_num <= 0:
        raise argparse.ArgumentTypeError("Value must be an integer larger than zero. The provided value was %d" % arg_num)

    return arg_num


_parser = ArgumentParser(prog='Genetic Artist',
                         description='Recreate any image by painting strokes into a canvas by means of a genetic algorithm',
                         epilog='Bottom text')

_parser.add_argument('-t', '--target', dest='TARGET_IMG_FILE', required=True, help='Target image path', type=is_valid_file)
_parser.add_argument('-s', '--strokes', dest='STROKE_IMG_DIR', required=True, help='Stroke directory path', type=is_valid_directory)
_parser.add_argument('-c', '--config', dest='CONFIG_FILE', help='Config file path', type=is_valid_file)
_parser.add_argument('-i', '--iterations', dest='ITERATIONS', required=True, help='Number of strokes to draw', type=is_positive_non_zero_int)
_parser.add_argument('-o', '--output', dest='OUTPUT_FILE', required=True, help='Output image filename', type=is_valid_new_filepath)
_parser.add_argument('--canvas', dest='CANVAS_IMG_FILE', help='Canvas image the artist starts with', type=is_valid_file)
_parser.add_argument('-v', '--verbose', dest='VERBOSE', help='Print the proccess\'s progress', action='store_true')
_parser.add_argument('--nogui', dest='NO_GUI', help='Do not show the graphical interface', action='store_true')

ARGS = _parser.parse_args()
