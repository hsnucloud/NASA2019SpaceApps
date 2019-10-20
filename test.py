import os, sys, traceback, platform, pkg_resources, logging, csv
import numpy as np
import xarray as xr
from anytree import AnyNode, RenderTree, search, LevelGroupOrderIter
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QGridLayout, QAction
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIcon, QStandardItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib import patches, rcParams
from shapely import geometry as sgeom
from cartopy import crs as ccrs
from cartopy.io import shapereader
from main_window import MainWindow

rcParams['agg.path.chunksize'] = 10000
LOG = logging.getLogger(__name__)
LOG = logging.getLogger(__name__)
mainwindow_ui_stream = pkg_resources.resource_stream(__name__, 'resource/ui/MainWindow.ui')
MainWindowFormClass, MainWindowBaseClass = loadUiType(mainwindow_ui_stream)


class PlotWidget(QWidget):
    def __init__(self, parent=None, statusbar=None):
        super().__init__(parent)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QHBoxLayout())
        self.statusbar = statusbar
        self.canvas = MyCanvas(parent=self)
        self.toolbar = MyToolbar(self.canvas, parent=self)
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        LOG.debug("Plot Widget OK")


class MyToolbar(NavigationToolbar):
    toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ['Home', 'Back', 'Forward', 'Pan', 'Zoom', 'Subplots', 'Save']]

    def __init__(self, canvas, parent):
        NavigationToolbar.__init__(self, canvas, parent, coordinates=False)
        self.setOrientation(Qt.Vertical)
        self.additional_action_list = []
        LOG.debug("Toolbar OK")


class MyCanvas(FigureCanvas):
    def __init__(self, parent, statusbar=None):
        self.fig = plt.Figure()
        self.fig.clear()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.statusbar = statusbar
        LOG.debug("Canvas OK")

    def updateView(self):
        for axes in self.fig.get_axes():
            axes.relim()
            axes.autoscale_view(True, True, True)
        self.fig.tight_layout()
        self.draw_idle()

    def mapPlot(self, dataset, title=""):
        axes = self.fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
        axes.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())
        axes.background_patch.set_visible(False)
        axes.outline_patch.set_visible(False)
        axes.set_title(title)

        shape = shapereader.natural_earth(resolution="110m", category="cultural", name="admin_1_states_provinces_lakes_shp")
        # shape = "C:\\Users\\Enoch\\Downloads\\gadm36_USA_shp\\gadm36_USA_1.shp"
        reader = shapereader.Reader(shape)
        axes.add_geometries(reader.geometries(), ccrs.PlateCarree(), facecolor="white", edgecolor="black")
        for data in dataset:
            axes.scatter(data[0], data[1], c=data[2], transform=ccrs.PlateCarree(), zorder=2)

        self.updateView()


