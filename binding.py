from tkinter import *
import config

def toggle_modal(event, isedit):
	if isedit.get() == True:
		event.widget.config(blockcursor=False)
		isedit.set(False)
		event.widget.tag_remove("mchar", "1.0", "end") #last
	else:
		isedit.set(True)
		event.widget.tag_add("mchar", "insert", "insert+1c") 
		event.widget.tag_config("mchar", foreground="white")
		event.widget.config(blockcursor=True)
	return "break"

def left(event, isedit):
	if isedit.get() == False:
		return
	event.widget.tag_remove("mchar", "1.0", "end")
	begin = event.widget.index("insert-1c")
	coords = event.widget.index("insert-1c").split(".")
	begin_plus_one = coords[0] + "." + str(int(coords[1]) + 1)
	event.widget.tag_add("mchar", begin, begin_plus_one)
	event.widget.tag_config("mchar", foreground="white")
	event.widget.mark_set("insert", "insert-1c")

def up(event, isedit):
	event.widget.tag_remove("mchar", "1.0", "end")
	begin = event.widget.index("insert")
	coords = event.widget.index("insert").split(".")
	if int(coords[0]) >= 1:
		begin = str(int(coords[0])-1) + "." + str(int(coords[1]))
		begin_plus_one = str(int(coords[0])-1) + "." + str(int(coords[1]) + 1)
		event.widget.tag_add("mchar", begin, begin_plus_one)
		event.widget.tag_config("mchar", foreground ="white")
		event.widget.mark_set("insert", begin)

def right(event, isedit):
	event.widget.tag_remove("mchar", "1.0", "end")
	begin = event.widget.index("insert+1c")
	coords = event.widget.index("insert+1c").split(".")
	print(int(coords[0]))
	begin_plus_one = coords[0] + "." + str(int(coords[1]) + 1)
	
	event.widget.tag_add("mchar", begin, begin_plus_one)
	event.widget.tag_config("mchar", foreground="white")
	event.widget.mark_set("insert", "insert+1c")

def down(event, isedit):
	event.widget.tag_remove("mchar", "1.0", "end")
	coords = event.widget.index("insert").split(".")
	begin =  str(int(coords[0])+1) + "." + str(int(coords[1]))
	begin_plus_one = str(int(coords[0])+1) + "." + str(int(coords[1]) + 1)
	event.widget.tag_add("mchar",  begin, begin_plus_one)
	event.widget.tag_config("mchar", foreground="white")
	event.widget.mark_set("insert", begin)

def kill(event, isedit):
	pass
def end_of_line(event, isedit):
	pass

def beginning_of_line(event, isedit):
	pass

def edit_mode(event, isedit):
	if isedit.get() == False:
		return
	#go left
	if event.keysym == config.config['left']:
		left(event, isedit)
	elif event.keysym == 'u' and config.config['left'] == '':
		left(event, isedit)

	#go right
	elif event.keysym == config.config['right']:
		right(event, isedit)
	elif event.keysym == 'o' and config.config['right'] == '':
		right(event, isedit)
	
	#go up
	elif event.keysym == config.config['up']:
		up(event, isedit)
	elif event.keysym == 'i' and config.config['up'] == '':
		up(event, isedit)
		
	#go down
	elif event.keysym == config.config['down']:
		down(event, isedit)
	elif event.keysym == 'j' and config.config['down'] == '':
		down(event, isedit)

	#backspace
	elif event.keysym == 'p':
		event.widget.delete("insert-1c")
	#delete line if at beginning of line or end of line
	elif event.keysym == 'k':
		#event.widget.tag_remove("mchar", "1.0", "end")
		if event.widget.get("insert") == "\n" or event.widget.index("insert") == event.widget.index("insert linestart"):
			event.widget.delete("insert linestart", "insert lineend+1c")

	#go to beginning of line
	elif event.keysym == 'U':
		event.widget.tag_remove("mchar", "1.0", "end")
		event.widget.tag_add("mchar", "insert linestart", "insert linestart+1c")
		event.widget.tag_config("mchar", foreground = "white")
		event.widget.mark_set("insert", "insert linestart")

	#go to end of line
	elif event.keysym == 'O':
		event.widget.tag_remove("mchar", "1.0", "end")
		event.widget.mark_set("insert", "insert lineend")

#	elif event.keysym == 'a':
		#cl_active.set(True)

	if event.keysym == 'f':
		toggle_modal(event, isedit) 
	return "break"
