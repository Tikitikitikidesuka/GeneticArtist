<h1 align="center">
    Genetic Artist
</h1>

<h4 align="center">
    Automagically redraw any image into a painting by means of artificial evolution.
</h4>

<p align="center">
    <a href="#key-features">Key Features</a> •
    <a href="#how-to-use">How to Use</a> •
    <a href="#try-it-out">Try it Out!</a> •
    <a href="#acknowledgements">Acknowledgements</a> •
    <a href="#license">License</a>
</p>

##  Key Features

* **Recreate any image through genetic algorithms**: _Genetic Artist_ uses genetic algorithms to recreate images by painting brushstrokes, resulting in unique and stunning artwork.
* **Customize the stroke library for any art style**: You can provide a folder of stroke images for the program to use. Experiment with known art styles or create your own unique mixes.
* **Don't start on a blank canvas**: The starting canvas image can be customized to help the artist recreate the image faster or experiment with the output.
* **Watch the creative process in action**: A window opens by default, allowing you to watch the artist at work and see the progress brushstroke by brushstroke.
* **Free and open-source!**: Every part of the _Genetic Artist_ is accessible for you to experiment and tinker with. Don't be shy and contribute all you want!
* **Run on any platform**: _Genetic Artist_ is cross-platform and easy to run on any machine, whether it be Windows, macOS or Linux.

## How to Use

To run this program you will need [Python 3](https://www.python.org/) with [pip](https://pypi.org/project/pip/) installed.

1. Clone this repository or [download](https://github.com/Tikitikitikidesuka/GeneticArtist/archive/refs/heads/main.zip) it instead:

```shell
git clone https://github.com/Tikitikitikidesuka/GeneticArtist.git
```

2. Go into the repository directory:

 ```shell
 cd GeneticArtist
 ```

3. Install the project's dependencies:

```shell
pip install -r requirements.txt
```

4. Run the artist:

```shell
python src/main.py --target <Target Image> \
                   --strokes <Stroke Directory> \
                   --config <Config File> \
                   --iterations <Number of Strokes To Draw> \
                   --output <Ouptut Image>
```


To hide the preview window add `--nogui` to the parameters.
In case you do want it, remember to press ESC when the program finishes to close it.

To get a detailed output of what the program is doing add `--verbose` to the parameters.

> :gear: **The GUI is still a prototype and will be changed shortly**

## Try it Out!

Ready to see the magic happen? Check out some examples of what you can create with _Genetic Artist_.

Example strokes, target images, and canvases are provided in the repository, so you can try out the program right away.
Here are a few examples to get you started:

### Night Sky

To create a painting of the night sky, navigate to the project folder and run the following command:

```shell
python src/main.py --target examples/targets/moon.jpg \
                   --strokes examples/strokes/ \
                   --canvas examples/canvases/white.jpg \
                   --config examples/configs/medium_quality.toml \
                   --iterations 256 \
                   --output outputs/my_moon256.png \
                   --verbose
```

This will produce a beautiful painting like the one shown below:

<p align="center">
    <img src="examples/outputs/moon0256.png" />
</p>

### Lake Landscape

If you prefer a peaceful lake landscape, run this command instead:

```shell
python src/main.py --target examples/targets/lake.jpg \
                   --strokes examples/strokes/ \
                   --canvas examples/canvases/black.jpg \
                   --config examples/configs/high_quality.toml \
                   --iterations 256 \
                   --output outputs/my_lake256.png \
                   --verbose
```

The result will look something like this:

<p align="center">
    <img src="examples/outputs/lake0256.png" />
</p>

Feel free to experiment with different target images, strokes, and canvases to see what unique creations you can come up with!

## Acknowledgements

This project wouldn't be possible without the following open source packages:

* **[PyGAD](https://pygad.readthedocs.io/en/latest/)** to power the image recreation process in our program.
* **[OpenCV](https://opencv.org/)** and **[Numpy](https://numpy.org/)** to handle the image processing and manipulation tasks.
* **[Numba](https://numba.pydata.org/)** to accelerate the custom image processing functions.

The example images are provided by [Pixabay](https://pixabay.com/):

* ***lake.jpg*** image by <a href="https://pixabay.com/users/jplenio-7645255/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=7644166">Joe</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=7644166">Pixabay</a>
* ***moon.jpg*** image by <a href="https://pixabay.com/users/kienvirak-11003985/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4855256">kien virak</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4855256">Pixabay</a>

## License

_Genetic Artist_ is distributed under the MIT License. See [`LICENSE.md`](https://github.com/Tikitikitikidesuka/GeneticArtist/blob/168171a1d6d329c7f488cee31380a57f945ed343/LICENSE.md) for more information.
