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

from fator_de_calibracao_cli import get_calibration_factor, list_ports, get_samples, Receiver
from ui_fator_de_calibracao import Ui_MainWindow

import sys

def extend_ui(ui):

    dummy_elements = False
    global com
    com = None

    def update_port_list():
        ports = list_ports()
        ui.cbox_seriais.clear()
        ui.cbox_seriais.addItems(['dummy-data-4', 'dummy-data-5', 'dummy-data-6',]) if dummy_elements else None 
        ui.cbox_seriais.addItems(ports)

    def get_samples_with_progress(com: Receiver, n_samples: int = 100):

        print("get_sample_with_progress()") if dummy_elements else None 
        samples = []
        sample_count = 0

        while(com.check_connection() and sample_count < n_samples):

            # ui.display_status.text()
            response = int(com.read_response())
            samples.append(response)
            sample_count+=1
            print(f"Sample {sample_count}: {response}")
            ui.progressBar.value = int(float(sample_count/n_samples)*100)

        return samples

    def connect_esp():

        port = str(ui.cbox_seriais.currentText())
        print(f"{port=}")
        global com
        com = Receiver(port)
        print(f"{com=}")
        com.send_command(b'INIT CONFIG\n')
        ui.display_status.setText('Conectado')

    def send_factor():
        print(f"{com=}")
        com.send_command(b'SET LOAD FACTOR ' + bytes(str(ui.line_edit_fator.text()).encode()) + b'\n')    
        i = 0
        while i < 10:
           print(com.read_response()) 
           i+=1

    def calculate_factor():
        print(f"{com=}")

        if com == None:
            return -1

        samples = get_samples_with_progress(com)
        expected_weight = ui.lineEdit_4.text()

        if expected_weight == '':
            return -1

        calibration_factor = get_calibration_factor(samples, float(expected_weight))

        ui.line_edit_fator.setText(str(calibration_factor))

    ports = list_ports()
    ui.cbox_seriais.addItems(['dummy-data-1', 'dummy-data-2', 'dummy-data-3',]) if dummy_elements else None 
    ui.cbox_seriais.addItems(ports)
    
    ui.btn_atualizar.clicked.connect(update_port_list)
    ui.btn_calcular.clicked.connect(calculate_factor)
    ui.btn_conectar.clicked.connect(connect_esp)
    ui.btn_enviar.clicked.connect(send_factor)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(window)
    extend_ui(ui)

    window.show()
    app.exec()
