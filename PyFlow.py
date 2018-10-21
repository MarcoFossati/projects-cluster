from tkinter import *
from tkinter import filedialog
import PyConfig
import os.path


master = Tk()
master.title("PyFlow")

# define objects for GUI
#Gmsh
gmsh_path_label = Label(master)
gmsh_text = Entry(master)
gmsh_browse = Button(master)
#SU2
su_path_label = Label(master)
su_path_text = Entry(master)
su_browse = Button(master)
#ParaView
paraview_path_label = Label(master)
paraview_path_text = Entry(master)
paraview_browse = Button(master)
#Project Path
project_path_label = Label(master)
project_path_text = Entry(master)
project_browse = Button(master)
#CAD file
cad_file_label = Label(master)
cad_file_text = Entry(master)
cad_browse = Button(master)
#Buttons
ok_button = Button(master)
cancel_button = Button(master)


def set_gui_text():
    #labels
    gmsh_path_label.config(text="Add path to Gmsh.exe")
    su_path_label.config(text="Add path to SU2 executable")
    paraview_path_label.config(text="Add path to ParaView executable")
    project_path_label.config(text="Add path to project location")
    cad_file_label.config(text="Add path to CAD file")
    #buttons
    gmsh_browse.config(text="Browse")
    su_browse.config(text="Browse")
    paraview_browse.config(text="Browse")
    project_browse.config(text="Browse")
    cad_browse.config(text="Browse")

    ok_button.config(text="OK")
    cancel_button.config(text="Cancel")


def set_grids():
    #Labels
    gmsh_path_label.grid(row=0)
    su_path_label.grid(row=2)
    paraview_path_label.grid(row=4)
    project_path_label.grid(row=6)
    cad_file_label.grid(row=8)
    #Entries
    gmsh_text.grid(row=1)
    su_path_text.grid(row=3)
    paraview_path_text.grid(row=5)
    project_path_text.grid(row=7)
    cad_file_text.grid(row=9)
    #Buttons
    gmsh_browse.grid(row=1, column=1)
    su_browse.grid(row=3, column=1)
    paraview_browse.grid(row=5, column=1)
    project_browse.grid(row=7, column=1)
    cad_browse.grid(row=9, column=1)
    #Buttons
    ok_button.grid(row=10)
    cancel_button.grid(row=10, column=1)


def check_file(path):
    return os.path.exists(path)


def ok_press():
    # print(get_paths())
    paths = get_paths()
    for i in range(0,5):
        print(paths[i])
    config_path = paths[3] + "/CONFIGURATION_FILE.txt"
    file = open(config_path,'a')
    for i in range(0,5):
        file.write(paths[i] + "\n")
    if check_file(config_path):
        print("Configuration file successfully created.")


def get_paths():
    return gmsh_text.get(),  su_path_text.get(), paraview_path_text.get(), project_path_text.get(), cad_file_text.get()


def set_buttons():
    ok_button.config(command=ok_press)
    # cancel_button.config(command=cancel_button)


def do_binds():
    gmsh_browse.bind("<1>", display_file_browser)
    su_browse.bind("<1>", display_file_browser)
    paraview_browse.bind("<1>", display_file_browser)
    project_browse.bind("<1>", display_file_browser)
    cad_browse.bind("<1>", display_file_browser)


def open_file_browser():
    return filedialog.askopenfilename(initialdir="/", title="Select configuration file",
                                      filetypes=(("text files", "*.txt"), ("all files", "*.*")))


def open_dir_browser():
    return filedialog.askdirectory()


def display_file_browser(event):
    print(str(event.widget))
    # filename = filedialog.askopenfilename(initialdir="/", title="Select configuration file",
    #                                       filetypes=(("text files", "*.txt"), ("all files", "*.*")))
    if str(event.widget) == ".!button":
        filename = open_file_browser()
        gmsh_text.insert(0,filename)
    elif str(event.widget) == ".!button2":
        filename = open_file_browser()
        su_path_text.insert(0,filename)
    elif str(event.widget) == ".!button3":
        filename = open_file_browser()
        paraview_path_text.insert(0,filename)
    elif str(event.widget) == ".!button4":
        filename = open_dir_browser()
        project_path_text.insert(0,filename)
    elif str(event.widget) == ".!button5":
        filename = open_file_browser()
        cad_file_text.insert(0,filename)
    else:
        return


# executable script
set_gui_text()
set_grids()
set_buttons()
do_binds()
master.mainloop()
