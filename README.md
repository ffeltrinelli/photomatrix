# Overview

Simple command-line Python application which concatenates a list of photos into a single photo which
shows them in a matrix. 

# How to build and run

Cd into the root folder.

Create a virtual environment and activate it:

```
python3 -m venv my_venv
source my_venv/bin/activate
```

Install the dev dependencies and the app dependencies into the virtual environment:

```
pip install -r requirements_dev.txt
pip install -e .
```

Run the app like this:

```
python -m photomatrix "data/input/*.jpg" data/matrix.jpg
```


