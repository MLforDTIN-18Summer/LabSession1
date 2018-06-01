from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTextEdit
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QImage
from PyQt4.QtGui import QColor
import cv2
from sklearn.externals import joblib

import pickle
import matplotlib.pyplot as plt
import numpy as np

import sys

class ScribbleArea(QtGui.QWidget):

		def __init__(self, parent=None):
				super(ScribbleArea, self).__init__(parent)

				"""
				Indicates that the widget contents are north-west aligned and static. On resize, 
				such a widget will receive paint events only for parts of itself that are newly visible. 
				This flag is set or cleared by the widget’s author. 
				"""
				self.setAttribute(QtCore.Qt.WA_StaticContents)
				self.modified = False
				self.scribbling = False
				self.myPenWidth = 10
				self.myPenColor = QtCore.Qt.black
				imageSize = QtCore.QSize(700, 500)
				self.image = QImage(imageSize, QtGui.QImage.Format_RGB32)
				self.lastPoint = QtCore.QPoint()

		def clearImage(self):
				self.image.fill(QtGui.qRgb(255, 255, 255))
				self.modified = True
				self.update()

		def mousePressEvent(self, QMouseEvent):
				if QMouseEvent.button() == QtCore.Qt.LeftButton:
						self.lastPoint = QMouseEvent.pos()
						self.scribbling = True

		def mouseMoveEvent(self, event):
				if (event.buttons() & QtCore.Qt.LeftButton) and self.scribbling:
						self.drawLineTo(event.pos())

		def mouseReleaseEvent(self, event):
				if event.button() == QtCore.Qt.LeftButton and self.scribbling:
						self.drawLineTo(event.pos())

		def paintEvent(self, QPaintEvent):
				painter = QtGui.QPainter(self)
				painter.drawImage(QPaintEvent.rect(), self.image)

		def drawLineTo(self, endPoint):
				painter = QtGui.QPainter(self.image)
				painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
						QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
				painter.drawLine(self.lastPoint, endPoint)
				self.modified = True

				# rad = self.myPenWidth / 2 + 2
				# self.update(QtCore.QRect(self.lastPoint, endPoint).normalized().adjusted(-rad, -rad, +rad, +rad))
				self.update()
				self.lastPoint = QtCore.QPoint(endPoint)

		def isModified(self):
				return self.modified

		def print_(self):
				printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)

				printDialog = QtGui.QPrintDialog(printer, self)
				if printDialog.exec_() == QtGui.QDialog.Accepted:
						painter = QtGui.QPainter(printer)
						rect = painter.viewport()
						size = self.image.size()
						size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
						painter.setViewPort(rect.x(), rect.y(), size.width(), size.height())
						painter.setWindow(self.image)
						painter.drawImage(0, 0, self.image)
						painter.end()

		def penColor(self):
				return self.myPenColor

		def penWidth(self):
				return self.myPenWidth

class PredictionArea(QtGui.QWidget):

		def __init__(self, parent=None):
				super(PredictionArea, self).__init__(parent)
				self.textBox = QTextEdit(self)
				self.textBox.resize(700, 50)
				self.textBox.setReadOnly(True)

		def predictionDisplay(self, textToDisplay=None):
				# self.textBox.textCursor().setHtml("<b>{}</b>".format(textToDisplay))
				self.textBox.setHtml("<b>{}</b>".format(textToDisplay))


