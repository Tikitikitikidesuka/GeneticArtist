import os.path
from argparse import ArgumentParser

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    return arg

parser = ArgumentParser(
                    prog = 'Genetic Artist',
                    description = 'Replicate target image by drawing the specified strokes',
                    epilog = 'Text at the bottom of help')

parser.add_argument('target_img_file', help='Filename of image to replicate', type=lambda x: is_valid_file(parser, x))
parser.add_argument('stroke_img_dir', help='Directory in which the strokes are stored')
parser.add_argument('--canvas', dest='canvas_img_file')
parser.add_argument('-v', '--verbose', action='store_true')

args = parser.parse_args()
print("Target image: " + args.target_img_file)
print("Stroke directory: " + args.stroke_img_dir)
print("Canvas image: " + args.canvas_img_file)

