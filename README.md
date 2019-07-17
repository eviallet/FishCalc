# FishCalc

This small calculator (<1MB) comes with a custom interpreter that :
- highlight functions, keywords, constants and parenthesis while typing
- allow to use variables
- allow to save or load scripts
- handle conversions (for now, ```rad``` and ```deg```)
- handle logic tests
- give the user helpful error messages

The scanner and parser are fully elaborated on the  online book [Crafting Interpreters](https://craftinginterpreters.com/) by [Bob Nystrom](https://github.com/munificent), but made easier (classes and scopes are not really required for a calculator)

The UI is built with PyQt5.

<img src="Capture.PNG" height="432" width="602">

<img src="Capture2.PNG" height="432" width="602">


# Usage

Simply type in an expression for it to evaluate. You can also :
- ```load``` a script in any text format. Newline ends the statements.
- mute the result of an expression with ```;```
- use the built in constants (```c```, ```kb```, ```h```, ```pi```...)
- use the built in functions (```cos```, ```log```, ```sqrt```...)
- use ```ans``` which is the last calculation result
- represent numbers as ```1e-3``` or ```10^3```
- convert an angle to degrees or radians : ```cos(pi) -> deg```


# Known bugs
- to highlight the text in real time, the terminal text is replaced on each key press; hence, the cursor can't be used properly → to fix an error at the start of an expression, you have to backspace your way to it
 
# TODO
- more conversion options (physical units...)
- ```save``` history and improve loaded scripts usage
