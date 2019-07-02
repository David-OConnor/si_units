# https://packaging.python.org/tutorials/packaging-projects/

import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name="si_units",
    version="0.0.2",
    author="David O'Connor",
    author_email="david.alan.oconnor@gmail.com",
    description="Perform operations on SI units",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/David-OConnor/si_units',
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    keywords="SI, units, dimensional analysis",
)