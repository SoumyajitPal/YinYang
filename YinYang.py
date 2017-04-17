# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ImageLoad.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import FileDialog
import ImDiffMod
import cv2
import ImDiff

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 389)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 310, 361, 31))
        self.textEdit.setObjectName("textEdit")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 310, 75, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.openFile)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 310, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.showDiff)
        self.pushButton_2.setEnabled(False)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(535, 310, 81, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.hideDiff)
        self.pushButton_3.setEnabled(False)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.label.setObjectName("label")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(350, 0, 0, 0))
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 532, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.fileOptions = FileDialog.App()

        self.safeFiles = []
    
    def ShowImage(self, im1, im2):

        im1 = cv2.resize(im1, dsize=None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        im2 = cv2.resize(im2, dsize=None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # image = QtGui.QImage(fileName)
        # if image.isNull():
        #     QtWidgets.QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
        #     return

        height, width, channels = im2.shape
        # height, width = im2.shape
        # print(im2.shape)
        bytesPerLine = 3*width
        try:
            qImg1 = QtGui.QImage(im1.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            # qImg2 = QtGui.QImage(im2.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            qImg3 = QtGui.QImage(im2.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        except TypeError:
            return
        print('Images converted')

        leftPixelMap = QtGui.QPixmap(qImg1)
        # rightPixelMap = QtGui.QPixmap(qImg2)
        diffPixelMap = QtGui.QPixmap(qImg3)

        print('PixelMaps drawn')

        self.label.setPixmap(leftPixelMap)
        self.label.resize(leftPixelMap.width(), leftPixelMap.height())
        self.label.show()

        # self.label_2.setPixmap(rightPixelMap)
        # self.label_2.resize(rightPixelMap.width(), rightPixelMap.height())
        # self.label_2.show()

        self.label_3.setPixmap(diffPixelMap)
        self.label_3.resize(diffPixelMap.width(), diffPixelMap.height())
        self.label_3.show()

    def openFile(self):
        fileName = self.fileOptions.openFileNameDialog()

        print('Opened')
        if fileName:
            self.safeFiles.append(fileName)
            self.im1, self.im2 = ImDiffMod.PrcessImage(fileName)
            # cv2.imwrite('CutUpImage1.png', self.im1)
            # cv2.imwrite('CutUpImage2.png', self.im2)
            self.ShowImage(self.im1, self.im2)
            
        self.scaleFactor = 1.0
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
    
    def showDiff(self):
        print('Showing differences')
        temp1 = self.im1.copy()
        temp2 = self.im2.copy()
        imP, imN = ImDiff.imDiff(temp1, temp2)
        # cv2.imwrite('Differences1.png', imP)
        # cv2.imwrite('Differences2.png', imN)
        self.ShowImage(imP, imN)
    
    def hideDiff(self):
        print('Hiding differences')
        self.ShowImage(self.im1, self.im2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Browse"))
        self.pushButton_2.setText(_translate("MainWindow", "Show"))
        self.pushButton_3.setText(_translate("MainWindow", "Hide"))
        self.label.setText(_translate("MainWindow", "Image A"))
        self.label_3.setText(_translate("MainWindow", "Image C"))

def SaveFile(files):
    with open('SafeFiles.txt', 'w') as f:
        for name in files:
            f.write(str(name).join('\n'))
    f.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ret = app.exec_()
    # print('Saving safe files')
    # SaveFile(ui.safeFiles)
    sys.exit(ret)
