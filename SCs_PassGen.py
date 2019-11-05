from modules.PW_Gen import PW_Gen

# основной метод
def Main():
    print("Serge Craft's Password Generator\n")
    pwg = PW_Gen()
    password = pwg.GeneratePassword()
    pwg.WriteToFile(password)
    print("Сгенерирован новый пароль: {0}".format(password))

if __name__ == "__main__":
    Main()