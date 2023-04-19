#!/usr/bin/env python
# release 0.9 from 2023-04-19

from copy import deepcopy
from sys import exit
import pygame
import time
import random
import numpy as np
import tkinter
import tkinter.filedialog


pygame.init()

# maps position to which square - used in visual support function
aloc =[[1,1,1,2,2,2,3,3,3],
       [1,1,1,2,2,2,3,3,3],
       [1,1,1,2,2,2,3,3,3],
       [4,4,4,5,5,5,6,6,6],
       [4,4,4,5,5,5,6,6,6],
       [4,4,4,5,5,5,6,6,6],
       [7,7,7,8,8,8,9,9,9],
       [7,7,7,8,8,8,9,9,9],
       [7,7,7,8,8,8,9,9,9]]

def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

def save_board(board,fname):
    with open(fname, 'w') as f:
        for line in board:
            lin = ''   
            for pos in line:
                lin = lin + str(pos) 
            f.write(lin)
            f.write('\n')    

def print_board(board):
    '''Prints the board'''
    boardString = ""
    for i in range(9):
        for j in range(9):
            boardString += str(board[i][j]) + " "
            if (j+1)%3 == 0 and j != 0 and (j+1) != 9:
                boardString += "| "
            if j == 8:
                boardString += "\n"
            if j == 8 and (i+1)%3 == 0 and (i+1) != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)

def find_empty (board):
    '''Finds an empty cell and returns its position as a tuple'''
    for i in range (9):
        for j in range (9):
            if board[i][j] == 0:
                return i,j

def valid(board, pos, num):
    '''Whether a number is valid in that cell, returns a bool'''
    for i in range(9):
        if board[i][pos[1]] == num and (i, pos[1]) != pos:  #make sure it isn't the same number we're checking for by comparing coords
            return False
    for j in range(9):
        if board[pos[0]][j] == num and (pos[0], j) != pos:  #Same row but not same number
            return False
    start_i = pos[0] - pos[0] % 3 #ex. 5-5%3 = 3 and thats where the grid starts
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):  #adds i and j as needed to go from start of grid to where we need to be
            if board[start_i + i][start_j + j] == num and (start_i + i, start_j + j) != pos:
                return False
    return True

def solve(board):
    '''Solves the Sudoku board via the backtracking algorithm'''
    empty = find_empty(board)
    if not empty: #no empty spots are left so the board is solved
        return True
    for nums in range(9):
        if valid(board, empty,nums+1):
            board[empty[0]][empty[1]] = nums+1
            if solve(board): #recursive step
                return True
            board[empty[0]][empty[1]] = 0 #this number is wrong so we set it back to 0
    return False

def get0(board):
    ''' returns all 0-positions in random tuple-list'''
    zero = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                zero.append((i,j))    
    if len(zero) > 1:
        random.shuffle(zero)
    return(zero)
    
def testsol(board,loc):
    ''' returns a list of possible values for valid solution at a given position'''
    sol=[]
    for t in range(1,10):
        test = deepcopy(board)
        if valid(test,loc,t):
            test[loc[0]][loc[1]] = t
            if solve(test) != False:
                sol.append(t)
    return sol     

def improve(board):
    ''' tests at all 0-positions, if there is more than one posible number for a valid solution'''
    ''' if yes, one of the multiple solutions is writen to the position'''
    improved = False
    zeros = get0(board)
    if len(zeros) > 0:
        for zerotest in zeros:
            tested = testsol(board,zerotest)
            if len(tested) > 1:
                random.shuffle(tested)
                board[zerotest[0]][zerotest[1]] = tested[0]
                #print(str(zerotest)+' imp > '+str(tested[0]))
                improved = True
                break
    return improved

def gen_square():
    # base-square 
    base = np.arange(1,10)
    np.random.shuffle(base)
    basemat = base.reshape(3,3)
    return basemat

