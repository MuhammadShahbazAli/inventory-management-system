from pkgutil import get_data
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_NAME, APP_NAME

class employee:
    def __init__(self,root):
        self.root=root
        self.root.title(APP_NAME)
        self.root.geometry("1100x500+220+190")
        self.root.config(bg="White")
        self.root.resizable(False, False)
        self.root.focus_force()

        #=================Variables================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id=StringVar()
        self.var_gender=StringVar()
        self.var_contact=StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_usertype = StringVar()
        self.var_salary = StringVar()


        #=================Search Frame================
        search_frame = LabelFrame(self.root, text="Search Employee", font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=RIDGE)
        search_frame.place(x=250, y=20, width=600, height=70)

        #=================Options================
        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_searchby, values=["Select", "Email", "Name", "Contact"], state="readonly", justify=CENTER, font=("goudy old style", 12, "bold"))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)
        txt_search = Entry(search_frame, font=("goudy old style", 15),textvariable= self.var_searchtxt, bg="#ECECEC").place(x=201, y=9)
        btn_search = Button(search_frame, text="Search",command=self.search, font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2").place(x=435, y=6, width=150, height=30)


        #================= Title ================
        title = Label(self.root, text="Employee Manager", font=("goudy old style", 20, "bold"), bg="#184a45", bd=3, relief=RIDGE, fg="white").place(x=50, y=100, width=1000)



        #=================Content Area================
            #=======Row1========
        lbl_emp_id = Label(self.root, text="Emp ID:*", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender:", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        txt_emp_id = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_emp_id).place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable= self.var_gender, values=["Select", "Male", "Female", "Others"], state="readonly", justify=CENTER, font=("goudy old style", 12))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_contact).place(x=850, y=150, width=180)

            #=======Row2========
        lbl_name = Label(self.root, text="Name:*", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B:", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        lbl_doj = Label(self.root, text="D.O.J:", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        txt_name = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_name).place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_dob).place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_doj).place(x=850, y=190, width=180)

            #=======Row3========
        lbl_email = Label(self.root, text="Email:*", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password:*", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        lbl_usertype = Label(self.root, text="User Type:", font=("goudy old style", 15), bg="white").place(x=750, y=230)

        txt_email = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_email).place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_pass).place(x=500, y=230, width=180)
        cmb_usertype = ttk.Combobox(self.root, textvariable=self.var_usertype, values=["Select", "Admin", "Employee"],state="readonly", justify=CENTER, font=("goudy old style", 12))
        cmb_usertype.place(x=850, y=230, width=180)
        cmb_usertype.current(0)

            #=======Row4========
        lbl_address = Label(self.root, text="Address:", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary:", font=("goudy old style", 15), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="#ECECEC")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        txt_salary = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_salary).place(x=600, y=270, width=180)

        #=======Action Buttons========
        btn_add = Button(self.root, text="Save",command=self.add_employee, font=("goudy old style", 15), bg="green", fg="white", cursor="hand2").place(x=500, y=305, width=110, height=28)
        btn_update = Button(self.root, text="Update",command=self.update_employee, font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2").place(x=620, y=305, width=110, height=28)
        btn_delete = Button(self.root, text="Delete",command=self.delete_employee, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2").place(x=740, y=305, width=110, height=28)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 15), bg="gray", fg="white", cursor="hand2").place(x=860, y=305, width=110, height=28)

        #=================Employee Details Table================
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.employee_table = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "pass", "utype", "address", "salary"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.employee_table.xview)
        scrolly.config(command=self.employee_table.yview)
        self.employee_table.heading("eid", text="Emp ID")
        self.employee_table.heading("name", text="Name")
        self.employee_table.heading("email", text="Email")
        self.employee_table.heading("gender", text="Gender")
        self.employee_table.heading("contact", text="Contact")
        self.employee_table.heading("dob", text="D.O.B")
        self.employee_table.heading("doj", text="D.O.J")
        self.employee_table.heading("pass", text="Password")
        self.employee_table.heading("utype", text="User Type")
        self.employee_table.heading("address", text="Address")
        self.employee_table.heading("salary", text="Salary")
        self.employee_table["show"] = "headings"

        self.employee_table.column("eid", width=90)
        self.employee_table.column("name", width=100)
        self.employee_table.column("email", width=100)
        self.employee_table.column("gender", width=100)
        self.employee_table.column("contact", width=100)
        self.employee_table.column("dob", width=100)
        self.employee_table.column("doj", width=100)
        self.employee_table.column("pass", width=100)
        self.employee_table.column("utype", width=100)
        self.employee_table.column("address", width=100)
        self.employee_table.column("salary", width=100)
        self.employee_table.pack(fill=BOTH, expand=1)
        self.employee_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_employee()
#===================Database Functions================
    def add_employee(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_emp_id.get() == "" or self.var_name.get() == "" or self.var_pass.get() == "" or self.var_email.get() == "":
                messagebox.showerror("Error", "All fields marked by * are required", parent=self.root)
            else:
                cursor.execute("Select * from employee where eid=?",(self.var_emp_id.get(),))
                row=cursor.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Employee ID already assigned, try different",parent=self.root)
                else:
                    cursor.execute("Insert into employee (eid,name, email,gender,contact,dob,doj,pass,utype,address,salary) values(?,?,?,?,?,?,?,?,?,?,?)",(
                        self.var_emp_id.get(),
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_doj.get(),
                        self.var_pass.get(),
                        self.var_usertype.get(),
                        self.txt_address.get('1.0',END),
                        self.var_salary.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Employee Added Successfully",parent=self.root)
                    self.show_employee()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def show_employee(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from employee")
            rows=cursor.fetchall()
            self.employee_table.delete(*self.employee_table.get_children())
            for row in rows:
                self.employee_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)


    def get_data(self,ev):
        f=self.employee_table.focus()
        content=(self.employee_table.item(f))
        row=content['values']
        if not row:        #clicked a heading or empty space, no data to fetch
            return
        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_doj.set(row[6])
        self.var_pass.set(row[7])
        self.var_usertype.set(row[8])
        self.txt_address.delete('1.0', END)
        self.txt_address.insert(END, row[9])
        self.var_salary.set(row[10])

    def update_employee(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_emp_id.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Employee ID and Name are required", parent=self.root)
            else:
                cursor.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invaled Employee ID", parent=self.root)
                else:
                    cursor.execute(
                        "update employee set name=?, email=?,gender=?,contact=?,dob=?,doj=?,pass=?,utype=?,address=?,salary=? where eid=?",
                        (
                            self.var_name.get(),
                            self.var_email.get(),
                            self.var_gender.get(),
                            self.var_contact.get(),
                            self.var_dob.get(),
                            self.var_doj.get(),
                            self.var_pass.get(),
                            self.var_usertype.get(),
                            self.txt_address.get('1.0', END),
                            self.var_salary.get(),
                            self.var_emp_id.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Employee Updated Successfully", parent=self.root)
                    self.show_employee()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete_employee(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            else:
                cursor.execute("Select * from employee where eid=?", (self.var_emp_id.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invaled Employee ID", parent=self.root)
                else:
                    confirmation = messagebox.askyesno("Confirm", "Do you really want to delete this Employee?", parent=self.root)
                    if confirmation == True:
                        cursor.execute("delete from employee where eid=?", (self.var_emp_id.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Employee Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_doj.set("")
        self.var_pass.set("")
        self.var_usertype.set("Admin")
        self.txt_address.delete('1.0', END)
        self.var_salary.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show_employee()

    def search(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cursor.execute("Select * from employee where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.employee_table.delete(*self.employee_table.get_children())
                    for row in rows:
                        self.employee_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__=="__main__":
    root=Tk()
    root.title(APP_NAME)
    obj=employee(root)
    root.mainloop()