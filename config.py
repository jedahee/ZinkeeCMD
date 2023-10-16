
# * IMPORTS *
# ***********
# ? Standard libraries
import pickle 

# ? Text colored in CMD
from colored import fg
# * ------- *


# * CONFIG OBJECT *
# ***************** 
class Config:
    def __init__(self):

        # ? Variables
        self.EMAIL = ''
        self.PASSW = ''
        self.SAVE_COOKIES = None
        self.MAX_TIMEOUT = 15
        self.TIME_ENTRY_MORNING = ""
        self.TIME_DEPARTURE_MORNING = ""
        self.TIME_ENTRY_AFTERNOON = ""
        self.TIME_DEPARTURE_AFTERNOON = ""
        self.TIME_ENTRY_BREAK = ""
        self.TIME_DEPARTURE_BREAK = ""

    # ? Text to show
    def __str__(self):
        
        # ? Color vars
        light_color = fg('white')
        primary_color = fg('light_green')
        error_color = fg('red')
        info_color = fg('light_blue')
        success_color = fg('green')

        if not self.SAVE_COOKIES:
            is_cookies = error_color+"No"+light_color
        else:
            is_cookies = success_color+"Si"+light_color
        
        # ? String to show
        string = """ 
        +----------+
        | """+success_color+"""OPCIONES"""+light_color+""" |
        +----------+
        """

        string += info_color+"\n[1]"+ light_color +" EMAIL: "+success_color+str(self.EMAIL) + "\n"
        string += info_color+"[2]"+ light_color +" CONTRASEÑA: "+success_color+str(self.PASSW) + "\n"
        string += info_color+"[3]"+ light_color +" GUARDAR COOKIES: "+is_cookies + "\n"
        string += info_color+"[4]"+ light_color +" TIEMPO DE ESPERA MÁXIMO (Solo modificar si tu conexión es lenta): "+success_color+str(self.MAX_TIMEOUT) + "s\n\n"
        string += info_color+"[5]"+ light_color +" HORA DE ENTRADA POR LA MAÑANA: "+success_color+str(self.TIME_ENTRY_MORNING) + "\n"
        string += info_color+"[6]"+ light_color +" HORA DE SALIDA POR LA MAÑANA: "+success_color+str(self.TIME_DEPARTURE_MORNING) + "\n\n"
        string += info_color+"[7]"+ light_color +" HORA DE ENTRADA POR LA TARDE: "+success_color+str(self.TIME_ENTRY_AFTERNOON) + "\n"
        string += info_color+"[8]"+ light_color +" HORA DE SALIDA POR LA TARDE: "+success_color+str(self.TIME_DEPARTURE_AFTERNOON) + "\n\n"
        string += info_color+"[9]"+ light_color +" HORA DE ENTRADA DEL DESCANSO: "+success_color+str(self.TIME_ENTRY_BREAK) + "\n"
        string += info_color+"[10]"+ light_color +" HORA DE SALIDA DEL DESCANSO: "+success_color+str(self.TIME_DEPARTURE_BREAK) + "\n"
        string += info_color+"\n[0]"+ light_color +" VOLVER\n"

        return string

    # ? Getters

    def get_email(self):
        return self.EMAIL
    def get_passw(self):
        return self.PASSW
    def get_save_cookies(self):
        return self.SAVE_COOKIES
    def get_max_timeout(self):
        return self.MAX_TIMEOUT
    def get_time_entry_morning(self):
        return self.TIME_ENTRY_MORNING
    def get_time_departure_morning(self):
        return self.TIME_DEPARTURE_MORNING
    def get_time_entry_afternoon(self):
        return self.TIME_ENTRY_AFTERNOON
    def get_time_departure_afternoon(self):
        return self.TIME_DEPARTURE_AFTERNOON
    def get_time_entry_break(self):
        return self.TIME_ENTRY_BREAK
    def get_time_departure_break(self):
        return self.TIME_DEPARTURE_BREAK
    

    # ? Setters

    def set_email(self, value):
        self.EMAIL = value
    def set_passw(self, value):
        self.PASSW = value
    def set_save_cookies(self, value):
        if (value == 'si'):
            self.SAVE_COOKIES = True
        elif (value == 'no'):
            self.SAVE_COOKIES = False
    
    def set_time_entry_morning(self, value):
        self.TIME_ENTRY_MORNING = value
    def set_time_departure_morning(self, value):
        self.TIME_DEPARTURE_MORNING = value
    def set_time_entry_afternoon(self, value):
        self.TIME_ENTRY_AFTERNOON = value
    def set_time_departure_afternoon(self, value):
        self.TIME_DEPARTURE_AFTERNOON = value
    def set_time_entry_break(self, value):
        self.TIME_ENTRY_BREAK = value
    def set_time_departure_break(self, value):
        self.TIME_DEPARTURE_BREAK = value
    def set_max_timeout(self, value):
        self.MAX_TIMEOUT = value


        
# * ------- *
