import tkinter as tk
import tkinter.ttk as ttk
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk

primary = '#CEF0F4'
secondary = '#0A4D68'
thirdly = '#FFFFFF'

# Set the options for our combobox
subject_options = [
    "Subject", "Accounting", "Art", "Biology", "Calculus", "Chemistry",
    "Classical Studies", "Computer Science", "Design and Visual Communication",
    "Digital Technologies", "Drama", "Economics", "English", "Geography",
    "Health", "History", "Media Studies", "Music", "Photography",
    "Physical Education", "Physics", "Statistics", "Technology", "Tourism"
]

subjects = []


class Career:
    # Assigning each category either name, pay, description and subjects
    def __init__(self, name, description, pay, subjects,
                 image_path):  # Creating the object
        self.name = name
        self.description = description
        self.pay = pay
        self.subjects = subjects
        self.image_path = image_path


class MainScreen(tk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.primary = '#CEF0F4'
        self.secondary = '#0A4D68'
        self.custom_font = ("Times", 30, 'bold')
        self.configure(bg=self.primary)
        self.searchable_career = self.load_career_data()
        self.create_widgets()

    def create_widgets(self):
        # Home button
        self.bttn(10, 10, "home_icon.png", "home_icon_hover.png", self.cmd1)

        # Label
        label = customtkinter.CTkLabel(self,
                                       text="Career Ideas",
                                       width=630,
                                       height=170,
                                       fg_color=secondary,
                                       text_color="white",
                                       font=("Inter", 64))
        label.place(x=400, y=10)

        # Dropdowns
        for i in range(5):
            subject = customtkinter.CTkComboBox(
                self,
                values=subject_options,
                height=60,
                width=225,
                font=("Inter", 20),
                dropdown_font=("Inter", 18),
                corner_radius=50,
                border_width=2,
                border_color=self.secondary,
                button_color=self.secondary,
                button_hover_color=self.secondary,
                dropdown_hover_color="#FE4C00",
                dropdown_fg_color=self.secondary,
                dropdown_text_color="white",
                text_color="black",
                hover=True,
                state="normal"  # normal
            )
            subject.place(x=25, y=230 + i * 135)
            subjects.append(subject)

        # Search button

        self.Enter = customtkinter.CTkButton(
            self,
            text='Get Career Ideas',
            text_color="black",
            font=("Inter", 48),
            width=444,
            height=58,
            corner_radius=30,
            fg_color="#FE4C00",
            bg_color=self.primary,
            command=lambda: self.search_career_list(
                self.get_selected_subjects(), self.searchable_career))
        self.Enter.place(x=450, y=600)

        self.Log = customtkinter.CTkButton(self,
                                           text='Logout',
                                           text_color="black",
                                           font=("Inter", 48),
                                           width=200,
                                           height=58,
                                           corner_radius=30,
                                           fg_color="#FE4C00",
                                           bg_color=self.primary,
                                           command=self.logout)
        self.Log.place(x=1200, y=50)

        # Create a canvas for the scrollable frame, initially hidden
        self.canvas = tk.Canvas(self, bg=self.primary)
        self.canvas.place(x=400, y=180, width=800, height=600)
        self.canvas.place_forget()

        # Create a vertical scrollbar linked to the canvas
        self.scrollbar = ttk.Scrollbar(self,
                                       orient="vertical",
                                       command=self.canvas.yview)
        self.scrollbar.place(x=1150, y=280, height=600)
        self.scrollbar.place_forget()

        # Create a frame inside the canvas
        self.scrollable_frame = ttk.Frame(self.canvas)

        # Link the scrollbar to the frame
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.
                                                           canvas.bbox("all")))
        self.canvas.create_window((0, 0),
                                  window=self.scrollable_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def logout(self):
        print("Logout...")
        self.event_generate("<<LogOut>>")

    def load_career_data(self):
        searchable_career = []
        try:
            with open("CareerInformation.txt", "r") as f:
                file_contents = f.read().strip().split("\n")
                for career in file_contents:
                    career_info = career.split("|")
                    if len(career_info) == 5:
                        career_item = Career(career_info[0], career_info[1],
                                             career_info[2], career_info[3],
                                             career_info[4])
                        searchable_career.append(career_item)
        except FileNotFoundError:
            messagebox.showerror(
                "File Not Found",
                "The file CareerInformation.txt was not found.")
        return searchable_career

    def search_career_list(self, selected_subjects, searchable_career):
        # Clear previous results
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        def matching_subjects_count(career):
            return sum(subject.lower() in career.subjects.lower()
                       for subject in selected_subjects)

        results = [
            career for career in searchable_career
            if matching_subjects_count(career) > 0
        ]
        results.sort(key=matching_subjects_count, reverse=True)

        if results:
            # Show the canvas and scrollbar
            self.canvas.place(x=400, y=280, width=800, height=600)
            self.scrollbar.place(x=1150, y=280, height=600)

            for career in results:
                card = customtkinter.CTkButton(
                    self.scrollable_frame,
                    height=250,
                    width=750,
                    corner_radius=10,
                    fg_color=self.secondary,
                    hover_color=self.secondary,
                    text="",
                    command=lambda c=career: self.on_card_click(c))
                card.pack(pady=10, padx=10, fill="x")

                img = Image.open(career.image_path).resize((195, 195))
                img = ImageTk.PhotoImage(img)
                img_label = customtkinter.CTkLabel(card,
                                                   image=img,
                                                   text="",
                                                   corner_radius=10)
                img_label.image = img  # Keep a reference to avoid garbage collection
                img_label.place(x=10, y=25)
                img_label.bind("<Button-1>",
                               lambda e, c=career: self.on_card_click(c))

                name_label = customtkinter.CTkLabel(card,
                                                    text=career.name,
                                                    font=("Inter", 18, "bold"),
                                                    text_color="white")
                name_label.place(x=220, y=25)
                name_label.bind("<Button-1>",
                                lambda e, c=career: self.on_card_click(c))

                desc_label = customtkinter.CTkLabel(card,
                                                    text=career.description,
                                                    font=("Inter", 14),
                                                    text_color="white",
                                                    wraplength=500,
                                                    justify="left")
                desc_label.place(x=220, y=75)
                desc_label.bind("<Button-1>",
                                lambda e, c=career: self.on_card_click(c))

                pay_label = customtkinter.CTkLabel(card,
                                                   text=career.pay,
                                                   font=("Inter", 14),
                                                   text_color="white",
                                                   wraplength=500,
                                                   justify="left")
                pay_label.place(x=220, y=125)
                pay_label.bind("<Button-1>",
                               lambda e, c=career: self.on_card_click(c))

                subjects_label = customtkinter.CTkLabel(card,
                                                        text=career.subjects,
                                                        font=("Inter", 14),
                                                        text_color="white",
                                                        wraplength=500,
                                                        justify="left")
                subjects_label.place(x=220, y=175)
                subjects_label.bind("<Button-1>",
                                    lambda e, c=career: self.on_card_click(c))

        else:
            messagebox.showinfo(
                "Search Result",
                "Sorry :(, We could not find this in our database")

        self.Enter.place(x=800, y=200)

    def on_card_click(self, career):
        print(f"You clicked on {career.name}")

    def get_selected_subjects(self):
        return [subject.get() for subject in subjects]

    def bttn(self, x, y, img1, img2, cmd):
        imageb = ImageTk.PhotoImage(Image.open(img2))
        imaged = ImageTk.PhotoImage(Image.open(img1))

        def on_entera(e):
            myButton1['image'] = imageb

        def on_leavea(e):
            myButton1['image'] = imaged

        myButton1 = tk.Button(self,
                              image=imaged,
                              border=0,
                              cursor="hand2",
                              command=cmd,
                              relief=tk.SUNKEN)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    def cmd1(self):
        print('hello world')
