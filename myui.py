import tkinter as tk
import mydb
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from shutil import *
import ast
import os

isInstructor = False
Lb1 = None
current_user = None

class LoginFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.user = tk.StringVar()
        self.password = tk.StringVar()
        self.initComponents()

    def initComponents(self):
        self.pack(expand=True)
        ttk.Label(self, text="User ").grid(column=0, row=4, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.user).grid(column=1, row=4)
        ttk.Label(self, text="Password ").grid(column=0, row=5, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.password).grid(column=1, row=5)

        ttk.Label(self, text='Welcome The Course', background="#a1dbcd").grid(row=1, column=0, columnspan=5)
        ttk.Label(self, text="Python Programming", background="#a1dbcd").grid(row=2, column=0,columnspan=5)
        ttk.Label(self, text='--------------------------------------------------------------', background="#a1dbcd").grid(
            row=3, column=0, columnspan=5)

        photo = tk.PhotoImage(file="UB.gif")
        photo_label = Label(self, image=photo)
        photo_label.image = photo
        photo_label.grid(column=0, row=0, columnspan=5)

        self.makeButtons()

    def makeButtons(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=0, row=6, columnspan=2, sticky=tk.E)
        ttk.Button(buttonFrame, text="login", command=self.login) \
            .grid(column=0, row=0, padx=5)
        ttk.Button(buttonFrame, text="Exit", command=self.parent.destroy) \
            .grid(column=1, row=0)

    def login(self):
        user = self.user.get()
        password = self.password.get()

        if self.user_aunthenticate(user, password):
            self.parent.destroy()
            newroot = tk.Tk()
            newroot.title("Main window ")
            newroot.configure(background="#a1dbcd")

            background_image = tk.PhotoImage(file="UB2.gif")
            background_label = tk.Label(newroot, image=background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            newroot.geometry("600x400")
            LoginSuccess(newroot)
            newroot.mainloop()
        else:
            message = "The username or password you entered were incorrect."
            messagebox.showinfo("Information", message)

    def user_aunthenticate(self, userid, password):
        global isInstructor
        global current_user
        people_list = mydb.get_people()
        for person in people_list:
            if person.id == int(userid):
                if person.password == password:
                    current_user = person
                    if person.isInstructor == "True":
                        isInstructor = True
                    else:
                        isInstructor = False
                    return True
        return False

class LoginSuccess(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.initComponents()
        self.newRoot = tk.Tk()

    def initComponents(self):
        self.pack(expand=True)
        ttk.Label(self, text="Welcome " + current_user.name + " to the app.").grid(row=0, column=0, columnspan=5)
        ttk.Label(self, text="Please select one of the options below:").grid(row=2, column=0, columnspan=5)
        ttk.Label(self, text='--------------------------------------------------------------',background="#a1dbcd").grid(
            row=3, column=0, columnspan=5)
        self.makeButtons()

    def makeButtons(self):
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=0, row=4,sticky = tk.W)
        ttk.Button(buttonFrame, text="Assigment", command=self.openAssignmentFrame).grid(column=0, row=0)
        ttk.Button(buttonFrame, text="Grade", command=self.openGradeFrame) \
            .grid(column=0, row=1, sticky = tk.W)
        ttk.Button(buttonFrame, text="Files", command=self.openFilesWindow) \
            .grid(column=0, row=2,sticky = tk.W)

    def openFilesWindow(self):
        self.newRoot = tk.Tk()
        self.newRoot.title("Files window ")
        self.newRoot.geometry("600x400")
        FileFrame(self.newRoot)
        self.newRoot.mainloop()

    def openAssignmentFrame(self):
        self.newRoot = tk.Tk()
        self.newRoot.title("Assigment")
        self.newRoot.geometry("900x400")
        AssignmentFrame(self.newRoot)
        self.newRoot.mainloop()

    def openGradeFrame(self):
        self.newRoot = tk.Tk()
        self.newRoot.title("Assignment")
        self.newRoot.geometry("900x500")
        if isInstructor:
            GradeFrameForInstructor(self.newRoot)
        else:
            GradeFrame(self.newRoot)
        self.newRoot.mainloop()

class GradeFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent=parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.label1 = ttk.Label(self.parent, text="Grade book for " + current_user.name,font=("Helvetica", 20))
        self.label1.grid(row=0, column=0)
        self.label2 = ttk.Label(self.parent,text='-----------------------------------------------------------------------------------')
        self.label2.grid(row=1, column=0)
        self.label3 = ttk.Label(self.parent, text='----------------------------------------------------')
        self.label3.grid(row=2, column=0)

        self.parent.title("Grade")
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="lavender")

        self.tree = ttk.Treeview( self.parent, columns=('Grade','maxPoint'))
        self.tree.heading('#0', text='assignmentName')
        self.tree.heading('#1', text='Grade')
        self.tree.heading('#2', text='maxPoint')

        self.tree.column('#0', stretch=tk.YES)
        self.tree.column('#1', stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)

        self.tree.grid(row=6, columnspan=5, sticky='nsew')
        self.treeview = self.tree
        assignments = mydb.get_assignments()
        for assignment in assignments:
            grades = ast.literal_eval(assignment.grades)
            if current_user.id in grades:
                grade = grades[current_user.id]
            else:
                grade = None
            self.treeview.insert('', 'end', text=assignment.name , \
                                 values=(grade, assignment.max_point))

