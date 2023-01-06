<h1 align='center'>
    Genetic Artist
</h1>

<h4 align='center'>
    Automagically redraw any image into a painting by means of artificial evolution.
</h4>

<p align="center">
    <a href="#key-features">Key Features</a> •
    <a href="#how-to-use">How To Use</a> •
    <a href="#dependencies">Dependencies</a> •
    <a href="#license">License</a>
</p>

<!-- Add progress gif here :) -->

##  Key Features

* **Recreate any image through genetic algorithms**: _Genetic Artist_ uses genetic algorithms to recreate images by painting brushstrokes, resulting in unique and stunning artwork.
* **Customize the stroke library for any art style**: You can provide a folder of stroke images for the program to use. Experiment with known art styles or create your own unique mixes.
* **Don't start on a blank canvas**: The starting canvas image can be customized to help the artist recreate the image faster or experiment with the output.
* **Watch the creative process in action**: A window opens by default, allowing you to watch the artist at work and see the progress brushstroke by brushstroke.
* **Free and open-source!**: Every part of the _Genetic Artist_ is accessible for you to experiment and tinker with. Don't be shy and contribute all you want!
* **Run on any platform**: _Genetic Artist_ is cross-platform and easy to run on any machine, whether it be Windows, macOS or Linux.

## How To Use

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
python src/main.py --target <Target Image> --strokes <Stroke Directory> --iterations <Number of Strokes To Draw> --output <Ouptut Image>
```

## Dependencies

This project wouldn't be possible without the following open source packages:

* **[PyGAD](https://pygad.readthedocs.io/en/latest/)** to power the image recreation process in our program.
* **[OpenCV](https://opencv.org/)** and **[Numpy](https://numpy.org/)** to handle the image processing and manipulation tasks.
* **[Numba](https://numba.pydata.org/)** to accelerate the custom image processing functions.

## License

_Genetic Artist_ is distributed under the MIT License. See `LICENSE.txt` for more information.