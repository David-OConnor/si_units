import setuptools

with open('README.rst') as f:
    readme = f.read()

setuptools.setup(
    name="siunits",
    version="0.0.1",

    author="David O'Connor",
    author_email="david.alan.oconnor@gmail.com",
    url='https://github.com/David-OConnor/si_units',
    description="Perform operations on SI units",
    long_description=readme,
    license="MIT",
    keywords="SI, units",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
)