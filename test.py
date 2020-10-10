import buffer
import bindings
from tkinter import *


bindings.Globals.window.title("test")
bindings.Globals.window.configure(background="black")
buffer.FileBuffer("test", "test", bindings.Globals.window, ("Roboto Mono", 10))



bindings.Globals.window.mainloop()

