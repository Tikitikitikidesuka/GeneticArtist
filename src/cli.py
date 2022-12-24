import os
from argparse import ArgumentParser, Namespace


def is_valid_path(arg: str) -> bool:
    return os.path.exists(arg)


def is_valid_file(parser: ArgumentParser, arg: str) -> str:
    if not is_valid_path(arg) or not os.path.isfile(arg):
        parser.error("Unable to locate the file %s" % arg)
    return arg


def is_valid_directory(parser: ArgumentParser, arg: str) -> str:
    if not is_valid_path(arg) or not os.path.isdir(arg):
        parser.error("Unable to locate the directory %s" % arg)
    return arg


def is_positive_int_no_zero(parser: ArgumentParser, arg: int) -> int:
    if arg <= 0:
        parser.error("Value must be larger than zero. The provided value was %d" % arg)


_parser = ArgumentParser(prog='Genetic Artist',
                         description='Replicate an image by painting the given strokes',
                         epilog='Bottom text')

_parser.add_argument('TARGET_IMG_FILE', help='Target image path', type=lambda x: is_valid_file(_parser, x))
_parser.add_argument('STROKE_IMG_DIR', help='Stroke directory path', type=lambda x: is_valid_directory(_parser, x))
_parser.add_argument('GENETIC_ARTIST_CONFIG_FILE', help='Config file path', type=lambda x: is_valid_file(_parser, x))
_parser.add_argument('--canvas', dest='CANVAS_IMG_FILE', type=lambda x: is_valid_file(_parser, x))
_parser.add_argument('-i', '--strokenum', dest='STROKE_NUM', type=lambda x: is_positive_int_no_zero(_parser, x))
_parser.add_argument('-v', '--verbose', action='store_true')

ARGS = _parser.parse_args()
