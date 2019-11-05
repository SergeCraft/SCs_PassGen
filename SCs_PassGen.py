from PWG_modules.PW_Gen import PW_Gen

def Main():
    print("Serge Craft's Password Generator\n")
    pwg = PW_Gen()
    password = pwg.GeneratePassword()
    print(password)

Main()
