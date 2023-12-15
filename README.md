# Login-Password-Infrastructure
**Object**: Create a program that can run several tests to ensure not only a valid password is entered, but also grade the strength of the password in regards to its content. The overall goal for this project to to create a system that can help the user ensure that their password is safe from the possibility of hackers utilizing common combinations to brute force (i.e. birthdays, first/last name, etc.)

**Ceaser Cypher Encryption** - Gives the user the ability the option to receive their password in Ceaser Cypher encrypted version to pad more security for the user's password.

<img width="943" alt="Screenshot 2023-12-15 at 12 14 56 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/9a2095a3-7b02-4598-98e2-4e9c4e5d0891">

**Stores Hashed Information** - Something neat that this program does is that it will store your password locally to your machine via login-info.txt in sha1 hashed text. **THIS IS A TEST DO NOT** store serious information in this system because it is not designed for practical use, simply a simulation of storing hashed information in a database. 

<img width="478" alt="Screenshot 2023-12-15 at 1 15 47 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/9d25e3ea-fb3a-469b-97de-4e3a0b23797d">

**Test**: Some of the tests that the user's password will go through will be the following ---->

**Similarity to email** - This test will utilize the Levenshtein Distance Test to discover the similarity of the user's email and password. If they are too similar to one another, the program will prompt the user to enter a new unique password. 

<img width="449" alt="Screenshot 2023-12-15 at 12 15 27 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/d0f6060b-9de7-49c3-b766-01dcc4546187">

**Special Characters** - This test will use a range of valid special characters that can be used in a password. When the test is run, it will check the user's password for a special character. 

<img width="495" alt="Screenshot 2023-12-15 at 12 16 15 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/1c90866d-abc3-4c58-8411-7294a934965e">

**Capitalization** - This test will check the user's input to see if it includes capitalization throughout the input to make the password more unique. 

<img width="497" alt="Screenshot 2023-12-15 at 12 16 26 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/53809d27-3de0-49d5-bd25-4ad544c215be">

**Character Length** - This test will ensure that the user's password has at least 12 characters in the string. This is important to make the password more complex and harder to guess. 

<img width="635" alt="Screenshot 2023-12-15 at 12 16 39 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/8b33ee79-3a98-476b-917b-d4b7de1dc34c">

**Numerical** - This will test to see if the user has included a numerical value in the string. The more complex the password, the harder it is to brute force the password. 

<img width="412" alt="Screenshot 2023-12-15 at 12 17 00 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/bee9d241-f79e-4115-b4a7-dc7fa75c6a4c">

**Password Analysis** - After each of these tests are completed, the system will increment the password's grade by one each time. To have a valid password, the user must have passed at least one of these tests. If the user fails to pass any of the tests, it will then remind the user with some helpful tips to encourage the user to include in their password to make it not only valid but safer password.

<img width="982" alt="Screenshot 2023-12-15 at 12 19 25 AM" src="https://github.com/mattsel/Login-Password-Infrastructure/assets/141775337/c87af342-8d22-49e7-9687-0f6740fa92b0">








