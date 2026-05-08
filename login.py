import tkinter as tk
import tkinter.ttk as ttk
import customtkinter
from tkinter import messagebox
import time

# File to store user data
user_data_file = 'user_data.txt'
primary = '#CEF0F4'
secondary = '#0A4D68'
custom_font = ("Times", 30, 'bold')


# Load user data from the file
def load_user_data():
    users = {}
    try:
        with open(user_data_file, 'r') as file:
            for line in file:
                user, pwd = line.strip().split(':')
                users[user] = pwd
    except FileNotFoundError:
        # If file does not exist, create an empty file
        open(user_data_file, 'w').close()
    return users


# Save user data to the file
def save_user_data(users):
    with open(user_data_file, 'w') as file:
        for user, pwd in users.items():
            file.write(f"{user}:{pwd}\n")


# Load existing users
users = load_user_data()


class LoginScreen(tk.Frame):
    username = button1 = None
    password = button2 = None
    error_label = None

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master

        self.users = load_user_data()
        self.primary = primary
        self.secondary = secondary
        self.custom_font = custom_font

        self.logo = tk.PhotoImage(file="Logo.png")
        self.image_label = tk.Label(self, image=self.logo, bg=self.primary)
        self.image_label.place(x=515, y=0)

        self.log_square = tk.Canvas(self,
                                    bg=self.secondary,
                                    height=439,
                                    width=769) 
        self.log_square.place(x=325, y=430)
        self.create_login_widgets()

    def create_login_widgets(self):
        self.login1 = customtkinter.CTkButton(self,
                                              text='Login',
                                              text_color="black",
                                              font=("Inter", 48),
                                              width=444,
                                              height=58,
                                              corner_radius=30,
                                              fg_color="#FE4C00",
                                              bg_color=self.secondary,
                                              command=self.login)
        self.login1.place(x=499, y=672)

        self.create2 = customtkinter.CTkButton(
            self,
            text='Create Account',
            text_color="white",
            hover_color=self.secondary,
            font=("Inter", 32, "underline"),
            width=444,
            height=58,
            corner_radius=0,
            fg_color=self.secondary,
            bg_color=self.secondary,
            command=self.open_register_window)
        self.create2.place(x=503, y=743)

        self.username = ttk.Entry(self, font=("inter", 24))
        self.username.insert(0, "Username or Email")
        self.username.place(width=593, height=68, x=415, y=488)
        self.username.bind("<FocusIn>", self.focus_in1)
        self.username.bind("<FocusOut>", self.focus_out1)

        self.password = ttk.Entry(self, font=("inter", 24), show="")
        self.password.insert(0, "Password")

        self.password.place(width=593, height=68, x=415, y=583)
        self.password.bind("<FocusIn>", self.focus_in2)
        self.password.bind("<FocusOut>", self.focus_out2)

    def focus_in1(self, e):
        if self.username.get() == "Username or Email":
            self.username.delete(0, "end")

    def focus_in2(self, e):
        if self.password.get() == "Password":
            self.password.delete(0, "end")
            self.password.config(show="*")

    def focus_out1(self, e):
        if self.username.get() == "":
            self.username.insert(0, "Username or Email")

    def focus_out2(self, e):
        if self.password.get() == "":
            self.password.insert(0, "Password")
            self.password.config(show="")

    def login(self):
        user = self.username.get()
        pwd = self.password.get()
        if user in self.users and self.users[user] == pwd:
            messagebox.showinfo("Login Info", "Login Successful!")
            self.event_generate("<<LoginSuccess>>")
        else:
            messagebox.showerror("Login Info", "Invalid Username or Password")

    def open_register_window(self):
        register_window = tk.Toplevel(self.master)
        register_window.geometry("600x500")
        register_window.configure(background=self.primary)

        reg_canvas = tk.Canvas(register_window,
                               bg=self.secondary,
                               height=350,
                               width=550)
        reg_canvas.place(x=25, y=50)

        reg_username_entry = ttk.Entry(register_window, font=("inter", 18))
        reg_username_entry.insert(0, "Username or email")
        reg_username_entry.place(width=450, height=50, x=75, y=75)
        reg_username_entry.bind(
            "<FocusIn>", lambda e: self.focus_in(e, reg_username_entry,
                                                 "Username or email"))
        reg_username_entry.bind(
            "<FocusOut>", lambda e: self.focus_out(e, reg_username_entry,
                                                   "Username or email"))

        reg_password_entry = ttk.Entry(register_window,
                                       font=("inter", 18),
                                       show="")
        reg_password_entry.insert(0, "Choose a Password")
        reg_password_entry.place(width=450, height=50, x=75, y=150)
        reg_password_entry.bind(
            "<FocusIn>", lambda e: self.focus_in(e, reg_password_entry,
                                                 "Choose a Password", True))
        reg_password_entry.bind(
            "<FocusOut>", lambda e: self.focus_out(e, reg_password_entry,
                                                   "Choose a Password"))

        reg_password_entry_confirm = ttk.Entry(register_window,
                                               font=("inter", 18),
                                               show="")
        reg_password_entry_confirm.insert(0, "Retype Password")
        reg_password_entry_confirm.place(width=450, height=50, x=75, y=225)
        reg_password_entry_confirm.bind(
            "<FocusIn>", lambda e: self.focus_in(e, reg_password_entry_confirm,
                                                 "Retype Password", True))
        reg_password_entry_confirm.bind(
            "<FocusOut>", lambda e: self.focus_out(
                e, reg_password_entry_confirm, "Retype Password"))

        def register():
            user = reg_username_entry.get()
            pwd = reg_password_entry.get()
            pwd_confirm = reg_password_entry_confirm.get()

            # Check if username is already taken
            if user in self.users:
                messagebox.showerror("Registration Info", "Username already exists!")
            # Check for empty username or password
            elif not user or not pwd:
                messagebox.showerror("Registration Info", "Username and Password cannot be empty!")
            # Check for username or password containing ":"
            elif ":" in user or ":" in pwd:
                messagebox.showerror("Registration Info", 'Username and Password cannot contain ":"')
            # Check for username or password containing " "
            elif " " in user or " " in pwd:
                messagebox.showerror("Registration Info", 'Username and Password cannot contain empty spaces')
            # Check for username or password containing newline characters
            elif "\n" in user or "\n" in pwd:
                messagebox.showerror("Registration Info", 'Username and Password cannot contain newline characters')
            # Check for username or password being over 15 characters
            elif len(user) > 15 or len(pwd) > 15:
                messagebox.showerror("Registration Info", 'Username and Password cannot be longer than 15                       characters')
            # Check for password being under 8 characters
            elif len(pwd) < 8:
                messagebox.showerror("Registration Info", 'Password must be at least 8 characters long')
            # Check if passwords match
            elif pwd != pwd_confirm:
                messagebox.showerror("Registration Info", "Passwords do not match!")
            else:
                # If all checks pass, save the user data
                self.users[user] = pwd
                save_user_data(self.users)
                messagebox.showinfo("Registration Info", "Account Created Successfully!")
                register_window.destroy()

        
        reg_button = customtkinter.CTkButton(register_window,
                                             text='Create Account',
                                             text_color="black",
                                             font=("Inter", 36),
                                             width=300,
                                             height=50,
                                             corner_radius=20,
                                             fg_color="#FE4C00",
                                             bg_color=self.secondary,
                                             command=register)
        reg_button.place(x=150, y=300)

    def focus_in(self, e, entry, placeholder, hide_text=False):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            if hide_text:
                entry.config(show="*")

    def focus_out(self, e, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(show="")
