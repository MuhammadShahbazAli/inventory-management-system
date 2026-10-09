from pkgutil import get_data
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3
from config import APP_NAME, DB_NAME

class product:
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

        self.cat_list = []
        self.sup_list = []
        self.var_cat=StringVar()
        self.var_pid=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_quant=StringVar()
        self.var_status=StringVar()

        self.fetch_cat_sup()

        #=================Product Frame================
        product_frame=Frame(self.root,bd=3,relief=RIDGE, bg="White")
        product_frame.place(x=10,y=10,width=450,height=480)

        #=================Title================
        title=Label(product_frame,text="Product Manager",font=("goudy old style",18,"bold"), bd=3, relief=RIDGE,bg="#184a45",fg="White",pady=10)
        title.pack(side=TOP,fill=X,padx=2, pady=2)

        #=================Entry Fields================
        cat_lbl = Label(product_frame, text="Select Category:", font=("goudy old style", 15), bg="White").place(x=10, y=70)
        sup_lbl = Label(product_frame, text="Select Supplier:", font=("goudy old style", 15), bg="White").place(x=10, y=120)
        name_lbl = Label(product_frame, text="Product Name:", font=("goudy old style", 15), bg="White").place(x=10, y=170)
        price_lbl = Label(product_frame, text="Price:", font=("goudy old style", 15), bg="White").place(x=10, y=220)
        quant_lbl = Label(product_frame, text="Quantity:", font=("goudy old style", 15), bg="White").place(x=10, y=270)
        status_lbl = Label(product_frame, text="Status:", font=("goudy old style", 15), bg="White").place(x=10, y=320)

        self.cat_combo = ttk.Combobox(product_frame,textvariable=self.var_cat, font=("goudy old style", 15), state="readonly", justify=CENTER)
        self.cat_combo.place(x=200, y=70, width=200)
        self.cat_combo["values"] = self.cat_list
        self.cat_combo.current(0)
        self.sup_combo = ttk.Combobox(product_frame,textvariable=self.var_sup, font=("goudy old style", 15), state="readonly", justify=CENTER)
        self.sup_combo.place(x=200, y=120, width=200)
        self.sup_combo["values"] = self.sup_list
        self.sup_combo.current(0)

        self.name_entry = Entry(product_frame,textvariable=self.var_name, font=("goudy old style", 15), bg="#ECECEC")
        self.name_entry.place(x=200, y=170, width=200)
        self.price_entry = Entry(product_frame,textvariable=self.var_price, font=("goudy old style", 15), bg="#ECECEC")
        self.price_entry.place(x=200, y=220, width=200)
        self.quant_entry = Entry(product_frame,textvariable=self.var_quant, font=("goudy old style", 15), bg="#ECECEC")
        self.quant_entry.place(x=200, y=270, width=200)

        self.status_combo = ttk.Combobox(product_frame,textvariable=self.var_status, font=("goudy old style", 15), state="readonly", justify=CENTER)
        self.status_combo.place(x=200, y=320, width=200)
        self.status_combo["values"] = ("Active", "Inactive")
        self.status_combo.current(0)

        #=================Buttons================
        btn_add = Button(product_frame, text="Save", command=self.add_product, font=("goudy old style", 15), bg="green", fg="white", cursor="hand2").place(x=10, y=390, width=100, height=40)
        btn_update = Button(product_frame, text="Update",command=self.update_product, font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2").place(x=120, y=390, width=100, height=40)
        btn_delete = Button(product_frame, text="Delete",command=self.delete_product, font=("goudy old style", 15), bg="red", fg="white", cursor="hand2").place(x=230, y=390, width=100, height=40)
        btn_clear = Button(product_frame, text="Clear",command=self.clear, font=("goudy old style", 15), bg="gray", fg="white", cursor="hand2").place(x=340, y=390, width=100, height=40)

        #=================Search Panel================
        search_frame=LabelFrame(self.root,text="Search Product",font=("goudy old style", 15), bd=2, relief=RIDGE, bg="White")
        search_frame.place(x=470,y=10,width=620,height=80)

        search_combo = ttk.Combobox(search_frame,textvariable=self.var_searchby, font=("goudy old style", 15), state="readonly", justify=CENTER)
        search_combo.place(x=10, y=10, width=180)
        search_combo["values"] = ("Select", "Category", "Supplier", "Name")
        search_combo.current(0)
        search_entry = Entry(search_frame,textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="#ECECEC")
        search_entry.place(x=200, y=10, width=240, height=30)
        btn_search = Button(search_frame,command=self.search, text="Search", font=("goudy old style", 15), bg="blue", fg="white", cursor="hand2").place(x=450, y=10, width=155, height=30)

        #=================Product Details================
        details_frame=Frame(self.root,bd=3,relief=RIDGE)
        details_frame.place(x=470,y=100,width=620,height=390)
        scrolly=Scrollbar(details_frame,orient=VERTICAL)
        scrollx=Scrollbar(details_frame,orient=HORIZONTAL)
        self.product_table=ttk.Treeview(details_frame,columns=("pid","cat","sup","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid",text="Product ID")
        self.product_table.heading("cat",text="Category")
        self.product_table.heading("sup",text="Supplier")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Quantity")
        self.product_table.heading("status",text="Status")
        self.product_table["show"]="headings"
        self.product_table.column("pid",width=90)
        self.product_table.column("cat",width=100)
        self.product_table.column("sup",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=100)
        self.product_table.column("status",width=100)
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)
        self.show_product()

    # ===================Database Functions================
    def fetch_cat_sup(self):
        self.cat_list.append("No Category Added")
        self.sup_list.append("No Supplier Added")
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("Select name from category")
            cat_rows = cursor.fetchall()
            if len(cat_rows) > 0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for row in cat_rows:
                    self.cat_list.append(row[0])
            cursor.execute("Select name from supplier")
            sup_rows = cursor.fetchall()
            if len(sup_rows) > 0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for row in sup_rows:
                    self.sup_list.append(row[0])
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def add_product(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_cat.get() == "No Category Added" or self.var_sup.get() == "No Supplier Added" or self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "" or self.var_price.get() == "" or self.var_quant.get() == "":
                messagebox.showerror("Error", "All Fields are required", parent=self.root)
            else:
                cursor.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cursor.fetchone()
                if row != None:
                    messagebox.showerror("Error", "This Product is Already added, try different",parent=self.root)
                else:
                    cursor.execute("Insert into product (Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",
                                (
                                    self.var_cat.get(),
                                    self.var_sup.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_quant.get(),
                                    self.var_status.get()
                                ))
                    conn.commit()
                    messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
                    self.show_product()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show_product(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("Select * from product")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        if not row:         #clicked a heading or empty area
            return
        self.var_pid.set(row[0]),
        self.var_cat.set(row[1]),
        self.var_sup.set(row[2]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_quant.set(row[5]),
        self.var_status.set(row[6])

    def update_product(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "" or self.var_price.get() == "" or self.var_quant.get() == "":
                messagebox.showerror("Error", "Product Id and Name are required", parent=self.root)
            else:
                cursor.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invaled Product ID", parent=self.root)
                else:
                    cursor.execute(
                        "update product set Category=?, Supplier=?,name=?,price=?,qty=?,status=? where pid=?",
                        (
                            self.var_cat.get(),
                            self.var_sup.get(),
                            self.var_name.get(),
                            self.var_price.get(),
                            self.var_quant.get(),
                            self.var_status.get(),
                            self.var_pid.get()
                        ))
                    conn.commit()
                    messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
                    self.show_product()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete_product(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Error", "Select Product from the List first", parent=self.root)
            else:
                cursor.execute("Select * from product where pid=?", (self.var_pid.get(),))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invaled Product", parent=self.root)
                else:
                    confirmation = messagebox.askyesno("Confirm", "Do you really want to delete this Product?",
                                                       parent=self.root)
                    if confirmation == True:
                        cursor.execute("delete from product where pid=?", (self.var_pid.get(),))
                        conn.commit()
                        messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def clear(self):
        self.var_pid.set("")
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_quant.set("")
        self.var_status.set("Active")

        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show_product()

    def search(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select Search By Option", parent=self.root)
            elif self.var_searchtxt.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cursor.execute(
                    "Select * from product where " + self.var_searchby.get() + " LIKE '%" + self.var_searchtxt.get() + "%'")
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)




if __name__=="__main__":
    root=Tk()
    root.title(APP_NAME)
    obj=product(root)
    root.mainloop()