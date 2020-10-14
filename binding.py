from tkinter import *
import config
import buffer
import os
import test

def toggle_modal(event, isedit):
	"""Toggle the state between insertion mode and edit mode."""

	if isedit.get() == True:
		event.widget.config(blockcursor=False)
		isedit.set(False)
		event.widget.tag_remove("mchar", "1.0", "end")
	else:
		isedit.set(True)
		event.widget.tag_add("mchar", "insert", "insert+1c") 
		event.widget.tag_config("mchar", foreground="white")
		event.widget.config(blockcursor=True)

	return "break"

def left(event):
	"""Move insertion cursor one character left inside a Text widget."""

	textbox = event.widget
	textbox.tag_remove("mchar", "1.0", "end")
	begin = textbox.index("insert-1c")
	coords = textbox.index("insert-1c").split(".")
	begin_plus_one = coords[0] + "." + str(int(coords[1]) + 1)
	textbox.tag_add("mchar", begin, begin_plus_one)
	textbox.tag_config("mchar", foreground="white")
	textbox.mark_set("insert", "insert-1c")
	textbox.see("insert")

def up(event):
	"""Move insertion cursor one row up with same column inside a Text widget."""

	textbox = event.widget
	textbox.tag_remove("mchar", "1.0", "end")
	begin = textbox.index("insert")
	coords = textbox.index("insert").split(".")
	if int(coords[0]) >= 1:
		begin = str(int(coords[0])-1) + "." + str(int(coords[1]))
		begin_plus_one = str(int(coords[0])-1) + "." + str(int(coords[1]) + 1)
		textbox.tag_add("mchar", begin, begin_plus_one)
		textbox.tag_config("mchar", foreground ="white")
		textbox.mark_set("insert", begin)
		textbox.see("insert")

def right(event):
	"""Move insertion cursor one character right inside a Text widget."""

	textbox = event.widget
	textbox.tag_remove("mchar", "1.0", "end")
	begin = textbox.index("insert+1c")
	coords = textbox.index("insert+1c").split(".")
	begin_plus_one = coords[0] + "." + str(int(coords[1]) + 1)
	
	textbox.tag_add("mchar", begin, begin_plus_one)
	textbox.tag_config("mchar", foreground="white")
	textbox.mark_set("insert", "insert+1c")
	textbox.see("insert")

def down(event):
	"""Moves insertion cursor one row down with same column inside a Text widget,
	   creates a newline and moves to newline if at end of file."""

	textbox = event.widget
	if textbox.index("insert") == textbox.index("end-1c"):
		textbox.insert("insert", "\n")
		textbox.mark_set("insert", "insert+1c")
	else:
		textbox.tag_remove("mchar", "1.0", "end")
		coords = textbox.index("insert").split(".")
		begin =  str(int(coords[0])+1) + "." + str(int(coords[1]))
		begin_plus_one = str(int(coords[0])+1) + "." + str(int(coords[1]) + 1)
		textbox.tag_add("mchar",  begin, begin_plus_one)
		textbox.tag_config("mchar", foreground="white")
		textbox.mark_set("insert", begin)
	event.widget.see(textbox.index("insert"))

#TODO: kill word, and kill if inside s-exp
def kill(event):
	"""Deletes line if insertion cursor is at beginning or end inside a Text widget"""

	textbox = event.widget
	if textbox.get("insert") == "\n" or textbox.index("insert") == textbox.index("insert linestart"):
		textbox.delete("insert linestart", "insert lineend+1c")

def end_of_line(event):
	"""Moves insertion cursor to the end of the current line inside a Text widget"""

	textbox = event.widget
	textbox.tag_remove("mchar", "1.0", "end")
	textbox.mark_set("insert", "insert lineend")

def beginning_of_line(event):
	"""Moves insertion cursor to the beginning of the current line inside a Text widget"""
	
	textbox = event.widget
	textbox.tag_remove("mchar", "1.0", "end")
	textbox.tag_add("mchar", "insert linestart", "insert linestart+1c")
	textbox.tag_config("mchar", foreground = "white")
	textbox.mark_set("insert", "insert linestart")

def directory_jump_expand_parent(event):
	"""jump to current expanded items parent directory"""

	item = event.widget.get("insert linestart", "insert lineend")
	tabs = countleadingtabs(item)
	if tabs == 0:
		return "break"

	above = event.widget.index("insert linestart")
	coords = event.widget.index("insert linestart").split(".")
	
	for i in range(1, int(coords[0])):
		if int(coords[0])-1 >= 0:	
			above = str(int(coords[0])-i) + "." + str(int(coords[1]))
			above_item = event.widget.get(above, f"{above} lineend")
			tabs2 = countleadingtabs(above_item)
				
			if tabs2 == tabs-1:
				event.widget.mark_set("insert", f"{above} lineend")
				event.widget.see(f"{above} lineend")
				break

