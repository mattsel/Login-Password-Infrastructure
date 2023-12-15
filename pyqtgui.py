import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Levenshtein
import hashlib

client_info = "login-info.txt"
special_character = "!@#$%^&*()-+?_=,<>/."
strength_meter = [0]
threshold = 0.3
ciphertext = ""

class PasswordStrengthMeter:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Meter")
        self.root.geometry("300x200")

        self.email_label = ttk.Label(root, text="Email:")
        self.email_entry = ttk.Entry(root,)
        self.email_label.grid(row=0, column=0, sticky=tk.W, padx=8, pady=5)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(root, text="Password:")
        self.password_entry = ttk.Entry(root, show='*')
        self.password_label.grid(row=1, column=0, sticky=tk.W, padx=8, pady=5)
        self.password_entry.grid(row=1, column=1, padx=8, pady=5)

        self.encrypt_checkbox = ttk.Checkbutton(root, text="Encrypt Password", command=self.toggle_shift_input)
        self.encrypt_checkbox.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=8, pady=5)

        self.shift_label = ttk.Label(root, text="Shift Value:")
        self.shift_entry = ttk.Entry(root, state=tk.DISABLED)
        self.shift_label.grid(row=3, column=0, sticky=tk.W, padx=8, pady=5)
        self.shift_entry.grid(row=3, column=1, padx=8, pady=5)

        self.submit_button = ttk.Button(root, text="Submit", command=self.on_submit_clicked)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=5)

    def toggle_shift_input(self):
        if self.encrypt_checkbox.instate(['selected']):
            self.shift_entry.config(state=tk.NORMAL)
        else:
            self.shift_entry.delete(0, tk.END)
            self.shift_entry.config(state=tk.DISABLED)

    def on_submit_clicked(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Check for valid email address
        if '@' not in email:
            messagebox.showerror("Error", "Invalid Email Address")
            return

        # Encrypt password if requested
        if self.encrypt_checkbox.instate(['selected']):
            try:
                n = int(self.shift_entry.get())
                password = ceaser_encryption(password, n)
                messagebox.showinfo("Encryption Result",
                                    f"Ciphertext: {ciphertext}\n\n"
                                    f"Decrypted Text: {ceaser_decryption(password, n)}\n\n"
                                    f"Thank you for using our Ceaser Cypher Password Encryption. "
                                    f"Your password is now considered fairly safe to use considering the "
                                    f"use of randomness of ciphertext as a password. "
                                    f"Although you now have an encrypted password, please avoid sharing your "
                                    f"password with others because it can easily cause your password to be compromised.")
            except ValueError:
                messagebox.showerror("Error", "Invalid Shift Value (must be an integer)")
            return

        # Check password strength
        strength_meter[0] = 0  # Reset strength meter
        numerical_test(password, strength_meter)
        special_test(password, strength_meter, special_character)
        capital_test(password, strength_meter)
        length_test(password, strength_meter)
        similarity = similarity_test(password, email)
        output_result = output(similarity, threshold, strength_meter)

        # Store data in a text file
        data_email, data_password = data_storing(email, password)
        with open(client_info, "a") as file:
            file.write(data_email + ": ")
            file.write(data_password + "\n")

        # Show password strength result
        messagebox.showinfo("Password Strength Result", output_result)

def ceaser_encryption(password, n):
    global ciphertext
    ciphertext = ""
    for char in password:
        if char.isalpha():
            if char.isupper():
                ciphertext += chr((ord(char) - ord('A') + n) % 26 + ord('A'))
            else:
                ciphertext += chr((ord(char) - ord('a') + n) % 26 + ord('a'))
        else:
            ciphertext += char
    return ciphertext

def ceaser_decryption(ciphertext, n):
    return ceaser_encryption(ciphertext, -n)

def special_test(password, strength_meter, special_character):
    if any(c in special_character for c in password):
        strength_meter[0] += 1

def capital_test(password, strength_meter):
    if any(char.isupper() for char in password):
        strength_meter[0] += 1

def length_test(password, strength_meter):
    if len(password) >= 12:
        strength_meter[0] += 1

def numerical_test(password, strength_meter):
    if any(c.isdigit() for c in password):
        strength_meter[0] += 1

def similarity_test(password, email):
    distance = Levenshtein.distance(password, email)
    max_length = max(len(password), len(email))
    similarity = 1 - (distance / max_length)
    return similarity

def output(similarity, threshold, strength_meter):
    if similarity > threshold:
        return "The password provided and your email are too similar. " \
               "This can lead to a potentially vulnerable password."
    elif strength_meter[0] == 4:
        return "Your password is considered EXCELLENT and unique."
    elif strength_meter[0] == 3:
        return "Your Password is considered strong."
    elif strength_meter[0] == 2:
        return "Your password is weak. Please consider making it more complex and diversified " \
               "in order to make for a safer password."
    elif strength_meter[0] == 1:
        return "Very Weak Password. This password is very simple and can be easily guessed."
    else:
        return "Please make sure your password includes at least one of the following: " \
               "a special character, capital letter, 12 characters long, or a numerical value."

def data_storing(email, password):
    email_hash = hashlib.sha1(email.encode()).hexdigest()
    password_hash = hashlib.sha1(password.encode()).hexdigest()
    return email_hash, password_hash


if __name__ == '__main__':
    root = tk.Tk()
    app = PasswordStrengthMeter(root)
    root.mainloop()
