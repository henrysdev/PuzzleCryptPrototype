from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
import master_frag
import time
import os.path

src_fr_filename = "/PATH/TO/INPUT/FILE"
dest_fr_location = os.path.dirname(os.path.realpath(__file__)) + "/OUT_FOLDER/"
n = 4

label_width = 18
x_padding = 5
y_padding = 2

class Demo1:
    def __init__(self, root):
        self.root = root

        root.title('PuzzleCrypt')

        # Fragmentation Window Area
        frag_frame = LabelFrame(root, text=" Fragment File ")
        frag_frame.grid(row=0, sticky=W, \
                 padx=5, pady=5, ipadx=5, ipady=5)

        self.r1_label = Label(frag_frame, text="Input File: ", width=label_width)
        self.r1_path = Entry(frag_frame, width=56) 
        self.r1_btn = Button(frag_frame, height=1, text="Browse...", command=self.pick_file) 
        self.r1_label.grid(row=0, column=0, padx=x_padding, pady=y_padding)
        self.r1_path.grid(row=0, column=1, padx=x_padding, pady=y_padding)
        self.r1_btn.grid(row=0, column=2, padx=x_padding, pady=y_padding)

        self.r2_label = Label(frag_frame, text="Output Destination: ", width=label_width)
        self.r2_path = Entry(frag_frame, width=56)
        self.r2_btn = Button(frag_frame, height=1, text="Browse...", command=self.pick_folder)
        self.r2_label.grid(row=1, column=0, padx=x_padding, pady=y_padding)
        self.r2_path.grid(row=1, column=1, padx=x_padding, pady=y_padding)
        self.r2_btn.grid(row=1, column=2, padx=x_padding, pady=y_padding)

        self.r3_label = Label(frag_frame, text="Number of Fragments: ", width=label_width)
        self.r3_n_field = Entry(frag_frame, width=5)
        self.r3_label.grid(row=2, column=0, padx=x_padding, pady=y_padding)
        self.r3_n_field.grid(row=2, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r4_label = Label(frag_frame, text="Encryption Password: ", width=label_width)
        self.r4_pword_field = Entry(frag_frame, show="*", width=14)
        self.r4_label.grid(row=3, column=0, padx=x_padding, pady=y_padding)
        self.r4_pword_field.grid(row=3, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r5_label = Label (frag_frame, text="Re-enter Password: ", width=label_width)
        self.r5_reenter_pword = Entry(frag_frame, show="*", width=14)
        self.r5_label.grid(row=4, column=0, padx=x_padding, pady=y_padding)
        self.r5_reenter_pword.grid(row=4, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r6_ERROR_field = Label(frag_frame, text="")
        self.r6_ERROR_field.grid(row=5, column=1, padx=x_padding, pady=y_padding)

        self.frag_btn = Button(frag_frame, text="Fragment", width=10, command=self.frag_file, state=DISABLED)
        self.frag_btn.grid(row=6,column=1, padx=x_padding, pady=y_padding)

        root.bind("<Key>", self.button_state)

        # Reassembly Window Area
        reasm_frame = LabelFrame(root, text=" Reassemble Fragments ")
        reasm_frame.grid(row=2, sticky=W, \
                     padx=5, pady=5, ipadx=5, ipady=5)

        self.r7_label = Label(reasm_frame, text="Fragments Folder: ", width=label_width)
        self.r7_path = Entry(reasm_frame, width=56)
        self.r7_btn = Button(reasm_frame, text="Browse...", command=self.pick_folder)
        self.r7_label.grid(row=0, column=0, padx=x_padding, pady=y_padding)
        self.r7_path.grid(row=0, column=1, padx=x_padding, pady=y_padding, sticky=W)
        self.r7_btn.grid(row=0, column=2, padx=x_padding, pady=y_padding)

        self.r8_label = Label(reasm_frame, text="Password: ")
        self.r8_pword_field = Entry(reasm_frame, width=14, show="*")
        self.r8_pword_field.grid(row=1, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r8_label.grid(row=1, column=0, padx=x_padding, pady=y_padding)
        self.r9_ERROR_field = Label(reasm_frame, text="")
        self.r9_ERROR_field.grid(row=2, column=1, padx=x_padding, pady=y_padding)

        self.reasm_btn = Button(reasm_frame, text="Reassemble", width=10, command=self.reasm_file)
        self.reasm_btn.grid(row=3,column=1, padx=x_padding, pady=y_padding)

        self.refresh(init=True)
    
    # button state refresh
    def button_state(self, key):
        if self.f_error_check():
            self.frag_btn.config(state=NORMAL)
        else:
            self.frag_btn.config(state=DISABLED)


    # update field entry values
    def refresh(self, init=False):
        self.r1_path.delete(0, 'end')
        self.r1_path.insert(0, src_fr_filename)

        self.r2_path.delete(0, 'end')
        self.r2_path.insert(0, dest_fr_location)

        self.r3_n_field.delete(0, 'end')
        self.r3_n_field.insert(0, str(n))

        self.r7_path.delete(0, 'end')
        self.r7_path.insert(0, dest_fr_location)

        if init == False:
            if self.f_error_check():
                self.frag_btn.config(state=NORMAL)

    # fragmentation error check
    def f_error_check(self):
        if os.path.isfile(self.r1_path.get()) == False:
            self.r6_ERROR_field.config(text="ERROR: input file not found", fg="red")
            return False

        if os.path.isdir(self.r2_path.get()) == False:
            self.r6_ERROR_field.config(text="ERROR: output destination not found", fg="red")
            return False

        try:
            int(self.r3_n_field.get())
        except:
            self.r6_ERROR_field.config(text="ERROR: invalid input for number of fragments", fg="red")
            return False

        if len(self.r4_pword_field.get()) > 10:
            if self.r4_pword_field.get() != self.r5_reenter_pword.get():
                self.r6_ERROR_field.config(text="ERROR: passwords do not match", fg="red")
                return False
        else:
            self.r6_ERROR_field.config(text="ERROR: password must be at least 10 characters", fg="red")
            return False

        self.r6_ERROR_field.config(text="")
        return True

    # reassembly error check
    def r_error_check(self):
        if len(self.r8_pword_field.get()) == 0:
            self.r9_ERROR_field.config(text="ERROR: must enter decryption password", fg="red")
            return False
        return True

    # call fragmentation function in master
    def frag_file(self):
        if self.f_error_check():
            n = int(self.r3_n_field.get())
            src_fr_filename = self.r1_path.get()
            secret_key = self.r4_pword_field.get()
            output = master_frag.partition_file(("python", src_fr_filename, n, secret_key))
            if output[0]:
                self.r6_ERROR_field.config(text=output[1], fg="green")
            else:
                self.r6_ERROR_field.config(text=output[1], fg="red")

    # call reassembly function in master
    def reasm_file(self):
        if self.r_error_check():
            secret_key = self.r8_pword_field.get()
            output = master_frag.reassemble(("python", dest_fr_location, secret_key))
            if output[0]:
                self.r9_ERROR_field.config(text=output[1], fg="green")
            else:
                self.r9_ERROR_field.config(text=output[1], fg="red")

    # pick file from system file browser
    def pick_file(self):
        global src_fr_filename
        selected_filename = askopenfilename()
        if selected_filename != "" and selected_filename != src_fr_filename:
            src_fr_filename = selected_filename
        self.r1_path.config(fg="black")
        self.refresh()

    # pick folder from system file browser
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