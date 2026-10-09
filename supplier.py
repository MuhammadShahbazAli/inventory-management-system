from pkgutil import get_data
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3
from config import DB_NAME, APP_NAME

class supplier:
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

        self.var_sup_invoice_id=StringVar()
        self.var_name = StringVar()
        self.var_contact=StringVar()


        #=================Search Frame================
        lbl_search = Label(self.root,text= "Search by Invoice No.",bg="white", font=("goudy old style", 12, "bold"))
        lbl_search.place(x=450, y=80)
        txt_search = Entry(self.root, font=("goudy old style", 15),textvariable= self.var_searchtxt, bg="#ECECEC").place(x=630, y=80, width=290)
        btn_search = Button(self.root, text="Search",command=self.search, font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2").place(x=935, y=80, width=110, height=28)


        #================= Title ================
        title = Label(self.root, text="Supplier Manager", font=("goudy old style", 20, "bold"), bg="#184a45",bd=3, relief=RIDGE, fg="white").place(x=50, y=10, width=1000, height=40)



        #=================Content Area================
            #=======Row1========
        lbl_sup_invoice_id = Label(self.root, text="Invoice No :", font=("goudy old style", 15), bg="white").place(x=50, y=80)
        txt_sup_invoice_id = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC", textvariable=self.var_sup_invoice_id).place(x=180, y=80, width=180)

            #=======Row2========
        lbl_name = Label(self.root, text="Name:", font=("goudy old style", 15), bg="white").place(x=50, y=120)
        txt_name = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_name).place(x=180, y=120, width=180)

            #=======Row3========
        lbl_contact = Label(self.root, text="Contact:", font=("goudy old style", 15), bg="white").place(x=50, y=160)
        txt_contact = Entry(self.root, font=("goudy old style", 15), bg="#ECECEC",textvariable=self.var_contact).place(x=180, y=160, width=180)

            #=======Row4========
        lbl_description = Label(self.root, text="Description:", font=("goudy old style", 15), bg="white").place(x=50, y=200)
        self.txt_description = Text(self.root, font=("goudy old style", 15), bg="#ECECEC")
        self.txt_description.place(x=180, y=200, width=470, height=90)

        #=======Action Buttons========
        btn_add = Button(self.root, text="Save",command=self.add_supplier, font=("goudy old style", 15), bg="green", fg="white", cursor="hand2").place(x=180, y=305, width=110, height=35)
        btn_update = Button(self.root, text="Update",command=self.update_supplier, font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2").place(x=300, y=305, width=110, height=35)
        btn_delete = Button(self.root, text="Delete",command=self.delete_supplier, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2").place(x=420, y=305, width=110, height=35)
        btn_clear = Button(self.root, text="Clear",command=self.clear, font=("goudy old style", 15), bg="gray", fg="white", cursor="hand2").place(x=540, y=305, width=110, height=35)

        #=================Supplier Details Table================
        suplier_frame = Frame(self.root, bd=3, relief=RIDGE)
        suplier_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(suplier_frame, orient=VERTICAL)
        scrollx = Scrollbar(suplier_frame, orient=HORIZONTAL)
        self.supplier_table = ttk.Treeview(suplier_frame, columns=("invoice", "name", "contact", "description"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplier_table.xview)
        scrolly.config(command=self.supplier_table.yview)
        self.supplier_table.heading("invoice", text="Invoice No.")
        self.supplier_table.heading("name", text="Name")
        self.supplier_table.heading("contact", text="Contact")
        self.supplier_table.heading("description", text="Description")
        self.supplier_table["show"] = "headings"

        self.supplier_table.column("invoice", width=90)
        self.supplier_table.column("name", width=100)
        self.supplier_table.column("contact", width=100)
        self.supplier_table.column("description", width=100)
        self.supplier_table.pack(fill=BOTH, expand=1)
        self.supplier_table.bind("<ButtonRelease-1>", self.get_data)

        self.show_supplier()
#===================Database Functions================
    def add_supplier(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_sup_invoice_id.get()=="" or self.var_name.get()=="":
                messagebox.showerror("Error","Invoice NO and Name are must be required",parent=self.root)
            else:
                cursor.execute("Select * from supplier where invoice=?",(self.var_sup_invoice_id.get(),))
                row=cursor.fetchone()
                if row!=None:
                    messagebox.showerror("Error","This Invoice No. already assigned, try different",parent=self.root)
                else:
                    cursor.execute("Insert into supplier (invoice,name, contact,description) values(?,?,?,?)",(
                        self.var_sup_invoice_id.get(),
                        self.var_name.get(),
                        self.var_contact.get(),
                        self.txt_description.get('1.0',END),
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Supplier Added Successfully",parent=self.root)
                    self.show_supplier()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def show_supplier(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from supplier")
            rows=cursor.fetchall()
            self.supplier_table.delete(*self.supplier_table.get_children())
            for row in rows:
                self.supplier_table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.supplier_table.focus()
        content = self.supplier_table.item(f)
        row = content['values']
        if not row:  # clicked a heading or empty area
            return
        self.var_sup_invoice_id.set(row[0])
        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_description.delete('1.0', END)
        self.txt_description.insert(END, row[3])

    def update_supplier(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_sup_invoice_id.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Invoice No. and Name are must be required", parent=self.root)
            else:
                cursor.execute("Select * from supplier where invoice=?", (self.var_sup_invoice_id.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invaled Invoice No.", parent=self.root)
                else:
                    cursor.execute(
                        "update supplier set name=?,contact=?,description=? where invoice=?",
                        (
                            self.var_name.get(),
                            self.var_contact.get(),
                            self.txt_description.get('1.0', END),
                            self.var_sup_invoice_id.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Supplier Updated Successfully", parent=self.root)
                    self.show_supplier()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete_supplier(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_sup_invoice_id.get() == "":
                messagebox.showerror("Error", "Invoice No. must be required", parent=self.root)
            else:
                cursor.execute("Select * from supplier where invoice=?", (self.var_sup_invoice_id.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invaled Invoice No.", parent=self.root)
                else:
                    confirmation = messagebox.askyesno("Confirm", "Do you really want to delete this Supplier?", parent=self.root)
                    if confirmation == True:
                        cursor.execute("delete from supplier where invoice=?", (self.var_sup_invoice_id.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Supplier Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_sup_invoice_id.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_description.delete('1.0', END)
        self.var_searchtxt.set("")
        self.show_supplier()

    def search(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
            else:
                cursor.execute("Select * from supplier where invoice=?", (self.var_searchtxt.get(),))
                row = cursor.fetchone()
                if row != None:
                    self.supplier_table.delete(*self.supplier_table.get_children())
                    self.supplier_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

if __name__=="__main__":
    root=Tk()
    root.title(APP_NAME)
    obj=supplier(root)
    root.mainloop()