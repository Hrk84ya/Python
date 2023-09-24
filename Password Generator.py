import string
import random

characters= list(string.ascii_letters+string.digits+"!@#$%^&*()")

def generate_password():
    password_length=int(input("Enter the length of the password: "))
    random.shuffle(characters)
    password=[]

    for x in range(password_length):
        password.append(random.choice(characters))
    
    random.shuffle(password)

    password="".join(password)

    print(password)

choice=input("Do you want to generate a password? (Yes/No) ")

if choice.lower()=="yes":
    generate_password()
else:
    print("Thank you for using the password generator")