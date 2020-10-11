import tkinter as tk
import binding

buffers = {'files': [], 'directories' : []}
root = tk.Tk()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
	
class FileBuffer(tk.Text):

	def __init__(self,file_path, file_name, font):
		super().__init__(root, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "white", foreground = "black", insertofftime = 0)

		self.bind('<Shift-space>', lambda event: binding.toggle_modal(event, self.isedit))
		self.bind('<KeyPress>', lambda event: binding.edit_mode(event,self.isedit))
		self.bind('<KeyRelease>', lambda event: self.get_rowcol(event))

		self.statusline = Statusline(("Roboto Mono", 10))
		self.isedit = tk.BooleanVar()
		self.curr_rowcol = tk.StringVar()
		self.curr_rowcol.trace("w", self.get_rowcol)
		
		self.file_name = file_name
		self.file_path = file_path

		buffers['files'].append(self)
		self.isedit.trace("w", self.statusline.mode_callback)
		self.isedit.set("False")
		
		self.statusline.set_name(self.file_name)

	def get_rowcol(self, *args):
		self.curr_rowcol.set(self.index("insert"))
		self.statusline.set_rolcol(self.curr_rowcol.get())
		return "break"
		
		
class DirectoryBuffer(tk.Text):
	def __init__(self, directory, font):
		super().__init__(root, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "black", foreground = "white", insertofftime = 0)
		super().configure(blockcursor = True)

		self.directory = directory

		self.statusline = Statusline(("Roboto Mono", 10))

		buffers['directories'].append(self)

class Statusline(tk.Label):
	def __init__(self, font):
		self.status = {'mode': "", 'index' : "", 'name': ""}
		self.status_string = tk.StringVar()
		self.status_string.set(f"{self.status['mode']}")
		super().__init__(root, textvariable = self.status_string, anchor = "w")
		super().grid(row=1, column=0, sticky= "swe")

	def mode_callback(self, *args):
		if root.getvar(name=args[0]) == True:
			self.status['mode'] = "<EDIT MODE>"
		else:
			self.status['mode'] = "--INSERT MODE--"
		self.set_status_string()

	def index_callback(self, *args):
		print(args)
		self.status['index'] = str(root.getvar(name=args[0]))
		print(self.status['index'])
		self.set_status_string()		

	def set_status_string(self):
		self.status_string.set(f"{self.status['mode']}    {self.status['index']}    {self.status['name']}")

	def set_rolcol(self, value):
		self.status['index'] = value
		self.set_status_string()

	def set_name(self, value):
		self.status['name'] = value
		self.set_status_string()
	
	#set file_type

class Commandline(tk.Entry):
	def __init__(self, font):
		self.cltext = tk.StringVar()
		super().__init__(root, textvariable = self.cltext)
		self.grid(row=2, column=0, sticky = "swe")

commandline = Commandline(("Roboto Mono", 10))
