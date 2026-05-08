import tkinter as tk
from login import LoginScreen
from main_screen import MainScreen

primary = '#CEF0F4'
secondary = '#0A4D68'
custom_font = ("Times", 30, 'bold')

app_width = 1435
app_height = 1020
current_screen = None

window = tk.Tk()
window.geometry(f"{app_width}x{app_height}")
window.configure(background=primary)

# Initialize first screen - Login
login_screen = LoginScreen(master=window, background=primary)
main_screen = MainScreen(master=window, background=primary)

# Ensure both screens are hidden initially
login_screen.pack_forget()
main_screen.pack_forget()

# Show the login screen initially
current_screen = login_screen
current_screen.pack(fill='both', expand=True)


# Function for switching from login screen to main screen
def login_success(event=None):
    global current_screen, login_screen, main_screen
    if current_screen == login_screen:
        current_screen.pack_forget()
        current_screen = main_screen
        current_screen.pack(fill='both', expand=True)


def log_out(event=None):
    print("Logouttttt")
    global current_screen, login_screen, main_screen
    current_screen.pack_forget()
    current_screen = login_screen
    current_screen.pack(fill='both', expand=True)


# Bind custom event to switch screens
window.bind("<<LoginSuccess>>", login_success)
window.bind("<<LogOut>>", log_out)
window.mainloop()
