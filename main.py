from tkinter import *
import os

buffers = {"text": [], "directory": []}
window = Tk()
window.title("oon")
window.configure(background="black")
directory = "D:\\all\\school\\inst126"

mode_string = StringVar()
mode_string.set("Test")
statusline_info = [mode_string]

def status_callback(*args):
	if edit_mode.get() == True:
		mode_string.set("<EDIT MODE>")	
	else:
		mode_string.set("--INSERT MODE--")

def cl_setfocus(*args):
	if cl_active.get() == True:
		commandline.focus_set()

cl_active = BooleanVar()
cl_active.trace("w", cl_setfocus)
cl_active.set(False)


edit_mode = BooleanVar()
edit_mode.trace("w", status_callback)
edit_mode.set(False)

def toggle_modal(event):
	global edit_mode
	if edit_mode.get() == True:
		event.widget.config(blockcursor=False)
		edit_mode.set(False)
		event.widget.tag_remove("mchar", "1.0", "end") #last
	else:
		edit_mode.set(True)
		event.widget.tag_add("mchar", "insert", "insert+1c") 
		event.widget.tag_config("mchar", foreground="white")
		event.widget.config(blockcursor=True)
	return "break"

def modal_mode(event):
	if edit_mode.get() == True:
		pass
	else:
		return
	#go left
	if event.keysym == 'u':
		event.widget.tag_remove("mchar", "1.0", "end")
		begin = event.widget.index("insert-1c")
		coords = event.widget.index("insert-1c").split(".")
		begin_plus_one = coords[0] + "." + str(int(coords[1]) + 1)
		event.widget.tag_add("mchar", begin, begin_plus_one)
		event.widget.tag_config("mchar", foreground="white")
		event.widget.mark_set("insert", "insert-1c")
		return "break"
	#go right
	elif event.keysym == 'o':
		event.widget.tag_remove("mchar", "1.0", "end")
		begin = event.widget.index("insert+1c")
		coords = event.widget.index("insert+1c").split(".")
		print(int(coords[0]))
		begin_plus_one = coords[0] + "." + str(int(coords[1]) + 1)

		event.widget.tag_add("mchar", begin, begin_plus_one)
		event.widget.tag_config("mchar", foreground="white")
		event.widget.mark_set("insert", "insert+1c")
		return "break"
	#go up
	elif event.keysym == "i":
		event.widget.tag_remove("mchar", "1.0", "end")
		begin = event.widget.index("insert")
		coords = event.widget.index("insert").split(".")
		if int(coords[0]) >= 1:
			begin = str(int(coords[0])-1) + "." + str(int(coords[1]))
			begin_plus_one = str(int(coords[0])-1) + "." + str(int(coords[1]) + 1)
			event.widget.tag_add("mchar", begin, begin_plus_one)
			event.widget.tag_config("mchar", foreground ="white")
			event.widget.mark_set("insert", begin)
		return "break"
	#go down
	elif event.keysym == 'j':
		event.widget.tag_remove("mchar", "1.0", "end")
		coords = event.widget.index("insert").split(".")
		begin =  str(int(coords[0])+1) + "." + str(int(coords[1]))
		begin_plus_one = str(int(coords[0])+1) + "." + str(int(coords[1]) + 1)
		event.widget.tag_add("mchar",  begin, begin_plus_one)
		event.widget.tag_config("mchar", foreground="white")
		event.widget.mark_set("insert", begin)
		return "break"
	#backspace
	elif event.keysym == 'p':
		event.widget.delete("insert-1c")
	#delete line if at beginning of line or end of line
	elif event.keysym == 'k':
		#event.widget.tag_remove("mchar", "1.0", "end")
		if event.widget.get("insert") == "\n" or event.widget.index("insert") == event.widget.index("current linestart"):
			event.widget.delete("current linestart", "current lineend+1c")
		return "break"
	#go to beginning of line
	elif event.keysym == 'U':
		event.widget.tag_remove("mchar", "1.0", "end")
		event.widget.mark_set("insert", "current linestart")
		return "break"
	#go to end of line
	elif event.keysym == 'O':
		event.widget.tag_remove("mchar", "1.0", "end")
		event.widget.mark_set("insert", "current lineend")
		return "break"
	elif event.keysym == 'a':
		cl_active.set(True)

	if event.keysym == 'f':
		toggle_modal(event)
		return "break"
	return "break"

cl_reset = StringVar()

def cl_commands(event):
	command = event.widget.get()
	if command == 'e':
		buffers['text'][-1].lift()
		buffers['text'][-1].focus_set()
	if command == 'dir':
		buffers['directory'].append(create_directory_buffer(window, directory, buffers))
		buffers['directory'][-1].focus_set()
	cl_reset.set("")

def directory_mode(event):
	if event.keysym == "Return":
		item = event.widget.get("insert linestart", "insert lineend")
		if item == "..":
			curr_path = curr_path[:curr_path.rfind("\\")]
		else:
			curr_path = directory + "\\" + item
		if os.path.isdir(curr_path):
			print("is directory")
			print(item)
			create_directory_buffer(window, curr_path, buffers)
		elif os.path.isfile(curr_path):
			print("is file")
			print(item)
			create_file_buffer(window, curr_path, buffers)
		return "break"

text_frame = Text(window, font = ("Roboto Mono", 10))
statusline = Label(window, textvariable = mode_string , fg = "white", bg = "grey", anchor = "w")
commandline = Entry(window, font = ("Roboto Mono", 9), textvariable = cl_reset)
#statusline.place(rely = .9, relwidth =  1)
statusline.grid(row=1,column=0, sticky = S+W+E)
commandline.grid(row=2, column=0, sticky = S + W + E)

text_frame.grid(row=0, column=0, sticky = N+S+W+E)
text_frame.configure(insertbackground="grey", insertofftime = 0)
text_frame.bind("<Shift-space>", toggle_modal)
text_frame.bind("<Key>", modal_mode)

commandline.bind("<Return>", cl_commands)

buffers['text'].append(text_frame)

#need string in class like type = dirbuffer?
def create_directory_buffer(window, path, buffers):
	dir_buffer = Text(window, font = ("Roboto Mono", 10))
	dir_buffer.grid(row = 0, column = 0, sticky = N + S + W + E)
	dir_buffer.configure(blockcursor=True, background = "white", foreground = "black")
	files = [file + "\n" for file in os.listdir(path)]
	dir_buffer.insert(END, "..\n")
	for file in files:
		dir_buffer.insert(END, file)
	dir_buffer.bind("<Key>", directory_mode)
	dir_buffer.focus_set()
	dir_buffer.lift()
	buffers['directory'].append(dir_buffer)
	return dir_buffer


def create_file_buffer(window, path, buffers):
	file_buffer = Text(window, font = ("Roboto Mono", 11))
	file_buffer.grid(row = 0, column = 0, sticky = N + S + W + E)
	file_buffer.configure(background = "white", foreground = "black", insertofftime = 0)
	file_buffer.bind("<Shift-space>", toggle_modal)
	file_buffer.bind("<Key>", modal_mode)
	with open(path, 'r') as f:
		file_buffer.insert(INSERT, f.read())
	file_buffer.focus_set()
	file_buffer.lift()
	buffers['text'].append(file_buffer)

def hide_buffers(window):
	for i in range(1, len(buffers)):
		buffers[i].grid_remove()



window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.mainloop()
