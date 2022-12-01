# Level 3 Computer Science GUI Project
Project for YR13 computer science where I replicate Conway's game of life.

## Dependancies
Customtkinter:
```
pip install customtkinter
```
Pillow:
```
pip install pillow
```
Pathlib:
```
pip install pathlib
```

## 'settings.json' guide
"max_columns" - Interger value of the maximum number of columns <br />
"max_rows" - Interger value of the maximum number of rows <br />
"desired_width" - Sets the width of the program to % of screenwidth <br />
"seed" - For a random seed; 'from_random' or 'random' will work, otherwise enter the name of the file where the seed is stored <br />
"primary_color" - The background color and most border colors <br />
"secondary_color" - The background color and most border colors <br />
"tertiary_color" - The background color and most border colors <br />
"alive_color" - The background color and most border colors <br />

## Seed formatting
Seeds are stored in csv files, and must contain 1's and 0's.
Example:
```
0,0,1
1,0,1
0,1,1
```
This seed will generate some console messages informing you that the seed will have rows and columns added as it is too small. But it is still a valid seed that will be accepted by the program as it contain's 1's and 0's in a csv type format.

## Version checklist (progress tracker)
### v0.00
- [x] Created a working and reliable game engine
- [x] Created a save function, with seed readability

### v0.10
- [x] Created console tests
- [x] Easy to generate/enter seeds
- [x] Basic grid displaying CGOL (Conway's game of life)

### v0.50
- [x] Created manipulatable grid (draw mode)
- [x] Easy to generate/enter seeds
- [x] Basic grid displaying CGOL (Conway's game of life)

### v0.55
- [x] Created basic GUI (shoved everything all together)

### v0.90
- [x] Created GUI according to mockups (cancelled due to feedback)
- [x] Full functional GUI

### v1.00
- [x] Optimised code
- [x] Made code more readable
- [x] Correct code formatting
- [x] Made sure code is efficent