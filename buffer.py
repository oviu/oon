import tkinter as tk
import bindings

buffers = {'files': [], 'directories' : []}

class FileBuffer(tk.Text):
	def __init__(self,file_path, file_name, window, font):
		super().__init__(window, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "white", foreground = "black", insertofftime = 0)
		self.bind('<Shift-space>', bindings.toggle_modal)
		self.bind('<Key>', bindings.edit_mode)

		self.file_name = file_name
		self.file_path = file_path

		buffers['files'].append(self)

class DirectoryBuffer(tk.Text):
	def __init__(self, directory, window, font):
		super().__init__(window, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "black", foreground = "white", insertofftime = 0)
		super().configure(blockcursor = True)

		self.directory = directory

		buffers['directories'].append(self)



		

