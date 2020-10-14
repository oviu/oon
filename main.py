import buffer
from tkinter import *

def main():
	cl = buffer.Commandline(buffer.buffers, ("Roboto Mono", 10))
	start_buffer = buffer.FileBuffer("main.py", "main.py", ("Roboto Mono", 10))
	buffer.root.mainloop()

if __name__ == '__main__':
	main()











