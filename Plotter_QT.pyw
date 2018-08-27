'''
Rewritten the tkinter plotting app in PyQt5
Still to add grid layout manager
'''


import csv
import sys
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib import style
from cycler import cycler
from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np

style.use('ggplot')
LARGE_FONT= ("Verdana", 12)

class Plotter(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(Plotter, self).__init__()
        self.initUi()
        
    def initUi(self):
        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle('Plotter')
        self.setWindowIcon(QtGui.QIcon('sincos.ico'))
        self.grid = QtWidgets.QGridLayout()
        self.setLayout(self.grid)

        config_plt_butt = QtWidgets.QPushButton('Configure plot', self)
        config_plt_butt.clicked.connect(self.config_plot)
        self.grid.addWidget(config_plt_butt,2,0)
        loadFile_butt = QtWidgets.QPushButton('Load file', self)
        loadFile_butt.clicked.connect(self.load_file)
        self.grid.addWidget(loadFile_butt,2,1)
        plot_butt = QtWidgets.QPushButton('Plot', self)
        plot_butt.clicked.connect(self.plot_it)
        self.grid.addWidget(plot_butt,2,2)
        clr_butt = QtWidgets.QPushButton('Clear plot', self)
        clr_butt.clicked.connect(self.clr_plot)
        self.grid.addWidget(clr_butt,2,3)

        self.plt_canvas = PlotCanvas(self, width=10, height=6)
        self.toolbar = NavigationToolbar2QT(self.plt_canvas, self)
        self.grid.addWidget(self.plt_canvas, 1,0,1,4)
        self.grid.addWidget(self.toolbar, 0,0,1,5)

        self.show()

        #Data holders
        self.plot_arrays_dict = {}
        self.plot_col_dict = {}
        self.Filename = ''
        self.Y_index_list = []
        self.Y2_index_list = []
        self.X_index = ''

    def config_plot(self):
        if self.Filename == '':
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("No file selected!")
            self.msg.setWindowTitle("Error")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.show()
        else:
            self.m = WhatToPlot(self)
            self.m.show()

    def plot_it(self):
        data = [1,2,3,4,5,6,7,8,9]
        self.plt_canvas.plot(data, self)

    def load_file(self):
        options=QtWidgets.QFileDialog.Options()
        #options
        self.Filename = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileNames()", "","All Files (*)", options=options)[0]
        extract_data(self)

    def clr_plot(self):
        self.plt_canvas.clear_all()



class PlotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.axis_1_colours = ['r','g','b','y','navy']    #sets different colour cyclers for each axis to avoid confusion
        self.axis_2_colours = ['y','m','k','gray','greenyellow']
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_prop_cycle(cycler('color', self.axis_1_colours))
        FigureCanvasQTAgg.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def plot(self,data, master):
        if master.Filename == '':
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("No file selected!")
            self.msg.setWindowTitle("Error")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.show()
        elif master.X_index == '':
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("No X data in config!")
            self.msg.setWindowTitle("Error")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.show()
        elif master.Y_index_list == []:
            self.msg = QtWidgets.QMessageBox()
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("No Y data in config!")
            self.msg.setWindowTitle("Error")
            self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msg.show()
        else:
            self.legend_ax1 = []
            for i in master.Y_index_list:
                self.ax1.plot(master.plot_arrays_dict[master.X_index], master.plot_arrays_dict[i], 'o')
                self.legend_ax1.append(master.data_titles[i])
            self.ax1.set_xlabel(master.data_titles[master.X_index])
            self.ax1.set_ylabel(master.data_titles[master.Y_index_list[0]]) #This should grab the first title that was plotted and set it
            self.ax1.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(10))
            self.ax1.legend(self.legend_ax1)
            if master.Y2_index_list != []:
                self.legend_ax2=[]
                self.ax2=self.ax1.twinx()
                self.ax2.set_prop_cycle(cycler('color', self.axis_2_colours))
                for i in master.Y2_index_list:
                    self.ax2.plot(master.plot_arrays_dict[master.X_index], master.plot_arrays_dict[i], 'o')
                    self.legend_ax2.append(master.data_titles[i])
                self.ax2.set_ylabel(master.data_titles[master.Y2_index_list[0]])
                self.ax2.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(10))
                self.ax2.legend(self.legend_ax2)
        self.draw()

    def clear_all(self):
        self.fig.clear()
        self.ax1 = self.fig.add_subplot(111)
        self.ax1.set_prop_cycle(cycler('color', self.axis_1_colours))
        self.draw()

