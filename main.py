from PyQt5.QtWidgets import QApplication
from views import MainView
import sys

app = QApplication(sys.argv)
main_view = MainView()

sys.exit(app.exec_())
