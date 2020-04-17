from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ms_model import *
import sys
import os


class MSWindow(QMainWindow):
    def __init__(self):
        super(MSWindow, self).__init__()
        elapsedTimer = QElapsedTimer()
        timer = QTimer()
        timer.timeout.connect(self.showTime)
        self.eTimer = elapsedTimer
        self.timer = timer                          # adds timer functionality
        widget = QWidget()
        self.setCentralWidget(widget)
        box = QHBoxLayout()
        self.numBombs = QLabel("")
        self.numBombs.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.numBombs.setAlignment(Qt.AlignCenter)
        box.addWidget(self.numBombs)
        self.time = QLabel("00:00:00")
        self.time.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.time.setAlignment(Qt.AlignCenter)
        box.addWidget(self.time)
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
            row = i // j  # dynamically uses bomb count to build rows
            col = i % j  # same but for cols
            grid.addWidget(self.buttons[i], row, col)
            button.setProperty("myRow", row)
            button.setProperty("myCol", col)
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(0)
        layout.addLayout(grid)
        widget.setLayout(layout)
        self.model = msModel()
        self.newGame(j)
        menu = self.menuBar()
        gameMenu = menu.addMenu("&Game")
        newAct = QAction("&New", self, shortcut=QKeySequence.New, triggered=self.redo)
        gameMenu.addAction(newAct)

    def newGame(self, i):
        for button in self.buttons:
            button.setEnabled(True)
            button.setText('')
        self.model.newGame(i)
        x = self.model.bombs
        y = str(x)
        self.numBombs.setText(y)
        self.numBombs.repaint()

    def buttonClicked(self):
        # sender() tells us who caused the action to take place
        if self.model.clicked == 1 or self.model.clicked == 0:
            self.timer.start(1000)
            self.eTimer.start()
            self.showTime()             # starts timer on first click
        clicked = self.sender()
        row = clicked.property("myRow")
        col = clicked.property("myCol")
        x = self.model.reveal(row, col)
        y = str(x)
        clicked.setText(y)
        clicked.setEnabled(False)
        clicked.hide()
        clicked.show()                  # hide//show used to force button update
        if x == 0:                      # used to cascade on getting 0
            if row != 0 and row != self.model.bombs - 1:
                if col != 0 and col != self.model.bombs - 1:
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 2):
                            self.buttons[i * self.model.bombs + j].click()
                elif col == 0:
                    for i in range(row - 1, row + 2):
                        for j in range(col, col + 2):
                            self.buttons[i * self.model.bombs + j].click()
                elif col == self.model.bombs - 1:
                    for i in range(row - 1, row + 2):
                        for j in range(col - 1, col + 1):
                            self.buttons[i * self.model.bombs + j].click()
            elif row == 0:
                if col == 0:
                    for i in range(row, row + 2):
                        for j in range(col, col + 2):
                            self.buttons[i * self.model.bombs + j].click()
                elif col == self.model.bombs - 1:
                    for i in range(row, row + 2):
                        for j in range(col - 1, col + 1):
                            self.buttons[i * self.model.bombs + j].click()
                else:
                    for i in range(row, row + 2):
                        for j in range(col - 1, col + 2):
                            self.buttons[i * self.model.bombs + j].click()
            elif row == self.model.bombs - 1:
                if col == 0:
                    for i in range(row - 1, row + 1):
                        for j in range(col, col + 2):
                            self.buttons[i * self.model.bombs + j].click()
                elif col == self.model.bombs - 1:
                    for i in range(row - 1, row + 1):
                        for j in range(col - 1, col + 1):
                            self.buttons[i * self.model.bombs + j].click()
                else:
                    for i in range(row - 1, row + 1):
                        for j in range(col - 1, col + 2):
                            self.buttons[i * self.model.bombs + j].click()
        state = self.model.getState(x, self.model.clicked)
        if state == -1:
            self.end(state, self.model.bombs)
        if state == 1:
            self.end(state, self.model.bombs)

    def end(self, state, j):
        for i in range(j * j):
            self.buttons[i].click()
        if state == -1:
            self.numBombs.setText("BOOM")
            self.numBombs.repaint()
            self.timer.start(100000000)             # stops timer
        if state == 1:
            self.numBombs.setText("WINNER")
            self.numBombs.repaint()
            self.timer.start(100000000)             # stops timer

    def redo(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)         # used to restart app on newgame

    def showTime(self):
        startTime = QTime(0, 0, 0)
        # setTime = QTime.currentTime()
        # holdTime = setTime
        currentTime = startTime.addSecs(self.eTimer.elapsed()/1000)   # used to calc time
        displayTxt = currentTime.toString('hh:mm:ss')
        self.time.setText(displayTxt)