def generate():
    diff = 28 # pre-filled tiles will be 27 - probably mor tha one solution possible  
    if uni == True:
        diff = 30 # lower diff will increase generation duration remarkably 
    # empty board (9x9, -> 9 3x3 squares)
    board = np.zeros((9,9),dtype='int')
    # put random filled squares in 1,5 and 9
    sq1 = gen_square()
    sq2 = gen_square()
    sq3 = gen_square()
    for j in range(0,3):
        for i in range(0,3):
            board[i][j] = sq1[i][j]   
    for j in range(3,6):
        for i in range(3,6):
            board[i][j] = sq2[i-3][j-3]        
    for j in range(6,9):
        for i in range(6,9):
            board[i][j] = sq3[i-6][j-6]
    
    # generate random sequence for filling the rest
    fill = np.arange(1,10)
    np.random.shuffle(fill)  
    # set square indices as tuples to test !! use upacking-parameter '*' for use in range
    indis = [[(0,3),(3,6)],
             [(0,3),(6,9)],
             [(3,6),(0,3)],
             [(3,6),(6,9)],
             [(6,9),(0,3)],
             [(6,9),(3,6)]]
    for item in fill:
        for indi in indis:
            placed = False
            for j in range(*indi[0]):
                if item not in board[:,j]: 
                    for i in range(*indi[1]):
                        if item not in board[i]:
                            test = deepcopy(board)
                            if test[i][j] == 0:
                                test[i][j] = item
                                if solve(test) == True:
                                    board[i][j] = item
                                    placed = True     
                            if placed == True:
                                break                
                    if placed == True:
                        break
    with open('solved.txt', 'w') as f:
        for line in board:
            lin = ''   
            for pos in line:
                lin = lin + str(pos) 
            f.write(lin)
            f.write('\n')    
    li = np.arange(1,10)
    np.random.shuffle(li)
    co = np.arange(1,10)
    np.random.shuffle(co)
    finished = False
    while finished == False:
        li = np.arange(0,9)
        np.random.shuffle(li)
        co = np.arange(0,9)
        np.random.shuffle(co)
        board[li[4]][co[5]] = 0    
        if np.count_nonzero(board) < diff:
            finished = True   
    elapsed = time.time() - startTime
    # print(elapsed)
    
    # make it unique
    if uni == True:
        unique = False
        while unique == False:
            test = improve(board)          
            if test == False:
                unique = True          
                elapsed = time.time() - startTime
                # print(elapsed)
    return board
             
