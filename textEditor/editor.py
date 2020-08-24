import tkinter as tk
import tkinter.filedialog

# Tutorial: https://www.youtube.com/watch?v=UlQRXJWUNBA
# Canvas:   https://canvas.gu.se/courses/37080/assignments/60654?module_item_id=209969

# Text Editor Skeleton

def on_new():
    # reset path and delete all text in the text box
    print("Not implemented")


def on_open():
    # let user choose what file to open from a dialog (tkFileDialog)
    # replace text in text box with text from file
    # handle cancelling of the dialog responsibly
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
    # not necessary but may make the code in other places nicer
    print("Not implemented")


def delete_all_text():
    # deletes all text in the text box
    # should be one line of code
    # not neccessary but may make the code in other places nicer
    print("Not implemented")

# save as file
def save_file():
    text_file = tk.filedialog.asksaveasfilename(
        defaultextension=".*",
        initialdir="/saved_texts",
        title="Save File",
        filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files","*.py"), ("All Files", "*.*")))
    if text_file:
        name = text_file
        fileName = name[name.rindex("/")+1:]
        # update status bar
        statusBar.config(text=f'Saved: {name}        ')
        app.title(f'{fileName} - Galaxy Brain')
        # save file
        text_file = open(text_file, 'w')
        text_file.write(textArea.get(1.0, tk.END))
        # close file
        text_file.close()


def read_file(file_path):
    # open file in file_path
    # return the text
    print("Not implemented")

def new_file():
    # from first line to end
    textArea.delete("1.0", tk.END)
    # update status bar
    app.title("Galaxy brain editor - New File")
    statusBar.config(text="New File        ")

def open_file():
    textArea.delete("1.0", tk.END)
    # grab file name
    text_file = tk.filedialog.askopenfilename(
        initialdir="/saved_texts/",
        title="Open File",
        filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    # full path
    name = text_file
    # get only file name from path
    fileName = name[name.rindex("/")+1:]
    # update status bar
    statusBar.config(text=f'{name}        ')
    app.title(f'{fileName} - Galaxy Brain')

    # open file
    text_file = open(text_file, 'r')
    textInFile = text_file.read()
    # add file to textbox
    textArea.insert(tk.END, textInFile)
    text_file.close()


# Initialize application
app = tk.Tk()
app.title("Galaxy brain editor")
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
filemenu.add_command(label="New", command=new_file)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save (Ctrl+s)", command=quit)
filemenu.add_command(label="Save as...", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

# "Edit" menu
editMenu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Cut", command=quit)
editMenu.add_command(label="Copy", command=quit)
editMenu.add_command(label="Paste", command=quit)
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

# STATUS BAR
statusBar = tk.Label(app, text='Ready        ', )
statusBar.pack(fill=tk.X, side=tk.RIGHT, ipady=5)

# TEXT WIDGET
textArea = tk.Text(frame, height=25, width=97, undo=True, yscrollcommand=scrollbar.set)
textArea.pack()


######################################################

# Start the main event loop (i.e. run the tkinter program)
app.mainloop()
