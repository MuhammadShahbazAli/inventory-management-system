import subprocess
from textwrap import shorten
from tkinter import *
from PIL import ImageTk # pip install pillow
from tkinter import messagebox
import sqlite3
import os
import smtplib # pip install secure-smtplib
from tkinter import ttk, messagebox
from config import SERVER_EMAIL, SERVER_PASSWORD, DB_NAME, APP_NAME, COMPANY_NAME
import sys
import  dashboard
import billing


#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file?newreg=bb4ff82240fc44e49e4e635175989340
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_db_path():
    if getattr(sys, 'frozen', False):
        # If the application is frozen (e.g., packaged with PyInstaller)
        base_path = os.path.dirname(sys.executable)
    else:
        # If the application is not frozen (e.g., running as a script)
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, DB_NAME)


#Login Class Start From Here------------
class Login:
    def __init__(self,root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        self.root.resizable(False, False)

        self.next_screen = None  # Initialize the next_screen attribute

        conn = sqlite3.connect(database=get_db_path())
        cursor = conn.cursor()
        cursor.execute("Select * from employee")
        rows = cursor.fetchall()
        if len(rows) != 0:
            self.show_login_window()
        else:
            self.register_admin(root)


    #=================Functions================
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.root.after(2000,self.animate)


    def login_User(self):
        conn = sqlite3.connect(database=get_db_path())
        cur = conn.cursor()
        try:
            if self.var_user.get() == "" or self.var_pass.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT utype FROM employee WHERE eid=? AND pass=?",
                            (self.var_user.get(), self.var_pass.get()))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID or Password", parent=self.root)
                else:
                    self.next_screen = "dashboard" if row[0] == "Admin" else "billing"
                    self.root.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()

    def forget_password(self):
        if self.var_user.get()=="":
            messagebox.showerror("Error","Employee ID should be required", parent=self.root)
        else:
            conn = sqlite3.connect(database=get_db_path())
            cur = conn.cursor()
            try:
                cur.execute("SELECT email FROM employee WHERE eid=?", (self.var_user.get(),))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error","Invalid Employee ID", parent=self.root)
                else:
                    self.var_email_in_db.set(user[0]) #email from database

                    self.forget_window=Toplevel(self.root)
                    self.forget_window.title("Forget Password")
                    self.forget_window.geometry("400x270+500+100")
                    self.forget_window.config(bg="white")
                    self.forget_window.resizable(False,False)
                    self.forget_window.focus_force()
                    lbl_title = Label(self.forget_window, text="Reset Password", font=("times new roman", 30, "bold"), bg="white",fg="#08A3D2").place(x=0, y=30, relwidth=1)
                    lbl_email=Label(self.forget_window,text="Email:",font=("times new roman",15),bg="white").place(x=75,y=110)
                    txt_email=Entry(self.forget_window,textvariable=self.var_email,font=("times new roman",15),bg="#ECECEC").place(x=75,y=140,width=250)
                    self.btn_send_otp=Button(self.forget_window,text="Send OTP",command=lambda: self.send_otp(self.var_email.get()),font=("times new roman",15),bg="#08A3D2",fg="white",cursor="hand2")
                    self.btn_send_otp.place(x=75,y=190,width=250,height=35)
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def send_otp(self, to_email):
        # Generate a random OTP
        import random
        self.var_new_gen_otp.set(str(random.randint(100000, 999999)))

        # Send the OTP to the user's email
        try:
            if self.var_email.get() != self.var_email_in_db.get():
                messagebox.showerror("Error", "Email does not match with your email in our records", parent=self.forget_window)
                return
            else:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(SERVER_EMAIL, SERVER_PASSWORD)  # Replace with your email and password
                #Email variables
                subject = f'Your Password Recovery OTP for {APP_NAME}'
                body = f'''
Hi,

We received a request to reset your password for the {APP_NAME}.

Your One-Time Password (OTP) is: {self.var_new_gen_otp.get()}

Please do not share it with anyone.

If you did not request this, please ignore this email or contact support.

Best regards,
Team {COMPANY_NAME}
                '''
                message = f'Subject: {subject}\n\n{body}'
                #Send Email
                #print(f"Sending OTP to {to_email}...")
                server.sendmail(SERVER_EMAIL, to_email, message)
                #Check if email was sent successfully
                chek = server.ehlo()
                if chek[0] == 250:
                    messagebox.showinfo("Success", "OTP sent successfully to your email", parent=self.forget_window)
                    self.btn_send_otp.config(text="Resend OTP")
                    self.forget_window.geometry("400x420+500+100")
                    lbl_otp=Label(self.forget_window,text="Enter OTP",font=("times new roman",15),bg="white").place(x=75,y=240)
                    txt_otp=Entry(self.forget_window,textvariable=self.var_otp,font=("times new roman",15),bg="#ECECEC").place(x=75,y=270,width=250)
                    btn_verify_otp=Button(self.forget_window,text="Verify OTP",command=self.verify_otp,font=("times new roman",15),bg="#08A3D2",fg="white",cursor="hand2").place(x=75,y=320,width=250,height=35)
                server.quit()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forget_window)

    def verify_otp(self):
        if self.var_otp.get() == self.var_new_gen_otp.get():
            messagebox.showinfo("Success", "OTP verified successfully", parent=self.forget_window)
            self.forget_window.geometry("400x590+500+100")
            lbl_new_pass=Label(self.forget_window,text="New Password",font=("times new roman",15),bg="white").place(x=75,y=370)
            txt_new_pass=Entry(self.forget_window,textvariable=self.var_new_pass,font=("times new roman",15),bg="#ECECEC").place(x=75,y=400,width=250)
            lbl_conf_pass=Label(self.forget_window,text="Confirm Password",font=("times new roman",15),bg="white").place(x=75,y=430)
            txt_conf_pass=Entry(self.forget_window,textvariable=self.var_conf_pass,font=("times new roman",15),bg="#ECECEC").place(x=75,y=460,width=250)
            btn_update_pass=Button(self.forget_window,text="Update Password",command=self.update_password,font=("times new roman",15),bg="#08A3D2",fg="white",cursor="hand2").place(x=75,y=510,width=250,height=35)
        else:
            messagebox.showerror("Error","Invalid OTP, please try again", parent=self.forget_window)


    def update_password(self):
        if self.var_new_pass.get() == "" or self.var_conf_pass.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.forget_window)
        elif self.var_new_pass.get() != self.var_conf_pass.get():
            messagebox.showerror("Error", "New Password and Confirm Password do not match", parent=self.forget_window)
        else:
            conn = sqlite3.connect(database=get_db_path())
            cur = conn.cursor()
            try:
                cur.execute("UPDATE employee SET pass=? WHERE eid=?", (self.var_new_pass.get(), self.var_user.get()))
                conn.commit()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_window)
                self.forget_window.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.forget_window)
            finally:
                conn.close()


    def show_login_window(self):
        # =================Variables================
        self.var_user = StringVar()
        self.var_pass = StringVar()
        self.var_employee_id = StringVar()
        self.var_email = StringVar()
        self.var_email_in_db = StringVar()
        self.var_new_gen_otp = StringVar()
        self.var_otp = StringVar()
        self.var_new_pass = StringVar()
        self.var_conf_pass = StringVar()


        # =================BG Image================
        self.bg = ImageTk.PhotoImage(file=resource_path("images\\phone.png"))
        lbl_bg = Label(self.root, image=self.bg, bd=0).place(x=200, y=30)

        # =================Login Frame================
        login_frame = Frame(self.root, bd=2, relief="ridge", bg="white")
        login_frame.place(x=650, y=80, width=350, height=460)

        lbl_title = Label(login_frame, text="LOGIN", font=("times new roman", 30, "bold"), bg="white",fg="#08A3D2").place(x=100, y=50)

        lbl_user = Label(login_frame, text="Employee ID", font=("Times New Roman", 15), bg="white", fg="#767171").place(x=50, y=120)
        txt_user = Entry(login_frame, textvariable=self.var_user, font=("times new roman", 15), bg="#ECECEC").place(x=50, y=150, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Times New Roman", 15), bg="white", fg="#767171").place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.var_pass, font=("times new roman", 15), bg="#ECECEC",show="*").place(x=50, y=230, width=250)

        btn_login = Button(login_frame, text="Login", command=self.login_User, font=("times new roman", 15),bg="#08A3D2", fg="white", cursor="hand2").place(x=50, y=290, width=250, height=35)

        hr_line = Label(login_frame, bg="lightgray").place(x=50, y=370, width=250, height=2)
        lbl_or = Label(login_frame, text="OR", font=("times new roman", 15), bg="white", fg="#767171").place(x=160,y=357)

        btn_forget = Button(login_frame, text="Forget Password?", command=self.forget_password,font=("times new roman", 12), bg="white", fg="#08A3D2", activebackground="white",activeforeground="#08A3D2", bd=0, cursor="hand2").place(x=50, y=400, width=250, height=35)

        # ==================Signup Frame=================
        signup_frame = Frame(self.root, bd=2, relief="ridge", bg="white")
        signup_frame.place(x=650, y=560, width=350, height=60)

        lbl_acc = Label(signup_frame, text="Developed By " + COMPANY_NAME,font=("times new roman", 10, "underline"), bg="white", fg="#767171").place(x=0, y=17,relwidth=1)
        # ==================Animated Images=================
        self.im1 = ImageTk.PhotoImage(file=resource_path("images\\im1.png"))
        self.im2 = ImageTk.PhotoImage(file=resource_path("images\\im2.png"))
        self.im3 = ImageTk.PhotoImage(file=resource_path("images\\im3.png"))

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367, y=133, width=240, height=428)

        self.animate()

    def register_admin(self, root):
        self.root=root
        self.root.geometry("1100x500+220+190")
        self.root.config(bg="White")
        self.root.resizable(False, False)
        self.root.focus_force()

        #=================Variables================
        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_usertype = StringVar()
        self.var_address = StringVar()
        self.var_salary = StringVar()

        # ================= Title ================
        title = Label(self.root, text="Admin Registration", font=("goudy old style", 20, "bold"), bg="green", bd=3,relief=RIDGE, fg="white").place(x=50, y=50, width=1000)

        # =================Content Area================
        # =======Row1========
        lbl_emp_id = Label(self.root, text="Emp ID:*", font=("goudy old style", 15), bg="white").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender:", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        txt_emp_id = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_emp_id).place(x=150, y=150, width=180)
        cmb_gender = ttk.Combobox(self.root, textvariable=self.var_gender,values=["Select", "Male", "Female", "Others"], state="readonly", justify=CENTER,font=("goudy old style", 15))
        cmb_gender.place(x=500, y=150, width=180)
        cmb_gender.current(0)
        txt_contact = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_contact).place(x=850, y=150, width=180)

        # =======Row2========
        lbl_name = Label(self.root, text="Name:*", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B:", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        lbl_doj = Label(self.root, text="D.O.J:", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        txt_name = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_name).place(x=150, y=190, width=180)
        txt_dob = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_dob).place(x=500, y=190, width=180)
        txt_doj = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_doj).place(x=850, y=190, width=180)

        # =======Row3========
        lbl_email = Label(self.root, text="Email:*", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_pass = Label(self.root, text="Password:*", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        lbl_usertype = Label(self.root, text="User Type:", font=("goudy old style", 15), bg="white").place(x=750, y=230)

        txt_email = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_email).place(x=150, y=230, width=180)
        txt_pass = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_pass).place(x=500, y=230, width=180)
        cmb_usertype = ttk.Combobox(self.root, textvariable=self.var_usertype, values=["Admin"],state="readonly", justify=CENTER, font=("goudy old style", 15))
        cmb_usertype.place(x=850, y=230, width=180)
        cmb_usertype.current(0)

        # =======Row4========
        lbl_address = Label(self.root, text="Address:", font=("goudy old style", 15), bg="white").place(x=350, y=270)
        lbl_salary = Label(self.root, text="Salary:", font=("goudy old style", 15), bg="white").place(x=50, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="#ECECEC")
        self.txt_address.place(x=500, y=270, width=300, height=60)
        txt_salary = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_salary).place(x=150, y=270, width=180)

        # =======Action Buttons========
        btn_add = Button(self.root, text="Save Admin", command=self.add_admin, font=("goudy old style", 20, "bold"), bg="#2196f3",fg="white", cursor="hand2").place(x=425, y=380, width=250, height=50)


    def add_admin(self):
        conn = sqlite3.connect(database=get_db_path())
        cursor = conn.cursor()
        try:
            if self.var_emp_id.get()=="" or self.var_name.get()=="" or self.var_pass.get()=="" or self.var_email.get()=="":
                messagebox.showerror("Error","All fields marked by * are required",parent=self.root)
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
                    self.go_to_login()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)


    def go_to_login(self):
        self.root.destroy()
        main()

def main():
    root = Tk()
    root.title(APP_NAME)
    obj = Login(root)
    root.mainloop()

    if obj.next_screen == "dashboard":
        dashboard.main()
    elif obj.next_screen == "billing":
        billing.main()


if __name__=="__main__":
    main()