class WhatToPlot(QtWidgets.QWidget):
    def __init__(self, master):
        super(WhatToPlot, self).__init__()
        self.setGeometry(50, 50, 300, 200)
        self.setWindowTitle('Configure plot')
        self.setWindowIcon(QtGui.QIcon('sincos.ico')) 
        self.options = ['']+master.data_titles
        
        self.XLabel = QtWidgets.QLabel(self, text='X')
        self.XLabel.move(50, 5)
        self.YLabel = QtWidgets.QLabel(self, text='Y1')
        self.YLabel.move(130, 5)
        self.Y2Label = QtWidgets.QLabel(self, text='Y1')
        self.Y2Label.move(210, 5)
        
        self.X=QtWidgets.QComboBox(self)
        self.X.addItems(self.options)
        self.X.move(10,20)

        self.Y_1=QtWidgets.QComboBox(self)
        self.Y_1.addItems(self.options)
        self.Y_1.move(90,20)
        self.Y_2=QtWidgets.QComboBox(self)
        self.Y_2.addItems(self.options)
        self.Y_2.move(90,40)
        self.Y_3=QtWidgets.QComboBox(self)
        self.Y_3.addItems(self.options)
        self.Y_3.move(90,60)
        self.Y_4=QtWidgets.QComboBox(self)
        self.Y_4.addItems(self.options)
        self.Y_4.move(90,80)
        self.Y_5=QtWidgets.QComboBox(self)
        self.Y_5.addItems(self.options)
        self.Y_5.move(90,100)

        self.Y2_1=QtWidgets.QComboBox(self)
        self.Y2_1.addItems(self.options)
        self.Y2_1.move(170,20)
        self.Y2_2=QtWidgets.QComboBox(self)
        self.Y2_2.addItems(self.options)
        self.Y2_2.move(170,40)
        self.Y2_3=QtWidgets.QComboBox(self)
        self.Y2_3.addItems(self.options)
        self.Y2_3.move(170,60)
        self.Y2_4=QtWidgets.QComboBox(self)
        self.Y2_4.addItems(self.options)
        self.Y2_4.move(170,80)
        self.Y2_5=QtWidgets.QComboBox(self)
        self.Y2_5.addItems(self.options)
        self.Y2_5.move(170,100)

        self.Y_obj_list = [self.Y_1,self.Y_2,self.Y_3,self.Y_4,self.Y_5]
        self.Y2_obj_list = [self.Y2_1,self.Y2_2,self.Y2_3,self.Y2_4,self.Y2_5]


        conf_butt = QtWidgets.QPushButton('Confirm', self)
        conf_butt.clicked.connect(lambda: self.confirm_and_close(master))
        conf_butt.move(90,140)
        

    def confirm_and_close(self, master):
        master.Y_index_list = self.check_vals(self.Y_obj_list, master.data_titles)
        master.Y2_index_list = self.check_vals(self.Y2_obj_list, master.data_titles)
        master.X_index = master.data_titles.index(str(self.X.currentText()))
        self.destroy()

    def check_vals(self, obj_list, data_titles):
        vals_list = []
        index_to_plot_list = []    
        for o in obj_list:
            if str(o.currentText()) == '':
                pass
            else:
                vals_list.append(str(o.currentText()))
        for val in vals_list:
            ind = data_titles.index(val)
            index_to_plot_list.append(ind)    
        return index_to_plot_list

def extract_data(master):
    master.plot_arrays_dict={}
    with open(master.Filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(read_csv):
            if len(row)>0:
                if index==0:
                    master.data_titles = row
                    number_cols = len(row)
                    for i in range(number_cols):
                        master.plot_col_dict[i]=[]
                else:
                    for i in range(number_cols):
                        master.plot_col_dict[i].append(row[i])
    for i in range(number_cols):
        master.plot_arrays_dict[i]=np.asarray(master.plot_col_dict[i], dtype='float')


app = QtWidgets.QApplication(sys.argv)
GUI=Plotter()
sys.exit(app.exec_())