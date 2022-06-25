


def checkSignupValid(typeCheck, userInput):
    if typeCheck == "username":
        if len(userInput) < 5:
            print("USERNAME MUST AT LEAST 5 CHARACTERS !")
        elif (all(c.isnumeric() or c.islower() for c in userInput)) == False:
            print("USERNAME includes a-z, 0-9")

    elif typeCheck == "password":
        if len(userInput) < 3:
            print("PASSWORD MUST AT LEAST 3 CHARACTERS !")

    elif typeCheck == "bank":
        if len(userInput) != 10:
            print("BANK ACCOUNT MUST HAS 10 CHARACTERS !")
        elif userInput.isnumeric() == False:
            print("BANK ACCOUNT includes 0-9")

    else:
        print("ERROR")

checkSignupValid("bank", "1231231235")
checkSignupValid("bank", "453asdgfdg")
checkSignupValid("bank", "123345567.")
checkSignupValid("bank", "123456789a")