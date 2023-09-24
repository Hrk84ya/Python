def slicer():
    print()
    print("#######################################")
    print("| Welcome to the -Blade- email slicer |")
    print("#######################################")
    print()

    #Taking the email-id as input
    email_input=input("Enter your email-id: ")

    #storing the username,domain and extension in the respective variables using split method
    (username,domain)=email_input.split("@")
    (domain,extension)=domain.split(".")

    #Printing the details
    print()
    print("Username: ",username)
    print("Domain: ",domain)
    print("Extension: ",extension)

#calling the function
slicer()