from PyQt5.QtWidgets import QApplication
from ms_view import *

# This is the main application, all it does is set up a Qt application,
# tell it to show our HangmanWindow, and then let Qt take over

app = QApplication([])
window = MSWindow()
window.show()
app.exec_()