class Board:
    '''A sudoku board made out of Tiles'''
    def __init__(self, window):       
        if lfile == True:
            sudofile = prompt_file()
            self.board = np.genfromtxt(sudofile,delimiter=1, dtype='int')  
        else:
            self.board = generate()    
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        self.tiles = [[Tile(self.board[i][j], window, i*60, j*60) for j in range(9)] for i in range(9)]
        self.window = window
        save_board(self.board,'generated.txt')
            
    def draw_board(self):
        '''Fills the board with Tiles and renders their values'''
        for i in range(9):
            for j in range(9):
                if j%3 == 0 and j != 0: #vertical lines
                    pygame.draw.line(self.window, (200, 200, 200), ((j//3)*180, 0), ((j//3)*180, 540), 4)

                if i%3 == 0 and i != 0: #horizontal lines
                    pygame.draw.line(self.window, (200, 200, 200), (0, (i//3)*180), (540, (i//3)*180), 4)

                self.tiles[i][j].draw((200,200,200), 1)

                if self.tiles[i][j].value != 0: #don't draw 0s on the grid
                    self.tiles[i][j].display(self.tiles[i][j].value, (21+(j*60), (11+(i*60))), (0, 0, 0))  #20,5 are the coordinates of the first tile
        #bottom-most line
        pygame.draw.line(self.window, (0, 0, 0), (0, ((i+1) // 3) * 180), (540, ((i+1) // 3) * 180), 4)

    def deselect(self, tile, row, col, val):
        '''Deselects every tile except the one currently clicked'''
        global missing
        avals=[1,2,3,4,5,6,7,8,9]
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].selected = False
                self.tiles[i][j].asoc = False
                self.tiles[i][j].same = False
                if val > 0:
                    if val == self.tiles[i][j].value:
                        self.tiles[i][j].same = True 
                else:
                    if j == row:
                        self.tiles[i][j].asoc = True
                    if i == col:
                        self.tiles[i][j].asoc = True
                    if aloc[i][j] == aloc[col][row]:
                        self.tiles[i][j].asoc = True
                if self.tiles[i][j].asoc == True:   
                    try:
                        avals.remove(self.tiles[i][j].value)
                    except:
                        pass    
        self.tiles[row][col].selected = True
        if val == 0:
            # print(avals)
            missing = avals
        else:
            missing=[]                    
                            
    def redraw(self, keys, wrong, time):
        '''Redraws board with highlighted tiles'''
        self.window.fill((255,255,255))
        self.draw_board()
        for i in range(9):
            for j in range(9):
                if self.tiles[j][i].selected:  #draws the border on selected tiles
                    self.tiles[j][i].draw((50, 205, 50), 3)

                elif self.tiles[i][j].correct:
                    self.tiles[j][i].draw((34, 139, 34), 3)

                elif self.tiles[i][j].incorrect:
                    self.tiles[j][i].draw((255, 0, 0), 3)
                    
                elif self.tiles[i][j].same and visual == True:
                    self.tiles[j][i].draw((0, 128, 255), 3) 
                
                elif self.tiles[i][j].asoc and visual == True:
                    self.tiles[j][i].draw((250, 200, 100), 3) 

        if len(keys) != 0: #draws inputs that the user places on board but not their final value on that tile
            for value in keys:
                self.tiles[value[0]][value[1]].display(keys[value], (21+(value[0]*60), (16+(value[1]*60))), (128, 128, 128))

        if len(missing) > 0 and visual == True:
            font = pygame.font.SysFont('comicsans', 24) #Missing values
            text = font.render(str(missing), True, (0, 0, 0))
            self.window.blit(text, (86, 548))
        
        if wrong > 0:
            font = pygame.font.SysFont('comicsans', 30) #Red X
            text = font.render('X:  ', True, (255, 0, 0))
            self.window.blit(text, (10, 542))

            font = pygame.font.SysFont('comicsans', 30) #Number of Incorrect Inputs
            text = font.render(str(wrong), True, (255, 0, 0))
            self.window.blit(text, (42, 542))

        font = pygame.font.SysFont('comicsans', 30) #Time Display
        text = font.render(str(time), True, (0, 0, 0))
        self.window.blit(text, (388, 542))
        pygame.display.flip()

    def visualSolve(self, wrong, time):
        '''Showcases how the board is solved via backtracking'''
        for event in pygame.event.get(): #so that touching anything doesn't freeze the screen
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0],empty[1]), nums+1):
                self.board[empty[0]][empty[1]] = nums+1
                self.tiles[empty[0]][empty[1]].value = nums+1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(63) #show tiles at a slower rate
                self.redraw({}, wrong, time)

                if self.visualSolve(wrong, time):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(63)
                self.redraw({}, wrong, time)

    def hint(self, keys):
        '''Shows a random empty tile's solved value as a hint'''
        while True: #keeps generating i,j coords until it finds a valid random spot
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.board[i][j] == 0: #hint spot has to be empty
                if (j,i) in keys:
                    del keys[(j,i)]
                self.board[i][j] = self.solvedBoard[i][j]
                self.tiles[i][j].value = self.solvedBoard[i][j]
                return True

            elif np.array_equal(self.board,self.solvedBoard):
                return False
                
class Tile:
    '''Represents each white tile/box on the grid'''
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60) #dimensions for the rectangle
        self.surf = pygame.Surface((self.rect.w,self.rect.h))
        self.selected = False
        self.correct = False
        self.incorrect = False
        self.same = False
        self.asoc = False

    def draw(self, color, thickness):
        '''Draws a tile on the board'''
        pygame.draw.rect(self.window, color, self.rect, thickness) 

    def display(self, value, position, color):
        '''Displays a number on that tile'''
        #font = pygame.font.SysFont('lato', 45)
        font = pygame.font.SysFont('comicsans', 32)
        text = font.render(str(value), True, color)
        self.window.blit(text, position)

    def clicked(self, mousePos):
        '''Checks if a tile has been clicked'''
        if self.rect.collidepoint(mousePos): #checks if a point is inside a rect
            self.selected = True
        return self.selected

def main():
    '''Runs the main Sudoku GUI/Game'''
    #initiliaze values and variables
    global visual
    wrong = 0
    board = Board(screen)
    selected = -1,-1 #NoneType error when selected = None, easier to just format as a tuple whose value will never be used
    keyDict = {}
    running = True
    startTime = time.time()
    
    while running:
        elapsed = time.time() - startTime
        passedTime = time.strftime("%H:%M:%S", time.gmtime(elapsed))
 
        if np.array_equal(board.board,board.solvedBoard):    #user has solved the board
            for i in range(9):
                for j in range(9):
                    board.tiles[i][j].selected = False
                    board.tiles[i][j].asoc = False
                    board.tiles[i][j].same = False
                    # finishing works
                    running = False
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #exit() #so that it doesnt go to the outer run loop
                running = False

            elif event.type == pygame.MOUSEBUTTONUP: #allow clicks only while the board hasn't been solved
                mousePos = pygame.mouse.get_pos()
                for i in range(9):
                    for j in range (9):
                        if board.tiles[i][j].clicked(mousePos):
                            selected = i,j
                            selrow = i
                            selcol = j
                            selval = board.tiles[j][i].value
                            board.deselect(board.tiles[i][j],selrow,selcol,selval) #deselects every tile except the one currently clicked
                            
            elif event.type == pygame.KEYDOWN:
                if board.board[selected[1]][selected[0]] == 0 and selected != (-1,-1):
                    if event.key == pygame.K_1:
                        keyDict[selected] = 1

                    if event.key == pygame.K_2:
                        keyDict[selected] = 2

                    if event.key == pygame.K_3:
                        keyDict[selected] = 3

                    if event.key == pygame.K_4:
                        keyDict[selected] = 4

                    if event.key == pygame.K_5:
                        keyDict[selected] = 5

                    if event.key == pygame.K_6:
                        keyDict[selected] = 6

                    if event.key == pygame.K_7:
                        keyDict[selected] = 7

                    if event.key == pygame.K_8:
                        keyDict[selected] = 8

                    if event.key == pygame.K_9:
                        keyDict[selected] = 9

                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:  # clears tile out
                        if selected in keyDict:
                            board.tiles[selected[1]][selected[0]].value = 0
                            del keyDict[selected]

                    elif event.key == pygame.K_RETURN:
                        if selected in keyDict:
                            if keyDict[selected] != board.solvedBoard[selected[1]][selected[0]]: #clear tile when incorrect value is inputted
                                wrong += 1
                                board.tiles[selected[1]][selected[0]].value = 0
                                del keyDict[selected]
                                break
                            #valid and correct entry into cell
                            board.tiles[selected[1]][selected[0]].value = keyDict[selected] #assigns current grid value
                            board.board[selected[1]][selected[0]] = keyDict[selected] #assigns to actual board so that the correct value can't be modified
                            del keyDict[selected]

                if event.key == pygame.K_h:
                    board.hint(keyDict)
                
                if event.key == pygame.K_s:
                    save_board(board.board,'current.txt')
                    
                if event.key == pygame.K_v:    # toggle the boolean visual
                    visual ^= True

                if event.key == pygame.K_SPACE:
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                    keyDict = {}  #clear keyDict out
                    board.visualSolve(wrong, passedTime)
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False #reset tiles
                    running = False
                    
        board.redraw(keyDict, wrong, passedTime)
        
    screen.fill((255, 255, 255))  # clear screen 

# this is the outer loop with the menu.png file
# could be replaced with various GUI's with buttons etc. 
missing = []
visual = True
uni = True
lfile = False
startTime = time.time()
pygame.display.set_caption("Sudoku - single solution board ")
screen = pygame.display.set_mode((540, 590))
imp = pygame.image.load("menu.png").convert()
menu = True
while menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                uni = True
                lfile = False
                main()
            if event.key == pygame.K_n:
                uni = False
                lfile = False
                main()        
            if event.key == pygame.K_l:
                uni = false
                lfile = True
                main()
                                     
    screen.blit(imp, (0, 0))
    pygame.display.flip()
pygame.quit()