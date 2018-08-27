import csv
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
from cycler import cycler
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np

style.use('ggplot')
LARGE_FONT= ("Verdana", 12)

class Plotter(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.iconbitmap(self, default="sincos.ico")
        Tk.wm_title(self, "Plotter")
        #Data holders
        self.plot_arrays_dict = {}
        self.plot_col_dict = {}
        self.Filename = ''
        self.Y_index_list = []
        self.Y2_index_list = []
        self.X_index = ''

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        #Frames hold the app pages
        self.frames = {}
        self.frames[StartPage] = StartPage(container, self)
        self.frames[StartPage].grid(row=0, column=0, sticky='nsew')
        #all page must be added to following tuple
        '''
        for F in (StartPage, WhatToPlot):
            frame=F(container, self)
            self.frames[F] = frame
            #defines the grid
            frame.grid(row=0, column=0, sticky="nsew")
        '''
        self.show_frame(StartPage)

    def show_frame(self, cont):
        #Raises the chosen page to the top.
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(ttk.Frame):
    def __init__(self, parent, controller): 
        Frame.__init__(self,parent)
        self.axis_1_colours = ['r','g','b','y','navy']    #sets different colour cyclers for each axis to avoid confusion
        self.axis_2_colours = ['y','m','k','gray','greenyellow']
        self.graph_set = False
        self.bind("<<ShowGraphPage>>", lambda event:self.on_show_graph_page(controller))
        self.Graph= Figure(figsize=(1,1), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.Graph, self) 
        self.canvas.get_tk_widget().pack(side="bottom", fill="both", expand = True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side="top", fill="both", expand = True)
        self.sp1_1 = self.Graph.add_subplot(111)
        self.sp1_1.set_prop_cycle(cycler('color', self.axis_1_colours))

        load_file_butt = ttk.Button(self, text="Choose data file", command=lambda: self.load_file(controller))
        load_file_butt.pack()

        configure_plot_butt = ttk.Button(self, text='Configure axis', command=lambda: self.config_plot(controller))
        configure_plot_butt.pack()

        plot_button = ttk.Button(self, text='Plot it', command=lambda: self.plot_it(controller))
        plot_button.pack()

        clr_plot_butt = ttk.Button(self, text='Clear plot', command=self.clear_plt)
        clr_plot_butt.pack()

    def load_file(self, controller):
        controller.Filename = askopenfilename(initialdir="Z:\\", title="Choose a file")
        extract_data(controller)

    def config_plot(self, controller):
        if controller.Filename == '':
            messagebox.showerror('No file loaded!')
        elif controller.data_titles == []:
            messagebox.showerror('Unrecognised file format')
        else:
            WhatToPlot(controller)

    def plot_it(self, controller):
        if controller.Filename == '':
            messagebox.showerror('No file loaded!')
        elif controller.X_index == '':
            messagebox.showerror('No X axis data')
        elif controller.Y_index_list == []:
            messagebox.showerror('No Y axis data')
        else:
            for i in controller.Y_index_list:
                self.sp1_1.plot(controller.plot_arrays_dict[controller.X_index], controller.plot_arrays_dict[i])
            self.sp1_1.set_xlabel(controller.data_titles[controller.X_index])
            self.sp1_1.set_ylabel(controller.data_titles[controller.Y_index_list[0]]) #This should grab the first title that was plotted and set it
            if controller.Y2_index_list != []:
                self.sp1_2=self.sp1_1.twinx()
                self.sp1_2.set_prop_cycle(cycler('color', self.axis_2_colours))
                for i in controller.Y2_index_list:
                    self.sp1_2.plot(controller.plot_arrays_dict[controller.X_index], controller.plot_arrays_dict[i])
                self.sp1_2.set_ylabel(controller.data_titles[controller.Y2_index_list[0]])
            self.canvas.draw()

    def clear_plt(self):
    	self.Graph.clear()
    	self.sp1_1 = self.Graph.add_subplot(111)
    	self.sp1_1.set_prop_cycle(cycler('color', self.axis_1_colours))
    	self.canvas.draw()

class WhatToPlot(Toplevel):
    def __init__(self, controller):
        Toplevel.__init__(self)
        self.geometry("500x300")
        self.title("What do you want to plot?")
        XLabel = ttk.Label(self, text='X-axis', font=LARGE_FONT)
        XLabel.grid(row=1,column=1, padx=20)
        YLabel = ttk.Label(self, text='Y-axis ?', font=LARGE_FONT)
        YLabel.grid(row=1,column=2, padx=20)
        Y2Label = ttk.Label(self, text='Y-axis 2', font=LARGE_FONT)
        Y2Label.grid(row=1,column=3, padx=20)
        
        self.X=ttk.Combobox(self, values=controller.data_titles)
        self.X.grid(row=2, column=1)

        Y_1=ttk.Combobox(self, values=controller.data_titles)
        Y_1.grid(row=2,column=2)
        Y_2=ttk.Combobox(self, values=controller.data_titles)
        Y_2.grid(row=3,column=2)
        Y_3=ttk.Combobox(self, values=controller.data_titles)
        Y_3.grid(row=4,column=2)
        Y_4=ttk.Combobox(self, values=controller.data_titles)
        Y_4.grid(row=5,column=2)
        Y_5=ttk.Combobox(self, values=controller.data_titles)
        Y_5.grid(row=6,column=2)

        Y2_1=ttk.Combobox(self, values=controller.data_titles)
        Y2_1.grid(row=2,column=3)
        Y2_2=ttk.Combobox(self, values=controller.data_titles)
        Y2_2.grid(row=3,column=3)
        Y2_3=ttk.Combobox(self, values=controller.data_titles)
        Y2_3.grid(row=4,column=3)
        Y2_4=ttk.Combobox(self, values=controller.data_titles)
        Y2_4.grid(row=5,column=3)
        Y2_5=ttk.Combobox(self, values=controller.data_titles)
        Y2_5.grid(row=6,column=3)

        self.Y_obj_list = [Y_1, Y_2, Y_3, Y_4, Y_5]
        self.Y2_obj_list = [Y2_1, Y2_2, Y2_3, Y2_4, Y2_5]


        conf_butt = ttk.Button(self, text="Confirm and close", command=lambda: self.confirm_and_close(controller))
        conf_butt.grid(row=7, column=2, columnspan=2)

    def confirm_and_close(self, controller):
        controller.Y_index_list = self.check_vals(self.Y_obj_list, controller.data_titles)
        controller.Y2_index_list = self.check_vals(self.Y2_obj_list, controller.data_titles)
        controller.X_index = controller.data_titles.index(self.X.get())
        self.destroy()

    def check_vals(self, obj_list, data_titles):
        vals_list = []
        index_to_plot_list = []    
        for o in obj_list:
            if o.get() == '':
                pass
            else:
                vals_list.append(o.get())
        for val in vals_list:
            ind = data_titles.index(val)
            index_to_plot_list.append(ind)    
        return index_to_plot_list


def extract_data(controller):
    controller.plot_arrays_dict={}
    with open(controller.Filename) as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        for index, row in enumerate(read_csv):
            if len(row)>0:
                if index==0:
                    controller.data_titles = row
                    number_cols = len(row)
                    for i in range(number_cols):
                        controller.plot_col_dict[i]=[]
                else:
                    for i in range(number_cols):
                        controller.plot_col_dict[i].append(row[i])
    for i in range(number_cols):
        controller.plot_arrays_dict[i]=np.asarray(controller.plot_col_dict[i], dtype='float')


app = Plotter()
app.geometry("1000x800")
app.mainloop()