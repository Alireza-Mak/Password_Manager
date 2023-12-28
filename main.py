import json
from random import randint, shuffle, choice
from tkinter import *
from tkinter import messagebox
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list.extend([choice(symbols) for _ in range(randint(2, 4))])
    password_list.extend([choice(numbers) for _ in range(randint(2, 4))])
    shuffle(password_list)
    return "".join(password_list)


def on_generate_password_click():
    password = create_password()
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    # ---------------------------- SAVE PASSWORD ------------------------------- #


def on_add_button_click():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {"email": email, "password": password}}
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Please check your inputs!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            messagebox.showinfo("Success!", "Your data has been successfully saved.")
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH ------------------------------- #
def on_search_click():
    query = website_entry.get().strip().title()
    if len(query) > 0:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror("Error", "No Data file Found.")
        else:
            if query in data:
                messagebox.showinfo(title=query, message=f"Email/Username: {data[query]['email']}\nPassword: "
                                                         f"{data[query]['password']}")
            else:
                messagebox.showinfo("Not Found", f"No details for {query} website exists.")
    else:
        messagebox.showwarning("Empty Field", "Please Enter a word to search!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

creator_label = Label(text="Created by Alireza Mak.\n www.alirezamak.com\n", bg="white", width=58)
creator_label.grid(row=5, column=0, columnspan=3)


# Entries

website_entry = Entry(width=32)
website_entry.grid(row=1, column=1, pady=5)
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2, pady=5)
email_entry.insert(END, "info@alirezamak.com")

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1, pady=5)

# Buttons
search_button = Button(text="Search", width=14, command=on_search_click)
search_button.grid(row=1, column=2, padx=5)

generate_password_button = Button(text="Generate Password", command=on_generate_password_click)
generate_password_button.grid(row=3, column=2, padx=5)

add_button = Button(text="Add", width=44, command=on_add_button_click)
add_button.grid(row=4, column=1, columnspan=2, pady=5)

window.mainloop()
