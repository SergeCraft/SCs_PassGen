from lxml import objectify, etree
import ast

class PW_Gen_setting ():
    """Класс конкретной настройки"""
    def __init__(self, _Name, _Value, _Input_dict, _Invite):
        self.Name = _Name
        self.Invite = _Invite
        self.Input_dict = _Input_dict
        self.Value = _Value

class PW_Gen_settings():
    """Класс настроек"""
    all = {}
    # Конструктор с параметрами
    def __init__(self):
        self.SetConfigFromFile()
        self.SetConfigFromUserInput()

    # Функция для ввода настройки пользователем
    def Input_setting(self, setting):
        while True: # Чтение настроек до победного
            setting_key = input(setting.Invite)
            try: # пример работы с исключениями
                if bool(setting.Input_dict): 
                    setting.Value = setting.Input_dict[setting_key]
                else:
                    setting.Value = setting_key
                break
            except:
                print("Неверно указан режим. Допустимые значения: {0}".format(", ".join(list(setting.Input_dict.keys())))) #неочевидно необходимое приведение словаря к удобочитаемому виду в одной строке
    
    # Функция для ввода настроек пользователем
    def SetConfigFromUserInput(self):
        for setting in self.all.values():
            self.Input_setting(setting)
            if setting.Name == "input_mode" and setting.Value == "file": break # костыль на случай, если пользователь выберет чтение настроек из файла
        else: #использование конструкции for...else
            self.WriteConfigToFile()
                
    # Функция для ввода настроек из конфиг-файла xml
    def SetConfigFromFile(self):
        print("Считываем файл настроек...")
        with open("config.xml", "r") as file: # использование with для чтения файла
            settings_str = file.read()
        settings_lxml = objectify.fromstring(settings_str) # парсинг xml
        settings = {}
        for setting_lxml in settings_lxml.getchildren():
            self.all.update(
                    {setting_lxml.Name :
                    PW_Gen_setting(
                           str(setting_lxml.Name),
                           setting_lxml.Value, 
                           ast.literal_eval(str(setting_lxml.Input_dict)), 
                           setting_lxml.Invite)
                    }
                )
            print("Настройка {0} установлена на {1}".format(setting_lxml.Name, setting_lxml.Value))
    
    # Запись текущих настроек в xml-файл
    def WriteConfigToFile(self):
        print("Записываем файл настроек...")
        settings_lxml = objectify.Element("settings")
        for setting in self.all.values():
            setting_lxml = objectify.Element(setting.Name)
            setting_lxml.Name = setting.Name
            setting_lxml.Value = setting.Value
            setting_lxml.Invite = setting.Invite
            setting_lxml.Input_dict = setting.Input_dict
            settings_lxml.append(setting_lxml)

            et = etree.ElementTree(settings_lxml)
            et.write("config.xml", pretty_print=True)