from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from master_frag import *
import time
import os

src_fr_filename = "/PATH/TO/INPUT/FILE"
dest_fr_location = os.path.dirname(os.path.realpath(__file__)) + '/OUT_FOLDER/'
n = 4


class Demo1:
    def __init__(self, master):
        self.master = master

        self.header = Label(master, text="Fragmentation").grid(row=0, column= 1)

        self.e1_label = Label(master, text="Input file: ")
        self.e1_btn = Button(master, text="Choose File", command=self.pick_file)
        self.e1_path = Entry(master, width=56, fg="red")

        self.e2_label = Label(master, text="Output destination: ")
        self.e2_btn = Button(master, text="Choose Folder", command=self.pick_folder)
        self.e2_path = Entry(master, width=56)

        self.e3_label = Label(master, text="Number of fragments: ")
        self.e3_n_field = Entry(master, width=5)
        self.e3_ERROR_field = Label(master, text="")

        self.e1_label.grid(row=1, column=0, sticky=W)
        self.e1_btn.grid(row=1, column=2)
        self.e1_path.grid(row=1, column=1)

        self.e2_label.grid(row=2, column=0, sticky=W)
        self.e2_btn.grid(row=2, column=2)
        self.e2_path.grid(row=2, column=1)

        self.e3_label.grid(row=3, column=0, sticky=W)
        self.e3_n_field.grid(row=3, column=1, sticky=W)
        self.e3_ERROR_field.grid(row=3, column=1)

        self.frag_btn = Button(master, text="Fragment", width=30, command=self.frag_file).grid(row=4,column=1)

        self.refresh()

    def refresh(self):
        global fr_filename
        global dest_fr_location
        self.e1_path.delete(0, 'end')
        self.e1_path.insert(0, src_fr_filename)

        self.e2_path.delete(0, 'end')
        self.e2_path.insert(0, dest_fr_location)

    def frag_file(self):
        global n
        try:
            n = int(self.e3_n_field.get())
        except:
            self.e3_ERROR_field.config(text="ERROR: invalid input for number of fragments", fg="red")
            return
        n = int(self.e3_n_field.get())
        print("input file: {}".format(src_fr_filename))
        print("output location: {}".format(dest_fr_location))
        print("n: {}".format(n))
        partition_file(("python", src_fr_filename, n))


    def pick_file(self):
        global src_fr_filename
        selected_filename = askopenfilename()
        if selected_filename != "" and selected_filename != src_fr_filename:
            src_fr_filename = selected_filename
        self.e1_path.config(fg="black")
        self.refresh()

    def pick_folder(self):
        global dest_fr_location
        selected_dir = askdirectory() + '/'
        if selected_dir != "" and selected_dir != dest_fr_location:
            dest_fr_location = selected_dir
        self.refresh()

def main(): 
    root = Tk()
    app = Demo1(root)
    root.resizable(width=False, height=False)
    root.geometry('{}x{}'.format(800, 400))
    root.mainloop()

if __name__ == '__main__':
    main()