class MyMainWindow(MainWindow):
    def __init__(self, parent=None):
        LOG.debug("initialize visualizer window")
        super().__init__()
        self.resize(750, 500)
        self.statusBar().showMessage('Ready', 5000)
        self.setWindowTitle("Map of Air Quality")
        self.setupUi()
        self.setLocationList()
        self.canvasWidget = PlotWidget(parent=self.plotWidget)
        layout = QGridLayout()
        layout.addWidget(self.canvasWidget)
        self.plotWidget.setLayout(layout)

        self.place_dict = {
            "Anaheim": (33.830585, -117.93851),
            "Glendora": (34.1439, -117.8508),
            "LaHabra": (33.92506, -117.95258),
            "LosAngeles": (34.0664, -118.227),
            "Reseda": (34.1992, -118.533),
            "SantaClarita": (34.3833, -118.528),
            "SouthLongBeach": (33.7922, -118.175),
        }
        self.time_tree = AnyNode(id="time_tree")
        self.search_dir = "C:\\Users\\Enoch\\Downloads\\Macth_Data"
        self.loadData()
        self.initSelection()

    def loadData(self):
        for root, dirs, files in os.walk(self.search_dir):
            for file in files:
                place = (file.split("2018_passData_")[-1]).split("_")[0]
                with open(os.path.join(self.search_dir, file), "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            date = row["Date"]
                            time_key = ["pm25"]
                            time = ["00:00:00"]
                        except:
                            date = row["YY-MM-DD"]
                            date = date[:4] + "-" + date[4:6] + "-" + date[6:8]
                            time_key = [" {:.1f}".format(t) for t in np.arange(0.5, 24.5, 1.0)]
                            time = ["{:02d}:30:00".format(i) for i in range(24)]

                        date_node = search.find_by_attr(self.time_tree, name="date", value=date, maxlevel=2)
                        if date_node is None:
                            date_node = AnyNode(parent=self.time_tree, date=date)
                        for t in zip(time, time_key):
                            time_node = search.find_by_attr(date_node, name="time", value=t[0], maxlevel=2)
                            if time_node is None:
                                try:
                                    pm25 = float(row[t[1]])
                                except:
                                    pm25 = None
                                time_node = AnyNode(parent=date_node, time=t[0])
                            place_node = search.find_by_attr(time_node, name="place", value=place, maxlevel=2)
                            if place_node is None:
                                place_node = AnyNode(parent=time_node, place=place, pm25=pm25, position=self.place_dict[place])
        LOG.debug(RenderTree(self.time_tree))
        with open("time_tree.txt", "w") as f:
            print(RenderTree(self.time_tree), file=f)

    def initSelection(self):
        self.date_idx = 0
        date_node_list = [node_list for node_list in LevelGroupOrderIter(node=self.time_tree, maxlevel=2)][-1]
        self.date_list = [node.date for node in date_node_list]
        self.comboBox_date.addItems(self.date_list)
        self.comboBox_date.setCurrentIndex(self.date_idx)

        self.time_idx = 0
        time_node_list = [node_list for node_list in LevelGroupOrderIter(node=date_node_list[self.date_idx], maxlevel=2)][-1]
        self.time_list = [node.time for node in time_node_list]
        self.comboBox_time.addItems(self.time_list)
        self.comboBox_time.setCurrentIndex(self.time_idx)

        self.place_idx_list = []
        place_node_list = [node_list for node_list in LevelGroupOrderIter(node=time_node_list[self.time_idx], maxlevel=2)][-1]
        self.place_list = [node.place for node in place_node_list]
        for p in self.place_list:
            p_item = QStandardItem(p)
            p_item.setCheckable(True)
            p_item.setCheckState(2)
            self.listView_locations.model().appendRow(p_item)


def dataLoader(file):
    data = np.loadtxt(file)
    return data


def genCOData():
    data = dataLoader("ref_co.dat")
    la, lo, idx = data[:, 0], data[:, 1], data[:, 2]
    color_list = ["#00e800", "#ffff00", "#ff7e00", "red", "#8f3f97", "#7e0023"]
    c = []
    for i in idx:
        if i < 4.5:
            c.append(color_list[0])
        elif i < 9.5:
            c.append(color_list[1])
        elif i < 12.5:
            c.append(color_list[2])
        elif i < 15.5:
            c.append(color_list[3])
        elif i < 30.5:
            c.append(color_list[4])
        else:
            c.append(color_list[5])
    return zip(lo, la, c)


def genNO2Data():
    data = dataLoader("ref_no2.dat")
    la, lo, idx = data[:, 0], data[:, 1], data[:, 2]
    color_list = ["#00e800", "#ffff00", "#ff7e00", "red", "#8f3f97", "#7e0023"]
    c = []
    for i in idx:
        if i < 54:
            c.append(color_list[0])
        elif i < 101:
            c.append(color_list[1])
        elif i < 361:
            c.append(color_list[2])
        elif i < 650:
            c.append(color_list[3])
        elif i < 1250:
            c.append(color_list[4])
        else:
            c.append(color_list[5])
    return zip(lo, la, c)


def genO3Data():
    data = dataLoader("ref_o3.dat")
    la, lo, idx = data[:, 0], data[:, 1], data[:, 2]
    color_list = ["#00e800", "#ffff00", "#ff7e00", "red", "#8f3f97", "#7e0023"]
    c = []
    for i in idx:
        if i < 0.055:
            c.append(color_list[0])
        elif i < 0.071:
            c.append(color_list[1])
        elif i < 0.086:
            c.append(color_list[2])
        elif i < 0.106:
            c.append(color_list[3])
        elif i < 0.201:
            c.append(color_list[4])
        else:
            c.append(color_list[5])
    return zip(lo, la, c)


def genAllData():
    data = dataLoader("all.dat")
    la, lo, idx = data[:, 0], data[:, 1], data[:, 2]
    color_list = ["#00e800", "#ffff00", "#ff7e00", "red", "#8f3f97", "#7e0023"]
    c = []
    for i in idx:
        if i < 2:
            c.append(color_list[0])
        elif i < 3:
            c.append(color_list[1])
        elif i < 4:
            c.append(color_list[2])
        elif i < 5:
            c.append(color_list[3])
        elif i < 6:
            c.append(color_list[4])
        else:
            c.append(color_list[5])
    return zip(lo, la, c)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    logging.basicConfig(level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO)
    app = QApplication(sys.argv)
    win = MyMainWindow()
    win.show()
    win.canvasWidget.canvas.mapPlot(genAllData(), title="AQI")
    sys.exit(app.exec_())
