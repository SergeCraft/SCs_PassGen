from PWG_modules.PW_Gen_settings import *

class PW_Gen ():
    """Генератор паролей"""

    def __init__(self):
        settings = PW_Gen_settings()
    
    def GeneratePassword(self):
        print("Генерируем пароль...")
