from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk, messagebox
class billing:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="White")

        # title
        self.icon_title=PhotoImage(file="images/logo1.png")
        self.title=Label(self.root,text="Inventory Management System",image=self.icon_title,compound="left",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        # button logout
        btn_logout=Button(self.root,text="Logout",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1100,y=5,height=50,width=150)

        # clock
        self.lbl_clock=Label(self.root,text="Welcome Inventory Management System\t\t Date:DD-MM-YYYY\t\t Time:HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

    #product frame

        # variable
        self.var_search=StringVar()


        product_frame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        product_frame1.place(x=6,y=110,width=410,height=550)

        p_title=Label(product_frame1,text="All products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        # search frame

        product_frame2=Frame(product_frame1,bd=2,relief=RIDGE,bg="white")
        product_frame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(product_frame2,text="Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)
        
        lbl_search=Label(product_frame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=45)
        txt_search=Entry(product_frame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=50,width=150,height=22)
        btn_search=Button(product_frame2,text="Search",font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=285,y=47,width=100,height=25)
        btn_show_all=Button(product_frame2,text="Show All",font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=285,y=10,width=100,height=25)

        # Product Details
        product_frame3 = Frame(product_frame1, bd=3, relief=RIDGE)
        product_frame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(product_frame3, orient=VERTICAL)
        scrollx = Scrollbar(product_frame3, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(product_frame3, columns=("pid","name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid", text="PID")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Quantity")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"

        self.productTable.column("pid", width=90)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=100)
        self.productTable.column("qty", width=100)
        self.productTable.column("status", width=100)
        # self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.productTable.pack(fill=BOTH, expand=1)
        lbl_note=Label(product_frame1,text="Note: Enter 0 QTY To Remove Product From Cart",font=("goudy old style",12,"bold"),anchor=W,bg="white",fg="red").pack(side=BOTTOM,fill=X)
        


        

if __name__=="__main__":
    root=Tk()
    obj=billing(root)
    root.mainloop() 