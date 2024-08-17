from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os
class sales:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Bright Bazaar")
        self.root.config(bg="White")
        self.root.focus_force()

        # Variable
        self.var_invoice=StringVar()
        self.bill_list=[]

        # title
        lbl_title=Label(self.root,text="View Customer Bill",font=("goudy old style",30,"bold"),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        # button
        btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="lightgrey",cursor="hand2").place(x=490,y=100,width=120,height=28)

        # sales frame
        sales_frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_frame.place(x=50,y=140,width=200,height=330)

        
        scrolly=Scrollbar(sales_frame,orient=VERTICAL)
        self.sales_list=Listbox(sales_frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH,expand=1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_data)


        # bill area frame
        bill_frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_frame.place(x=280,y=140,width=390,height=390)

        lbl_title2=Label(bill_frame,text="Customer Bill Area",font=("goudy old style",20,),bg="orange").pack(side=TOP,fill=X)

        scrolly2=Scrollbar(bill_frame,orient=VERTICAL)
        scrollx2=Scrollbar(bill_frame,orient=HORIZONTAL)
        self.bill_area=Text(bill_frame,bg="lightyellow",yscrollcommand=scrolly2.set,xscrollcommand=scrollx2)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrollx2.pack(side=BOTTOM,fill=X)
        scrolly2.config(command=self.bill_area.yview)
        scrolly2.config(command=self.bill_area.xview)
        self.bill_area.pack(fill=BOTH,expand=1)

        # image
        self.bill_photo=Image.open("images/cat2.jpg")
        self.bill_photo=self.bill_photo.resize((450,300),Image.LANCZOS)
        self.bill_photo=ImageTk.PhotoImage(self.bill_photo)


        lbl_image=Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=700,y=110)

        self.show()

    # functions
    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        for i in os.listdir('bill'):
            if i.split('.')[-1]=='txt':
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.sales_list.curselection()
        file_name=self.sales_list.get(index_)
        self.bill_area.delete('1.0',END)
        fp=open(f'bill/{file_name}','r')    
        for i in fp:
            self.bill_area.insert(END,i) 
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be reguired",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')  
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i) 
                fp.close()
            else:
                messagebox.showerror("Error","Invoice no. not found",parent=self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)
        self.var_invoice.set("")

if __name__=="__main__":
    root=Tk()
    obj=sales(root)
    root.mainloop() 