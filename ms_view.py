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
        self.puzzle1.setAlignment(Qt.AlignLeft)
        self.puzzle1.setGeometry(QRect(100, 100, 100, 100))
        box.addWidget(self.puzzle1)
        self.puzzle2 = QLabel("Ho")
        self.puzzle2.setGeometry(QRect(100, 100, 100, 100))
        self.puzzle2.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.puzzle2.setAlignment(Qt.AlignRight)
        self.puzzle2.setGeometry(QRect(100, 100, 100, 100))
        box.addWidget(self.puzzle2)
        layout = QVBoxLayout()
        box.addLayout(layout)
        grid = QGridLayout()
        self.buttons = []
        for i in range(100):
            button = QPushButton()
            button.clicked.connect(self.buttonClicked)
            self.buttons.append(button)
            button.setText('hi')
            # button.setText(button.label)
            row = i // 10 # integer division by # of columns to get the row
            col = i % 10  # remainder when divided by # of cols gives us a column
            grid.addWidget(self.buttons[i], row, col) # note we set the location
            button.setProperty("myRow", row)
            button.setProperty("myCol", col)
        layout.addLayout(grid)
        widget.setLayout(box)
        self.model = msModel()
        self.newGame()

    def newGame(self):
        print("Start a new game!")
        for button in self.buttons:
            button.setEnabled(True)
        self.model.newGame()

    def buttonClicked(self):
        # sender() tells us who caused the action to take place
        clicked = self.sender()
        row = clicked.property("myRow")
        col = clicked.property("myCol")
        x = self.model.reveal(row, col)
        x = str(x)
        print(x)
        clicked.setText(x)
        clicked.setEnabled(False)
        print(self.model.clicked)
        state = self.model.getState(x, self.model.clicked)
        if state == -1:
            self.puzzle1.setText("BOOM")
            self.end()
        if state == 1:
            self.puzzle1.setText("WINNER")
            self.end()

    def end(self):                          # ends game, works
        for i in range(100):
            self.buttons[i].click()

    def hello(self):
        print("bob")


# whsat about this
