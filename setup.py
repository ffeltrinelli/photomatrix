import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="photomatrix",
    version="0.0.2",
    author="Francesco Feltrinelli",
    description="Concat photos together in a matrix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ffeltrinelli/photomatrix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.7',
    install_requires=[
        'pillow>=7'
    ],
    entry_points={
        "console_scripts": [
            "photomatrix = photomatrix.__main__:main",
        ]
    }
)
