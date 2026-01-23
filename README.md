# wordle-solver

**wordle-solver** is a solver/helper program for *The New York Times* *Wordle* game, written in Python.

## Requirements

#### Python Version
- Python 3.9+

#### Packages:
- opencv-python
- Pillow
- numpy
- customtkinter
- CTkToolTip
- CTkMessagebox

## Installation 
```
git clone https://github.com/amerm12/wordle-solver.git
python -m venv
pip install opencv-python pillow numpy customtkinter CTkToolTip CTkMessagebox
python main.py
```

## About 
**wordle-solver** isn't intended to be used as a standalone solver, but as a helper to the user. Image can be uploaded to the program, or screenshot can be taken directly from the program. Based on the image, program will return 3 best next guesses. Guesses are ranked by letter frequency in English language. It only uses list of 2315 words *(as of 23.01.2026.)* that can be valid Wordle answers. It does not use the full list of ~12,960 typable words. Works on both light and dark mode. 

## Performance
It has been tested in 100 games, and has win percentage of 98%, meaning that it successfully solved 98 out of 100 games. Tests have been conducted in a way that only first offered word from list was used every time. Testing was done on [Wordle Unlimited](https://wordleunlimited.org) (Wordle copy).

![Game Statistics](gameStats.png)
>**_Note:_** Current Streak and Max Streak stats should be ignored since they are always showing 1.

## License
This project is licensed under the MIT License.