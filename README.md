# Login-Password-Infrastructure
**Object**: Create a program that can run several tests to ensure not only a valid password is entered, but also grade the strength of the password in regards to its content. The overall goal for this project to to create a system that can help the user ensure that their password is safe from the possibility of hackers utilizing common combinations to brute force (i.e. birthdays, first/last name, etc.)

**Test**: Some of the tests that the user's password will go through will be the following ---->

**Similarity to email** - This test will utilize the Levenshtein Distance Test to discover the similarity of the user's email and password. If they are too similar to one another, the program will prompt the user to enter a new unique password. 

**Special Characters** - This test will use a range of valid special characters that can be used in a password. When the test is run, it will check the user's password for a special character. 

**Capitalization** - This test will check the user's input to see if it includes capitalization throughout the input to make the password more unique. 

**Character Lenght** - This test will ensure that the user's password has at least 12 characters in the string. This is important to make the password more complex and harder to guess. 

**Numerical** - This will test to see if the user has included a numerical value in the string. The more complex the password, the harder it is to brute force the password. 

**Password Analysis** After each of these tests are completed, the system will increment the password's grade by one each time. To have a valid password, the user must have passed at least one of these tests. If the user fails to pass any of the tests, it will then remind the user with some helpful tips to encourage the user to include in their password to make it not only valid but safer password. The grading scale goes as follows:
**4 points**: "Excellent Password"
**3 points**: "Password is Strong"
**2 points**: "Password is Weak"
**1 point**: "Very Weak Password"
**0 points**: "Please make sure your password includes at least one of the following: a special character, capital letter, 12 characters long, or includes a numerical value.









