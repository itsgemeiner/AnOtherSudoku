# AnOtherSudoku
Phyton Code using PyGame for GUI
I have reviewed several projects and compiled a working python code, which reflects those functions, which i feel usefull when dealing with sudoku boards.
Most code examples showed problems with the generation of boards. Some quick codes produce insufficient probability distribution, other codes showed excessive runtime-bandwidths. I implemented a generator, which quickly fills 3 diagonal squares and does the rest with random walk - trial and error. 
An other challenge is the uniqueness of solutions. I tested a compromise, where a board with 29 filled tiles is checked with random walk and tiles with more than one valid number entries are filled with one of these numbers, so the result is a board with 30 to 35 solved tiles, which is is a medium challenge to resolve. Execution time usually is raesonable.
Helper-functions are included too. The visual helper function makes a big difference in solving effort, therfore the user can switch it on/off with single keystroke.
For the outer loop, i do a very minimalistic approach. Handling instructions are based on a 540x590 pixel png-file, which can be easily created with any preferred image-software and commands are single keyboard keys.
For more flexibility there is also an option for geneating a 27 tile board without uniqueness-chek and an option to load a board from a textfile. 
Remark: As the code checks the board against an fully solved board an not against a solver-function, all boards with more than one possible solution will give you probably more errors than against a solver-function.

Any remarks on improvement issues or errors in the code are welcome! 
