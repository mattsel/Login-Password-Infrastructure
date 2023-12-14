special_character = "!@#$%^&*()-+?_=,<>/"
password = input("Please Enter your Password Here: ")
strength_meter = 0

def special_test(password, strength_meter, special_character):
    if any(c in special_character for c in password):
        strength_meter += 1
    else:
        print("Please include a special character in your password.")

def capital_test(password, strength_meter):
    if any(char.isupper() for char in password):
        strength_meter += 1
    else:
        print("Please include a capitalized letter in your password.")

def length_test(password, strength_meter):
    if len(password) >= 12:
        strength_meter += 1
    else: 
        print("Please ensure your password includes at least 12 characters.")
def meter(strength_meter):
    if strength_meter == 3:
        print("Excellent Password")
    elif strength_meter == 2:
        print("Password is Good")
    elif strength_meter == 1:
        print("Password is Weak")
    else:
        print("Please make sure your password includes a special character, capital letter, and is at least 12 characters long.")
    