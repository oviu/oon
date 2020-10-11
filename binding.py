from tkinter import *


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


def edit_mode(event, isedit):
	if isedit.get() == True:
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
#	elif event.keysym == 'a':
		#cl_active.set(True)

	if event.keysym == 'f':
		toggle_modal(event, isedit)
		return "break"
	return "break"