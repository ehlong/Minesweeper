from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ms_model import *


# build UI for MS



# 1. Create a QVBoxLayout
# 2. Add to it a QHBoxLayout containing two QLabels
# 3. Add the QGridLayout to the QVBoxLayout
class MSWindow(QMainWindow):
    def __init__(self):
        super(MSWindow, self).__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        box = QHBoxLayout()
        self.puzzle1 = QLabel("Hi")
        self.puzzle1.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.puzzle1.setAlignment(Qt.AlignCenter)
        box.addWidget(self.puzzle1)
        self.puzzle2 = QLabel("Ho")
        self.puzzle2.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.puzzle2.setAlignment(Qt.AlignCenter)
        box.addWidget(self.puzzle2)
        layout = QVBoxLayout()
        layout.addLayout(box)
        grid = QGridLayout()
        self.buttons = []
        j, pressed = QInputDialog.getInt(self, "Size Selector", "Number of Bombs:", 10, 5, 20, 1)
        for i in range(j * j):
            button = QPushButton()
            button.clicked.connect(self.buttonClicked)
            self.buttons.append(button)
            button.setText('')
            button.setFixedWidth(35)
            row = i // j # integer division by # of columns to get the row
            col = i % j  # remainder when divided by # of cols gives us a column
            grid.addWidget(self.buttons[i], row, col) # note we set the location
            button.setProperty("myRow", row)
            button.setProperty("myCol", col)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        layout.addLayout(grid)
        widget.setLayout(layout)
        self.model = msModel()
        self.newGame(j)
        menu = self.menuBar().addMenu("&Game")
        newAct = QAction("&New", self, shortcut=QKeySequence.New, triggered=self.newGame)
        menu.addAction(newAct)
        menu.addSeparator()
        quitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit, triggered=self.close)
        menu.addAction(quitAct)

    def newGame(self, i):
        print("Start a new game!")
        for button in self.buttons:
            button.setEnabled(True)
            button.setText('')
        self.model.newGame(i)
        x = self.model.bombs
        y = str(x)
        self.puzzle1.setText(y)
        self.puzzle1.repaint()

    def buttonClicked(self):
        # sender() tells us who caused the action to take place
        clicked = self.sender()
        row = clicked.property("myRow")
        col = clicked.property("myCol")
        x = self.model.reveal(row, col)
        y = str(x)
        print(y)
        clicked.setText(y)
        clicked.setEnabled(False)
        clicked.repaint()
        print(self.model.clicked)
        if x == 0:
            if row != 0 and row != self.model.bombs - 1:
                if col != 0 and col != self.model.bombs - 1:
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 2):
                            self.buttons[i*10 + j].click()
                elif col == 0:
                    for i in range(row - 1, row + 2):
                        for j in range(col, col + 2):
                            self.buttons[i * 10 + j].click()
                elif col == self.model.bombs - 1:
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 1):
                            self.buttons[i * 10 + j].click()
            elif row == 0:
                if col == 0:
                    for i in range(row, row + 2):
                        for j in range(col, col + 2):
                            self.buttons[i * 10 + j].click()
                elif col == self.model.bombs - 1:
                    for i in range(row, row + 2):
                        for j in range(col - 1, col + 1):
                            self.buttons[i * 10 + j].click()
                else:
                    for i in range(row, row + 2):
                        for j in range(col - 1, col + 2):
                            self.buttons[i * 10 + j].click()
            elif row == self.model.bombs - 1:
                if col == 0:
                    for i in range(row - 1, row + 1):
                        for j in range(col, col + 2):
                            self.buttons[i * 10 + j].click()
                elif col == self.model.bombs - 1:
                    for i in range(row - 1, row + 1):
                        for j in range(col - 1, col + 1):
                            self.buttons[i * 10 + j].click()
                else:
                    for i in range(row - 1, row + 1):
                        for j in range(col - 1, col + 2):
                            self.buttons[i * 10 + j].click()
        state = self.model.getState(x, self.model.clicked)
        if state == -1:
            self.end(state, self.model.bombs)
        if state == 1:
            self.end(state, self.model.bombs)

    def end(self, state, j):                          # ends game, works
        for i in range(j * j):
            self.buttons[i].click()
        if state == -1:
            self.puzzle1.setText("BOOM")
            self.puzzle1.repaint()
        if state == 1:
            self.puzzle1.setText("WINNER")
            self.puzzle1.repaint()
