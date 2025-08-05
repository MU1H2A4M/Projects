from tkinter import *
from tkinter import ttk 
import sqlite3
from PIL import Image, ImageTk


conn = sqlite3.connect("pharma.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS medicines (
          mid INTEGER PRIMARY KEY AUTOINCREMENT,
           mname TEXT,
           manufacter TEXT,
           price INTEGER,
           expiry TEXT
          )""")

c.execute("""CREATE TABLE IF NOT EXISTS Employee (
          eid INTEGER PRIMARY KEY AUTOINCREMENT,
           ename TEXT,
           password TEXT,
           email TEXT
          )""")

def confirm(ID, password):
    pass_chk = "SELECT password FROM Employee WHERE eid = ? LIMIT 10000"
    c.execute(pass_chk, (ID,))
    global result
    result = c.fetchone()
    if result and result[0] == password:
        login = Label(root, text="you are logged-in!", fg="green", padx=70)
        login.place(relx=0.5, rely=0.45, anchor=CENTER)
        next = Button(root, text="Med-Table", fg="blue", font=("Arial", 13), command=Med_table_info)
        next.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        incorrect = Label(root, text="password or UserID incorrect", fg='red')
        incorrect.place(relx=0.5, rely=0.45, anchor=CENTER)
    
def Insert_Cred(ename, password, email):
    email_chk = "SELECT 1 FROM Employee WHERE email = ? LIMIT 10000"
    c.execute(email_chk, (email,))
    global result
    result = c.fetchone()
    if result is None:
        c.execute("""INSERT INTO Employee (ename, password, email) VALUES (?, ?, ?)""", (ename, password, email))
        conn.commit()
        creation = Label(root, text="Account Created!", fg="green", padx=70)
        creation.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        fail = Label(root, text="Email already exists.", fg='red')
        fail.place(relx=0.5, rely=0.5, anchor=CENTER)

def print_table(table_name): 
    c.execute(f"SELECT * FROM {table_name}") 
    rows = c.fetchall() 
    for row in rows: 
        print(row)

print_table("Employee")
print_table("medicines")

def display(check):
    query = "SELECT * FROM Employee WHERE password = ? LIMIT 10000"
    c.execute(query, (check,))
    global result
    result = c.fetchone()

    if result:
        hidden = "*" * len(result[2])
        display = Label(root, text=f"Account Info:\neid: {result[0]}\nUser-Name: {result[1]}\nPassword: {hidden}\nEmail: {result[3]}", font=("Arial", 12, "bold"))
        display.place(relx=0.5, rely=0.4, anchor=CENTER)
    else:
        display2 = Label(root, text=" ", padx=400, pady=50).place(relx=0.5, rely=0.4, anchor=CENTER) 

def display_table(table_name, root, conn):
    main_frame = ttk.Frame(root)
    main_frame.pack(pady=20)
    
    frame = ttk.Frame(main_frame, width=1600, height=800)
    frame.pack_propagate(False)  
    frame.pack()

    tree = ttk.Treeview(frame, height=25)  
    tree.pack(side="left", fill="x")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]

    tree["columns"] = columns
    tree["show"] = "headings"

    col_width = int(1600 / len(columns)) 
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=col_width, stretch=False)

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

def Med_insertion():
    for widget in root.winfo_children():
        widget.destroy()
    load_background_img(root ,"background_1.jpg")
    canva = Canvas(root, width=600, height=500, bg="#90b7f5")
    canva.place(relx=0.5, rely=0.35, anchor=CENTER)  
    Label(root, text="PHARMA ENTRY:", bg="#90b7f5", font=("Arial", 22, "bold")).place(relx=0.5, rely=0.15, anchor=CENTER)
    row1_entry = Entry(root, width=25, border=3)
    row1_entry.place(relx=0.6, rely=0.3, anchor=CENTER)
    row2_entry = Entry(root, width=25, border=3)
    row2_entry.place(relx=0.6, rely=0.35, anchor=CENTER)
    row3_entry = Entry(root, width=25, border=3)
    row3_entry.place(relx=0.6, rely=0.4, anchor=CENTER)
    row4_entry = Entry(root, width=25, border=3)
    row4_entry.place(relx=0.6, rely=0.45, anchor=CENTER)
    row1_label = Label(root, text="Enter Medicine Name:", bg="#90b7f5", font=("Arial", 10, "bold"))
    row1_label.place(relx=0.45, rely=0.3, anchor=CENTER)
    row2_label = Label(root, text="Enter Manufacter Name:", bg="#90b7f5", font=("Arial", 10, "bold"))
    row2_label.place(relx=0.45, rely=0.35, anchor=CENTER)
    row3_label = Label(root, text="Enter Medicine Price:", bg="#90b7f5", font=("Arial", 10, "bold"))
    row3_label.place(relx=0.45, rely=0.4, anchor=CENTER)
    row4_label = Label(root, text="Enter Medicine Expiry:", bg="#90b7f5", font=("Arial", 10, "bold"))
    row4_label.place(relx=0.45, rely=0.45, anchor=CENTER)
    enter_values = Button(root, text="Next", bg="#90b7f5", font=("Arial", 10, "bold"), command=lambda: Med_changes(str(row1_entry.get()), str(row2_entry.get()), str(row3_entry.get()), str(row4_entry.get())))
    enter_values.place(relx=0.65, rely=0.55, anchor=CENTER)
    back = Button(root, text="Back", bg="#90b7f5", font=("Arial", 10, "bold"), command=Med_table_info)
    back.place(relx=0.35, rely=0.55, anchor=CENTER)


    def Med_changes(med_name, med_fname, med_price, med_expiry):
        if not med_name or not med_fname or not med_price or not med_expiry:
            Label(root, text="Fill all the entries", fg="red").place(relx=0.5, rely=0.45, anchor=CENTER)
            return

        mname_chk = "SELECT 1 FROM medicines WHERE mname = ? LIMIT 1"
        c.execute(mname_chk, (med_name,))
        result = c.fetchone()

        def add_entry():
            c.execute("""INSERT INTO medicines (mname, manufacter, price, expiry) VALUES (?, ?, ?, ?)""", (med_name, med_fname, med_price, med_expiry))
            conn.commit()
            Label(root, text="Entries Successfully Added!", fg="green", padx=70).place(relx=0.5, rely=0.5, anchor=CENTER)

        if result is None:
            add_entry()
        else:
            Label(root, text="Already made that entry.\nAre you sure you want to enter again?", fg="red").place(relx=0.5, rely=0.5, anchor=CENTER)
            yes_button = Button(root, text="Yes", fg="green", width=10, command=add_entry)
            yes_button.place(relx=0.6, rely=0.5, anchor=CENTER)
            no_button = Button(root, text="No", fg="red", width=10, command=Med_insertion)
            no_button.place(relx=0.4, rely=0.5, anchor=CENTER)

def mdel(delete):
    try:
        delete = int(delete)
        
        del_chk = "DELETE FROM medicines WHERE mid = ?"
        c.execute(del_chk, (delete,))
        conn.commit()
        
        if c.rowcount > 0:
            Label(root, text=f"Row with mid = {delete} deleted successfully.", fg="green").place(relx=0.5, rely=0.1, anchor=CENTER)
            root.after(1500, Med_table_info)  
        else:
            Label(root, text=f"No row found with mid = {delete}.", fg="red", padx=20).place(relx=0.5, rely=0.1, anchor=CENTER)
    except ValueError:
        Label(root, text="Please enter a valid integer for mid.", fg="red", padx=20).place(relx=0.5, rely=0.1, anchor=CENTER)
    except Exception as e:
        Label(root, text=f"Error: {str(e)}", fg="red", padx=20).place(relx=0.5, rely=0.1, anchor=CENTER)

def Med_deletion():
    Label(root, text="Enter Mid to delete:", font=("Arial", 10)).place(relx=0.4, rely=0.95, anchor=CENTER)
    deletion = Entry(root, width=25, border=2)
    deletion.place(relx=0.5, rely=0.95, anchor=CENTER)
    Button(root, text="Delete", command=lambda: mdel(deletion.get())).place(relx=0.65, rely=0.95, anchor=CENTER)
def Med_table_info():
    for widget in root.winfo_children():
        widget.destroy()
    load_background_img(root ,"background_5.jpg")
    canva = Canvas(root, width=500, height=150, bg="#b8e0bf")
    canva.place(relx=0.5, rely=0.85, anchor=CENTER)  
    display_table("medicines", root, conn)
    Label(root, text="MEDICINE TABLE ", border=4, font=("Arial", 20 , "bold")).place(relx=0.45, rely=0.10 , anchor= CENTER)
    Button(root, text="Insert into table",border=4, command=Med_insertion).place(relx=0.5, rely=0.95, anchor=CENTER)
    Button(root, text="Delete from the table",border=4, command=Med_deletion).place(relx=0.5, rely=0.9, anchor=CENTER)
    Button(root, text="<<", border=4 ,command=Existed_Employee).place(relx=0.35, rely=0.9, anchor=CENTER)

def login_menu():
    for widget in root.winfo_children():
        widget.destroy()
    load_background_img(root ,"background_3.png")
    canva = Canvas(root, width=1900, height=180, bg="#e8e8e3")
    canva.place(relx=0.5, rely=0.52, anchor=CENTER)  
    logo_img(root,"logo.png",0.25,0.53)
    login_menu_label = Label(root, text="LOGIN OR SIGN-UP AS EMPLOYEE", bg="#e8e8e3",font=("Arial", 20, "bold")).place(relx=0.5, rely=0.46, anchor=CENTER)
    account_creation = Button(root, text="Create Account", bg="#b5575f" , fg= "#e8e8e3", width=15, border=5, command=New_Employee).place(relx=0.4, rely=0.53, anchor=CENTER)
    account_verification = Button(root, text="Sign-in", bg="#b5575f" , fg= "#e8e8e3" , width=15, border=5, command=Existed_Employee).place(relx=0.6, rely=0.53, anchor=CENTER)
    Button(root,text="<<" , bg="#b5575f" , fg= "#e8e8e3" , command= main_menu).place(relx=0.5, rely=0.57, anchor=CENTER)
    
def Next_fn(name, pass1, pass2, email):
    if len(name) < 1 or len(pass1) < 1 or len(pass2) < 1 or len(email) < 1:
        eight_char = Label(root, text="Fill all the entries!", fg="red", padx=10)
        eight_char.place(relx=0.5, rely=0.45, anchor=CENTER)
    elif len(pass1) < 8:
        chk_pass = Label(root, text="Password Must Be at least 8 characters!", fg="red", padx=40)
        chk_pass.place(relx=0.5, rely=0.45, anchor=CENTER)
    elif pass1 != pass2:
        fill_AE = Label(root, text="Password Does Not Match!", fg="red", padx=90)
        fill_AE.place(relx=0.5, rely=0.5, anchor=CENTER)
    else:
        space = Label(root, text=" ", bg="#90b7f5", padx=150)
        space.place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(root, text=" ", bg="#90b7f5", padx=150).place(relx=0.5, rely=0.45, anchor=CENTER)
        Insert_Cred(name, pass1, email)
        display(pass1)

def Existed_Employee():
    for widget in root.winfo_children():
        widget.destroy()
    load_background_img(root ,"background_4.jpg")
    canva = Canvas(root, width=700, height=400, bg="#5d7080")
    canva.place(relx=0.5, rely=0.35, anchor=CENTER)  
    logo_img(root,"logo.png",0.05,0.1)
    entry_box1 = Entry(root, width=35)
    entry_box1.place(relx=0.55, rely=0.3, anchor=CENTER)
    entry_box2 = Entry(root, width=35, show="*")
    entry_box2.place(relx=0.55, rely=0.35, anchor=CENTER)
    heading = Label(root, text="LOGIN TO CF-PHARMACY DATABASE", bg="#5d7080", font=("Arial", 20, "bold"))
    heading.place(relx=0.5, rely=0.2, anchor=CENTER)
    entry_label1 = Label(root, text="UserID:", bg="#5d7080", font=("Arial", 11))
    entry_label1.place(relx=0.4, rely=0.3, anchor=CENTER)
    entry_label2 = Label(root, text="Password:", bg="#5d7080", font=("Arial", 11))
    entry_label2.place(relx=0.4, rely=0.35, anchor=CENTER)
    confirm_button = Button(root, text="Next", bg="#5d7080", font=("Arial", 11, "bold"), command=lambda: confirm(entry_box1.get(), str(entry_box2.get())))
    confirm_button.place(relx=0.65, rely=0.5, anchor=CENTER)
    previous_button = Button(root, text="Back", bg="#5d7080", font=("Arial", 11, "bold"), command=login_menu)
    previous_button.place(relx=0.35, rely=0.5, anchor=CENTER)

def New_Employee():
    for widget in root.winfo_children():
        widget.destroy()
    load_background_img(root ,"background_4.jpg")
    canva = Canvas(root, width=750, height=800, bg="#5d7080")
    canva.place(relx=0.5, rely=0.1, anchor=CENTER)
    logo_img(root,"logo.png",0.05,0.1)
    Label(root, text="CREATE NEW EMPLOYEE:" , bg="#5d7080" ,font=("Arial", 22, "bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    entry_box1 = Entry(root, width=15)
    entry_box1.place(relx=0.55, rely=0.15, anchor=CENTER)
    entry_box2 = Entry(root, width=15, show="*")
    entry_box2.place(relx=0.55, rely=0.2, anchor=CENTER)
    entry_box3 = Entry(root, width=15, show="*")
    entry_box3.place(relx=0.55, rely=0.25, anchor=CENTER)
    entry_box4 = Entry(root, width=35)
    entry_box4.place(relx=0.58, rely=0.3, anchor=CENTER)
    entry_label1 = Label(root, text="Name:", bg="#5d7080", font=("Arial", 12))
    entry_label1.place(relx=0.45, rely=0.15, anchor=CENTER)
    entry_label2 = Label(root, text="Password:", bg="#5d7080", font=("Arial", 12))
    entry_label2.place(relx=0.45, rely=0.2, anchor=CENTER)
    entry_label3 = Label(root, text="Confirm Password:", bg="#5d7080", font=("Arial", 12))
    entry_label3.place(relx=0.45, rely=0.25, anchor=CENTER)
    entry_label4 = Label(root, text="Email:", bg="#5d7080", font=("Arial", 12))
    entry_label4.place(relx=0.45, rely=0.3, anchor=CENTER)
    confirm_button = Button(root, text="Next", bg="#5d7080", font=("Arial", 12, "bold"), command=lambda: Next_fn(str(entry_box1.get()), str(entry_box2.get()), str(entry_box3.get()), str(entry_box4.get())))
    confirm_button.place(relx=0.65, rely=0.4, anchor=CENTER)
    previous_button = Button(root, text="Back", bg="#5d7080", font=("Arial", 12, "bold"), command=login_menu)
    previous_button.place(relx=0.35, rely=0.4, anchor=CENTER)

def blink(label):
    if label.winfo_exists():
        if label.cget("foreground") == "black":
            label.config(foreground="white")
        else:
            label.config(foreground="black")
        root.after(500, blink, label)

def logo_img(window,image_path,x,y):
    try:
        image = Image.open(image_path)
        image = image.resize((160, 160), Image.Resampling.LANCZOS)  
        photo = ImageTk.PhotoImage(image)

        
        label = Label(window, image=photo)
        label.image = photo  
        label.place(relx=x, rely=y, anchor=CENTER)  

    except Exception as e:
        print(f"Error loading logo image: {e}")
        label = Label(window, text="Error loading background image", bg="white", fg="red")
        label.place(relx=x, rely=y, anchor=CENTER)     


def load_background_img(window, image_path):
    try:
        window.update_idletasks()  
        win_width = window.winfo_width()
        win_height = window.winfo_height()

        image = Image.open(image_path)
        image = image.resize((win_width, win_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        label = Label(window, image=photo)
        label.image = photo  
        label.place(x=0, y=0, relwidth=1, relheight=1) 

    except Exception as e:
        print(f"Error loading background image: {e}")
        label = Label(window, text="Error loading background image", bg="white", fg="red")
        label.place(x=0, y=0, relwidth=1, relheight=1)  


def main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    
    load_background_img(root ,"background_2.jpg")
    frame = Frame(root, bg="#90b7f5")
    frame.place(relx=0.5, rely=0.53, anchor=CENTER)
    canva = Canvas(frame, width=520, height=600, bg="#97a1a1")
    canva.pack()
    logo_img(root,"logo.png",0.5,0.1) 
    Label(root, text="Welcome to CF-Pharmaceuticals", fg="black", bg="#97a1a1", font=("Arial", 16, "bold")).place(relx=0.5, rely=0.22, anchor=CENTER)

    canva.create_text(250, 150, text="MADE BY", font=("Arial", 15, "bold"), fill="black")
    canva.create_text(250, 180, text="MUHAMMAD UZAIR", font=("Arial", 11, "bold"), fill="black")
    
    
    canva.create_rectangle(70, 100, 430, 300, outline="black", width=2.05)

    button = Button(root, text="Press this button to continue", bg="#97a1a1", font=("Arial", 12), command=login_menu)
    button.place(relx=0.5, rely=0.75, anchor=CENTER)
    blink(button)

root = Tk()
root.title("Pharmacy Database")
root.geometry("1600x900")


main_menu()

root.mainloop()

conn.commit()
conn.close()