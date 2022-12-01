from tkinter import *
import customtkinter

class App():
    def __init__(self, root):
        self.master = Frame(root)
        self.master.place(relx=.5, rely=.5, anchor=CENTER)
        self.value1 = IntVar()
        self.value2 = IntVar()
        self.string1 = StringVar()

        self.entry1 = customtkinter.CTkEntry(self.master, textvariable=self.value1)
        self.entry1.grid(row=0)

        self.slider1 = customtkinter.CTkSlider(self.master, from_=4, to=256, number_of_steps=256-4, command=self.slider_event_1, variable=self.value1)
        self.slider1.grid(row=1)

        print(type(self.value1))

        self.value1.trace("w",lambda x, y, z, entry=self.entry1, sv=self.value1: self.callback(entry, sv))
    
    def callback(self, entry, sv):
        if len(entry.get()) >= 1:
            if entry.get()[-1].isnumeric() == False:
                entry.delete((len(entry.get())-1), END)
        else:
            entry.insert(0, 0)
        if len(entry.get()) >= 2:
            if entry.get()[0] == '0':
                entry.delete(0, 1)
        if int(sv.get()) >= 256:
            entry.delete(0, END)
            entry.insert(0, '256')
    
    def slider_event_1(self, value):
        self.string1 = str(value)
        self.entry1.configure()

    def slider_event_2(self, value):
        self.string2 = str(value)
        self.entry2.configure()

if __name__ == '__main__':
    root = Tk()
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    app = App(root)
    root.mainloop()