from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from master_frag import *
import time
import os

src_fr_filename = "/PATH/TO/INPUT/FILE"
dest_fr_location = os.path.dirname(os.path.realpath(__file__)) + '/OUT_FOLDER/'
n = 4

decor_width = 18

class Demo1:
    def __init__(self, root):
        self.root = root

        # Fragmentation Window Area
        frag_frame = LabelFrame(root, text=" Fragment File ")
        frag_frame.grid(row=0, sticky='W', \
                 padx=5, pady=5, ipadx=5, ipady=5)

        self.r1_label = Label(frag_frame, text="Input File: ", width=decor_width)
        self.r1_path = Entry(frag_frame, width=56, fg="red") 
        self.r1_btn = Button(frag_frame, text="Browse", command=self.pick_file) 
        self.r1_label.grid(row=0, column=0)
        self.r1_path.grid(row=0, column=1)
        self.r1_btn.grid(row=0, column=2)

        self.r2_label = Label(frag_frame, text="Output Destination: ", width=decor_width)
        self.r2_path = Entry(frag_frame, width=56)
        self.r2_btn = Button(frag_frame, text="Browse", command=self.pick_folder)
        self.r2_label.grid(row=1, column=0)
        self.r2_path.grid(row=1, column=1)
        self.r2_btn.grid(row=1, column=2)

        self.r3_label = Label(frag_frame, text="Number of Fragments: ", width=decor_width)
        self.r3_n_field = Entry(frag_frame, width=5)
        self.r3_ERROR_field = Label(frag_frame, text="")
        self.r3_label.grid(row=2, column=0)
        self.r3_n_field.grid(row=2, column=1, sticky=W)
        self.r3_ERROR_field.grid(row=2, column=1)

        self.frag_btn = Button(frag_frame, text="Fragment", width=10, command=self.frag_file).grid(row=4,column=1)


        # Reassembly Window Area
        reasm_frame = LabelFrame(root, text=" Reassemble Fragments ")
        reasm_frame.grid(row=2, sticky='W', \
                     padx=5, pady=5, ipadx=5, ipady=5)

        self.r4_label = Label(reasm_frame, text="Fragments Folder: ", width=decor_width)
        self.r4_path = Entry(reasm_frame, width=56)
        self.r4_btn = Button(reasm_frame, text="Choose Folder", command=self.pick_folder)
        self.r4_label.grid(row=0, column=0)
        self.r4_path.grid(row=0, column=1)
        self.r4_btn.grid(row=0, column=2)

        self.reasm_btn = Button(reasm_frame, text="Reassemble", width=10, command=self.reasm_file).grid(row=1,column=1)


        self.refresh()
        

    def refresh(self):
        self.r1_path.delete(0, 'end')
        self.r1_path.insert(0, src_fr_filename)

        self.r2_path.delete(0, 'end')
        self.r2_path.insert(0, dest_fr_location)

        self.r3_n_field.delete(0, 'end')
        self.r3_n_field.insert(0, str(n))

        self.r4_path.delete(0, 'end')
        self.r4_path.insert(0, dest_fr_location)

    def frag_file(self):
        global n
        try:
            n = int(self.r3_n_field.get())
        except:
            self.r3_ERROR_field.config(text="ERROR: invalid input for number of fragments", fg="red")
            return
        n = int(self.r3_n_field.get())
        print("input file: {}".format(src_fr_filename))
        print("output location: {}".format(dest_fr_location))
        print("n: {}".format(n))
        partition_file(("python", src_fr_filename, n))

    def reasm_file(self):
        reassemble(("python", dest_fr_location))


    def pick_file(self):
        global src_fr_filename
        selected_filename = askopenfilename()
        if selected_filename != "" and selected_filename != src_fr_filename:
            src_fr_filename = selected_filename
        self.r1_path.config(fg="black")
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
    root.geometry('{}x{}'.format(826, 400))
    root.mainloop()

if __name__ == '__main__':
    main()