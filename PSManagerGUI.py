from App import App
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip
import random
import string

class PSManagerGUI:
    def __init__(self, master, user, password, cluster_name):
        self.master = master
        self.master.title("PSManager")
        self.master.attributes('-zoomed', True)
        self.app = App(user=user, password=password, cluster_name=cluster_name)

        self.label = tk.Label(master, text="PSManager", font=('Helvetica', 22)).pack(pady=20)

        button_frame = tk.Frame(master)
        button_frame.pack()

        tk.Button(button_frame, text="New login", font=('Helvetica', 10) , width=25, command=self.login_popup).pack(side=tk.LEFT, padx=25)
        tk.Button(button_frame, text="Update login", font=('Helvetica', 10), width=25, command=self.update_popup).pack(side=tk.LEFT, padx=25)
        tk.Button(button_frame, text="Delete login", font=('Helvetica', 10), width=25, command=self.delete_popup).pack(side=tk.LEFT, padx=25)
        tk.Button(button_frame, text="Import CSV", font=('Helvetica', 10), width=25, command=self.import_popup).pack(side=tk.LEFT, padx=25)

        self.tree_container = tk.Frame(master, bg='white', highlightthickness=1, highlightbackground='black')
        self.tree_container.pack(fill=tk.BOTH, expand='yes', padx=20, pady=20)

        self.show_logins()
        
        
    def show_logins(self):
        logins = self.app.list_colletion()
        columns = list(logins[0].keys())

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 12), anchor='center')
        self.tree = ttk.Treeview(self.tree_container, columns=columns, show='headings', selectmode='extended')
        self.tree.tag_configure('font_size', font=('Helvetica', 11))
        self.tree.bind("<Control-Key-c>", lambda x: self.copy_from_treeview(self.tree, x))

        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        for item in logins:
            self.tree.insert('', tk.END, values=[item[col] for col in columns], tags='font_size')
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    def login_popup(self):
        def confirm_password(password_var, entry_password, password_window):
            confirmed_password = password_var.get()
            entry_password.delete(0, tk.END)
            entry_password.insert(0, confirmed_password)
            password_window.destroy()

        def generate_password():
            def on_generate_password():
                nonlocal password_var
                chars = string.ascii_letters + string.digits

                punct = punct_var.get()
                if punct == 1:
                    chars += string.punctuation

                chars_l = length_var.get()

                password = ''.join(random.choices(chars, k=chars_l))
                password_var.set(password)

            password_window = tk.Toplevel(self.master)
            password_window.title("Generate Password")
            password_window.geometry("350x300")

            password_var = tk.StringVar()
            punct_var = tk.IntVar(value=1)
            length_var = tk.IntVar(value=14)

            tk.Label(password_window, text="Generate Password".upper(), font=('Helvetica', 13)).pack(pady=10)

            tk.Checkbutton(password_window, text="Include special characters", variable=punct_var, font=('Helvetica', 11)).pack(pady=5)
            
            length_frame = tk.Frame(password_window)
            length_frame.pack(pady=5)
            tk.Label(length_frame, text="Password Length:", font=('Helvetica', 11)).pack(anchor=tk.W)
            tk.Scale(length_frame, from_=6, to=25, orient=tk.HORIZONTAL, variable=length_var, font=('Helvetica', 10)).pack(side=tk.RIGHT)

            tk.Button(password_window, text="Generate", font=('Helvetica', 11), command=on_generate_password).pack(pady=15)

            tk.Entry(password_window, textvariable=password_var, font=('Helvetica', 12), state='readonly', width=30, bg='white').pack(pady=10)

            tk.Button(password_window, text="Confirm Password", font=('Helvetica', 11), command=lambda: confirm_password(password_var, entry_password, password_window)).pack(pady=10)
            
            # Initial password generation
            on_generate_password()

            password_window.transient(self.master)
            password_window.grab_set()
            self.master.wait_window(password_window)

        def create_login():
            service = entry_service_var.get()
            login = entry_login_var.get()
            password = entry_password_var.get()
            if service and login and password:
                self.app.create_login(service.capitalize(), login, password)
                self.tree.destroy()
                self.show_logins()
                popup_window.destroy()
            else:
                messagebox.showwarning("Error", 'Please make sure all fields are filled.')


        popup_window = tk.Toplevel(self.master)
        popup_window.title("New login")
        popup_window.geometry("500x400")
        popup_window.transient(self.master)

        entry_service_var = tk.StringVar()
        entry_login_var = tk.StringVar()
        entry_password_var = tk.StringVar()

        tk.Label(popup_window, text="Enter login details", font=('Helvetica', 13)).pack(pady=25)

        tk.Label(popup_window, text="Service name:", font=('Helvetica', 11)).pack(pady=1, anchor=tk.W, padx=10)
        entry_service = tk.Entry(popup_window, width=60, font=('Helvetica', 11), textvariable=entry_service_var)
        entry_service.pack(pady=(3, 20))

        tk.Label(popup_window, text="Login:", font=('Helvetica', 11)).pack(pady=1, anchor=tk.W, padx=10)
        entry_login = tk.Entry(popup_window, width=60, font=('Helvetica', 11), textvariable=entry_login_var)
        entry_login.pack(pady=(3, 20))

        tk.Label(popup_window, text="Password:", font=('Helvetica', 11)).pack(pady=1, anchor=tk.W, padx=10)
        entry_password = tk.Entry(popup_window, width=60, font=('Helvetica', 11), textvariable=entry_password_var)
        entry_password.pack(pady=(3, 10))

        tk.Button(popup_window, text="Generate password", command=generate_password, font=('Helvetica', 9), width=15).pack(anchor=tk.W, padx=10, pady=(0, 55))
        tk.Button(popup_window, text="Create login", command=create_login, font=('Helvetica', 12), width=20).pack(anchor='center', padx=10, pady=(0, 0))
  

    def copy_from_treeview(self, tree, event):
        selection = tree.selection()
        column = tree.identify_column(event.x)
        column_no = int(column.replace("#", "")) - 1
                
        copy_values = []
        for each in selection:
            try:
                value = tree.item(each)["values"][column_no]
                copy_values.append(str(value))
            except:
                pass
            
        copy_string = "\n".join(copy_values)
        pyperclip.copy(copy_string)


    def update_popup(self):
        def update_login():
            service = entry_service_var.get()
            login = entry_login_var.get()
            password = entry_password_var.get()
            update = {
                '$set': {
                    'service': service,
                    'login': login,
                    'password': password
                }
            }

            if service and login and password:
                try:
                    self.app.update_login(search_filter, update)
                except NameError:
                    messagebox.showwarning("Error", "Couldn't find a match in the database.")
                self.tree.destroy()
                self.show_logins()
                popup_window.destroy()
            else:
                messagebox.showwarning("Error", 'Please make sure all fields are filled.')
        
        def confirm_password(password_var, entry_password, password_window):
            confirmed_password = password_var.get()
            entry_password.delete(0, tk.END)
            entry_password.insert(0, confirmed_password)
            password_window.destroy()
    
        def generate_password():
            def on_generate_password():
                nonlocal password_var
                chars = string.ascii_letters + string.digits

                punct = punct_var.get()
                if punct == 1:
                    chars += string.punctuation

                chars_l = length_var.get()

                password = ''.join(random.choices(chars, k=chars_l))
                password_var.set(password)

            password_window = tk.Toplevel(self.master)
            password_window.title("Generate Password")
            password_window.geometry("350x300")

            password_var = tk.StringVar()
            punct_var = tk.IntVar(value=1)
            length_var = tk.IntVar(value=14)

            tk.Label(password_window, text="Generate Password".upper(), font=('Helvetica', 13)).pack(pady=10)

            tk.Checkbutton(password_window, text="Include special characters", variable=punct_var, font=('Helvetica', 11)).pack(pady=5)
            
            length_frame = tk.Frame(password_window)
            length_frame.pack(pady=5)
            tk.Label(length_frame, text="Password Length:", font=('Helvetica', 11)).pack(anchor=tk.W)
            tk.Scale(length_frame, from_=6, to=25, orient=tk.HORIZONTAL, variable=length_var, font=('Helvetica', 10)).pack(side=tk.RIGHT)

            tk.Button(password_window, text="Generate", font=('Helvetica', 11), command=on_generate_password).pack(pady=15)

            tk.Entry(password_window, textvariable=password_var, font=('Helvetica', 12), state='readonly', width=30, bg='white').pack(pady=10)

            tk.Button(password_window, text="Confirm Password", font=('Helvetica', 11), command=lambda: confirm_password(password_var, entry_password, password_window)).pack(pady=10)
            
            # Initial password generation
            on_generate_password()

            password_window.transient(self.master)
            password_window.grab_set()
            self.master.wait_window(password_window)


        popup_window = tk.Toplevel(self.master)
        popup_window.title("Update login")
        popup_window.geometry("500x400")
        popup_window.transient(self.master)

        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, 'values')
            search_filter = {
                'service': values[0],
                'login': values[1],
                'password': values[2]
            }
        except IndexError:
            values = ['', '', '']

        entry_service_var = tk.StringVar()
        entry_login_var = tk.StringVar()
        entry_password_var = tk.StringVar()

        tk.Label(popup_window, text="Update login details", font=('Helvetica', 13)).pack(pady=25)

        tk.Label(popup_window, text="Service name:", font=('Helvetica', 11)).pack(pady=1, anchor=tk.W, padx=10)
        entry_service = tk.Entry(popup_window, width=60, font=('Helvetica', 11), textvariable=entry_service_var)
        entry_service.insert(0, values[0])
        entry_service.pack(pady=(3, 20))

        tk.Label(popup_window, text="Login:", font=('Helvetica', 11)).pack(pady=1, anchor=tk.W, padx=10)
        entry_login = tk.Entry(popup_window, width=60, font=('Helvetica', 11), textvariable=entry_login_var)
        entry_login.insert(0, values[1])
        entry_login.pack(pady=(3, 20))

        tk.Label(popup_window, text="Password:", font=('Helvetica', 11)).pack(pady=1, anchor=tk.W, padx=10)
        entry_password = tk.Entry(popup_window, width=60, font=('Helvetica', 11), textvariable=entry_password_var)
        entry_password.insert(0, values[2])
        entry_password.pack(pady=(3, 10))

        tk.Button(popup_window, text="Generate password", command=generate_password, font=('Helvetica', 9), width=15).pack(anchor=tk.W, padx=10, pady=(0, 55))
        tk.Button(popup_window, text="Update login", command=update_login, font=('Helvetica', 12), width=20).pack(anchor='center', padx=10, pady=(0, 0))


    def delete_popup(self):
        def delete_login():
            try:
                self.app.delete_login(search_filter)
            except NameError:
                messagebox.showwarning("Error", "Couldn't find a match in the database.")
            self.tree.destroy()
            self.show_logins()
            popup_window.destroy()

        popup_window = tk.Toplevel(self.master)
        popup_window.title("Delete login")
        popup_window.geometry("400x320")
        popup_window.transient(self.master)

        try:
            item = self.tree.selection()[0]
            values = self.tree.item(item, 'values')
            search_filter = {
                'service': values[0],
                'login': values[1],
                'password': values[2]
            }
        except IndexError:
            values = ['', '', '']

        entry_service_var = tk.StringVar()
        entry_login_var = tk.StringVar()
        entry_password_var = tk.StringVar()

        tk.Label(popup_window, text="Proceed with deletion?", font=('Helvetica', 13)).pack(pady=20)

        tk.Label(popup_window, text="Service name:", font=('Helvetica', 11)).pack(pady=5, anchor=tk.W, padx=15)
        entry_service = tk.Entry(popup_window, textvariable=entry_service_var, font=('Helvetica', 12), width=40, bg='white')
        entry_service.pack(pady=5)
        entry_service.insert(0, values[0])
        entry_service.config(state='readonly')

        tk.Label(popup_window, text="Login name:", font=('Helvetica', 11)).pack(pady=5, anchor=tk.W, padx=15)
        entry_login = tk.Entry(popup_window, textvariable=entry_login_var, font=('Helvetica', 12), width=40, bg='white')
        entry_login.pack(pady=5)
        entry_login.insert(0, values[1])
        entry_login.config(state='readonly')

        tk.Label(popup_window, text="Password name:", font=('Helvetica', 11)).pack(pady=5, anchor=tk.W, padx=15)
        entry_password = tk.Entry(popup_window, textvariable=entry_password_var, font=('Helvetica', 12), width=40, bg='white')
        entry_password.pack(pady=5)
        entry_password.insert(0, values[2])
        entry_password.config(state='readonly')

        tk.Button(popup_window, text="Delete", command=delete_login, font=('Helvetica', 11), width=13).pack(side=tk.LEFT, padx=16, pady=(0, 0))
        tk.Button(popup_window, text="Cancel", command=popup_window.destroy, font=('Helvetica', 11), width=13).pack(side=tk.RIGHT, padx=16, pady=(0, 0))


    def import_popup(self):
        def import_csv():
            path = path_var.get()
            check = self.app.csv_to_dict(path)
            if check[0]:
                ok_window = tk.Toplevel(self.master)
                ok_window.title("Done")
                ok_window.geometry("250x100")
                ok_window.transient(self.master)

                tk.Label(ok_window, text=f"Import done.\n{check[1]} imports made", font=('Helvetica', 12)).pack(pady=10)
                tk.Button(ok_window, text="OK", command=ok_window.destroy, font=('Helvetica', 11), width=8).pack(anchor='center', pady=8)
            else:
                messagebox.showwarning("Error", {check[1]})
                popup_window.destroy()
            self.tree.destroy()
            self.show_logins()
            popup_window.destroy()

        popup_window = tk.Toplevel(self.master)
        popup_window.title("Import credentials")
        popup_window.geometry("400x200")
        popup_window.transient(self.master)

        path_var = tk.StringVar()

        tk.Label(popup_window, text="Insert credentials file path", font=('Helvetica', 13)).pack(pady=15)

        tk.Label(popup_window, text="File path:", font=('Helvetica', 12)).pack(pady=5, anchor=tk.W, padx=15)
        entry_password = tk.Entry(popup_window, textvariable=path_var, font=('Helvetica', 11), width=45, bg='white')
        entry_password.pack(pady=5)

        tk.Button(popup_window, text="Import", command=import_csv, font=('Helvetica', 11), width=13).pack(anchor='center', pady=30)

