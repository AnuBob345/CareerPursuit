import tkinter as tk
import tkinter.ttk as ttk
import customtkinter

primary = '#CEF0F4'
secondary = '#0A4D68'
custom_font = ("Times",30,'bold')

# Creating the main window
window = tk.Tk()
window.geometry("900x800")
window.configure(background=primary)

log_square = tk.Canvas(window, bg=secondary, height=439, width=769).place(x=325,y=430)

button = customtkinter.CTkButton(window, text='Login', text_color="black", font=("Inter", 48), width=444, height=58, corner_radius=30, fg_color="#FE4C00", bg_color=secondary)
button.place(x=450, y=400)