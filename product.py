from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class product:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Bright Bazaar")
        self.root.config(bg="White")
        self.root.focus_force()

        # Variables
        self.var_searchBy = StringVar()
        self.var_searchtxt = StringVar()
        self.var_pid = StringVar()
        self.var_category = StringVar()
        self.var_suppliers = StringVar()
        self.var_price = StringVar()
        self.var_quantity = StringVar()
        self.var_status = StringVar()
        self.var_name = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sup()

        # Product Frame
        product_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_frame.place(x=10, y=10, width=450, height=480)

        # Title
        title = Label(product_frame, text="Manage Products Details", font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # Labels and Entries
        lbl_category = Label(product_frame, text="Category", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_frame, text="Supplier", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_frame, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=160)
        lbl_price = Label(product_frame, text="Price", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=210)
        lbl_qty = Label(product_frame, text="Quantity", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=260)
        lbl_status = Label(product_frame, text="Status", font=("goudy old style", 15, "bold"), bg="white").place(x=30, y=310)

        # Category Combobox
        cmb_cat = ttk.Combobox(product_frame, textvariable=self.var_category, values=self.cat_list, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_cat.place(x=150, y=60, width=200)
        cmb_cat.current(0)

        # Supplier Combobox
        cmb_supplier = ttk.Combobox(product_frame, textvariable=self.var_suppliers, values=self.sup_list, state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_supplier.place(x=150, y=110, width=200)
        cmb_supplier.current(0)

        # Product Name Entry
        txt_name = Entry(product_frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=160, width=200)

        # Price Entry
        txt_price = Entry(product_frame, textvariable=self.var_price, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=210, width=200)

        # Quantity Entry
        txt_qty = Entry(product_frame, textvariable=self.var_quantity, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=260, width=200)

        # Status Combobox
        cmb_status = ttk.Combobox(product_frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_status.place(x=150, y=310, width=200)
        cmb_status.current(0)

        # Buttons
        btn_add = Button(product_frame, text="Save", command=self.add, font=("goudy old style", 15), bg="#2196f3", fg="white", cursor="hand2").place(x=10, y=400, width=100, height=40)
        btn_update = Button(product_frame, text="Update", command=self.update, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=120, y=400, width=100, height=40)
        btn_delete = Button(product_frame, text="Delete", command=self.delete, font=("goudy old style", 15), bg="#f44336", fg="white", cursor="hand2").place(x=230, y=400, width=100, height=40)
        btn_clear = Button(product_frame, text="Clear", command=self.clear, font=("goudy old style", 15), bg="#607d8b", fg="white", cursor="hand2").place(x=340, y=400, width=100, height=40)

        # Search Frame
        SearchFrame = LabelFrame(self.root, text="Search Product", bg="white", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE)
        SearchFrame.place(x=480, y=10, width=600, height=80)

        # Search Options
        cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchBy, values=("Select", "Category", "Supplier", "Name"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10, width=180)
        btn_search = Button(SearchFrame, text="Search", command=self.search, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        # Product Details
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)

        self.productTable = ttk.Treeview(p_frame, columns=("pid", "category", "supplier", "name", "price", "qty", "status"), yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrollx.config(command=self.productTable.xview)
        scrolly.config(command=self.productTable.yview)

        self.productTable.heading("pid", text="PID")
        self.productTable.heading("category", text="Category")
        self.productTable.heading("supplier", text="Supplier")
        self.productTable.heading("name", text="Name")
        self.productTable.heading("price", text="Price")
        self.productTable.heading("qty", text="Quantity")
        self.productTable.heading("status", text="Status")
        self.productTable["show"] = "headings"

        self.productTable.column("pid", width=90)
        self.productTable.column("category", width=100)
        self.productTable.column("supplier", width=100)
        self.productTable.column("name", width=100)
        self.productTable.column("price", width=100)
        self.productTable.column("qty", width=100)
        self.productTable.column("status", width=100)
        self.productTable.bind("<ButtonRelease-1>", self.get_data)

        self.productTable.pack(fill=BOTH, expand=1)

        self.show()

    # Function to fetch categories and suppliers
    def fetch_cat_sup(self):
        con = sqlite3.connect('ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM category")
            cats = cur.fetchall()
            self.cat_list.append("Select")
            if len(cats) > 0:
                for cat in cats:
                    self.cat_list.append(cat[0])

            cur.execute("SELECT name FROM supplier")
            sups = cur.fetchall()
            self.sup_list.append("Select")
            if len(sups) > 0:
                for sup in sups:
                    self.sup_list.append(sup[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # Add Product
    def add(self):
        if self.var_category.get() == "Select" or self.var_suppliers.get() == "Select" or self.var_name.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()

                # Check if the product already exists
                cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Product already exists. Please try a different one.", parent=self.root)
                else:
                    # Insert the new product into the database
                    cur.execute("INSERT INTO product (category, supplier, name, price, qty, status) VALUES (?, ?, ?, ?, ?, ?)",
                                (
                                    self.var_category.get(),
                                    self.var_suppliers.get(),
                                    self.var_name.get(),
                                    self.var_price.get(),
                                    self.var_quantity.get(),
                                    self.var_status.get()
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Product added successfully", parent=self.root)
                    self.show()
                    self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    # Delete Product
    def delete(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product ID. Please select the product from the list.", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
                    if op == True:
                        cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Success", "Product deleted successfully", parent=self.root)
                        self.show()
                        self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    # Clear Fields
    def clear(self):
        self.var_pid.set("")
        self.var_category.set("Select")
        self.var_suppliers.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_quantity.set("")
        self.var_status.set("Active")
        self.var_searchtxt.set("")
        self.var_searchBy.set("Select")
        self.show()

    # Update Product
    def update(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
        elif self.var_category.get() == "Select" or self.var_suppliers.get() == "Select" or self.var_name.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()

                # Check if the product exists
                cur.execute("SELECT * FROM product WHERE pid=?", (self.var_pid.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Product ID. Please select the product from the list.", parent=self.root)
                else:
                    # Update the product's information
                    cur.execute("""UPDATE product SET category=?, supplier=?, name=?, price=?, qty=?, status=? WHERE pid=? """, (
                        self.var_category.get(),
                        self.var_suppliers.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_quantity.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success", "Product updated successfully", parent=self.root)
                    self.show()
                    self.clear()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

    # Show Products
    def show(self):
        try:
            con = sqlite3.connect('ims.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()
            self.productTable.delete(*self.productTable.get_children())
            for row in rows:
                self.productTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # Get Data from Table
    def get_data(self, event):
        f = self.productTable.focus()
        content = self.productTable.item(f)
        row = content['values']
        if row:  # Check if the row is not empty
            self.var_pid.set(row[0])
            self.var_category.set(row[1])
            self.var_suppliers.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_quantity.set(row[5])
            self.var_status.set(row[6])

    # Search Products
    def search(self):
        if self.var_searchBy.get() == "Select":
            messagebox.showerror("Error", "Please select a search criterion", parent=self.root)
        elif self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
        else:
            try:
                con = sqlite3.connect('ims.db')
                cur = con.cursor()
                if self.var_searchBy.get() == "Category":
                    cur.execute("SELECT * FROM product WHERE category LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                elif self.var_searchBy.get() == "Supplier":
                    cur.execute("SELECT * FROM product WHERE supplier LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                elif self.var_searchBy.get() == "Name":
                    cur.execute("SELECT * FROM product WHERE name LIKE ?", ('%' + self.var_searchtxt.get() + '%',))
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.productTable.delete(*self.productTable.get_children())
                    for row in rows:
                        self.productTable.insert('', END, values=row)
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
            finally:
                con.close()

if __name__ == "__main__":
    root = Tk()
    obj = product(root)
    root.mainloop()
