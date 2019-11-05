from PWG_modules.settings_description import settings_description as sd
from lxml import objectify, etree

class PW_Gen_setting ():
    """Класс настроек генератора"""
    def __init__(self, _Name, _Value, _Input_dict, _Invite):
        self.Name = _Name
        self.Invite = _Invite
        self.Input_dict = _Input_dict
        self.Value = _Value

class PW_Gen_settings():
           
    def __init__(self):
        self.all = {s[0] : PW_Gen_setting(s[0], s[1], s[2], s[3]) for s in sd}
        self.WriteConfigToFile()
        self.SetConfigFromUserInput()

    def Input_setting(self, setting):
        while True:
            setting_key = input(setting.Invite)
            try:
                setting.Value = setting.Input_dict[setting_key]
                break
            except:
                print("Неверно указан режим. Допустимые значения: {0}".format(", ".join(list(setting.Input_dict.keys()))))

    def SetConfigFromFile(self):
        pass
                    
    def SetConfigFromUserInput(self):
        for setting in self.all.values():
            self.Input_setting(setting)
            if setting.Name == "input_mode" and setting.Value == "file":
                self.SetConfigFromFile()
                break

    def SetConfigFromFile(self):
        print("Считываем файл настроек...")
        with open("config.xml", "r") as file:
            settings_str = file.read()
        settings_lxml = objectify.fromstring(settings_str)
        settings = {}
        for setting_lxml in settings_lxml.getchildren():
            self.all.update(
                    {setting_lxml.Name :
                    PW_Gen_setting(
                           setting_lxml.Name,
                           setting_lxml.Value, 
                           setting_lxml.Input_dict, 
                           setting_lxml.Invite)
                    }
                )

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