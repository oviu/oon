import buffer
import binding
from tkinter import *


def main():
	buffer.FileBuffer("test", "test", ("Roboto Mono", 10))	
	buffer.root.mainloop()

if __name__ == '__main__':
	main()



