from modules.PW_Gen_settings import *
import random

class PW_Gen ():
    """Генератор паролей"""

    letters_dict = { "ru_lc_letters" : range(1072, 1104),
                   "ru_uc_letters" : range(1040, 1072), 
                   "en_lc_letters" : range(97, 123), 
                   "en_uc_letters" : range(65, 91), 
                   "numbers_letters" : range(48, 58)}

    def __init__(self):
        self.settings = PW_Gen_settings()
    
    def GeneratePassword(self):
        print("Генерируем пароль...")
        pw_length = self.settings.all["password_length"].Value
        symbols_pool = self.GetSymbolsPool()
        random.shuffle(symbols_pool)
        starting_symbol = random.randrange(len(symbols_pool) - pw_length)
        pw_indexed = symbols_pool[starting_symbol : starting_symbol + pw_length]
        pw_refined = self.BringPasswordQuality(pw_indexed)
        return "".join(chr(id) for id in pw_refined)

    def GetSymbolsPool(self):
        sp = []
        sp.extend(self.letters_dict["numbers_letters"])
        sp.extend(self.letters_dict["en_lc_letters"])
        stg = self.settings
        if stg.all["include_Cyrillic"].Value == True: 
            sp.extend(self.letters_dict["ru_lc_letters"])
        
        if stg.all["include_Uppercase"].Value == True:
            sp.extend(self.letters_dict["en_uc_letters"])
            if stg.all["include_Cyrillic"].Value == True:
                sp.extend(self.letters_dict["ru_uc_letters"])
        return sp

    def BringPasswordQuality(self, pw_indexed):
        for charlist in self.letters_dict.values():
            if not set(charlist) & set(pw_indexed):
                pw_indexed[random.randrange(len(pw_indexed))] = charlist[random.randrange(len(charlist))]
        return pw_indexed

    def WriteToFile(self, text):
        file_path = str(self.settings.all["output_file_path"].Value)
        print("Записываем файл с паролем {0}...".format(file_path))
        with open(file_path, "w") as file:
            file.write(text)