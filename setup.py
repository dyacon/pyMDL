'''
pymdl package setup
'''

import setuptools

setuptools.setup(
    name="pymdl",
    version="2.0",
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
    python_requires='>=3.6',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mdldisplay=pymdl.display:run'
        ]
    }
)