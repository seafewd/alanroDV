import tkinter as tk
import tkinter.filedialog

# Tutorial: https://www.youtube.com/watch?v=UlQRXJWUNBA
# Canvas:   https://canvas.gu.se/courses/37080/assignments/60654?module_item_id=209969


# Initialize application
app = tk.Tk()
app.title("Galaxy brain editor")
# Sets the geometry on the form widthxheight+x_pos+y_pos
app.geometry("800x500+300+300")

# Save path, empty until file is opened or saved
# Used to mimic common file saving/opening behavior
path = ''

# set variable for open file name
global open_status_name
open_status_name = False

# clipboard
global selected
selected = False

# ----------------------------------------------------

# save as file
def save_as_file(e):
    global open_status_name
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
        open_status_name = text_file
        # close file
        text_file.close()
        print("saved as " + fileName)

# save file
def save_file(e):

    global open_status_name
    print(open_status_name)
    if open_status_name:
        # save file
        text_file = open(open_status_name, 'w')
        text_file.write(textArea.get(1.0, tk.END))
        # close file
        text_file.close()
        statusBar.config(text=f'Saved: {open_status_name}        ')
        print("file saved")
    else:
        save_as_file(e)

def new_file(e):
    # from first line to end
    textArea.delete("1.0", tk.END)
    # update status bar
    app.title("Galaxy brain editor - New File")
    statusBar.config(text="New File        ")

    # reset global name
    global open_status_name
    open_status_name = False
    print("new file")

def open_file(e):
    print("open file")
    textArea.delete("1.0", tk.END)
    # grab file name
    text_file = tk.filedialog.askopenfilename(
        initialdir="/saved_texts/",
        title="Open File",
        filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))

    # get full path
    name = text_file

    # check if there is a file name
    if text_file:
        # make file name global so we can access it later
        global open_status_name
        open_status_name = text_file

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

# Cut text
def cut_text(e):
    print("cut")
    global selected
    selection = textArea.selection_get()
    # check if keyboard shortcut used
    if e:
        selected = app.clipboard_get()
    else:
        if selection:
            # grab selected text from textbox
            selected = selection
            # delete from first highlighted to last highlighted
            textArea.delete("sel.first", "sel.last")
            app.clipboard_clear()
            app.clipboard_append(selected)

def copy_text(e):
    print("copy")
    global selected
    selection = textArea.selection_get()
    # check to see if we used keyboard shortcuts
    if e:
        selected = app.clipboard_get()

    if selection:
        # grab selected text from textbox
        selected = selection
        # clear clipboard and set it to new selection
        app.clipboard_clear()
        app.clipboard_append(selected)

def paste_text(e):
    print("paste")
    global selected
    # check to see if keyboard shortcut used
    if e:
        selected = app.clipboard_get()
    else:
        if selected:
            # assign position to wherever cursor is
            position = textArea.index(tk.INSERT)
            textArea.insert(position, selected)



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
filemenu.add_command(label="New            ", command=lambda: new_file(False), accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=lambda: open_file(False), accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=lambda: save_file(False), accelerator="Ctrl+S")
filemenu.add_command(label="Save as...", command=lambda: save_as_file(False), accelerator="Ctrl+Shift+S")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)

# "Edit" menu
editMenu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Cut            ", command=lambda: cut_text(False), accelerator="Ctrl+X")
editMenu.add_command(label="Copy", command=lambda: copy_text(False), accelerator="Ctrl+C")
editMenu.add_command(label="Paste", command=lambda: paste_text(False), accelerator="Ctrl+V")
editMenu.add_separator()
editMenu.add_command(label="Undo", accelerator="Ctrl+Z")
editMenu.add_command(label="Redo", accelerator="Ctrl+Y")

# Main frame
frame = tk.Frame(app)
frame.pack(pady=5)

# BUTTON EXAMPLE
# button = tk.Button(app, text="Exit", command=quit)
# button.pack(side=tk.BOTTOM, fill=tk.X)

# SCROLLBARS
scrollbarY = tk.Scrollbar(frame)
scrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
scrollbarX = tk.Scrollbar(frame, orient='horizontal')
scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

# STATUS BAR
statusBar = tk.Label(app, text='Ready        ', )
statusBar.pack(fill=tk.X, side=tk.RIGHT, ipady=5)

# TEXT WIDGET
textArea = tk.Text(
    frame,
    height=25,
    width=97,
    undo=True,
    yscrollcommand=scrollbarY.set,
    xscrollcommand=scrollbarX.set,
    wrap="none")
textArea.pack()

# config scroll bars
scrollbarY.config(command=textArea.yview())
scrollbarX.config(command=textArea.xview())

# edit bindings
app.bind('<Control-Key-x>', cut_text)
app.bind('<Control-Key-c>', copy_text)
app.bind('<Control-Key-v>', paste_text)
app.bind('<Control-Key-o>', open_file)
app.bind('<Control-Key-s>', save_file)
app.bind('<Shift-Control-S>', save_as_file)
app.bind('<Control-Key-n>', new_file)

######################################################

# Start the main event loop (i.e. run the tkinter program)
app.mainloop()
