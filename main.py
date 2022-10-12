from tkinter import *
import random
from tkinter import messagebox
import json

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*()+=?1234567890'
LENGTH_CHARS = len(CHARS)
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    new_pass = ""
    password_entry.delete(0, END)
    for _ in range(12):
        choice = random.randint(0, LENGTH_CHARS - 1)
        new_pass += CHARS[choice]
    password_entry.insert(0, new_pass)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    site_name = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        site_name:{
            "username": username,
            "password": password
        }
    }
    if password == '' or site_name == '' or username == '':
        messagebox.showwarning(title="Whoops", message="Don't leave any fields blank.")
        return
    else:
        website_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

# --------------------------SEARCH------------------------------------- #
def search():
    query = website_entry.get()
    with open("data.json", "r") as file:
        searchable_data = json.load(file)
    try:
        response = searchable_data[query]
        username = response["username"]
        password = response["password"]
    except KeyError:
        messagebox.showwarning(title="Whoops", message="Site not found.")
    else:
        messagebox.showinfo(title=f"{query}", message=f"Username: {username}\nPassword: {password}")
# ---------------------------- UI SETUP ------------------------------- #

main_window = Tk()
main_window.title("Password Manager")
main_window.config(pady=30, padx=30)
logo_space = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
logo_space.create_image(100, 100, image=logo_img)
logo_space.grid(row=0, column=1)

website_label = Label(text="Website:", font="Arial 12 bold")
website_label.grid(row=1, column=0, sticky="E")
website_entry = Entry(width=30)
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="W")
search_button = Button(text="Search",width=15, command=search)
search_button.grid(row=1, column=2)

username_label = Label(text="Email/Username:", font="Arial 12 bold")
username_label.grid(row=2, column=0, sticky="E")
username_entry = Entry(width=42)
username_entry.grid(row=2, column=1, columnspan=2, sticky="W")

password_label = Label(text="Password:", font="Arial 12 bold")
password_label.grid(row=3, column=0, sticky="E")
password_entry = Entry(width=30)
password_entry.grid(row=3, column=1, columnspan=2, sticky="W")
generate_button = Button(text="Generate password", command=generate)
generate_button.grid(row=3, column=2, sticky="W")

add_button = Button(text="Add", width=30, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, sticky="W")

main_window.mainloop()
