
import sys
import os
#import test
from PyQt5.QtCore import (
    QCoreApplication, Qt, QSize, QMetaObject, QItemSelectionModel, QItemSelection, QSettings, QSignalMapper, QFile,
    QFileInfo, QVariant, QProcess, QT_VERSION_STR, PYQT_VERSION_STR, QPoint, pyqtSlot
)
from PyQt5.QtWidgets import (
    QMainWindow, QDialog, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit, QMessageBox, QDoubleSpinBox,
    QDialogButtonBox, QTextBrowser, QTreeView, QPushButton, QSplitter, QFrame, QTableWidgetItem, QSpacerItem, QAction,
    QGridLayout, QComboBox, QFileDialog, QGroupBox, QTableWidget, QTabWidget, QSizePolicy, QListView, QStackedLayout,
    QToolBar, QToolTip, QMenu, QMenuBar, QSpinBox, QStatusBar, QRadioButton, QAbstractScrollArea, QApplication,
    QAbstractItemView
)
from PyQt5.QtGui import (
    QIcon, QImage, QFont, QCursor, QKeySequence, QStandardItem, QStandardItemModel, QValidator, QDoubleValidator, QColor, QWheelEvent
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(750, 500)
        self.statusBar().showMessage('Ready', 5000)
        self.setWindowTitle("Map of Air Quality")
        self.setupUi()
        self.setLocationList()
    # Set up ui
    def setupUi(self):
        # Left - loading files and parameter setting
        groupBox_data = QGroupBox("\u3010Data\u3011")
        self.pushButton_load_satellite = QPushButton(QIcon('images/open.png'), "Open satellite data")
        self.pushButton_load_satellite.setIconSize(QSize(30, 30))
        self.pushButton_load_ground = QPushButton(QIcon('images/open.png'), "Open ground data")
        self.pushButton_load_ground.setIconSize(QSize(30, 30))
        verticalLayout_data = QVBoxLayout()
        verticalLayout_data.addWidget(self.pushButton_load_satellite)
        verticalLayout_data.addWidget(self.pushButton_load_ground)
        groupBox_data.setLayout(verticalLayout_data)

        groupBox_time = QGroupBox("\u3010Date/Time\u3011")
        label_time_step = QLabel("Time step: ")
        self.radioButton_hour = QRadioButton("Hour")
        self.radioButton_day = QRadioButton("Day")
        self.radioButton_month = QRadioButton("Month")
        self.radioButton_day.setChecked(True)
        horizontalLayout_time_step = QHBoxLayout()
        horizontalLayout_time_step.addWidget(self.radioButton_hour)
        horizontalLayout_time_step.addWidget(self.radioButton_day)
        horizontalLayout_time_step.addWidget(self.radioButton_month)
        self.comboBox_date = QComboBox()
        self.comboBox_time = QComboBox()
        verticalLayout_time = QVBoxLayout()
        verticalLayout_time.addWidget(label_time_step)
        verticalLayout_time.addLayout(horizontalLayout_time_step)
        verticalLayout_time.addWidget(self.comboBox_date)
        verticalLayout_time.addWidget(self.comboBox_time)
        groupBox_time.setLayout(verticalLayout_time)

        label_location = QLabel("Display of Locations")
        label_location.setAlignment(Qt.AlignCenter)
        self.listView_locations = QListView()
        self.listView_locations.setEditTriggers(QListView.NoEditTriggers)

        verticalLayout_left = QVBoxLayout()
        verticalLayout_left.addWidget(groupBox_data)
        verticalLayout_left.addWidget(groupBox_time)
        verticalLayout_left.addWidget(label_location)
        verticalLayout_left.addWidget(self.listView_locations)
        verticalLayout_left.addStretch(1)

        frame_left = QFrame()
        frame_left.setFrameStyle(QFrame.StyledPanel)
        frame_left.setLayout(verticalLayout_left)

        # Right - map
        self.plotWidget = QWidget()

        frame_right = QFrame()
        frame_right.setFrameStyle(QFrame.StyledPanel)
        verticalLayout_right = QVBoxLayout()
        verticalLayout_right.addWidget(self.plotWidget)
        frame_right.setLayout(verticalLayout_right)

        # Total layout
        splitter_central = QSplitter(Qt.Horizontal)
        splitter_central.addWidget(frame_left)
        splitter_central.addWidget(frame_right)
        splitter_central.setSizes([250, 750])
        horizontalLayout_window = QHBoxLayout()
        horizontalLayout_window.addWidget(splitter_central)

        self.central_widget = QWidget()
        self.central_widget.setLayout(horizontalLayout_window)
        self.setCentralWidget(self.central_widget)

    # Load locations into list view
    def setLocationList(self):
        self.model = QStandardItemModel(self.listView_locations)
        all = QStandardItem("All locations")
        all.setCheckable(True)
        all.setCheckState(2)
        self.model.appendRow(all)
        self.listView_locations.setModel(self.model)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    #mainwindow.gridPlotWidget.widget_list[0][0].canvas.mapPlot(test.genAllData(), title="2019/10/19 AQI")
    app.exec_()
