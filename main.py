from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.config import Config
#import speech_recognition 
import sys
#Importando las screen creadas
from base.homescreen import HomeScreen
from base.settingsscreen import SettingsScreen
from base.calendarioscreen import CalendarioScreen
from base.tareasscreen import TareasScreen


class MyApp(MDApp):
    def build(self):
        self.title='Agenda'

        self.theme_cls.primary_palette='Blue'#'DeepOrange'
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        return Builder.load_file("main.kv")
    
    def cerrar_ventana(self):
        sys.exit()
        
    def activar_microfono(self):
        pass
        # print('activar micro')
        # recognizer=speech_recognition.Recognizer()
        # with speech_recognition.Microphone() as source:
        #     print('Di una frase')
        #     audio=recognizer.listen(source)
        # print(recognizer.recognize_google(audio,language='es'))
        #segundo video 3.29

if __name__=="__main__":
    MyApp().run()