class GradeFrameForInstructor(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent=parent
        self.initialize_user_interface()

    def initialize_user_interface(self):
        ttk.Label(self.parent, text="Grade Tool for Instructor ", font=("Helvetica", 20))\
            .grid(row=0, column=0, columnspan = 5)
        ttk.Label(self.parent, text="--------------------------------------------------- ", font=("Helvetica", 20))\
            .grid(row=1, column=0, columnspan = 5)
        ttk.Button(self.parent, text="Grade This student", command=self.gradestudent)\
            .grid(column=0, row=2, padx=5)

        ttk.Label(self.parent, text="StudentID:").grid(column=1, row=2, sticky=tk.E)
        self.student_entry = ttk.Entry(self.parent, width=25)
        self.student_entry.grid(column=2, row=2)
        ttk.Label(self.parent, text="AssignmentID:").grid(column=1, row=3, sticky=tk.E)
        self.assignment_entry = ttk.Entry(self.parent, width=25)
        self.assignment_entry.grid(column=2, row=3)
        ttk.Label(self.parent, text="Grade:").grid(column=1, row=4, sticky=tk.E)
        self.grade_entry=ttk.Entry(self.parent, width=25)
        self.grade_entry.grid(column=2, row=4)
        ttk.Button(self.parent, text="Browse submitted files", command=self.browse_file) \
            .grid(column=0, row=5, padx=5)
        self.grade_summary()


    def browse_file(self):
        filelocation = filedialog.askopenfilename(initialdir="submission", title="Select file")
        if filelocation:
            Title = os.path.basename(filelocation)
            savelocation = filedialog.asksaveasfilename(initialdir="submission", initialfile=Title, title="Save file to:")
            if savelocation:
                copy2(filelocation, savelocation)
                message = "File is saved"
                messagebox.showinfo("Information", message)

    def gradestudent(self):
        assignments = mydb.get_assignments()
        for assignment in assignments:
            if assignment.id == int(self.assignment_entry.get()):
                break
        grades = ast.literal_eval(assignment.grades)
        grades[int(self.student_entry.get())] = int(self.grade_entry.get())
        strgrades = str(grades)
        mydb.update_grade(self.assignment_entry.get(),strgrades)
        self.grade_summary()

    def grade_summary(self):
        students = mydb.get_people()
        assignments = mydb.get_assignments()
        i = 1
        ttk.Label(self.parent, text="Grade Summary ", font=("Helvetica", 16)) \
            .grid(row=8, column=0, columnspan=5)
        ttk.Label(self.parent, text="--------------------------------------------------- ", font=("Helvetica", 20)) \
            .grid(row=9, column=0, columnspan=5)

        for assignment in assignments:
            ttk.Label(self.parent, text="AssignmentID: " + str(assignment.id) + "    ").grid(column=i, row=10)
            i += 1

        i = 11
        for student in students:
            if student.isInstructor=="False":
                ttk.Label(self.parent, text = "StudentID: " + str(student.id)).grid(column=0, row=i)
                i += 1

        ttk.Label(self.parent, text="Grade Summary ", font=("Helvetica", 16)) \
            .grid(row=8, column=0, columnspan=5)
        ttk.Label(self.parent, text="--------------------------------------------------- ", font=("Helvetica", 20)) \
            .grid(row=9, column=0, columnspan=5)

        j = 1
        for assignment in assignments:
            i = 11
            for student in students:
                if student.isInstructor == "False":
                    grades = ast.literal_eval(assignment.grades)
                    if student.id in grades:
                        grade = grades[student.id]
                    else:
                        grade = None
                    # print(str(i) +" "+ str(j)+" " + str(grade))
                    ttk.Label(self.parent, text=grade).grid(row=i ,column=j)
                    i += 1
            j += 1

class AssignmentFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.name = tk.StringVar()
        self.maxPoint = tk.StringVar()
        self.file = StringVar()
        self.tree = ttk.Treeview( self.parent, columns=('name','fileID','maxPoint'))
        self.initialize_user_interface()

    def initialize_user_interface(self):
        self.parent.title("Assignments for " + current_user.name)
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.config(background="lavender")

        label1 = ttk.Label(self.parent, text="Assignment panel for " + current_user.name,font=("Helvetica", 20))
        label1.grid(row=0, column=0, columnspan = 2)

        label2 = ttk.Label(self.parent,
                                text='---------------------------------------------------------------------------------------------------')
        label2.grid(row=1, column=0)

        download_button = ttk.Button(self.parent, text="Download", command=self.download1)
        download_button.grid(row=5, column=0, sticky=tk.W)

        self.tree.heading('#0', text='assignmenID')
        self.tree.heading('#1', text='name')
        self.tree.heading('#2', text='fileID')
        self.tree.heading('#3', text='maxPoint')

        self.tree.column('#0', stretch=tk.YES)
        self.tree.column('#1', stretch=tk.YES)
        self.tree.column('#2', stretch=tk.YES)
        self.tree.column('#3', stretch=tk.YES)

        self.tree.grid(row=12, columnspan=5, sticky='nsew')
        self.treeview = self.tree
        assignments = mydb.get_assignments()
        for assignment in assignments:
            self.treeview.insert('', 'end', text=assignment.id , values=(assignment.name, assignment.files, assignment.max_point))

        if not isInstructor:
            self.submit_button = ttk.Button(self.parent, text="Submit", command=self.submit_assignment)
            self.submit_button.grid(row=9, column=0,sticky=tk.W)

        if isInstructor:
            self.name_label = ttk.Label(self.parent, text="name:")
            self.name_label.grid(row=2, column=0, sticky=tk.W)
            self.name_entry = ttk.Entry(self.parent, textvariable = self.name)
            self.name_entry.grid(row=2, column=1)

            self.point_label = ttk.Label(self.parent, text="maxPoint:")
            self.point_label.grid(row=3, column=0, sticky=tk.W)
            self.point_entry = ttk.Entry(self.parent, textvariable = self.maxPoint)
            self.point_entry.grid(row=3, column=1)

            self.file_label = ttk.Label(self.parent, text="file:")
            self.file_label.grid(row=4, column=0, sticky=tk.W)
            # self.file_entry = ttk.Entry(self.parent, textvariable = self.file, state="readonly")
            # self.file_entry.grid(row=3, column=1)

            self.add_button = ttk.Button(self.parent, text=" --- Select file ---", command=self.add_file)
            self.add_button.grid(row=4, column=1)

            self.add_button = ttk.Button(self.parent, text="Add Assignment", command=self.add_assignment)
            self.add_button.grid(row=7, column=1, rowspan = 3)

            self.add_button = ttk.Button(self.parent, text="Delete Assignment", command=self.delete_assigment)
            self.add_button.grid(row=8, column=0,sticky=tk.W)

    def delete_assigment(self):
        select = self.tree.selection()
        if select:
            item = self.tree.item(select) #{'text': 2, 'image': '', 'values': ['C++ homework', 15], 'open': 0, 'tags': ''}
            # Delete from database
            mydb.delete_assignment(item['text'])
            # Refresh the database
            assignments = mydb.get_assignments()
            self.treeview.delete(*self.treeview.get_children())
            for assignment in assignments:
                self.treeview.insert('', 'end', text=assignment.id,
                                     values=(assignment.name, assignment.files, assignment.max_point))

    def download1(self):
        select = self.tree.selection()
        if select:
            item = self.tree.item(select) #{'text': 2, 'image': '', 'values': ['C++ homework', 15], 'open': 0, 'tags': ''}
            self.get_selected_file(item['values'][1])
        else:
            message = "No file is selected. Please select one to download"
            messagebox.showinfo("Information", message)

    def get_selected_file(self, fileid):
        filelocation = mydb.get_file_location(fileid)
        Title = os.path.basename(filelocation)
        filename = filedialog.asksaveasfilename(initialdir="/", initialfile=Title, title="Save file to:")
        if filename:
            copy2(filelocation, filename)
            message = "File is downloaded"
            messagebox.showinfo("Information", message)

    def add_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        self.file.set(filename)
        if not os.path.exists("files"):
            os.makedirs("files")
        copy2(filename, "files")
        self.file_id = mydb.add_file_to_db(filename)

        message = "Assignment added"
        messagebox.showinfo("Information", message)

    def add_assignment(self):
        mydb.add_assignment(self.name_entry.get(), self.file_id,self.point_entry.get())
        assignments = mydb.get_assignments()
        self.treeview.delete(*self.treeview.get_children())
        for assignment in assignments:
            self.treeview.insert('', 'end', text=assignment.id,
                                 values=(assignment.name, assignment.files, assignment.max_point))


    def submit_assignment(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        if filename:
            # print(filename)
            if not os.path.exists("submission"):
                os.makedirs("submission")
            copy2(filename,"submission" )

class FileFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent
        self.pack(expand = True)
        self.initComponents()
        self.parent.config(background="lavender")

    def initComponents(self):
        ttk.Label(self, text="Select one of the file below").grid(row=0, column=0, columnspan=5)
        ttk.Label(self, text='-----------------------------------------------------------------------------------',
                  background="#a1dbcd").grid(
            row=2, column=0, columnspan=5)
        self.lb1 = Listbox(self)

        for file in mydb.get_files():
            self.lb1.insert(END, file)

        self.lb1.grid(row=4, column=0, columnspan = 4, sticky='nsew')
        self.bttn1 = ttk.Button(self, text = "Download", command = self.download_file) \
                .grid(column=1, row=1, sticky=tk.E)
        if isInstructor:
            self.bttn2 = ttk.Button(self, text="Delete", command=self.delete_file) \
                .grid(column=2, row=1, sticky=tk.E)
            self.bttn3 = ttk.Button(self, text="Add", command=self.add_file) \
                .grid(column=3, row=1)

    def download_file(self):
        current_selection = self.lb1.curselection()
        Title = os.path.basename(self.lb1.get(current_selection))
        filename = filedialog.asksaveasfilename(initialdir="/",initialfile = Title, title="Save file to:")
        if filename :
            copy2(self.lb1.get(current_selection), filename)
            message = "File is downloaded"
            messagebox.showinfo("Information", message)

    def delete_file(self):
        current_selection = self.lb1.curselection()
        self.lb1.delete(current_selection)
        message = "File is deleted"
        messagebox.showinfo("Information", message )
        mydb.delete_file(self.lb1.get(current_selection))
        os.remove(self.lb1.get(current_selection))

    def add_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select file")
        self.upload_file(self.filename)
        self.lb1.insert(END, self.filename)

    def upload_file(self, filename):
        if not os.path.exists("files"):
            os.makedirs("files")

        copy2(self.filename,"files" )

if __name__ == "__main__":
    mydb.connect()
    root = tk.Tk()
    root.title("Student Course ")
    root.configure(background="#a1dbcd")
    background_image = tk.PhotoImage(file="UB3.gif")
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    root.geometry("600x400")
    LoginFrame(root)
    root.mainloop()
    mydb.close()
