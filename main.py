import Levenshtein

special_character = "!@#$%^&*()-+?_=,<>/."
strength_meter = [0]
threshold = 0.3
while True:
    email = input("Please enter your email: ")
    email_index = email.find('@')
    if email_index == -1:
        print("Invalid Email Address")
    else:
        email = email[:email_index]
        break

password = input("Please Enter your Password Here: ")

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
    if any(c.isdigit() for c in password ):
        strength_meter[0] += 1

def similarity_test(password, email):
    distance = Levenshtein.distance(password, email)
    max_length = max(len(password), len(email))
    similarity = 1 - (distance / max_length)
    return similarity
similarity = similarity_test(password, email)

def meter(strength_meter):
    if strength_meter[0] == 4:
        return "Excellent Password"
    elif strength_meter[0] == 3:
        return "Password is Strong"
    elif strength_meter[0] == 2:
        return "Password is Weak"
    elif strength_meter[0] == 1:
        return "Very Weak Password"

numerical_test(password, strength_meter)
special_test(password, strength_meter, special_character)
capital_test(password, strength_meter)
length_test(password, strength_meter)

def output(similarity, threshold, strength_meter):
    if similarity > threshold:
        return "The password provided and your email are too similar."
    elif strength_meter[0] > 0:
        return meter(strength_meter)
    else:
        return "Please make sure your password includes at least one of the following: a special character, capital letter, 12 characters long, or a numerical value."
output_result = output(similarity, threshold, strength_meter)
print(output_result)