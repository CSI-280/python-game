python-game
===========

## Overview
Info about the game, maybe add story context if we have any

## Installation

You'll need to install libtcod to run this project.

### On Windows (non virtual environment)

Run the following code in a command-line to install tcod on your computer
```
py -m pip install tcod
```

### PyCharm (virtual environment)

1. Upgrade pip using the command
```
python -m pip install --upgrade pip
```

2. Install tcod using the command
```
pip install tcod
```

If you need help, this tutorial from the library's page is very helpful and where I got the information on how to install it in the first place.

https://python-tcod.readthedocs.io/en/latest/installation.html

## Planned Features

1. Inventory management system

2. Room system, randomly generated as well as scripted for puzzles. Full navigation

3. Combat system

4. Beautiful groundbreaking ASCII art


## Contributors

Josh Bogin
Louis Vinton
Wes Beard
Kai Wilens ^_^
Ethan Trope   ¯\_(^_^)_/¯
Michaelangelo Leonardo Raphael Donatello
Noah Anderson
Steven Pershyn
Will Gesler

Puzzle Info File:
https://docs.google.com/document/d/1RTI1KXnnTR8Qo6oZBsA5HZLdGG-oU7rfZ9q67ya60f4/edit?usp=sharing

Map Generator:
https://azgaar.github.io/Fantasy-Map-Generator/
Load the .map file from the repo to make edits


## Design Guide
* Should follow classic Rogue style
* Only use extended ascii characters

 * There will be one location on the screen at a time,  
but it won't zoom in so rooms can be different sizes   
as long as they fit on the screen.

* Each location can be a single room or made up of many connected rooms   
but they should all be contained on the screen at one time.  

* The character is one char on the screen so the scale will always be the same

* Different screens like a menu or inventory can take up the whole screen  
and overlay onto the current location

* We could set aside room at the top and bottom for messages and players stats

## Art Key
Here you can put any of your ascii characters and what they correspond to  
[Extended ascii character list](https://www.redbubble.com/people/barnsis/journal/3570534-complete-ascii-list-of-symbols)

| Character     | Description |
|:-------------:|-------------|
|       ║       | A wall      |
|       ╬       | A door      |

## Keybindings
All controls can be put here for reference  

| Keybind       | Description |
|:-------------:|-------------|
|       W       | Move up     |
|       A       | Move left   |
|       S       | Move down   |
|       D       | Move right  |
