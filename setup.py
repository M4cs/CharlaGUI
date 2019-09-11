import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''
    
setuptools.setup(
    name="CharlaGUI",
    version="1.1",
    author="Max Bridgland",
    install_requires=[
        'PySimpleGUIQt>=0.26.0',
        'PySide2>=5.13.0',
        'psutil==5.6.2'
    ],
    author_email="mabridgland@protonmail.com",
    description="GUI for Charlatano and RatPoison CS:GO Cheat",
    long_description=readme(),
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': [
            'charlagui = charlagui.__main__:start'
        ]
    },
    keywords="csgo, steam, valve, charlatano, hack, gui. pysimplegui",
    url="https://github.com/M4cs/CharlaGUI",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ),
)
