import Levenshtein

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
        return "Excellent Password"
    elif strength_meter[0] == 3:
        return "Password is Strong"
    elif strength_meter[0] == 2:
        return "Password is Weak"
    elif strength_meter[0] == 1:
        return "Very Weak Password"

def output(similarity, threshold, strength_meter):
    if similarity > threshold:
        return "The password provided and your email are too similar."
    elif strength_meter[0] > 0:
        return meter(strength_meter)
    else:
        return "Please make sure your password includes at least one of the following: a special character, capital letter, 12 characters long, or a numerical value."

while True:
    email = input("Please enter your email: ")
    email_index = email.find('@')
    if email_index == -1:
        print("Invalid Email Address")
    else:
        email = email[:email_index]
        break

password = input("Please Enter your Password Here: ")

ceaser_encryption_ques = input("Would you like to utilize an encrypted version of your password? If yes, reply 'y'. If not, reply 'n': ")
ceaser_encryption_flag = ceaser_encryption_ques.lower()


if ceaser_encryption_flag == "y":
    n = int(input("Select a random value between (0 --> 25): "))
    password = ceaser_encryption(password, n)
    print("\nCiphertext:", ciphertext, "\n")
    print("Decrypted Text:", ceaser_decryption(password, n), "\n")
    print("Thank you for using our Ceaser Cypher Password Encryption.\nYour password is now considered fairly safe to use considering the use of randomness of ciphertext as a password.")
    print("Although you know have a encrypted password, please avoid sharing your password with others because it can easily cause for your password to be compromised")
else:
    numerical_test(password, strength_meter)
    special_test(password, strength_meter, special_character)
    capital_test(password, strength_meter)
    length_test(password, strength_meter)
    similarity = similarity_test(password, email)
    output_result = output(similarity, threshold, strength_meter)
    print(output_result)