def edit_mode(event, isedit):
	"""Keybindings when inside edit mode"""

	buffer.buffers['cl'][-1].cltext.set("")
	if isedit.get() == False:
		return
	if event.keysym == config.config['movement']['left']:
		left(event)
	elif event.keysym == 'u' and config.config['movement']['left'] == '':
		left(event)

	elif event.keysym == config.config['movement']['right']:
		right(event)
	elif event.keysym == 'o' and config.config['movement']['right'] == '':
		right(event)
	
	elif event.keysym == config.config['movement']['up']:
		up(event)
	elif event.keysym == 'i' and config.config['movement']['up'] == '':
		up(event)
		
	elif event.keysym == config.config['movement']['down']:
		down(event)
	elif event.keysym == 'j' and config.config['movement']['down'] == '':
		down(event)

	elif event.keysym == 's':
		savefile(event)

	elif event.keysym == 'p':
		event.widget.delete("insert-1c")

	elif event.keysym == 'k':
		kill(event)

	elif event.keysym == 'U':
		beginning_of_line(event)

	elif event.keysym == 'O':
		end_of_line(event)

	elif event.keysym == 'a': #go to commandline
		event.widget.tag_remove("mchar", "1.0", "end")
		buffer.buffers['cl'][-1].focus_set()

	elif event.keysym == 'f':
		toggle_modal(event, isedit) 

	return "break"

#open directory mode in parent directory, specified directory, or default directory
def cl_dir():
	pass

def cl_commands(event, buffers):
	command = event.widget.get()
	if command == 'e':
		buffers['files'][-1].focus_set()
		buffers['files'][-1].lift()
	if command == 'dir':
			buffer.DirectoryBuffer("D:\\all",("Roboto Mono", 10))
			buffers['current'].focus_set()
	event.widget.cltext.set("")

def directory_mode(event):
	if event.keysym == config.config['movement']['left']:
		left(event)
	elif event.keysym == 'u' and config.config['movement']['left'] == '':
		left(event)

	elif event.keysym == config.config['movement']['right']:
		right(event)
	elif event.keysym == 'o' and config.config['movement']['right'] == '':
		right(event)
	
	elif event.keysym == config.config['movement']['up']:
		up(event)
	elif event.keysym == 'i' and config.config['movement']['up'] == '':
		up(event)
		
	elif event.keysym == config.config['movement']['down']:
		down(event)
	elif event.keysym == 'j' and config.config['movement']['down'] == '':
		down(event)

	elif event.keysym == 'I':
		directory_jump_expand_parent(event)

	elif event.keysym == 'a':
		event.widget.tag_remove("mchar", "1.0", "end")
		buffer.buffers['cl'][-1].focus_set()
	return "break"

def directory_enter(event):
	# path = event.widget.path_expansion
	# item = event.widget.get("insert linestart", "insert lineend")
	# if item == "..":
		# if "\\" in path:
			# path = path[:path.rindex('\\')]
	# else:
		# path = path + "\\" + item.strip()
	# if "\\" not in path:
		# path = path + "\\"
	# print("path expansion: " + path)
	item = event.widget.get("insert linestart", "insert lineend")
	tabs = countleadingtabs(item)
	path = getfilepath(item, tabs, event) #item, tabs, event
	if os.path.isdir(path):
		buffer.DirectoryBuffer(path, ("Roboto Mono", 10))
	elif os.path.isfile(path):
		buffer.FileBuffer(path, item, ("Roboto Mono", 10))
	return "break"


def directory_expand(event):
	item = event.widget.get("insert linestart", "insert lineend")
	tabs = countleadingtabs(item)
	item = item.strip()
	#collapse, directory
	coords = event.widget.index("insert linestart").split(".")
	for i in range(1, 1000):
		below = str(int(coords[0])+1) + ".0" 
		check_string = event.widget.get(below, f"{below} lineend+1c")
		below_tabs = countleadingtabs(check_string)
		if below_tabs > tabs:
			event.widget.delete(below, f"{below} lineend+1c") #f"{below} lineend+1c")

		elif tabs >= below_tabs and i > 1:
			return "break"
		else: 
			break
		
	curr_path = getfilepath(item, tabs, event)
	event.widget.path_expansion = curr_path

	if os.path.isdir(curr_path):
		event.widget.mark_set("insert", "insert lineend")
		files = [file for file in os.listdir(curr_path)]
		tabs = '\t' if tabs == 0 else'\t'*(tabs+1)
		for file in files:
			event.widget.insert("insert lineend", f"\n{tabs}{file}")
	return "break"

def countleadingtabs(item):
	tabs = 0
	for c in item:
		if c == '\t':
			tabs += 1
		else:
			break
	return tabs

def getfilepath(item, tabs, event):
	list = ["\\" + item.strip()]
	coords = event.widget.index("insert linestart").split(".")
	count = 0
	for i in range(1, 100000):
		above = str(int(coords[0])-i) + ".0"
		above_item = event.widget.get(above, f"{above} lineend")
		above_tabs = countleadingtabs(above_item)
		if above_tabs < tabs-count:
			list.append("\\" + above_item.strip())
			count += 1
		if tabs-count == 0:
			break
		if above_tabs == 0:
			break
	list.reverse()
	print(list)
	print(event.widget.path + "".join(list))
	return event.widget.path + "".join(list)
    
def savefile(event):
	file = open(event.widget.file_path, 'w')
	file.write(event.widget.get(1.0, END))
	file.close()
	buffer.buffers['cl'][-1].cltext.set("FILE SAVED")
