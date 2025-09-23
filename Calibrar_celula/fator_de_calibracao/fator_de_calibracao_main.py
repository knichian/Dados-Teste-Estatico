from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)

from fator_de_calibracao_cli import *
from ui_fator_de_calibracao import Ui_MainWindow

import sys


def extend_ui(ui):

    def update_port_list():
        ports = list_ports()
        ui.dispositivoSerialComboBox.clear()
        ui.dispositivoSerialComboBox.addItems(['dummy-data-4', 'dummy-data-5', 'dummy-data-6',]) # TODO: remove later
        ui.dispositivoSerialComboBox.addItems(ports)

    ports = list_ports()
    ui.dispositivoSerialComboBox.addItems(['dummy-data-1', 'dummy-data-2', 'dummy-data-3',]) # TODO: remove later
    ui.dispositivoSerialComboBox.addItems(ports)
    
    ui.pushButton_4.clicked.connect(update_port_list)
    

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(window)
    extend_ui(ui)

    window.show()
    app.exec()
