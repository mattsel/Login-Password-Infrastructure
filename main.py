import Levenshtein
#Initiallizes variables
special_character = "!@#$%^&*()-+?_=,<>/."
strength_meter = [0]
threshold = 0.3
ciphertext = ""
#Function that converts user input to ceaser cypher encryption. User can select a value to shift the letters by.
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
#Function that is able runs the ceaser encryption, but with a negative shift to decrypt the message. 
def ceaser_decryption(ciphertext, n):
    return ceaser_encryption(ciphertext, -n)
#Tests if the function includes a special character as defined in the initial variables. 
def special_test(password, strength_meter, special_character):
    if any(c in special_character for c in password):
        strength_meter[0] += 1
#Tests to see if the password includes a capital letter.
def capital_test(password, strength_meter):
    if any(char.isupper() for char in password):
        strength_meter[0] += 1
#Tests to see if the function is at least 12 characters long to ensure security of the password. 
def length_test(password, strength_meter):
    if len(password) >= 12:
        strength_meter[0] += 1
#Checks to see if the user has a numerical value included inside of their password. 
def numerical_test(password, strength_meter):
    if any(c.isdigit() for c in password):
        strength_meter[0] += 1
#Tests for user's password and email to determine if they are similar to one another. 
def similarity_test(password, email):
    distance = Levenshtein.distance(password, email)
    max_length = max(len(password), len(email))
    similarity = 1 - (distance / max_length)
    return similarity
#Each time a function has passed a test, the strength_meter is incremented by one which will determine the passwords strength. 
def meter(strength_meter):
    if strength_meter[0] == 4:
        return "\nExcellent Password"
    elif strength_meter[0] == 3:
        return "\nPassword is Strong"
    elif strength_meter[0] == 2:
        return "\nPassword is Weak"
    elif strength_meter[0] == 1:
        return "\nVery Weak Password"
#The output will test to see if the calculation of similarity is passed the threshold defined in the variable initialization. 
#If the condition is true, the program will inform the user about the similarity issue to avoid having a vulnerable password.
#The other condition will run the strenght meter and depending on the amount of tests that it has passed, it will output the password's strength.
#If the user hasn't passed any of the tests, it will remind the user of some of the recommended requirements for creating a valid password. 
def output(similarity, threshold, strength_meter):
    if similarity > threshold:
        return "\nThe password provided and your email are too similar. This can lead to a potentially vulnerable password.\n"
    elif strength_meter[0] > 0:
        return meter(strength_meter)
    else:
        return "\nPlease make sure your password includes at least one of the following: a special character, capital letter, 12 characters long, or a numerical value.\n"
#This function will only accept an email if it includes an @ symbol. Without it will output a invalid email response.
#After the user enters a valid email, the system will ONLY test the similarity of the email, before the @ symbol because of the slice in the string. 
while True:
    email = input("\nPlease enter your email: ")
    email_index = email.find('@')
    if email_index == -1:
        print("\nInvalid Email Address")
    else:
        email = email[:email_index]
        break
#Prompts that the user will be initially asked. Depending on their response will determine the programs next steps. 
password = input("\nPlease Enter your Password Here: ")
while True:
    ceaser_encryption_ques = input("\nWould you like to utilize an encrypted version of your password? If yes, reply 'y'. If not, reply 'n': ")
    ceaser_encryption_flag = ceaser_encryption_ques.lower()
    #If the user selects to encrypt their password, they will be prompted to select a shift value. This will then print the users encrypted and decrypted version of their password to ensure accuracy. 
    if ceaser_encryption_flag == "y":
        n = int(input("\nSelect a random value between (0 --> 25): "))
        password = ceaser_encryption(password, n)
        print("\nCiphertext:", ciphertext, "\n")
        print("Decrypted Text:", ceaser_decryption(password, n), "\n")
        print("Thank you for using our Ceaser Cypher Password Encryption.\nYour password is now considered fairly safe to use considering the use of randomness of ciphertext as a password.")
        print("Although you know have a encrypted password, please avoid sharing your password with others because it can easily cause for your password to be compromised.\n")
        break
    #If the user decides to not use the encryption system, the program will continue to test it's strength by running it through the other series of tests.
    elif ceaser_encryption_flag == "n":
        numerical_test(password, strength_meter)
        special_test(password, strength_meter, special_character)
        capital_test(password, strength_meter)
        length_test(password, strength_meter)
        similarity = similarity_test(password, email)
        output_result = output(similarity, threshold, strength_meter)
        print(output_result) 
        break
    else:
        print("\nPlease ensure your respond with 'y' or 'n' ")
    
