from pkgutil import get_data
from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
from config import DB_NAME, APP_NAME

class sales:
    def __init__(self,root):
        self.root=root
        self.root.title(APP_NAME)
        self.root.geometry("1100x500+220+190")
        self.root.config(bg="White")
        self.root.resizable(False, False)
        self.root.focus_force()

    #=================Variables================
        self.var_invoice=StringVar()
        self.bill_list = []

    #===================Title================
        title=Label(self.root,text="Sales Manager",font=("goudy old style",25,"bold"), bd=3, relief=RIDGE,bg="#184a45",fg="White",pady=10)
        title.pack(side=TOP,fill=X,padx=10, pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=("times new roman",20),bg="White").place(x=50,y=100)
        self.txt_invoice=Entry(self.root,textvariable= self.var_invoice, font=("times new roman",15),bg="#ECECEC")
        self.txt_invoice.place(x=200,y=100,width=180,height=30)

    #===================Buttons================
        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman", 15), bg="green", fg="white", cursor="hand2").place(x=400, y=100, width=150, height=30)
        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15), bg="red", fg="white", cursor="hand2").place(x=560, y=100, width=150, height=30)

    #===================Bill List================
        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=150,width=220,height=330)

        scroll_y=Scrollbar(sales_frame,orient=VERTICAL)
        scroll_y.pack(side=RIGHT,fill=Y)
        self.sales_list=Listbox(sales_frame,font=("goudy old style",15),bg="#ECECEC")
        scroll_y.config(command=self.sales_list.yview)
        self.sales_list.pack(side=LEFT,fill=BOTH,expand=1)
        self.sales_list.bind("<ButtonRelease-1>", self.get_bill_data)

    #===================Bill Area================
        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=150,width=430,height=330)

        lbl_title=Label(bill_frame,text="Customer Bill Area",font=("times new roman",20),bg="orange").pack(side=TOP,fill=X)

        scroll_y=Scrollbar(bill_frame,orient=VERTICAL)
        scroll_y.pack(side=RIGHT,fill=Y)
        self.bill_area=Text(bill_frame,bg="#ECECEC",yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)
        self.update_bill_frame()

    #===================Images================
        self.im1=Image.open("images/cat2.jpg")
        self.im1=self.im1.resize((360,300),Image.Resampling.LANCZOS)
        self.im1=ImageTk.PhotoImage(self.im1)
        self.lbl_im1=Label(self.root,image=self.im1,bd=0,relief=RAISED)
        self.lbl_im1.place(x=720,y=160)

        self.show_bill()
    #================Functions===================
    def show_bill(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        for i in os.listdir("Bills"):
            if i.split(".")[-1] == "txt":
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split(".")[0])

    def get_bill_data(self, ev):
        bill_list_index = self.sales_list.curselection()
        file_name = self.sales_list.get(bill_list_index)
        self.bill_area.delete(1.0,END)
        fp = open(f"Bills/{file_name}", "r")
        for line in fp:
            self.bill_area.insert(END,line)
        fp.close()


    def clear(self):
        self.show_bill()
        self.bill_area.delete(1.0,END)
        self.txt_invoice.delete(0,END)

    def search(self):
        if self.var_invoice.get() == "":
            messagebox.showerror("Error", "Invoice No. should be required", parent=self.root)
        else:
            if self.var_invoice.get().capitalize() in self.bill_list:
                fp = open(f"Bills/{self.var_invoice.get()}.txt", "r")
                self.bill_area.delete(1.0, END)
                for line in fp:
                    self.bill_area.insert(END, line)
                fp.close()
            else:
                messagebox.showerror("Error", "Invalid Invoice No.", parent=self.root)


    def update_bill_frame(self):
        self.bill_list.clear()
        if not os.path.isdir("Bills"):
            self.bill_area.delete(1.0, END)
            return

        for i in os.listdir("Bills"):
            if i.split(".")[-1] == "txt":
                self.bill_list.append(i.split(".")[0])
        self.bill_area.delete(1.0, END)
        if not self.bill_list:
            return

        file_name = self.bill_list[0]
        with open(f"Bills/{file_name}.txt", "r") as fp:
            for line in fp:
                self.bill_area.insert(END, line)

if __name__=="__main__":
    root=Tk()
    root.title(APP_NAME)
    obj=sales(root)
    root.mainloop()