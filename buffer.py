import tkinter as tk
import binding

buffers = {'files': [], 'directories' : []}
root = tk.Tk()

class FileBuffer(tk.Text):
	isedit = tk.BooleanVar()
	isedit.set("False")

	def __init__(self,file_path, file_name, font):
		super().__init__(root, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "white", foreground = "black", insertofftime = 0)
		self.bind('<Shift-space>', lambda event: binding.toggle_modal(event, self.isedit))
		self.bind('<Key>', lambda event: binding.edit_mode(event,self.isedit))

		self.file_name = file_name
		self.file_path = file_path

		buffers['files'].append(self)

class DirectoryBuffer(tk.Text):
	def __init__(self, directory, font):
		super().__init__(root, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "black", foreground = "white", insertofftime = 0)
		super().configure(blockcursor = True)

		self.directory = directory

		buffers['directories'].append(self)


class Statusline(tk.Label):
	mode_string = tk.StringVar()
	def __init__(self, directory, font):
		super().__init__(root, textvariable = mode_string)
		

