import Levenshtein
import hashlib

client_info = "login-info.txt"
special_character = "!@#$%^&*()-+?_=,<>/."
strength_meter = [0]
threshold = 0.3
ciphertext = ""

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

def meter(strength_meter):
    if strength_meter[0] == 4:
        return "\nYour password is considered EXCELLENT and unique"
    elif strength_meter[0] == 3:
        return "\nYour Password is considered strong"
    elif strength_meter[0] == 2:
        return "\nYour password is weak. Please consider making it more complex and diversified in order to make for a safer password."
    elif strength_meter[0] == 1: 
        return "\nVery Weak Password. This password is very simple and can be easily guessed."

def output(similarity, threshold, strength_meter):
    if similarity > threshold:
        return "\nThe password provided and your email are too similar. This can lead to a potentially vulnerable password.\n"
    elif strength_meter[0] > 0:
        return meter(strength_meter)
    else:
        return "\nPlease make sure your password includes at least one of the following: a special character, capital letter, 12 characters long, or a numerical value.\n"
    
def data_storing(email_initial, password):
    email_hash = hashlib.sha256(email_initial.encode()).hexdigest()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return email_hash, password_hash

while True:
    email_initial = input("\nPlease enter your email: ")
    email_index = email_initial.find('@')
    if email_index == -1:
        print("\nInvalid Email Address")
    else:
        email = email_initial[:email_index]
        break
    
password = input("\nPlease Enter your Password Here: ")
data_email, data_password = data_storing(email_initial, password)
while True:
    ceaser_encryption_ques = input("\nWould you like to utilize an encrypted version of your password? If yes, reply 'y'. If not, reply 'n': ")
    ceaser_encryption_flag = ceaser_encryption_ques.lower()
    if ceaser_encryption_flag == "y":
        n = int(input("\nSelect a random value between (0 --> 25): "))
        password = ceaser_encryption(password, n)
        print("\nCiphertext:", ciphertext, "\n")
        print("Decrypted Text:", ceaser_decryption(password, n), "\n")
        print("Thank you for using our Ceaser Cypher Password Encryption.\nYour password is now considered fairly safe to use considering the use of randomness of ciphertext as a password.")
        print("Although you know have a encrypted password, please avoid sharing your password with others because it can easily cause for your password to be compromised.\n")
        break
   
    elif ceaser_encryption_flag == "n":
        numerical_test(password, strength_meter)
        special_test(password, strength_meter, special_character)
        capital_test(password, strength_meter)
        length_test(password, strength_meter)
        similarity = similarity_test(password, email)
        output_result = output(similarity, threshold, strength_meter)
        with open(client_info, "a") as file:
            file.write(data_email + ": ")
            file.write(data_password + "\n")
        print(output_result) 
        break
    else:
        print("\nPlease ensure your respond with 'y' or 'n' ")
    
