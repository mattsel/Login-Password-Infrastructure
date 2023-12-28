# app.py

from flask import Flask, render_template, request, redirect, url_for
import hashlib
import Levenshtein
from validate_email_address import validate_email

app = Flask(__name__)

client_info = "login-info.txt"
special_character = "!@#$%^&*()-+?_=,<>/."
strength_meter = [0]
threshold = 0.3
ciphertext = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        encrypt_checkbox = 'encrypt_checkbox' in request.form
        shift_value = request.form['shift_value'] if encrypt_checkbox else None

        result = process_form(email, password, encrypt_checkbox, shift_value)
        return redirect(url_for('result', result=result))

    return render_template('index.html')

@app.route('/result', methods=['GET'])
def result():
    result_message = request.args.get('result', '')
    return render_template('result.html', result=result_message)

def is_valid_domain(email):
    valid_domains = ['example.com', 'yourdomain.com', 'gmail.com']
    user_domain = email.split('@')[1].lower()
    return user_domain in valid_domains

def numerical_test(password, strength_meter):
    if any(c.isdigit() for c in password):
        strength_meter[0] += 1

def special_test(password, strength_meter, special_character):
    if any(c in special_character for c in password):
        strength_meter[0] += 1

def capital_test(password, strength_meter):
    if any(char.isupper() for char in password):
        strength_meter[0] += 1

def length_test(password, strength_meter):
    if len(password) >= 12:
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
    ciphertext_hash = hashlib.sha1(ciphertext.encode()).hexdigest()
    return email_hash, password_hash, ciphertext_hash

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

def process_form(email, password, encrypt_checkbox, shift_value):
    global strength_meter
    global ciphertext

    # Check for a valid email format using validate_email_address library
    if not validate_email(email):
        return "Invalid Email Address"

    # Check for a valid email domain
    if not is_valid_domain(email):
        return "Invalid Email Domain"

    # Encrypt password if requested
    if encrypt_checkbox:
        try:
            n = int(shift_value)
            if not (0 <= n < 26):  # Ensure the shift value is between 0 and 25
                return "Invalid Shift Value (must be between 0 and 25)"

            # Rest of your encryption logic...
            password = ceaser_encryption(password, n)
            result_message = f"Ciphertext: {ciphertext}\n\n" \
                             f"Decrypted Text: {ceaser_decryption(password, n)}\n\n" \
                             f"Thank you for using our Caesar Cipher Password Encryption. " \
                             f"Your password is now considered fairly safe to use considering the " \
                             f"use of randomness of ciphertext as a password. " \
                             f"Although you now have an encrypted password, please avoid sharing your " \
                             f"password with others because it can easily cause your password to be compromised."
            return result_message
        except ValueError:
            return "Invalid Shift Value (must be an integer)"

    # Check password strength
    strength_meter[0] = 0  # Reset strength meter
    numerical_test(password, strength_meter)
    special_test(password, strength_meter, special_character)
    capital_test(password, strength_meter)
    length_test(password, strength_meter)
    similarity = similarity_test(password, email)
    output_result = output(similarity, threshold, strength_meter)

    # Store data in a text file
    data_email, data_password, data_ciphertext = data_storing(email, password)
    with open(client_info, "a") as file:
        file.write(data_email + ": ")
        file.write(data_password + "\n")

    return output_result

if __name__ == '__main__':
    app.run(debug=True, port=5001)