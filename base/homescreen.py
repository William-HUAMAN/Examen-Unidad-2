from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.uix.label import Label
from kivy.clock import Clock
import time


class HomeScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()

        Clock.schedule_interval(self.actualizar_hora,1)

    def on_pre_enter(self, *args):
        self.app.title="Inicio"

    def actualizar_hora(self,dt):
        self.ids.hora_actual.text=time.strftime('%H:%M:%S')

        

