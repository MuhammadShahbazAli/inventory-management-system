from tkinter import*
from PIL import Image,ImageTk
from employee import employee
from supplier import supplier
from category import category
from product import product
from sales import sales
import sqlite3 as sql
from tkinter import messagebox
import os
import sys
import time
from config import DB_NAME, APP_NAME, BUSINESS_NAME, APP_NICK_NAME, COMPANY_NAME, CONTACT_NUMBER
import login


#https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file?newreg=bb4ff82240fc44e49e4e635175989340
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class IMS:
    def __init__(self,root):
        self.root=root
        self.root.title(APP_NAME)
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="White")

    #=================Variables================
        self.child_window=None

    # ==============Title================
        self.title_img=PhotoImage(file=resource_path("images\\logo1.png"))
        title=Label(self.root,text=BUSINESS_NAME+" "+APP_NICK_NAME,image=self.title_img,compound="left",bd=10,relief=GROOVE,font=("times new roman",40,"bold"),bg="#010c48",fg="White", anchor="w", padx=10,pady=20)
        title.pack(side=TOP,fill=X)

    #=====Logout_Button===========
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2")
        btn_logout.place(relx=0.9,y=65,height=50,width=180, anchor="e")

    #=================Clock================
        self.lbl_clock=Label(self.root,text="Welcome to "+BUSINESS_NAME+" "+APP_NAME+"\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.pack(side=TOP,fill=X)

    #=================Left Menu================
        self.menu_logo=Image.open(resource_path("images\\menu_im.png"))
        self.menu_logo=self.menu_logo.resize((200,200),Image.Resampling.LANCZOS)
        self.menu_logo=ImageTk.PhotoImage(self.menu_logo)

        left_menu=Frame(self.root,bd=2,relief=RIDGE,bg="White")
        left_menu.pack(side=LEFT,fill=Y)
        lbl_menu_logo=Label(left_menu,image=self.menu_logo,bd=2,relief=RIDGE)
        lbl_menu_logo.pack(side=TOP,fill=X)

        menu_label=Label(left_menu,text="Menu",font=("times new roman",20, "bold"),bg="#009688")
        menu_label.pack(side=TOP,fill=X)

        #=================Menu Buttons================
        self.btn_icon=PhotoImage(file=resource_path("images\\side.png"))
        btn_employee=Button(left_menu,text="Employee",image=self.btn_icon, compound="left", padx=5, anchor="w",command=self.employee,font=("times new roman",20,"bold"),bg="white",cursor="hand2")
        btn_employee.pack(side=TOP,fill=X)
        btn_supplier = Button(left_menu, text="Supplier", image=self.btn_icon, compound="left", padx=5, anchor="w",command=self.supplier, font=("times new roman", 20, "bold"), bg="white", cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X)
        btn_category = Button(left_menu, text="Category", image=self.btn_icon, compound="left", padx=5, anchor="w",command=self.category, font=("times new roman", 20, "bold"), bg="white", cursor="hand2")
        btn_category.pack(side=TOP, fill=X)
        btn_product = Button(left_menu, text="Products", image=self.btn_icon, compound="left", padx=5, anchor="w",command=self.product, font=("times new roman", 20, "bold"), bg="white", cursor="hand2")
        btn_product.pack(side=TOP, fill=X)
        btn_sales = Button(left_menu, text="Sales", image=self.btn_icon, compound="left", padx=5, anchor="w",command=self.sales, font=("times new roman", 20, "bold"), bg="white", cursor="hand2")
        btn_sales.pack(side=TOP, fill=X)
        btn_exit = Button(left_menu, text="Exit", image=self.btn_icon, compound="left", padx=5, anchor="w",command=self.exit, font=("times new roman", 20, "bold"), bg="white", cursor="hand2")
        btn_exit.pack(side=TOP, fill=X)

    #=================Content Area================
        self.lbl_employee=Label(self.root,text="Total Employees\n 0 ",bd=5,relief=RIDGE,font=("goudy old style",20,"bold"),bg="#33bbf9",fg="white")
        self.lbl_employee.place(x=300,y=200,height=150,width=300)
        self.lbl_supplier = Label(self.root, text="Total Suppliers\n 0 ", bd=5, relief=RIDGE, font=("goudy old style", 20, "bold"), bg="#ff5722", fg="white")
        self.lbl_supplier.place(x=650, y=200, height=150, width=300)
        self.lbl_category = Label(self.root, text="Total Categories\n 0 ", bd=5, relief=RIDGE, font=("goudy old style", 20, "bold"), bg="#009688", fg="white")
        self.lbl_category.place(x=1000, y=200, height=150, width=300)
        self.lbl_product = Label(self.root, text="Total Products\n 0 ", bd=5, relief=RIDGE, font=("goudy old style", 20, "bold"), bg="#607d8b", fg="white")
        self.lbl_product.place(x=300, y=400, height=150, width=300)
        self.lbl_sales = Label(self.root, text="Total Sales\n 0 ", bd=5, relief=RIDGE, font=("goudy old style", 20, "bold"), bg="#ffc107", fg="white")
        self.lbl_sales.place(x=650, y=400, height=150, width=300)

    #=================Footer================
        lbl_footer=Label(self.root,text=BUSINESS_NAME+" "+APP_NAME+" | Developed by "+COMPANY_NAME+" | 2026\n For Any Technical Issue Feel Free to Contact: "+CONTACT_NUMBER,font=("times new roman",12),bg="#4d636d",fg="white")
        lbl_footer.pack(side=BOTTOM,fill=X)

        self.update_content()
    #=================Logout Function================
    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op == True:
            self.root.destroy()
            login.main()

    #=================Employee Function================
    def employee(self):
        if self.child_window==None or not self.child_window.winfo_exists():
            self.new_Window=Toplevel(self.root)
            self.app=employee(self.new_Window)
            self.child_window=self.new_Window
        else:
            self.child_window.destroy()
            self.new_Window=Toplevel(self.root)
            self.app=employee(self.new_Window)
            self.child_window=self.new_Window

    #=================Supplier Function================
    def supplier(self):
        if self.child_window==None or not self.child_window.winfo_exists():
            self.new_Window=Toplevel(self.root)
            self.app=supplier(self.new_Window)
            self.child_window=self.new_Window
        else:
            self.child_window.destroy()
            self.new_Window=Toplevel(self.root)
            self.app=supplier(self.new_Window)
            self.child_window=self.new_Window

    #=================Category Function================
    def category(self):
        if self.child_window==None or not self.child_window.winfo_exists():
            self.new_Window=Toplevel(self.root)
            self.app=category(self.new_Window)
            self.child_window=self.new_Window
        else:
            self.child_window.destroy()
            self.new_Window=Toplevel(self.root)
            self.app=category(self.new_Window)
            self.child_window=self.new_Window

    #=================Product Function================
    def product(self):
        if self.child_window==None or not self.child_window.winfo_exists():
            self.new_Window=Toplevel(self.root)
            self.app=product(self.new_Window)
            self.child_window=self.new_Window
        else:
            self.child_window.destroy()
            self.new_Window=Toplevel(self.root)
            self.app=product(self.new_Window)
            self.child_window=self.new_Window

    #=================Sales Function================
    def sales(self):
        if self.child_window==None or not self.child_window.winfo_exists():
            self.new_Window=Toplevel(self.root)
            self.app=sales(self.new_Window)
            self.child_window=self.new_Window
        else:
            self.child_window.destroy()
            self.new_Window=Toplevel(self.root)
            self.app=sales(self.new_Window)
            self.child_window=self.new_Window

    #=================Exit Function================
    def exit(self):
        op = messagebox.askyesno("Confirm", "Do you really want to exit?", parent=self.root)
        if op == True:
            self.root.destroy()


    def update_content(self):
        con=sql.connect(database=resource_path(r'ims_database.db'))
        cur=con.cursor()
        try:
            #===================Employee Count================
            cur.execute("select * from employee")
            emp=cur.fetchall()
            self.lbl_employee.config(text=f"Total Employees\n {str(len(emp))} ")

            #===================Supplier Count================
            cur.execute("select * from supplier")
            sup = cur.fetchall()
            self.lbl_supplier.config(text=f"Total Suppliers\n {str(len(sup))} ")

            #===================Category Count================
            cur.execute("select * from category")
            cat = cur.fetchall()
            self.lbl_category.config(text=f"Total Categories\n {str(len(cat))} ")

            #===================Product Count================
            cur.execute("select * from product")
            pro = cur.fetchall()
            self.lbl_product.config(text=f"Total Products\n {str(len(pro))} ")

            #===================Sales Count================
            if not os.path.exists('Bills'):
                os.makedirs('Bills')
            self.lbl_sales.config(text=f"Total Sales\n {str(len(os.listdir('Bills')))} ")

            #===================Clock Update================
            current_time = time.strftime("%H:%M:%S")
            current_date = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to {BUSINESS_NAME} {APP_NAME}\t\t Date: {current_date}\t\t Time: {current_time}")
            self.lbl_clock.after(1000, self.update_content)  # Update every second

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent=self.root)

def main():
    root=Tk()
    root.title(APP_NAME)
    obj=IMS(root)
    root.mainloop()

if __name__=="__main__":
        main()