class MainWindow(QtGui.QMainWindow):
		def __init__(self):
				super(MainWindow, self).__init__()

				self.resize(700, 650)

				self.scribbleArea = ScribbleArea(self)
				self.scribbleArea.clearImage()

				self.scribbleArea.move(0, 0)
				self.scribbleArea.resize(700, 500)

				button = QPushButton('Predict', self)
				button.clicked.connect(self.predictNumber)
				button.move(300, 520)
				button.resize(100, 50)

				self.predictionArea = PredictionArea(self)
				self.predictionArea.move(0, 600)
				self.predictionArea.resize(700, 50)


				self.createActions()
				self.createMenus()

				self.setWindowTitle("Scribble")


		def createActions(self):

				# self.predictAct = QtGui.QAction("&Predict", self,
				#                                 shortcut="Alt+Shift+F10", triggered=self.predictNumber)

				self.clearScreenAct = QtGui.QAction("&Clear Screen", self,
																						shortcut="Ctrl+L", triggered=self.scribbleArea.clearImage)
				self.printAct = QtGui.QAction("&Print...", self,
																			triggered=self.scribbleArea.print_)

		def createMenus(self):
				optionMenu = QtGui.QMenu("&Options", self)
				optionMenu.addAction(self.clearScreenAct)

				self.menuBar().addMenu(optionMenu)

		def predictNumber(self):
				inputImage = self.scribbleArea.image
				tmp_image_path = ".~tmpImage.png"
				inputImage.save("{}".format(tmp_image_path))
				inputImage = cv2.imread("{}".format(tmp_image_path))
				inputImage = cv2.cvtColor(inputImage, cv2.COLOR_RGB2GRAY)
				######## for later ###################
				# for x in range(0, inputImage.width()):
				#     for y in range(0, inputImage.height()):
				#         c = inputImage.pixel(x, y)
				#         colors = QColor(c).getRgbF()
				#         print(colors)

				row, col = inputImage.shape

				npImage = cv2.imread("{}".format(tmp_image_path))

				min_non_zero_pixel = [col, row]
				max_non_zero_pixel = [0, 0]

				for x in range(row):
						for y in range(col):
								if inputImage[x, y] == 0:
										if y < min_non_zero_pixel[0]:
												min_non_zero_pixel[0] = y

										if y > max_non_zero_pixel[0]:
												max_non_zero_pixel[0] = y

										if x < min_non_zero_pixel[1]:
												min_non_zero_pixel[1] = x

										if x > max_non_zero_pixel[1]:
												max_non_zero_pixel[1] = x

				w_bottleneck = max_non_zero_pixel[1] - min_non_zero_pixel[1]
				h_bottleneck = max_non_zero_pixel[0] - min_non_zero_pixel[0]

				bottleneck = w_bottleneck if w_bottleneck > h_bottleneck else h_bottleneck
				bottleneck //= 2
				bottleneck += 20

				center = [(max_non_zero_pixel[0] + min_non_zero_pixel[0])//2, (max_non_zero_pixel[1] + min_non_zero_pixel[1])//2]

				min_non_zero_pixel = [center[0] - bottleneck if center[0] - bottleneck > 0 else 0 ,center[1] - bottleneck if center[1] - bottleneck else 0]
				max_non_zero_pixel = [center[0] + bottleneck if center[0] + bottleneck < col else col ,center[1] + bottleneck if center[1] + bottleneck < row else row]	

				roi = inputImage[min_non_zero_pixel[1]:max_non_zero_pixel[1], \
							min_non_zero_pixel[0]:max_non_zero_pixel[0]]

				subImage = np.reshape(cv2.resize(np.invert(roi), (28, 28)), (-1, 784))

				logisticModel = joblib.load("../model/logistic_model.pk")
				svmModel = joblib.load("../model/svm_model.pk")
				knnModel = joblib.load("../model/knn_model.pk")

				prediction = {
												"logistic_result":logisticModel.predict(subImage)[0], \
												"svm_result":svmModel.predict(subImage)[0], \
												"knn_result":knnModel.predict(subImage)[0]
										 }
				print("Logistic Model : {}\nSVM Model : {}\nKNN Model : {}".format(prediction.get("logistic_result"), prediction.get("svm_result"), prediction.get("knn_result")))

				self.predictionArea.predictionDisplay(textToDisplay="Logistic Model : {}\nSVM Model : {}\nKNN Model : {}".format(prediction.get("logistic_result"), prediction.get("svm_result"), prediction.get("knn_result")))

if __name__=="__main__":
		import sys

		app = QtGui.QApplication(sys.argv)
		window = MainWindow()
		window.show()
		sys.exit(app.exec_())