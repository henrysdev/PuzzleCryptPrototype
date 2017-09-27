from tkinter import *
from tkinter import font
from tkinter.filedialog import askopenfilename, askdirectory
import master_frag
import time
import getpass
import os.path
import platform

system_type = platform.system()
# if system_type== "Darwin":
#     self.r9_path.config(text='/Users/' + getpass.getuser() + '/Desktop/')
# elif system_type == "Linux":
#     self.r9_path.config(text='/home/' + getpass.getuser() + '/Desktop/')

n = 4

min_password_length = 10

label_width = 24
x_padding = 5
y_padding = 2

class Demo1:
    def __init__(self, root):
        self.root = root

        root.title('PuzzleCrypt')

        # Fragmentation Window Area
        title_font = font.Font(family="Helvetica", size=14, weight="bold")
        frag_frame = LabelFrame(root, text=" Fragment File ", name="frag_frame", font=title_font)
        frag_frame.grid(row=0, sticky=W, \
                 padx=5, pady=5, ipadx=5, ipady=10)

        self.r1_label = Label(frag_frame, text="Input File: ", width=label_width)
        self.r1_path = Entry(frag_frame, width=56)
        self.r1_btn = Button(frag_frame, height=1, text="Browse...", command=self.pick_file) 
        self.r1_label.grid(row=0, column=0, padx=x_padding, pady=y_padding)
        self.r1_path.grid(row=0, column=1, padx=x_padding, pady=y_padding)
        self.r1_btn.grid(row=0, column=2, padx=x_padding, pady=y_padding)

        self.r2_label = Label(frag_frame, text="Number of Fragments: ", width=label_width)
        self.r2_n_field = Entry(frag_frame, width=5)
        self.r2_label.grid(row=1, column=0, padx=x_padding, pady=y_padding)
        self.r2_n_field.grid(row=1, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r3_label = Label(frag_frame, text="Encryption Password: ", width=label_width)
        self.r3_pword_field = Entry(frag_frame, show="*", width=14)
        self.r3_label.grid(row=2, column=0, padx=x_padding, pady=y_padding)
        self.r3_pword_field.grid(row=2, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r4_label = Label (frag_frame, text="Re-enter Password: ", width=label_width)
        self.r4_reenter_pword = Entry(frag_frame, show="*", width=14)
        self.r4_label.grid(row=3, column=0, padx=x_padding, pady=y_padding)
        self.r4_reenter_pword.grid(row=3, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r5_label = Label(frag_frame, text="Output Folder (for fragments): ", width=label_width)
        self.r5_path = Entry(frag_frame, width=56)
        self.r5_btn = Button(frag_frame, height=1, text="Browse...", command=self.pick_o_folder)
        self.r5_label.grid(row=4, column=0, padx=x_padding, pady=y_padding)
        self.r5_path.grid(row=4, column=1, padx=x_padding, pady=y_padding)
        self.r5_btn.grid(row=4, column=2, padx=x_padding, pady=y_padding)

        self.r6_ERROR_field = Label(frag_frame, text="")
        self.r6_ERROR_field.grid(row=5, column=1, padx=x_padding, pady=y_padding)

        self.frag_btn = Button(frag_frame, text="Fragment", width=10, command=self.frag_file, state=DISABLED)
        self.frag_btn.grid(row=6,column=1, padx=x_padding, pady=y_padding)

        root.bind("<Key>", self.button_state)

        # Reassembly Window Area
        reasm_frame = LabelFrame(root, text=" Reassemble Fragments ", name="reasm_frame", font=title_font)
        reasm_frame.grid(row=2, sticky=W, \
                     padx=5, pady=10, ipadx=5, ipady=5)

        self.r7_label = Label(reasm_frame, text="Input Folder (fragments): ", width=label_width)
        self.r7_path = Entry(reasm_frame, width=56)
        self.r7_btn = Button(reasm_frame, text="Browse...", command=self.pick_i_folder)
        self.r7_label.grid(row=0, column=0, padx=x_padding, pady=y_padding)
        self.r7_path.grid(row=0, column=1, padx=x_padding, pady=y_padding, sticky=W)
        self.r7_btn.grid(row=0, column=2, padx=x_padding, pady=y_padding)

        self.r8_label = Label(reasm_frame, text="Decryption Password: ")
        self.r8_pword_field = Entry(reasm_frame, width=14, show="*")
        self.r8_label.grid(row=1, column=0, padx=x_padding, pady=y_padding)
        self.r8_pword_field.grid(row=1, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r9_label = Label(reasm_frame, text="Output Location (for file): ")
        self.r9_path = Entry(reasm_frame, width=56)
        self.r9_btn = Button(reasm_frame, text="Browse...", command=self.pick_final_folder)
        self.r9_label.grid(row=2, column=0, padx=x_padding, pady=y_padding)
        self.r9_path.grid(row=2, column=1, sticky=W, padx=x_padding, pady=y_padding)
        self.r9_btn.grid(row=2, column=2, padx=x_padding, pady=y_padding)

        self.r10_label = Label(reasm_frame, text="Output Filename (with .extension): ")
        self.r10_filename_field = Entry(reasm_frame, width=14)
        self.r10_label.grid(row=3, column=0, padx=x_padding, pady=y_padding)
        self.r10_filename_field.grid(row=3, column=1, sticky=W, padx=x_padding, pady=y_padding)

        self.r11_ERROR_field = Label(reasm_frame, text="")
        self.r11_ERROR_field.grid(row=4, column=1, padx=x_padding, pady=y_padding)

        self.reasm_btn = Button(reasm_frame, text="Reassemble", width=10, command=self.reasm_file, state=DISABLED)
        self.reasm_btn.grid(row=5,column=1, padx=x_padding, pady=y_padding)

        if system_type == "Darwin":
            os.chdir("/home/".format(getpass.getuser()))
        elif system_type == "Linux":
            os.chdir("/home/{}/".format(getpass.getuser()))
    
    # button state refresh
    def button_state(self, event):
        parent = event.widget.winfo_parent()
        if "frag_frame" in parent:
            if self.f_error_check():
                self.frag_btn.config(state=NORMAL)
            else:
                self.frag_btn.config(state=DISABLED)
        elif "reasm_frame" in parent:
            if self.r_error_check():
                self.reasm_btn.config(state=NORMAL)
            else:
                self.reasm_btn.config(state=DISABLED)

    def f_clear_input(self):
        self.r1_path.delete(0, 'end')
        self.r2_n_field.delete(0, 'end')
        self.r3_pword_field.delete(0,'end')
        self.r4_reenter_pword.delete(0, 'end')

    def r_clear_input(self):
        self.r8_pword_field.delete(0, 'end')

    # fragmentation error check
    def f_error_check(self):
        if os.path.isfile(self.r1_path.get()) == False:
            self.r6_ERROR_field.config(text="ERROR: input file not found", fg="red")
            return False

        try:
            int(self.r2_n_field.get())
        except:
            self.r6_ERROR_field.config(text="ERROR: invalid input for number of fragments", fg="red")
            return False
        if int(self.r2_n_field.get()) <= 1 or int(self.r2_n_field.get()) > 99:
            self.r6_ERROR_field.config(text="ERROR: number of fragments must be an integer between 2 and 99", fg="red")
            return False

        if len(self.r3_pword_field.get()) >= min_password_length:
            if self.r3_pword_field.get() != self.r4_reenter_pword.get():
                self.r6_ERROR_field.config(text="ERROR: passwords do not match", fg="red")
                return False
        else:
            self.r6_ERROR_field.config(text="ERROR: password must be at least 10 characters", fg="red")
            return False

        print(self.r5_path.get())
        if os.path.isdir(self.r5_path.get()) == False:
            self.r6_ERROR_field.config(text="ERROR: output destination not found", fg="red")
            return False
        
        self.r6_ERROR_field.config(text="")
        return True

    # reassembly error check
    def r_error_check(self):
        if len(self.r8_pword_field.get()) == 0:
            self.r11_ERROR_field.config(text="ERROR: must enter decryption password", fg="red")
            return False

        if os.path.isdir(self.r9_path.get()) == False:
            self.r11_ERROR_field.config(text="ERROR: output destination not found", fg="red")
            return False

        if len(self.r10_filename_field.get()) == 0:
            self.r11_ERROR_field.config(text="ERROR: must enter an output filename", fg="red")
            return False
        return True

    # call fragmentation function in master
    def frag_file(self):
        if self.f_error_check():
            n = int(self.r2_n_field.get())
            src_file = self.r1_path.get()
            secret_key = self.r3_pword_field.get()
            dest_loc = self.r5_path.get()
            output = master_frag.partition_file(("python", src_file, n, secret_key, dest_loc))
            if output[0]:
                self.r6_ERROR_field.config(text=output[1], fg="green")
                self.f_clear_input()
            else:
                self.r6_ERROR_field.config(text=output[1], fg="red")

    # call reassembly function in master
    def reasm_file(self):
        if self.r_error_check():
            secret_key = self.r8_pword_field.get()
            filename = self.r10_filename_field.get()
            input_loc = self.r5_path.get()
            output = master_frag.reassemble(("python", input_loc, secret_key, self.r9_path.get(), filename))
            if output[0]:
                self.r11_ERROR_field.config(text=output[1], fg="green")
                self.r_clear_input()
            else:
                self.r11_ERROR_field.config(text=output[1], fg="red")

    # pick file from system file browser
    def pick_file(self):
        selected_filename = askopenfilename()
        self.r1_path.delete(0)
        self.r1_path.insert(0, selected_filename)
        if self.f_error_check():
            self.frag_btn.config(state=NORMAL)
        else:
            self.frag_btn.config(state=DISABLED)

    # pick folder from system file browser
    def pick_o_folder(self):
        selected_dir = askdirectory() + '/'
        self.r5_path.delete(0)
        self.r5_path.insert(0, selected_dir)
        if self.f_error_check():
            self.frag_btn.config(state=NORMAL)
        else:
            self.frag_btn.config(state=DISABLED)

    # pick folder from system file browser
    def pick_i_folder(self):
        selected_dir = askdirectory() + '/'
        self.r7_path.delete(0)
        self.r7_path.insert(0, selected_dir)
        if self.r_error_check():
            self.reasm_btn.config(state=NORMAL)
        else:
            self.reasm_btn.config(state=DISABLED)

    # pick folder from system file browser for final output
    def pick_final_folder(self):
        print("called")
        selected_dir = askdirectory() + '/'
        self.r9_path.delete(0)
        self.r9_path.insert(0, selected_dir)
        if self.r_error_check():
            self.reasm_btn.config(state=NORMAL)
        else:
            self.reasm_btn.config(state=DISABLED)

def main(): 
    root = Tk()
    app = Demo1(root)
    root.resizable(width=False, height=False)
    #root.geometry('{}x{}'.format(826, 400))
    root.mainloop()

if __name__ == '__main__':
    main()