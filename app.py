from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
import Levenshtein
from validate_email_address import validate_email
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.envioren.get('DATABASE_URL', 'sqlite:///site.db')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

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

    new_user = User(email=email_hash, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return email_hash, password_hash

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

    if not validate_email(email):
        return "Invalid Email Address"

    if not is_valid_domain(email):
        return "Invalid Email Domain"

    if encrypt_checkbox:
        try:
            n = int(shift_value)
            if not (0 <= n < 26):
                return "Invalid Shift Value (must be between 0 and 25)"

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

    strength_meter[0] = 0
    numerical_test(password, strength_meter)
    special_test(password, strength_meter, special_character)
    capital_test(password, strength_meter)
    length_test(password, strength_meter)
    similarity = similarity_test(password, email)
    output_result = output(similarity, threshold, strength_meter)

    data_email, data_password = data_storing(email, password)

    return output_result

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    #app.run(debug=True, port=5001)
