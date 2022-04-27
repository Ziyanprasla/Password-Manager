from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    if len(password_entry.get()) > 0:
        password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [(random.choice(letters)) for _ in range(nr_letters)]
    password_symbols = [(random.choice(symbols)) for _ in range(nr_symbols)]
    password_numbers = [(random.choice(numbers)) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    generate_pass = "".join(password_list)
    password_entry.insert(0, generate_pass)
    pyperclip.copy(generate_pass)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
        "email": email,
        "password": password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Opps", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()
# ---------------------------- SEARCH DATA ------------------------------------- #
def search_data():
    website = website_entry.get().title()
    if len(website) == 0:
        messagebox.showerror(title="Error", message="Please enter the website you want to search for")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not found")
        else:
            if website in data:
                get_website = data[website]
                get_email = get_website["email"]
                get_password = get_website["password"]
                messagebox.showinfo(title=website, message=f"Email: {get_email}\n"
                                                           f"Password: {get_password}")
            else:
                messagebox.showerror(title="Error", message=f"No details for {website} exists")
        finally:
            website_entry.delete(0, END)
# ---------------------------- UI SETUP ---------------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="black")

# canvas
canvas = Canvas(width=200, height=200, highlightthickness=0, bg="black")
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text="Website:", bg="black", foreground="White")
email_label = Label(text="Email/Username:", bg="black", foreground="White")
password_label = Label(text="Password:", bg="black", foreground="White")

website_label.grid(column=0, row=1, pady=(0, 10))
email_label.grid(column=0, row=2, pady=(0, 10))
password_label.grid(column=0, row=3, pady=(0, 10))

# entries
website_entry = Entry(width=52)
website_entry.focus()
email_entry = Entry(width=52)
password_entry = Entry(width=30)
website_entry.grid(column=1, row=1, sticky="EW", pady=(0, 10), ipady=5, padx=(0, 10))
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW", ipady=5, pady=(0, 10))
password_entry.grid(column=1, row=3, sticky="EW", pady=(0, 10), ipady=5, padx=(0, 10))

# buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
add_button = Button(text="Add", width=60, command=save)
search_button = Button(text="Search", command=search_data)

generate_password_button.grid(column=2, row=3, sticky="we", ipady=2, pady=(0, 10))
add_button.grid(column=1, row=4, columnspan=2, sticky="EW", ipady=2, pady=(0, 10))
search_button.grid(column=2, row=1, sticky="we", ipady=2, pady=(0, 10))

window.mainloop()