#Import some things
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from tkinter import scrolledtext
import tkinter.ttk as ttk
import pickle
import os.path
 
class Application(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.initialize_user_interface()
 
    def initialize_user_interface(self):
        # Configure the root object for the Application
        self.root.title("Pixel_EDM")
        self.root.state("zoomed")
 
        #Frames
        self.Main_Left = tk.Frame(self.root)
        self.Main_Left.grid(column = 0, row = 0, pady = 10, padx = 10, sticky="w")
        self.Main_Right = tk.Frame(self.root)
        self.Main_Right.grid(column = 1, row = 0, pady = 10, padx = 10, sticky="w")
        self.Treeview = tk.Frame(self.Main_Left)
        self.Treeview.grid(column = 0, row = 0, pady = 10, padx = 10, sticky="w")
        self.Values = tk.Frame(self.Main_Left)
        self.Values.grid(column = 0, row = 1, pady = 10, padx = 10, sticky="w")
        self.Settings_Frame_1 = tk.Frame(self.Main_Left)
        self.Settings_Frame_1.grid(column = 0, row = 2, pady = 10, padx = 10, sticky="w")
        self.Settings_Frame_2 = tk.Frame(self.Main_Left)
        self.Settings_Frame_2.grid(column = 0, row = 3, pady = 10, padx = 10, sticky="w")
        
        #Treeview
        self.tree = ttk.Treeview(self.Treeview, columns=('X', 'Y'))
        self.tree.grid(row=0, column=0)
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        
        #Treeview Headings
        self.tree.heading('#0', text='Machining Order')
        self.tree.heading('#1', text='X')
        self.tree.heading('#2', text='Y')
        
        #Treeview Scrollbar
        scrollbar = ttk.Scrollbar(self.Treeview, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
 
        #Some other stuff
        self.treeview = self.tree
        self.id = 0
        self.iid = 0
        
        #Labels
        self.name_label = tk.Label(self.Values, text="X:")
        self.name_label.grid(row=0, column=0)
        self.idnumber_label = tk.Label(self.Values, text="Y:")
        self.idnumber_label.grid(row=1, column=0, sticky="w")
        self.startcode_label = tk.Label(self.Settings_Frame_1, text="Startcode:")
        self.startcode_label.grid(row=0, column=0, sticky="w")
        self.operationcode_label = tk.Label(self.Settings_Frame_1, text="Operationcode:")
        self.operationcode_label.grid(row=0, column=1, sticky="w")
        self.endcode_label = tk.Label(self.Settings_Frame_2, text="Endcode:")
        self.endcode_label.grid(row=0, column=0, sticky="w")
        self.travelspeed_label = tk.Label(self.Settings_Frame_2, text="Travelspeed:")
        self.travelspeed_label.grid(row=0, column=1, sticky="w")
        
        #Entrys
        self.travelspeed = tk.Entry(self.Settings_Frame_2)
        self.travelspeed.grid(row=1, column=1, pady = 10, padx = 10, sticky="n")
        
        #Spinboxes
        self.name_spinbox = tk.Spinbox(self.Values, from_=0.0, to=9999.0, increment=5.0, format='%10.2f', font=('sans-serif', 14))
        self.name_spinbox.grid(row=0, column=1)
        self.idnumber_spinbox = tk.Spinbox(self.Values, from_=0.0, to=9999.0, increment=5.0, format='%10.2f', font=('sans-serif', 14))
        self.idnumber_spinbox.grid(row=1, column=1)
        
        #Buttons
        self.submit_button = tk.Button(self.Values, text="+", command=self.insert_data)
        self.submit_button.grid(row=0, column=2, sticky="ew")
        self.delete_button = tk.Button(self.Values, text="-", command=self.delete_data)
        self.delete_button.grid(row=1, column=2, sticky="ew")
        self.btn_up = tk.Button(self.Values, text='↑', command=self.moveUp)
        self.btn_up.grid(row=0, column=3, sticky="ew")
        self.btn_down = tk.Button(self.Values, text='↓', command=self.moveDown)
        self.btn_down.grid(row=1, column=3, sticky="ew")
        self.save_gcode_button = tk.Button(self.Values, text='Save GCODE', command=self.save_gcode)
        self.save_gcode_button.grid(row=0, column=4, pady = 30, padx = 30, sticky="e")
        self.save_settings_button = tk.Button(self.Values, text='Save Settings', command=self.save_settings)
        self.save_settings_button.grid(row=1, column=4, pady = 30, padx = 30, sticky="e")
        
 
        #Scrolled Texts
        self.startcode_scrolledtext = scrolledtext.ScrolledText(self.Settings_Frame_1, wrap = tk.WORD, width = 20, height = 4, font = ("Courier", 12))
        self.startcode_scrolledtext.grid(column = 0, row = 1, pady = 10, padx = 10)
        self.operationcode_scrolledtext = scrolledtext.ScrolledText(self.Settings_Frame_1, wrap = tk.WORD, width = 20, height = 4, font = ("Courier", 12))
        self.operationcode_scrolledtext.grid(column = 1, row = 1, pady = 10, padx = 10)
        self.endcode_scrolledtext = scrolledtext.ScrolledText(self.Settings_Frame_2, wrap = tk.WORD, width = 20, height = 4, font = ("Courier", 12))
        self.endcode_scrolledtext.grid(column = 0, row = 1, pady = 10, padx = 10)
        
        #Plot
        fig = Figure(figsize = (5, 5), dpi = 100)
        plot = fig.add_subplot()
        plot.axis([0, 200, 0, 200])
        plot.plot([], [])
        canvas = FigureCanvasTkAgg(fig, master = self.root)   
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=4, pady = 30, padx = 30, sticky="e")
        
        #If no Pickle File exists, create one
        defaultSettings = {"Travelspeed": "Empty", "Startcode": "Empty", "Operationcode": "Empty", "Endcode": "Empty"}
        if os.path.isfile("Settings.p") == False:
         pickle.dump(defaultSettings, open("Settings.p", "wb"))

        #Load Settings from File
        SettingValues = pickle.load(open("Settings.p", "rb"))
        self.travelspeed.insert(0, SettingValues.get("Travelspeed"))
        self.startcode_scrolledtext.insert(1.0, SettingValues.get("Startcode"))
        self.operationcode_scrolledtext.insert(1.0, SettingValues.get("Operationcode"))
        self.endcode_scrolledtext.insert(1.0, SettingValues.get("Endcode"))

    def insert_data(self):
        self.treeview.insert('', 'end', iid=self.iid, text=str(self.id), values=(self.name_spinbox.get(), self.idnumber_spinbox.get()))
        self.iid = self.iid + 1
        self.id = self.id + 1
        self.update()
 
    def delete_data(self):
        row_id = int(self.tree.focus())
        self.treeview.delete(row_id)
        self.update()
        
    def update(self):
     for idx, node in enumerate(self.treeview.get_children()):
        self.tree.item(node, text=str(idx))
     treeview_output = [self.tree.item(child)["values"] for child in self.tree.get_children()]
     output_remove_whitespace = [[x.strip(' ') for x in elem] for elem in treeview_output]
     output_string_to_float = [[float(x) for x in elem] for elem in output_remove_whitespace]
     output_x_values = [x for x,y in output_string_to_float]
     output_y_values = [y for x,y in output_string_to_float]
     fig = Figure(figsize = (5, 5), dpi = 100)
     plot = fig.add_subplot()
     plot.axis([0, 200, 0, 200])
     plot.plot(output_x_values, output_y_values, "s", markersize=5)
     canvas = FigureCanvasTkAgg(fig, master = self.root)   
     canvas.draw()
     canvas.get_tk_widget().grid(row=0, column=4, pady = 30, padx = 30, sticky="e")

    def save_gcode(self):
     treeview_output = [self.tree.item(child)["values"] for child in self.tree.get_children()]
     output_remove_whitespace = [[x.strip(' ') for x in elem] for elem in treeview_output]
     #output_string_to_float = [[float(x) for x in elem] for elem in output_remove_whitespace]
     output_x_values = [x for x,y in output_remove_whitespace]
     output_y_values = [y for x,y in output_remove_whitespace]
     gcode_x = ["G0 X" + item +  " " for item in output_x_values]
     gcode_y = ["Y" + item + " F" +  self.travelspeed.get() + "\n" for item in output_y_values]
     gcode_xy_zip = zip(gcode_x, gcode_y)
     gcode_xy_list = list(gcode_xy_zip)
     gcode_xy = ["".join(item) for item in gcode_xy_list]
     gcode_xy_oprationcode = [item + self.operationcode_scrolledtext.get(1.0, "end") for item in gcode_xy]
     gcode_string = "".join(gcode_xy_oprationcode)
     gcode_output = self.startcode_scrolledtext.get(1.0, "end") + gcode_string + self.endcode_scrolledtext.get(1.0, "end")
     sF = filedialog.asksaveasfilename(defaultextension=".gcode", title="Save GCODE", filetypes=(("GCODE Files", "*.gcode"),))
     with open(sF, "w") as outfile:
        outfile.write(gcode_output)
    
    #Save Settings to File
    def save_settings(self):
     SettingValues = {"Travelspeed": self.travelspeed.get(), "Startcode": self.startcode_scrolledtext.get(1.0,
                     "end"), "Operationcode": self.operationcode_scrolledtext.get(1.0,
                     "end"), "Endcode": self.endcode_scrolledtext.get(1.0, "end")}
     pickle.dump( SettingValues, open( "Settings.p", "wb" ) )
     
    def OnDoubleClick(self, event):
     treeview_output = [self.tree.item(child)["values"] for child in self.tree.get_children()]
     output_remove_whitespace = [[x.strip(' ') for x in elem] for elem in treeview_output]
     output_string_to_float = [[float(x) for x in elem] for elem in output_remove_whitespace]
     output_x_values = [x for x,y in output_string_to_float]
     output_y_values = [y for x,y in output_string_to_float]
     #selected_output = [self.tree.item(child)["values"] for child in self.tree.focus()]
     selected_item = self.tree.focus()
     selected_output = self.tree.item(selected_item)["values"]
     selected_remove_whitespace = [x.strip(' ') for x in selected_output]
     selected_string_to_float = [float(x) for x in selected_remove_whitespace]
     selected_x_values = selected_string_to_float[0]
     selected_y_values = selected_string_to_float[1]
     fig = Figure(figsize = (5, 5), dpi = 100)
     plot = fig.add_subplot()
     plot.axis([0, 200, 0, 200])
     plot.plot(output_x_values, output_y_values, "s", markersize=5)
     plot.plot(selected_x_values, selected_y_values, "ro", markersize=5)
     canvas = FigureCanvasTkAgg(fig, master = self.root)   
     canvas.draw()
     canvas.get_tk_widget().grid(row=0, column=4, pady = 30, padx = 30, sticky="e")
    
    # create a function to move the selected row up
    def moveUp(self):
     leaves = self.tree.selection()
     for i in leaves:
        self.tree.move(i, self.tree.parent(i), self.tree.index(i)-1)
        self.update()

    # create a function to move the selected row down
    def moveDown(self):
     leaves = self.tree.selection()
     for i in reversed(leaves):
        self.tree.move(i, self.tree.parent(i), self.tree.index(i)+1)
        self.update()
        
app = Application(tk.Tk())
app.root.mainloop()
