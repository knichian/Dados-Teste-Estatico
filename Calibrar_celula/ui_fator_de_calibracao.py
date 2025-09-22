# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'fator_de_calibracaoRXQvey.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(698, 717)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(32, 32, 32, 32)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.frame_1 = QFrame(self.frame_2)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Shadow.Sunken)
        self.verticalLayout_2 = QVBoxLayout(self.frame_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.frame_1)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QFrame.Shape.NoFrame)
        self.label_2.setFrameShadow(QFrame.Shadow.Raised)
        self.label_2.setTextFormat(Qt.TextFormat.PlainText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame = QFrame(self.frame_1)
        self.frame.setObjectName(u"frame")
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setReadOnly(False)

        self.horizontalLayout_2.addWidget(self.lineEdit, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)


        self.verticalLayout_2.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout_4.addWidget(self.frame_1, 0, Qt.AlignmentFlag.AlignHCenter)

        self.verticalSpacer = QSpacerItem(614, 68, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.groupBox_4 = QGroupBox(self.frame_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dispositivoSerialComboBox = QComboBox(self.groupBox_4)
        self.dispositivoSerialComboBox.setObjectName(u"dispositivoSerialComboBox")

        self.horizontalLayout_3.addWidget(self.dispositivoSerialComboBox)

        self.pushButton_4 = QPushButton(self.groupBox_4)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_3.addWidget(self.pushButton_4)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(self.frame_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.groupBox_2.setFlat(False)
        self.formLayout = QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.lineEdit_3 = QLineEdit(self.groupBox_2)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit_3)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_4)

        self.espaOEntreAmostrasLabel = QLabel(self.groupBox_2)
        self.espaOEntreAmostrasLabel.setObjectName(u"espaOEntreAmostrasLabel")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.espaOEntreAmostrasLabel)

        self.espaOEntreAmostrasLineEdit = QLineEdit(self.groupBox_2)
        self.espaOEntreAmostrasLineEdit.setObjectName(u"espaOEntreAmostrasLineEdit")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.espaOEntreAmostrasLineEdit)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.frame_3)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame_3)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout_4.addWidget(self.frame_3, 0, Qt.AlignmentFlag.AlignHCenter)


        self.verticalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
#if QT_CONFIG(shortcut)
        self.label_2.setBuddy(self.lineEdit)
        self.label.setBuddy(self.lineEdit_3)
        self.label_3.setBuddy(self.lineEdit_4)
        self.espaOEntreAmostrasLabel.setBuddy(self.espaOEntreAmostrasLineEdit)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEdit, self.pushButton_3)
        QWidget.setTabOrder(self.pushButton_3, self.dispositivoSerialComboBox)
        QWidget.setTabOrder(self.dispositivoSerialComboBox, self.pushButton_4)
        QWidget.setTabOrder(self.pushButton_4, self.lineEdit_3)
        QWidget.setTabOrder(self.lineEdit_3, self.lineEdit_4)
        QWidget.setTabOrder(self.lineEdit_4, self.pushButton)
        QWidget.setTabOrder(self.pushButton, self.pushButton_2)

        self.retranslateUi(MainWindow)
        self.pushButton_3.clicked.connect(self.lineEdit.selectAll)
        self.pushButton_3.clicked.connect(self.lineEdit.copy)
        self.pushButton_2.clicked.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fator de Calibra\u00e7\u00e3o", None))
        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Vazio", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Copiar", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Dispositivo Serial: ", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Atualizar", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Ajustes: ", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Quantidade de Amostras: ", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Peso Real: ", None))
        self.espaOEntreAmostrasLabel.setText(QCoreApplication.translate("MainWindow", u"Espa\u00e7o entre Amostras", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Calcular", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Fechar", None))
    # retranslateUi

