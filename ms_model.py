# put in rules of MS
# store system state
import random


class msModel:
    def __init__(self):
        self.newGame(1)

    def newGame(self, bombs):
        clicked = 0
        cols = bombs
        rows = bombs
        bombs = bombs
        grid = [[0] * (rows) for i in range(cols)]
        self.puzzle = grid
        self.clicked = clicked
        self.bombs = bombs
        bombCount = rows
        bomb = '*'
        for x in range(0, rows):
            y = random.randrange(rows)
            z = random.randrange(cols)
            if grid[y][z] != bomb:
                grid[y][z] = bomb
            else:
                x = x - 1                   # sets bombs in grid
        for x in range(0, rows):
            for y in range(0, cols):
                if grid[x][y] != '*':       # if not bomb
                    if x == 0:              # if in first row
                        if y == 0:          # if in first col
                            if grid[0][1] == '*':
                                grid[x][y] += 1
                            if grid[1][0] == '*':
                                grid[x][y] += 1
                            if grid[1][1] == '*':
                                grid[x][y] += 1
                        elif y == cols - 1:
                            for q in range(x, x + 2):
                                for z in range(y - 1, y + 1):
                                    if grid[q][z] == '*':
                                        grid[x][y] += 1
                        else:
                            for q in range(x, x + 2):
                                for z in range(y - 1, y + 2):
                                    if grid[q][z] == '*':
                                        grid[x][y] += 1
                    elif x == rows - 1:
                        if y == 0:          # if in first col
                            if grid[rows - 2][0] == '*':
                                grid[x][y] += 1
                            if grid[rows - 2][1] == '*':
                                grid[x][y] += 1
                            if grid[rows - 1][1] == '*':
                                grid[x][y] += 1
                        elif y == cols - 1:
                            if grid[rows - 2][cols - 1] == '*':
                                grid[x][y] += 1
                            if grid[rows - 2][cols - 2] == '*':
                                grid[x][y] += 1
                            if grid[rows - 1][cols - 2] == '*':
                                grid[x][y] += 1
                        else:
                            for q in range(x - 1, x + 1):
                                for z in range(y - 1, y + 2):
                                    if grid[q][z] == '*':
                                        grid[x][y] += 1
                    else:
                        for q in range(x - 1, x + 2):
                            if y != 0 and y != cols - 1:
                                for z in range(y - 1, y + 2):
                                    if grid[q][z] == '*':
                                        grid[x][y] += 1
                            elif y == cols - 1:
                                for z in range(y - 1, y + 1):
                                    if grid[q][z] == '*':
                                        grid[x][y] += 1
                            else:
                                for z in range(y, y + 2):
                                    if grid[q][z] == '*':
                                        grid[x][y] += 1
        for x in range(0, bombs):
            print(grid[x])

    def reveal(self, row, col):
        self.clicked += 1
        return self.puzzle[row][col]

    #def getMoveCount(self):
        # returns the number of moves made

    def getState(self, value, clicked):
        # -1 -- loss
        #  0 -- in progress
        #  1 -- win
        if (100 - self.clicked) == self.bombs:
            return 1
        elif value == "*":
            return -1
        return 0
