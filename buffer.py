import tkinter as tk
import binding

buffers = {'files': [], 'directories' : []}
root = tk.Tk()

class FileBuffer(tk.Text):

	def __init__(self,file_path, file_name, font):
		super().__init__(root, font = font)
		super().grid(row = 0, column = 0, sticky = 'nswe')
		super().configure(background = "white", foreground = "black", insertofftime = 0)

		self.isedit = tk.BooleanVar()
		self.isedit.set("False")

		self.bind('<Shift-space>', lambda event: binding.toggle_modal(event, self.isedit))
		self.bind('<Key>', lambda event: binding.edit_mode(event,self.isedit))

		self.statusline = Statusline(("Roboto Mono", 10))

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

		self.statusline = Statusline(("Roboto Mono", 10))

		buffers['directories'].append(self)

class Statusline(tk.Label):
	def __init__(self, font):
		self.mode_string = tk.StringVar()
		self.mode_string.set("")
		super().__init__(root, textvariable = self.mode_string)
		super().grid(row=1, column=0, sticky= "swe")

	def status_callback():
		pass


class Commandline(tk.Entry):
	pass
