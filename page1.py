from tkinter import *
import pymysql
from PIL import ImageTk
from tkinter import messagebox
from tkinter import ttk
from datetime import date


class Library:
    def __init__(self, root):
        self.mypwd = ""
        '''Write your Password here'''
        self.mydb = ""
        '''Write your Database Name here'''
        self.username_info = ''

        self.root = root
        self.root.geometry("1199x600+100+50")
        self.root.resizable(False, False)
        self.root.title("Login Page")
        self.data_var = []
        # background image
        self.bg = ImageTk.PhotoImage(file="images/lib.jpg")
        self.bg_image = Label(self.root, image=self.bg).place(
            x=0, y=0, relwidth=1, relheight=1)

        # login frame
        Frame_login = Frame(self.root, bg="white")
        Frame_login.place(x="350", y="150", height="340", width="500")

        title = Label(Frame_login, text="Login Here", font=(
            "Arial", 35, "bold"), bg="white", fg="#E0550B").place(x=120, y=30)
        btn1 = Button(Frame_login, text="Login as a Student", font=(
            "Arial", 15, "bold"),
            bg='#E0550B', fg='white', command=self.student_login)
        btn1.place(x=130, y=140, relwidth=0.45, relheight=0.2)
        btn2 = Button(Frame_login, text="Login as Staff", font=(
            "Arial", 15, "bold"),
            bg='#E0550B', fg='white', command=self.staff_login)
        btn2.place(x=130, y=200, relwidth=0.45, relheight=0.2)
        btn3 = Button(Frame_login, text="Register as a new user", font=(
            "Arial", 15, "bold"),
            bg='#E0550B', fg='white', command=self.register)
        btn3.place(x=130, y=260, relwidth=0.45, relheight=0.2)

    def register(self):
        global screen1
        screen1 = Toplevel(root)
        screen1.title("Register")
        screen1.geometry("300x350")

        global username
        global password
        global username_entry
        global password_entry
        username = StringVar()
        password = StringVar()
        global email
        global year
        global branch
        global contact
        global email_entry
        global year_entry
        global branch_entry
        global contact_entry

        username = StringVar()
        password = StringVar()
        year = StringVar()
        contact = StringVar()
        branch = StringVar()
        email = StringVar()

        Label(screen1, text="Please enter details below").pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Username * ").pack()
        username_entry = Entry(screen1, textvariable=username)
        username_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Password * ").pack()
        password_entry = Entry(screen1, textvariable=password, show="*")
        password_entry.pack()
        Label(screen1, text="Contact No. * ").pack()
        contact_entry = Entry(screen1, textvariable=contact)
        contact_entry.pack()
        Label(screen1, text="Email * ").pack()
        email_entry = Entry(screen1, textvariable=email)
        email_entry.pack()
        Label(screen1, text="Year * ").pack()
        year.set("First")
        year_entry = ttk.Combobox(screen1, width=27, textvariable=year, values=[
            'First', 'Second', 'Third', 'Fourth']).pack()
        branch.set("CSE")
        Label(screen1, text="Branch * ").pack()
        branch_entry = ttk.Combobox(screen1, width=27, textvariable=branch, values=[
            'CSE', 'EC', 'Civil', 'EE', 'Mechanical']).pack()
        Label(screen1, text="").pack()
        Button(screen1, text="Register", width=10,
               height=1, command=self.register_user).pack()

    def register_user(self):
        username_info = username.get()
        password_info = password.get()
        year_info = year.get()
        branch_info = branch.get()
        email_info = email.get()
        contact_info = contact.get()

        username_entry.delete(0, END)
        password_entry.delete(0, END)
        email_entry.delete(0, END)
        contact_entry.delete(0, END)

        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()

        insertStudent = "insert into student_user(name, password, email, year, contact_no, branch) values('" + \
            username_info+"', '"+password_info+"', '"+email_info+"', '" + \
            year_info+"', '"+contact_info+"', '"+branch_info+"')"
        if (username_info == "" or password_info == ""):
            messagebox.showinfo("Error", "Empty fields not allowed")
        else:
            check = "select * from student_user where name= '"+username_info+"'"
            check2 = "select * from student_user where email='"+email_info+"'"
            c1 = cur.execute(check)
            c2 = cur.execute(check2)
            if c1:
                messagebox.showinfo("Error", "username already exists")
            elif c2:
                messagebox.showinfo(
                    "Error", "AN account with this email ID already exists. Try using another email ID.")
            else:
                try:
                    cur.execute(insertStudent)
                    con.commit()
                    messagebox.showinfo(
                        'Success', "Student added successfully")

                    Label(screen1, text="Registration Sucessful",
                          fg="green", font=("calibri", 11)).pack()
                    screen1.destroy()
                    self.username_info = username_info
                    self.student_dashboard()
                except:
                    messagebox.showinfo(
                        "Error", "Can't add data into Database")

    def student_login(self):
        global loginscreen
        loginscreen = Toplevel(root)
        loginscreen.title("Login")
        loginscreen.geometry("300x250")
        global username
        global password
        global username_entry
        global password_entry
        username = StringVar()
        password = StringVar()
        Label(loginscreen, text="Please enter details below").pack()
        Label(loginscreen, text="").pack()
        Label(loginscreen, text="Username * ").pack()
        username_entry = Entry(loginscreen, textvariable=username)
        username_entry.pack()
        Label(loginscreen, text="Password * ").pack()
        password_entry = Entry(loginscreen, textvariable=password, show="*")
        password_entry.pack()
        Label(loginscreen, text="").pack()
        Button(loginscreen, text="Login", width=10,
               height=1, command=self.check_student_user).pack()

    def check_student_user(self):
        username_info = username.get()
        password_info = password.get()
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "select * from student_user where name= '" + \
            username_info+"' and password= '"+password_info+"'"
        data = cur.execute(query)
        con.commit()
        if not data:
            messagebox.showinfo("Error", "User does not exist")
        else:
            self.username_info = username_info
            print("This is my username: ", self.username_info)
            self.student_dashboard()

    def staff_login(self):
        global loginscreen
        loginscreen = Toplevel(root)
        loginscreen.title("Login")
        loginscreen.geometry("300x250")
        global username
        global password
        global username_entry
        global password_entry
        username = StringVar()
        password = StringVar()
        Label(loginscreen, text="Please enter details below").pack()
        Label(loginscreen, text="").pack()
        Label(loginscreen, text="Username * ").pack()
        username_entry = Entry(loginscreen, textvariable=username)
        username_entry.pack()
        Label(loginscreen, text="Password * ").pack()
        password_entry = Entry(loginscreen, textvariable=password, show="*")
        password_entry.pack()
        Label(loginscreen, text="").pack()
        Button(loginscreen, text="Login", width=10,
               height=1, command=self.check_staff_user).pack()

    def check_staff_user(self):
        username_info = username.get()
        password_info = password.get()
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "select * from staff_user where name= '" + \
            username_info+"' and password= '"+password_info+"'"
        data = cur.execute(query)
        con.commit()
        if not data:
            messagebox.showinfo("Error", "User does not exist")
        else:
            self.username_info = username_info
            self.staff_dashboard()

    def student_dashboard(self):
        dashboard = Toplevel()
        dashboard.title("Dashboard")
        dashboard.geometry("300x250")
        title = Label(dashboard, text="Welcome, "+self.username_info+" !", bd=10, relief=GROOVE, font=(
            "Arial", 35, "bold"), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        Manage_Frame = Frame(dashboard, bd=4, relief=RIDGE, bg="#60CFCF")
        Manage_Frame.place(x=50, y=100, width=560, height=300)
        Record_Frame = Frame(dashboard, bd=4, relief=RIDGE, bg="#60CFCF")
        Record_Frame.place(x=50, y=410, width=560, height=350)
        Search_Frame = Frame(dashboard, bd=4, relief=RIDGE, bg="#60CFCF")
        Search_Frame.place(x=650, y=100, width=800, height=650)
        title = Label(Manage_Frame, text="My Profile", bd=1, relief=GROOVE, font=(
            "Arial", 30), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        title = Label(Record_Frame, text="My Records", bd=1, relief=GROOVE, font=(
            "Arial", 30), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        title = Label(Search_Frame, text="Search Books", bd=1, relief=GROOVE, font=(
            "Arial", 30), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        # ---------------------Manage Frame------------------------
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "select name, branch, year, email, contact_no, fine, student_id from student_user where name = '" + \
            self.username_info+"'"

        cur.execute(query)
        data = cur.fetchall()
        query2 = "select student_id,sum(fee) from record group by student_id having student_id= " + \
            str(data[0][6])
        cur.execute(query2)
        rec = cur.fetchall()
        con.commit()
        print(rec)
        name_label = Label(Manage_Frame, text="Name: "+data[0][0],
                           bg="#60CFCF", fg="white", font="Calibri")
        name_label.pack()
        batch_label = Label(Manage_Frame, text="Branch: "+data[0][1],
                            bg="#60CFCF", fg="white", font="Calibri")
        batch_label.pack()
        year_label = Label(Manage_Frame, text="Year: "+data[0][2],
                           bg="#60CFCF", fg="white", font="Calibri")
        year_label.pack()
        email_label = Label(Manage_Frame, text="Email: "+data[0][3],
                            bg="#60CFCF", fg="white", font="Calibri")
        email_label.pack()
        contact_label = Label(Manage_Frame, text="Contact no.: "+data[0][4],
                              bg="#60CFCF", fg="white", font="Calibri")
        contact_label.pack()
        fine_label = Label(Manage_Frame, text="Total Fine Due: "+str(rec[0][1]),
                           bg="#60CFCF", fg="white", font=("Calibri", 25))
        fine_label.pack()
        edit_btn = Button(Manage_Frame, text="Edit Profile",
                          width=10, command=self.edit_student_profile).pack(pady=5, side=TOP)
        refresh_btn = Button(Manage_Frame, text="Refresh",
                             width=10, ).pack(pady=5, side=RIGHT)
        con.close()
        # ---------------------Record Frame------------------------
        RF = Frame(Record_Frame, bd=4, relief=RIDGE, bg="#60CFCF")
        RF.place(x=10, y=50, width=540, height=280)

        scroll_x2 = Scrollbar(RF, orient=HORIZONTAL)
        scroll_y2 = Scrollbar(RF, orient=VERTICAL)
        self.Return_table = ttk.Treeview(RF, columns=("date_issued", "return_date", "book_title",
                                                      "fine"), xscrollcommand=scroll_x2.set, yscrollcommand=scroll_y2.set)
        scroll_x2.pack(side=BOTTOM, fill=X)
        scroll_y2.pack(side=RIGHT, fill=Y)
        scroll_x2.config(command=self.Return_table.xview)
        scroll_y2.config(command=self.Return_table.yview)
        self.Return_table.heading("date_issued", text="Date Issued")
        self.Return_table.heading("return_date", text="Return Date")
        self.Return_table.heading("book_title", text="Book Title")
        self.Return_table.heading("fine", text="Return Status/Fine")
        self.Return_table.column("date_issued", width=135)
        self.Return_table.column("return_date", width=135)
        self.Return_table.column("book_title", width=135)
        self.Return_table.column("fine", width=135)
        self.Return_table['show'] = 'headings'
        self.Return_table.pack(fill=BOTH, expand=1)
        self.fetch_my_record()
        # ---------------------Search Frame------------------------
        self.search_by = StringVar()
        self.search_txt = StringVar()
        search_label = Label(Search_Frame, text="Search By: ",
                             bg="#60CFCF", fg="white", font="Calibri")
        search_label.pack()
        combo = ttk.Combobox(Search_Frame, textvariable=self.search_by, font=(
            "Calibri", 13, "bold"), state="readonly")
        combo['values'] = ("Title", "Author", "Category")
        combo.pack()
        search_text = Entry(Search_Frame, textvariable=self.search_txt, font=(
            "Calibri", 13, "bold"), bd=5, relief=GROOVE)
        search_text .pack(pady=10)

        btn1 = Button(Search_Frame, text="Go", width=10,
                      command=self.search_books_data).pack(pady=5, side=TOP)
        btn2 = Button(Search_Frame, text="Show All",
                      width=10, command=self.fetch_books_data).pack(pady=5, side=TOP)

        # -------------Search Table-------------------
        SF = Frame(Search_Frame, bd=4, relief=RIDGE, bg="#60CFCF")
        SF.place(x=10, y=240, width=760, height=350)

        scroll_x = Scrollbar(SF, orient=HORIZONTAL)
        scroll_y = Scrollbar(SF, orient=VERTICAL)
        self.Book_table = ttk.Treeview(SF, columns=("title", "author", "category",
                                                    "edition", "copies"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Book_table.xview)
        scroll_y.config(command=self.Book_table.yview)
        self.Book_table.heading("title", text="Book Title")
        self.Book_table.heading("author", text="Author")
        self.Book_table.heading("category", text="Category")
        self.Book_table.heading("edition", text="Edition")
        self.Book_table.heading("copies", text="Copies Available")
        self.Book_table.column("title", width=280)
        self.Book_table.column("author", width=190)
        self.Book_table.column("category", width=190)
        self.Book_table.column("edition", width=100)
        self.Book_table.column("copies", width=100)
        self.Book_table['show'] = 'headings'
        self.Book_table.pack(fill=BOTH, expand=1)
        self.fetch_books_data()

    def fetch_books_data(self):
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "select * from books"
        data = cur.execute(query)
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Book_table.delete(*self.Book_table.get_children())
            for row in rows:
                self.Book_table.insert(
                    '', END, values=[row[1], row[2], row[3], row[4], row[6]])
            con.commit()
        con.close()

    def search_books_data(self):
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "select * from books where " + \
            str(self.search_by.get())+" like '%" + \
            str(self.search_txt.get())+"%'"
        data = cur.execute(query)
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Book_table.delete(*self.Book_table.get_children())
            for row in rows:
                self.Book_table.insert(
                    '', END, values=[row[1], row[2], row[3], row[4], row[6]])
            con.commit()
        con.close()

    def fetch_my_record(self):
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        print("Printing username: ", self.username_info)
        query = "select r.date_issued, r.return_date, b.title, r.return_status, r.fee from record r inner join student_user s on r.STUDENT_ID=s.STUDENT_ID inner join books b on b.isbn=r.isbn where s.name = '"+self.username_info+"'"
        data = cur.execute(query)
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Return_table.delete(*self.Return_table.get_children())
            for row in rows:
                self.Return_table.insert(
                    '', END, values=[row[0], row[1], row[2], str(row[3])+"/"+str(row[4])])
            con.commit()
        con.close()

    def edit_student_profile(self):
        global screen1
        screen1 = Toplevel(root)
        screen1.title("Edit Profile")
        screen1.geometry("300x350")

        global email
        global year
        global branch
        global contact
        global email_entry
        global year_entry
        global branch_entry
        global contact_entry

        year = StringVar()
        contact = StringVar()
        branch = StringVar()
        email = StringVar()
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "select contact_no, email, year, branch from student_user where name = '" + \
            self.username_info+"'"
        cur.execute(query)
        row = cur.fetchall()[0]
        Label(screen1, text="Edit your profile:").pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Contact No. * ").pack()
        contact_entry = Entry(screen1, textvariable=contact)
        contact.set(row[0])
        contact_entry.pack()
        Label(screen1, text="Email * ").pack()
        email_entry = Entry(screen1, textvariable=email)
        email.set(row[1])
        email_entry.pack()
        Label(screen1, text="Year * ").pack()
        year.set(row[2])
        year_entry = ttk.Combobox(screen1, width=27, textvariable=year, values=[
            'First', 'Second', 'Third', 'Fourth']).pack()
        branch.set(row[3])
        Label(screen1, text="Branch * ").pack()
        branch_entry = ttk.Combobox(screen1, width=27, textvariable=branch, values=[
            'CSE', 'EC', 'Civil', 'EE', 'Mechanical']).pack()
        Label(screen1, text="").pack()
        Button(screen1, text="Edit", width=10,
               height=1, command=self.edit_info).pack()

    def edit_info(self):
        year_info = year.get()
        branch_info = branch.get()
        email_info = email.get()
        contact_info = contact.get()

        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()

        updateStudent = "update student_user set contact_no = '" + contact_info+"', email = '"+email_info + \
            "', branch = '"+branch_info+"', year = '" + year_info + \
            "' where name = '"+self.username_info+"'"

        check2 = "select * from student_user where email = '" + \
            email_info+"' and name != '"+self.username_info+"'"
        c2 = cur.execute(check2)
        if c2:
            messagebox.showinfo(
                "Error", "An account with this email ID already exists. Try using another email ID.")
        else:
            try:
                cur.execute(updateStudent)
                con.commit()
                messagebox.showinfo(
                    'Success', "Profile edited successfully")

                Label(screen1, text="Edit Successful",
                      fg="green", font=("calibri", 11)).pack()
                screen1.destroy()
            except:
                messagebox.showinfo(
                    "Error", "Can't add data into Database")

    def staff_dashboard(self):
        dashboard = Toplevel()
        dashboard.title("Staff Dashboard")
        dashboard.geometry("300x250")
        title = Label(dashboard, text="Welcome, "+self.username_info+" !", bd=10, relief=GROOVE, font=(
            "Arial", 35, "bold"), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        Search_Frame = Frame(dashboard, bd=4, relief=RIDGE, bg="#60CFCF")
        Search_Frame.place(x=50, y=100, width=560, height=650)
        Record_Frame = Frame(dashboard, bd=4, relief=RIDGE, bg="#60CFCF")
        Record_Frame.place(x=650, y=100, width=800, height=650)
        title.pack(side=TOP, fill=X)
        title = Label(Search_Frame, text="Books", bd=1, relief=GROOVE, font=(
            "Arial", 30), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        title = Label(Record_Frame, text="Library Record", bd=1, relief=GROOVE, font=(
            "Arial", 30), bg="white", fg="#60CFCF")
        title.pack(side=TOP, fill=X)
        # ---------------------Record Frame------------------------
        #  ----crud functionalities----
        SRF = Frame(Record_Frame, bd=4, relief=RIDGE, bg="white")
        SRF.place(x=10, y=70, width=370, height=190)
        ARF = Frame(Record_Frame, bd=4, relief=RIDGE, bg="white")
        ARF.place(x=390, y=70, width=380, height=190)
        btn1 = Button(ARF, text="Issue Book", width=15,
                      command=self.issue).pack(pady=5, side=TOP)
        btn2 = Button(ARF, text="Return Book",
                      width=15, command=self.return_book).pack(pady=5, side=TOP)
        btn3 = Button(ARF, text="Delete a Record", width=15,
                      command=self.delete).pack(pady=5, side=TOP)
        '''btn4 = Button(ARF, text="Update a Record",
                      width=15, command=self.fetch_books_data).pack(pady=5, side=TOP)'''
        btn8 = Button(ARF, text="Deselect",
                      width=15, command=self.deselect).pack(pady=5, side=TOP)
        #     ---search record section---
        self.search_record_by = StringVar()
        self.search_record_txt = StringVar()
        search_record_label = Label(SRF, text="Search By: ",
                                    bg="white", fg="#60CFCF", font="Calibri")
        search_record_label.grid(row=0, column=0)
        combo = ttk.Combobox(SRF, textvariable=self.search_record_by, font=(
            "Calibri", 13, "bold"), state="readonly")
        combo['values'] = ("DATE_ISSUED", "RETURN_STATUS", "STUDENT_ID")
        combo.grid(row=1, column=0)
        search_record_text = Entry(SRF, textvariable=self.search_record_txt, font=(
            "Calibri", 13, "bold"), bd=5, relief=GROOVE)
        search_record_text .grid(row=2, column=0)

        btn5 = Button(SRF, text="Go", width=10, command=self.search_records_data
                      ).grid(row=2, column=1)
        btn6 = Button(SRF, text="Show All",
                      width=10, command=self.fetch_record_data).grid(row=4, column=0)
        btn7 = Button(SRF, text="Students with Due Fee",
                      width=20, command=self.fetch_duefee_records).grid(row=4, column=1)

        # -------------Record Table-------------------
        SF = Frame(Record_Frame, bd=4, relief=RIDGE, bg="#60CFCF")
        SF.place(x=10, y=270, width=760, height=360)

        scroll_x = Scrollbar(SF, orient=HORIZONTAL)
        scroll_y = Scrollbar(SF, orient=VERTICAL)
        self.Record_table = ttk.Treeview(SF, columns=("RECORD_ID", "STUDENT", "BRANCH",
                                                      "BATCH/YEAR", "ISBN", "BOOK_NAME", "ISSUE_DATE", "RETURN_DATE", "FEE_DUE"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Record_table.xview)
        scroll_y.config(command=self.Record_table.yview)
        self.Record_table.heading("RECORD_ID", text="RECORD_ID")
        self.Record_table.heading("STUDENT", text="STUDENT")
        self.Record_table.heading("BRANCH", text="BRANCH")
        self.Record_table.heading("BATCH/YEAR", text="BATCH/YEAR")
        self.Record_table.heading("ISBN", text="ISBN")
        self.Record_table.heading("BOOK_NAME", text="BOOK_NAME")
        self.Record_table.heading("ISSUE_DATE", text="ISSUE_DATE")
        self.Record_table.heading("RETURN_DATE", text="RETURN_DATE")
        self.Record_table.heading("FEE_DUE", text="FEE DUE")

        self.Record_table.column("RECORD_ID", width=80)
        self.Record_table.column("STUDENT", width=190)
        self.Record_table.column("BRANCH", width=120)
        self.Record_table.column("BATCH/YEAR", width=100)
        self.Record_table.column("ISBN", width=90)
        self.Record_table.column("BOOK_NAME", width=190)
        self.Record_table.column("ISSUE_DATE", width=190)
        self.Record_table.column("RETURN_DATE", width=190)
        self.Record_table.column("FEE_DUE", width=190)

        self.Record_table['show'] = 'headings'
        self.Record_table.pack(fill=BOTH, expand=1)
        self.fetch_record_data()
        self.Record_table.bind("<ButtonRelease-1>", self.cursor_value)
        #-------------Books Frame------------------------------------#
        BF = Frame(Search_Frame, bd=4, relief=RIDGE, bg="#60CFCF")
        BF.place(x=10, y=50, width=530, height=450)
        scroll_x = Scrollbar(BF, orient=HORIZONTAL)
        scroll_y = Scrollbar(BF, orient=VERTICAL)

        self.Book_table = ttk.Treeview(BF, columns=("title", "author", "category",
                                                    "edition", "copies"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Book_table.xview)
        scroll_y.config(command=self.Book_table.yview)
        self.Book_table.heading("title", text="Book Title")
        self.Book_table.heading("author", text="Author")
        self.Book_table.heading("category", text="Category")
        self.Book_table.heading("edition", text="Edition")
        self.Book_table.heading("copies", text="Copies Available")
        self.Book_table.column("title", width=280)
        self.Book_table.column("author", width=190)
        self.Book_table.column("category", width=190)
        self.Book_table.column("edition", width=100)
        self.Book_table['show'] = 'headings'
        self.Book_table.pack(fill=BOTH, expand=1)
        self.fetch_books_data()
        self.Book_table.bind("<ButtonRelease-1>", self.cursor_value)
        self.search_by = StringVar()
        self.search_txt = StringVar()
        self.Book_table.bind("<ButtonRelease-1>", self.cursor_value)

        BSF = Frame(Search_Frame, bd=4, relief=RIDGE, bg="#60CFCF")
        BSF.place(x=60, y=515, width=400, height=110)
        search_label = Label(BSF, text="Search By: ",
                             bg="#60CFCF", fg="white", font="Calibri")
        search_label.grid(row=0, column=1)
        combo = ttk.Combobox(BSF, textvariable=self.search_by, font=(
            "Calibri", 13, "bold"), state="readonly")
        combo['values'] = ("Title", "Author", "Category")
        combo.grid(row=1, column=1)
        search_text = Entry(BSF, textvariable=self.search_txt, font=(
            "Calibri", 13, "bold"), bd=5, relief=GROOVE)
        search_text .grid(row=2, column=1)

        btn1 = Button(BSF, text="Go", width=10,
                      command=self.search_books_data).grid(row=1, column=3)
        btn2 = Button(BSF, text="Show All",
                      width=10, command=self.fetch_books_data).grid(row=2, column=3)
        btn3 = Button(BSF, text="Add Books", width=15,
                      command=self.add_books).grid(row=1, column=4)
        btn4 = Button(BSF, text="Remove Books",
                      width=15, command=self.remove_books).grid(row=2, column=4)

    def add_books(self):
        global screen1
        screen1 = Toplevel(root)
        screen1.title("Add Book")
        screen1.geometry("350x450")

        global isbn
        global title
        global author
        global category
        global edition
        global copies
        global isbn_entry
        global title_entry
        global author_entry
        global edition_entry
        global copies_entry
        global category_entry

        isbn = StringVar()
        title = StringVar()
        author = StringVar()
        category = StringVar()
        edition = StringVar()
        copies = StringVar()
        Label(screen1, text="Please enter details below").pack()
        Label(screen1, text="").pack()
        Label(screen1, text="ISBN: ").pack()
        isbn_entry = Entry(screen1, textvariable=isbn)
        isbn_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Title: ").pack()
        title_entry = Entry(screen1, textvariable=title)
        title_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Author: ").pack()
        author_entry = Entry(screen1, textvariable=author)
        author_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Edition: ").pack()
        edition_entry = Entry(screen1, textvariable=edition)
        edition_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="No. of copies: ").pack()
        copies_entry = Entry(screen1, textvariable=copies)
        copies_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Category: ").pack()
        category_entry = Entry(screen1, textvariable=category)
        category_entry.pack()
        Label(screen1, text="").pack()
        Button(screen1, text="Add", width=10,
               height=1, command=self.add_books_util).pack()

    def add_books_util(self):
        title_info = title.get()
        isbn_info = isbn.get()
        category_info = category.get()
        edition_info = edition.get()
        copies_info = copies.get()
        author_info = author.get()

        title_entry.delete(0, END)
        isbn_entry.delete(0, END)
        author_entry.delete(0, END)
        edition_entry.delete(0, END)
        copies_entry.delete(0, END)
        category_entry.delete(0, END)

        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()

        checkexistence = "select isbn from books where isbn = "+isbn_info
        d1 = cur.execute(checkexistence)
        addexistingbook = "update books set copies= copies + " + \
            copies_info+" where isbn= "+isbn_info
        addnewbook = "insert into books(isbn, title, author, category, edition, copies) values('" + \
            isbn_info+"', '"+title_info+"', '"+author_info+"', '" + \
            category_info+"','"+edition_info+"','"+copies_info+"') "
        if (title_info == "" or isbn_info == "" or author_info == "" or category_info == "" or edition_info == "" or copies_info == ""):
            messagebox.showinfo("Error", "Empty fields not allowed")
        elif(d1):
            try:
                cur.execute(addexistingbook)
                con.commit()
            except:
                messagebox.showinfo(
                    "Error", "Can't add data into Database")
        else:
            try:
                cur.execute(addnewbook)
                con.commit()
                messagebox.showinfo(
                    'Success', "Book added successfully")
            except:
                messagebox.showinfo(
                    "Error", "Can't add data into Database")
        Label(screen1, text="Book Addition Sucessful",
              fg="green", font=("calibri", 11)).pack()
        screen1.destroy()

    def remove_books(self):
        global screen1
        screen1 = Toplevel(root)
        screen1.title("Remove Books")
        screen1.geometry("350x450")

        global isbn
        global copies
        global isbn_entry
        global copies_entry
        isbn = StringVar()
        copies = StringVar()
        Label(screen1, text="Please enter details below").pack()
        Label(screen1, text="").pack()
        Label(screen1, text="ISBN: ").pack()
        isbn_entry = Entry(screen1, textvariable=isbn)
        isbn_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="No. of copies: ").pack()
        copies_entry = Entry(screen1, textvariable=copies)
        copies_entry.pack()
        Label(screen1, text="").pack()
        Button(screen1, text="Remove", width=10,
               height=1, command=self.remove_books_util).pack()

    def remove_books_util(self):
        isbn_info = isbn.get()
        copies_info = copies.get()

        isbn_entry.delete(0, END)
        copies_entry.delete(0, END)

        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()

        checkexistence = "select isbn from books where isbn = "+isbn_info
        d1 = cur.execute(checkexistence)
        removebooks = "update books set copies= copies - " + \
            copies_info+" where isbn= "+isbn_info
        if (isbn_info == "" or copies_info == ""):
            messagebox.showinfo("Error", "Empty fields not allowed")
        elif not d1:
            messagebox.showinfo("Error", "Can't add data into Database")
        else:
            try:
                cur.execute(removebooks)
                con.commit()
                messagebox.showinfo(
                    'Success', "Books removed")
            except:
                messagebox.showinfo(
                    "Error", "Can't remove books from library")
        Label(screen1, text="Book Removal Sucessful",
              fg="green", font=("calibri", 11)).pack()
        screen1.destroy()

    def fetch_record_data(self):
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "SELECT R.RECORD_ID,S.NAME, S.BRANCH, S.YEAR, B.ISBN, B.TITLE, R.DATE_ISSUED, R.RETURN_DATE, R.FEE FROM BOOKS B INNER JOIN RECORD R ON B.ISBN=R.ISBN INNER JOIN STUDENT_USER S ON R.STUDENT_ID=S.student_ID ORDER BY R.DATE_ISSUED DESC;"
        data = cur.execute(query)
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Record_table.delete(*self.Record_table.get_children())
            for row in rows:
                self.Record_table.insert(
                    '', END, values=[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
            con.commit()
        con.close()

    def fetch_duefee_records(self):
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "SELECT R.RECORD_ID,S.NAME, S.BRANCH, S.YEAR, B.ISBN, B.TITLE, R.DATE_ISSUED, R.RETURN_DATE, R.FEE FROM BOOKS B INNER JOIN RECORD R ON B.ISBN=R.ISBN INNER JOIN STUDENT_USER S ON R.STUDENT_ID=S.student_ID WHERE R.FEE>0 ORDER BY R.DATE_ISSUED DESC;"
        data = cur.execute(query)
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Record_table.delete(*self.Record_table.get_children())
            for row in rows:
                self.Record_table.insert(
                    '', END, values=[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
            con.commit()
        con.close()

    def issue(self):
        global screen1
        screen1 = Toplevel(root)
        screen1.title("Issue Book")
        screen1.geometry("300x350")

        global student_id
        global isbn
        global student_entry
        global isbn_entry

        student_id = StringVar()
        isbn = StringVar()
        Label(screen1, text="Please enter details below").pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Student ID: ").pack()
        student_entry = Entry(screen1, textvariable=student_id)
        student_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="ISBN: ").pack()
        isbn_entry = Entry(screen1, textvariable=isbn)
        isbn_entry.pack()
        Label(screen1, text="").pack()
        Button(screen1, text="Issue", width=10,
               height=1, command=self.issue_book).pack()

    def issue_book(self):
        student_info = student_id.get()
        isbn_info = isbn.get()

        student_entry.delete(0, END)
        isbn_entry.delete(0, END)

        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        print(d1)
        q1 = "select copies from books where isbn = "+isbn_info+" and copies>0"
        q2 = "select record_id from record where isbn = " + \
            isbn_info+" and student_id = " + student_info
        d2 = cur.execute(q1)
        d3 = cur.execute(q2)
        print("copies: ", d2)
        if(not d2):
            messagebox.showinfo("Error", "Book not available presently")
        elif d3:
            messagebox.showinfo("Error", "Book already issued to this student")
        else:
            countbook = "update books set copies = copies-1 where isbn = "+isbn_info
            insertStudent = "insert into record(student_id, date_issued, isbn, return_status) values('" + \
                student_info+"', '"+d1+"', '"+isbn_info+"', 'ISSUED') "
            if (student_info == "" or isbn_info == ""):
                messagebox.showinfo("Error", "Empty fields not allowed")
            else:
                check = "select * from student_user where student_id= '"+student_info+"'"
                check2 = "select * from books where isbn='"+isbn_info+"'"
                c1 = cur.execute(check)
                c2 = cur.execute(check2)
                if not c1:
                    messagebox.showinfo("Error", "Student user does not exist")
                elif not c2:
                    messagebox.showinfo(
                        "Error", "Book not available")
                else:
                    try:
                        cur.execute(insertStudent)
                        cur.execute(countbook)
                        con.commit()
                        messagebox.showinfo(
                            'Success', "Book issued successfully")

                        Label(screen1, text="Issue Sucessful",
                              fg="green", font=("calibri", 11)).pack()
                        screen1.destroy()
                    except:
                        messagebox.showinfo(
                            "Error", "Can't add data into Database")

    def search_records_data(self):
        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()
        query = "SELECT R.RECORD_ID,S.NAME, S.BRANCH, S.YEAR, B.ISBN, B.TITLE, R.DATE_ISSUED, R.RETURN_DATE, R.FEE FROM BOOKS B INNER JOIN RECORD R ON B.ISBN=R.ISBN INNER JOIN STUDENT_USER S ON R.STUDENT_ID=S.student_ID WHERE R." + \
            str(self.search_record_by.get())+" like '%" + \
            str(self.search_record_txt.get(
            ))+"%'ORDER BY R.DATE_ISSUED DESC"
        data = cur.execute(query)
        rows = cur.fetchall()
        if len(rows) != 0:
            self.Record_table.delete(*self.Record_table.get_children())
            for row in rows:
                self.Record_table.insert(
                    '', END, values=[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
            con.commit()
        con.close()

    def cursor_value(self, ev):
        cursor_row = self.Record_table.focus()
        contents = self.Record_table.item(cursor_row)
        data_row = contents['values']
        print(data_row)
        self.data_var = data_row

    def delete(self):
        if self.data_var:
            con = pymysql.connect(host="localhost", user="root", port=3306,
                                  password=self.mypwd, database=self.mydb)
            cur = con.cursor()
            query = "DELETE FROM RECORD WHERE RECORD_ID = " + \
                str(self.data_var[0])
            cur.execute(query)
            con.commit()
            con.close()
            self.fetch_record_data()

    def deselect(self):
        self.data_var = []
        self.fetch_record_data()

    def return_book(self):
        global screen1
        screen1 = Toplevel(root)
        screen1.title("Return Book")
        screen1.geometry("300x350")

        global student_id
        global isbn
        global student_entry
        global isbn_entry
        student_id = StringVar()
        isbn = StringVar()
        Label(screen1, text="Please enter details below").pack()
        Label(screen1, text="").pack()
        Label(screen1, text="Student ID: ").pack()
        student_entry = Entry(screen1, textvariable=student_id)
        student_entry.pack()
        Label(screen1, text="").pack()
        Label(screen1, text="ISBN: ").pack()
        isbn_entry = Entry(screen1, textvariable=isbn)
        isbn_entry.pack()
        Label(screen1, text="").pack()
        Button(screen1, text="Return", width=10,
               height=1, command=self.return_book_util).pack()

    def return_book_util(self):
        student_info = student_id.get()
        isbn_info = isbn.get()

        student_entry.delete(0, END)
        isbn_entry.delete(0, END)

        con = pymysql.connect(host="localhost", user="root", port=3306,
                              password=self.mypwd, database=self.mydb)
        cur = con.cursor()

        countbook = "update books set copies = copies+1 where isbn = "+isbn_info
        changerecord = "update record set return_status = 'RETURNED', fee=0 where isbn = "+isbn_info
        student_info+"' and isbn = '"+isbn_info+"'"
        if (student_info == "" or isbn_info == ""):
            messagebox.showinfo("Error", "Empty fields not allowed")
        else:
            check = "select * from record where student_id= '" + \
                student_info+"' and isbn='"+isbn_info+"'"
            c1 = cur.execute(check)
            if not c1:
                messagebox.showinfo("Error", "Record does not exist")
            else:
                cur.execute(countbook)
                cur.execute(changerecord)
                con.commit()
                messagebox.showinfo(
                    'Success', "Book returned successfully")

                Label(screen1, text="Issue Sucessful",
                      fg="green", font=("calibri", 11)).pack()
                screen1.destroy()


root = Tk()
obj = Library(root)
root.mainloop()
