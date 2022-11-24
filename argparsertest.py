import os.path
from argparse import ArgumentParser

def is_valid_path(arg: str) -> bool:
    return os.path.exists(arg)

def is_valid_file(parser: ArgumentParser, arg: str):
    if not is_valid_path(arg) or not os.path.isfile(arg):
        parser.error("Unable to locate the file %s" % arg)
    return arg

def is_valid_directory(parser: ArgumentParser, arg: str):
    if not is_valid_path(arg) or not os.path.isdir(arg):
        parser.error("Unable to locate the directory %s" % arg)
    return arg

parser = ArgumentParser(
                    prog = 'Genetic Artist',
                    description = 'Replicate target image by drawing the specified strokes',
                    epilog = 'Text at the bottom of help')

parser.add_argument('TARGET_IMG_FILE', help='Filename of image to replicate', type=lambda x: is_valid_file(parser, x))
parser.add_argument('STROKE_IMG_DIR', help='Directory in which the strokes are stored', type=lambda x: is_valid_directory(parser, x))
parser.add_argument('--canvas', dest='CANVAS_IMG_FILE', type=lambda x: is_valid_file(parser, x))
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()

print("Target image: " + args.TARGET_IMG_FILE)
print("Stroke directory: " + args.STROKE_IMG_DIR)
if args.CANVAS_IMG_FILE:
    print("Canvas image: " + args.CANVAS_IMG_FILE)

