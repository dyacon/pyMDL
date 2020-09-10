'''
pymdl package setup
'''

import setuptools

setuptools.setup(
    name="pymdl",
    version="0.3",
    author="Chris Cox",
    author_email="chrisrycx@gmail.com",
    description="Python code for Dyacon MDL-700",
    url="https://github.com/dyacon/pyMDL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pyyaml'],
    python_requires='>=3.6'
)