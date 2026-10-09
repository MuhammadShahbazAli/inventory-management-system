from tkinter import*
from tkinter import ttk, messagebox
from PIL import Image,ImageTk
import sqlite3
import time
import os
import tempfile
from config import DB_NAME, APP_NAME, BUSINESS_NAME, APP_NICK_NAME, COMPANY_NAME, CONTACT_NUMBER, CLIENT_CONTACT_NUMBER
import login

class billManager:
    def __init__(self,root):
        self.root=root
        self.root.title(APP_NAME)
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="White")
        self.root.resizable(False, False)
        self.cart_list = []
        self.chk_print = 0

    # ==============Title================
        self.title_img=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text=BUSINESS_NAME+" "+APP_NICK_NAME,image=self.title_img,compound="left",bd=10,relief=GROOVE,font=("times new roman",40,"bold"),bg="#010c48",fg="White", anchor="w", padx=10,pady=20)
        title.pack(side=TOP,fill=X)

    #=====Logout_Button===========
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2")
        btn_logout.place(relx=0.9,y=65,height=50,width=180, anchor="e")

    #=================Clock================
        self.lbl_clock=Label(self.root,text=f"Welcome to {BUSINESS_NAME} {APP_NAME}\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.pack(side=TOP,fill=X)


    #=================Content Area================
        #=============Product Frame================
        productFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        productFrame1.place(x=6,y=160,width=410,height=515)

        pfTitle = Label(productFrame1, text="All Products", font=("goudy old style", 20, "bold"), bg="green", fg="white")
        pfTitle.pack(side=TOP, fill=X)

        #=================Search Frame================
        self.var_search=StringVar()

        productFrame2 = Frame(productFrame1, bd=2, relief=RIDGE, bg="white")
        productFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(productFrame2, text="Search Product | By Name", font=("goudy old style", 15, "bold"), bg="white", fg="green")
        lbl_search.place(x=2, y=5)

        lbl_name = Label(productFrame2, text="Product Name", font=("goudy old style", 15, "bold"), bg="white")
        lbl_name.place(x=5, y=45)
        txt_search = Entry(productFrame2,bd="2", textvariable=self.var_search, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=150, y=47, width=150, height=22)
        btn_search = Button(productFrame2, text="Search", command=self.search, font=("times new roman", 15), bg="#2196f3", fg="white", cursor="hand2")
        btn_search.place(x=310, y=45, width=80, height=25)
        btn_show_all = Button(productFrame2, text="Show All", command=self.show_product, font=("times new roman", 15), bg="orange", fg="white", cursor="hand2")
        btn_show_all.place(x=290, y=10, width=100, height=25)

        #=================Product Details Frame================
        productFrame3 = Frame(productFrame1, bd=3, relief=RIDGE)
        productFrame3.place(x=2, y=140, width=398, height=335)

        scrolly = Scrollbar(productFrame3, orient=VERTICAL)
        scrollx = Scrollbar(productFrame3, orient=HORIZONTAL)
        self.product_table = ttk.Treeview(productFrame3, columns=("pid", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid", text="PID")
        self.product_table.heading("name", text="Name")
        self.product_table.heading("price", text="Price")
        self.product_table.heading("qty", text="Qty")
        self.product_table.heading("status", text="Status")
        self.product_table["show"] = "headings"
        self.product_table.column("pid", width=60)
        self.product_table.column("name", width=100)
        self.product_table.column("price", width=90)
        self.product_table.column("qty", width=60)
        self.product_table.column("status", width=80)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(productFrame1, text="Note: Enter 0 Qty to remove product from the Cart !", font=("goudy old style", 12, "bold"), anchor="w", bg="white", fg="red")
        lbl_note.pack(side=BOTTOM, fill=X)

        #=================Customer Frame================
        self.var_name=StringVar()
        self.var_contact=StringVar()
        customer_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        customer_frame.place(x=420, y=160, width=530, height=80)

        cTitle = Label(customer_frame, text="Customer Details", font=("goudy old style", 15, "bold"), bg="lightgray")
        cTitle.pack(side=TOP, fill=X)
        lbl_name = Label(customer_frame, text="Name:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_name.place(x=5, y=40)
        txt_name = Entry(customer_frame,bd="2", textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
        txt_name.place(x=75, y=40, width=150, height=22)
        lbl_contact = Label(customer_frame, text="Contact No.", font=("goudy old style", 15, "bold"), bg="white")
        lbl_contact.place(x=235, y=40)
        txt_contact = Entry(customer_frame,bd="2", textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
        txt_contact.place(x=355, y=40, width=155, height=22)

        #=================Calculator & Cart Frame================
        cal_cart_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        cal_cart_frame.place(x=420, y=240, width=530, height=320)

        #=================Calculator Frame================
        self.var_cal_input = StringVar()
        self.var_cal_input.set("0")

        cal_frame = Frame(cal_cart_frame, bd=4, relief=RIDGE, bg="white")
        cal_frame.place(x=3, y=5, width=268, height=300)

        self.txt_cal_screen = Entry(cal_frame, bd=3, textvariable=self.var_cal_input, font=("goudy old style", 20), bg="lightyellow", state="readonly", justify="right")
        self.txt_cal_screen.pack(side=TOP, fill=X, ipady=15)

        btns_frame = Frame(cal_frame, bd=2, relief=RIDGE, bg="white")
        btns_frame.pack(side=TOP, fill=BOTH, expand=1)

        btns = [
            ("AC", 1, 0), ("%", 1, 1), ("C", 1, 2), ("/", 1, 3), ("*", 1, 4),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("4", 2, 3), ("-", 2, 4),
            ("5", 3, 0), ("6", 3, 1), ("1", 3, 2), ("2", 3, 3), ("+", 3, 4),
            ("3", 4, 0), ("0", 4, 1), ("00", 4, 2), (".", 4, 3), ("=", 4, 4)
        ]
        for (text, row, col) in btns:
            if text == "=":
                btn = Button(btns_frame, text=text, font=("goudy old style", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2", command=self.calculate)
            else:
                btn = Button(btns_frame, text=text, font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=lambda t=text: self.calculator_input(t))
            btn.grid(row=row, column=col, sticky="nsew")
        for i in range(5):
            btns_frame.rowconfigure(i,pad=13, weight=1)
            btns_frame.columnconfigure(i, weight=1)

        #=================Bill Frame================
        bill_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        bill_frame.place(x=955, y=160, width=390, height=400)
        bill_title = Label(bill_frame, text="Customer Bills", font=("goudy old style", 15, "bold"), bg="green", fg="white")
        bill_title.pack(side=TOP, fill=X)

        scrolly = Scrollbar(bill_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        self.txt_Bill_area = Text(bill_frame, yscrollcommand=scrolly.set, state=DISABLED)
        scrolly.config(command=self.txt_Bill_area.yview)
        self.txt_Bill_area.pack(side=LEFT, fill=BOTH, expand=1)

        #=================Bill Related Buttons================
        btn_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        btn_frame.place(x=955, y=565, width=390, height=110)

        self.lbl_bill_amount = Label(btn_frame, text="Bill Amount\n0.00", font=("goudy old style", 15),relief="sunken", bg="#3f51b5", fg="white")
        self.lbl_bill_amount.place(x=2, y=5, width=120, height=50)
        self.lbl_discount = Label(btn_frame, text="Discount\n0.00", font=("goudy old style", 15),relief="sunken", bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=124, y=5, width=120, height=50)
        self.lbl_net_pay = Label(btn_frame, text="Net Pay\n0.00", font=("goudy old style", 15),relief="sunken", bg="#607d8b", fg="white")
        self.lbl_net_pay.place(x=246, y=5, width=135, height=50)

        btn_print = Button(btn_frame, text="Print", command=self.print_bill, font=("times new roman", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2")
        btn_print.place(x=2, y=60, width=120, height=40)
        btn_delete_bill = Button(btn_frame, text="Delete Bill", command=self.delete_bill, font=("times new roman", 15, "bold"), bg="red", fg="white", cursor="hand2")
        btn_delete_bill.place(x=124, y=60, width=120, height=40)
        btn_generate_bill = Button(btn_frame, text="Generate Bill", command=self.generate_bill, font=("times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_generate_bill.place(x=246, y=60, width=135, height=40)


        #=================Cart Frame================
        cart_frame = Frame(cal_cart_frame, bd=4, relief=RIDGE, bg="white")
        cart_frame.place(x=275, y=5, width=245, height=300)
        self.cart_title = Label(cart_frame, text="Cart \t Total Product: 0", font=("times new roman", 13, "bold"), bg="lightgray")
        self.cart_title.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cart_frame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx = Scrollbar(cart_frame, orient=HORIZONTAL)
        scrollx.pack(side=BOTTOM, fill=X)
        self.cart_table = ttk.Treeview(cart_frame, columns=("pid", "name", "price", "qty"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrolly.config(command=self.cart_table.yview)
        scrollx.config(command=self.cart_table.xview)
        self.cart_table.heading("pid", text="PID")
        self.cart_table.heading("name", text="Name")
        self.cart_table.heading("price", text="Price")
        self.cart_table.heading("qty", text="Qty")
        self.cart_table["show"] = "headings"
        self.cart_table.column("pid", width=40)
        self.cart_table.column("name", width=100)
        self.cart_table.column("price", width=100)
        self.cart_table.column("qty", width=40)
        self.cart_table.pack(fill=BOTH, expand=1)
        self.cart_table.bind("<ButtonRelease-1>", self.get_cart_data)

        #=================Add Cart Widget================
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        add_cart_widget_frame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        add_cart_widget_frame.place(x=420, y=565, width=530, height=110)

        pro_Name = Label(add_cart_widget_frame, text="Product Name:", font=("goudy old style", 15, "bold"), bg="white")
        pro_Name.place(x=5, y=5)
        txt_pro_name = Entry(add_cart_widget_frame,bd="2", font=("goudy old style", 15), textvariable=self.var_pname, bg="lightyellow", state="readonly")
        txt_pro_name.place(x=5, y=35, width=190, height=22)
        pro_price = Label(add_cart_widget_frame, text="Price Per Unit:", font=("goudy old style", 15, "bold"), bg="white")
        pro_price.place(x=200, y=5)
        txt_pro_price = Entry(add_cart_widget_frame,bd="2", font=("goudy old style", 15), textvariable=self.var_price, bg="lightyellow", state="readonly")
        txt_pro_price.place(x=200, y=35, width=150, height=22)
        pro_qty = Label(add_cart_widget_frame, text="Quantity:", font=("goudy old style", 15, "bold"), bg="white")
        pro_qty.place(x=360, y=5)
        txt_pro_qty = Entry(add_cart_widget_frame,bd="2", font=("goudy old style", 15), textvariable=self.var_qty, bg="lightyellow")
        txt_pro_qty.place(x=360, y=35, width=150, height=22)

        lbl_Stock = Label(add_cart_widget_frame, text="Stock:", font=("goudy old style", 15, "bold"), bg="white")
        lbl_Stock.place(x=5, y=70)
        txt_Stock = Entry(add_cart_widget_frame,bd="2", font=("goudy old style", 15), textvariable=self.var_stock, bg="lightyellow", state="readonly")
        txt_Stock.place(x=75, y=75, width=120, height=22)

        btn_clear_cart = Button(add_cart_widget_frame, text="Clear All", command=self.clear_cart, font=("Times New Roman", 15, "bold"), bg="red", fg="white", cursor="hand2")
        btn_clear_cart.place(x=200, y=70, width=100, height=30)
        btn_add_cart = Button(add_cart_widget_frame, text="Add | Update Cart", command=self.add_update_cart, font=("Times New Roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2")
        btn_add_cart.place(x=310, y=70, width=200, height=30)

        # ===============Footer Area==================
        footer = Label(self.root,text=BUSINESS_NAME+" "+APP_NAME+" | Developed by "+COMPANY_NAME+" | 2026 : For Any Technical Issue Feel Free to Contact: "+CONTACT_NUMBER,font=("times new roman", 10), bg="#4d636d", fg="white")
        footer.pack(side=BOTTOM, fill=X)


        self.show_product()
        self.update_time_date()

#=================Functions================
    def logout(self):
        op = messagebox.askyesno("Confirm", "Do you really want to logout?", parent=self.root)
        if op == True:
            self.root.destroy()
            login.main()



    def calculator_input(self, value):
        current = self.var_cal_input.get()
        if value == "AC":
            self.var_cal_input.set("0")
        elif value == "C":
            self.var_cal_input.set(current[:-1] or "0")
        elif current == "0" and value == ".":
            self.var_cal_input.set("0.")
        elif current == "0":
            self.var_cal_input.set(value)
        else:
            self.var_cal_input.set(current + value)

    def calculate(self):
        try:
            result = eval(self.var_cal_input.get())
            self.var_cal_input.set(str(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            self.var_cal_input.set("0")


    def show_product(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("Select pid,name,price,qty,status from product where status='Active'")
            rows = cursor.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def search(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cursor.execute(
                    "Select pid,name,price,qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status='Active'")
                rows = cursor.fetchall()
                if len(rows) != 0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showinfo("Info", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def get_data(self, ev):
        f = self.product_table.focus()
        content = (self.product_table.item(f))
        row = content['values']
        if not row:         # clicked on heading or empty area of the table
            return

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_stock.set(row[3])
        self.var_qty.set("1")  # Default quantity to 1 when a product is selected

    def get_cart_data(self, ev):
        f = self.cart_table.focus()
        content = (self.cart_table.item(f))
        row = content['values']
        if not row:         # clicked on heading or empty area of the table
            return

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])  # Assuming the quantity is in the 4th column of the product table
        self.var_stock.set(row[4])  # Assuming the stock is in the 5th column of the product table

    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == "":
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        else:
            try:
                quantity = int(self.var_qty.get())
                stock = int(self.var_stock.get())
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a valid whole number", parent=self.root)
                return

            if quantity < 0 or quantity > stock:
                messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
                return

            product_id = self.var_pid.get()
            existing_index = next(
                (i for i, item in enumerate(self.cart_list) if item[0] == product_id),
                None
            )

            if quantity == 0:
                if existing_index is not None:
                    self.cart_list.pop(existing_index)
            else:
                price_cal = float(self.var_price.get())
                cart_data = [product_id, self.var_pname.get(), price_cal, quantity, self.var_stock.get()]

                if existing_index is not None:
                    option = messagebox.askyesno(
                        "Confirm",
                        f"{self.var_pname.get()} is already in the cart. Do you want to update the quantity or remove it?",
                        parent=self.root
                    )
                    if option:
                        self.cart_list[existing_index] = cart_data
                else:
                    self.cart_list.append(cart_data)

            self.update_cart_table()
            self.update_bill_amount()

    def update_cart_table(self):
        self.cart_table.delete(*self.cart_table.get_children())
        for item in self.cart_list:
            self.cart_table.insert('', END, values=item)


    def update_bill_amount(self):
        total_amount = sum(item[2] * item[3] for item in self.cart_list)
        discount = total_amount * 0.05
        net_pay = total_amount - discount

        self.lbl_bill_amount.config(text=f"Bill Amount\n{total_amount:.2f}")
        self.lbl_discount.config(text=f"Discount\n{discount:.2f}")
        self.lbl_net_pay.config(text=f"Net Pay\n{net_pay:.2f}")
        self.cart_title.config(text=f"Cart \t Total Product: {len(self.cart_list)}")


#==================Bill Generation and Printing Functions================
    def generate_bill(self):
        if self.chk_print == 1:
            self.chk_print = 0  # Reset the print flag for a new bill
        if not self.cart_list:
            messagebox.showerror("Error", "Cart is empty. Please add products to generate a bill.", parent=self.root)
            return

        if self.var_name.get() == "" or self.var_contact.get() == "":
            messagebox.showerror("Error", "Customer details are required to generate a bill.", parent=self.root)
            return

        invoice_no = f"INV{int(time.time())}"
        bill_content = f'''  
{BUSINESS_NAME}-{APP_NICK_NAME}
Phone No. {CLIENT_CONTACT_NUMBER} , Gujjranwala-52250
{str("-"*40)}
Invoice No: {invoice_no}\nCustomer Name: {self.var_name.get()}\nContact: {self.var_contact.get()}\n\n
{str("-"*40)}
Product\tPrice\tQty\tTotal
{str("-"*40)}
        '''

        total_amount = 0
        for item in self.cart_list:
            total = item[2] * item[3]
            total_amount += total
            bill_content += f"\n{item[1]}\t{item[2]:.2f}\t{item[3]}\t{total:.2f}\n"

        discount = total_amount * 0.05
        net_pay = total_amount - discount

        bill_content += "-" * 40 + "\n"
        bill_content += f"Total Amount: {total_amount:.2f}\n"
        bill_content += f"Discount (5%): {discount:.2f}\n"
        bill_content += f"Net Pay: {net_pay:.2f}\n"

        # Save the bill to a text file
        with open(f"Bills/{invoice_no}.txt", "w") as f:
            f.write(bill_content)

        # Display the bill in the bill area
        self.txt_Bill_area.config(state=NORMAL)
        self.txt_Bill_area.delete(1.0, END)
        self.txt_Bill_area.insert(END, bill_content)
        self.txt_Bill_area.config(state=DISABLED)

        # Show Success Message
        messagebox.showinfo("Success", f"Bill generated successfully!\nInvoice No: {invoice_no}", parent=self.root)

        self.chk_print = 1  # Set the print flag to indicate that the bill has been generated
        self.update_stock_after_sale()  # Update stock in the database after sale
        self.clear_cart() # Clear the cart and reset the form



    def update_stock_after_sale(self):
        conn = sqlite3.connect(database=DB_NAME)
        cursor = conn.cursor()
        for item in self.cart_list:
            new_qty = int(item[4]) - int(item[3])  # item[4] is stock, item[3] is quantity sold
            cursor.execute("UPDATE product SET qty=?, status=? WHERE pid=?", (
                new_qty, "Active" if new_qty > 0 else "Inactive", item[0]))
        conn.commit()
        conn.close()
        self.show_product()  # Refresh the product list to show updated quantities


    def clear_cart(self):
        self.cart_list.clear()
        self.update_cart_table()
        self.update_bill_amount()
        self.var_name.set("")
        self.var_contact.set("")
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_stock.set("")
        self.var_search.set("")

    def delete_bill(self):
        if self.txt_Bill_area.get(1.0, END).strip() == "":
            messagebox.showerror("Error", "No bill to delete.", parent=self.root)
            return
        self.txt_Bill_area.config(state=NORMAL)
        self.txt_Bill_area.delete(1.0, END)
        self.txt_Bill_area.config(state=DISABLED)
        self.chk_print = 0 # Reset the print flag since the bill has been deleted

    def update_time_date(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to {BUSINESS_NAME} {APP_NAME}\t\t Date: {current_date}\t\t Time: {current_time}")
        self.root.after(1000, self.update_time_date)  # Update every second

    def print_bill(self):
        if self.chk_print == 1:
            # Save the bill content to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
            temp_file.write(self.txt_Bill_area.get(1.0, END).encode('utf-8'))
            temp_file.close()

            # Open the temporary file with the default text editor for printing
            os.startfile(temp_file.name, "print")
        else:
            messagebox.showerror("Error", "Please generate the bill before printing.", parent=self.root)


def main():
    root = Tk()
    root.title(APP_NAME)
    obj = billManager(root)
    root.mainloop()

if __name__=="__main__":
    main()