# Overview

Simple command-line application which concatenates a list of photos into a single photo
showing them in a matrix (in other words, a grid). 

# Installation

First of all, you need [Python](https://www.python.org/) 3.7 or greater installed in your system.
Then, as `photomatrix` is a command line application, open a terminal and be ready to type commands.

## Install automatically with pip

`photomatrix` is available from the Python Package Index ([PyPI](https://pypi.org/)) so installable
with [pip](https://pip.pypa.io/):

```
pip3 install photomatrix
```

You should now have `photomatrix` available in your shell. For example, print the command help:

```
photomatrix -h
```

## Build locally

Clone this project from Github.
Cd into the root folder.

Create a virtual environment (e.g. named `my_env`) and activate it:

```
python3 -m venv my_venv
source my_venv/bin/activate
```

Install the dev dependencies and the app dependencies into the virtual environment:

```
pip3 install -r requirements_dev.txt
pip3 install -e .
```

Run like this:

```
python3 -m photomatrix -h
```

# Usage

The basic usage is:

```
photomatrix INPUT_IMAGES OUTPUT_IMAGE
```

where all the images found in the specified input path will be loaded, sorted, combined in a matrix
and the resulting image will be written in the specified output path.  

Further options that you can customize are:
* Number of rows vs columns
* Resize and crop
* Sorting
* Border
* Text to print (e.g. filename or Exif original date)

See the command help for more info on these options.

# Examples

The following examples use these test input images:

![](./data/input/01.jpg | width=200)
![](./data/input/02.jpg | width=200)

until

![](./data/input/12.jpg | width=200)

## Matrix with border

To build a matrix with a simple border:

```
photomatrix "data/input/*.jpg" data/output/matrix_border.jpg --border-width-ratio 0.1
```

resulting in:

![](./data/output/matrix_border.jpg | width=600)
