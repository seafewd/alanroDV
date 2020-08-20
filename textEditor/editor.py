import tkinter as tk
import tkinter.filedialog


# Text Editor Skeleton

def on_new():
    # reset path and delete all text in the text box
    print("Not implemented")


def on_open():
    # let user choose what file to open from a dialog (tkFileDialog)
    # replace text in text box with text from file
    # handle cancelling of the dialog responsibely
    print("Not implemented")


def on_save():
    # mimic common "save" behavior
    # if the path is already set, save the file using save_file(), otherwise:
    # let user choose a file to save the content in the text box to (tkFileDialog)
    # make sure the path is valid (not empty), save the file using save_file()
    print("Not implemented")


def on_save_as():
    # mimic common "save as" behavior
    # almost the same as on_save(), difference: this always opens a file dialog
    print("Not implemented")


def get_all_text():
    # returns all text in the text box
    # should be one line of code
    # not neccessary but may make the code in other places nicer
    print("Not implemented")


def delete_all_text():
    # deletes all text in the text box
    # should be one line of code
    # not neccessary but may make the code in other places nicer
    print("Not implemented")


def save_file(save_path, text):
    # open file in save_path in write mode
    # write the text to the file
    # close the file
    print("Not implemented")


def read_file(file_path):
    # open file in file_path
    # return the text
    print("Not implemented")


# Initialize application
app = tk.Tk()
app.title("Your Title Here")
# Sets the geometry on the form widthxheight+x_pos+y_pos
app.geometry("800x500+300+300")

# Save path, empty until file is opened or saved
# Used to mimic common file saving/opening behavior
path = ''

######################################################
# IMPLEMENT UI HERE
######################################################

# MENU BAR EXAMPLE
menu_bar = tk.Menu()

# Set menu bar as menu for the app
app.config(menu=menu_bar)

# "File" menu
filemenu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=quit)
filemenu.add_command(label="Save (Ctrl+s)", command=quit)
filemenu.add_command(label="Save as...", command=quit)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

# "Edit" menu
editMenu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Cut", command=quit)
editMenu.add_command(label="Cut", command=quit)
editMenu.add_command(label="Undo", command=quit)
editMenu.add_command(label="Redo", command=quit)

# Main frame
frame = tk.Frame(app)
frame.pack(pady=5)

# BUTTON EXAMPLE
button = tk.Button(app, text="Exit", command=quit)
button.pack(side=tk.BOTTOM, fill=tk.X)

# SCROLLBAR
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


# TEXT WIDGET
textArea = tk.Text(frame, height=25, width=97, undo=True, yscrollcommand=scrollbar.set)
textArea.pack()


######################################################

# Start the main event loop (i.e. run the tkinter program)
app.mainloop()
