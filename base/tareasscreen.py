
from logging import currentframe
from os import name
from kivy.uix.screenmanager import Screen
import time
from kivymd.app import MDApp
import psycopg2
from kivy.clock import Clock
#from base.banner import Banner
#Para el banner
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.graphics import Color,RoundedRectangle
from functools import partial

#clase encargada de crear las filas
class Banner(FloatLayout):
    
    def __init__(self,hora,actividad, **kwargs):
        self.hora=hora
        self.actividad=actividad
        super().__init__()
        with self.canvas.before:
            Color(rgba=(0,.5,1,.1))
            self.rect=RoundedRectangle(radius=[(20.0,20.0),(20.0,20.0),(20.0,20.0),(20.0,20.0)])
        
        self.bind(pos=self.update_rect,size=self.update_rect)

        #etiquetas
        self.title_hora=MDLabel(text=self.hora,pos_hint={'center_x': .1, 'center_y':.5},size_hint=(.15,.3),halign='center')
        
        self.title_actividad=MDLabel(text=self.actividad,pos_hint={'center_x': .6, 'center_y':.5},size_hint=(.75,.3),halign='left')

        self.menos=MDIconButton(icon='close',pos_hint={'center_x': .95, 'center_y':.5},on_release=kwargs['on_release'])

        self.add_widget(self.title_hora)
        self.add_widget(self.title_actividad)
        self.add_widget(self.menos)
    
    def update_rect(self,*args):
        self.rect.pos=self.pos
        self.rect.size=self.size
        


class TareasScreen(Screen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        self.fecha_hoy=int(time.strftime('%Y%m%d'))
        self.fecha_hoy_texto=(time.strftime('%d/%m/%Y'))
        Clock.schedule_interval(self.actualizar_scroll,2)
        
    def on_pre_enter(self, *args):
        self.app.title="Tareas"

    def consultar_bd(self,codigo_fecha):
        sql=""" SELECT hora,actividad FROM tareas WHERE codigo_fecha=%s;"""
        conn=None
        try:
            conn=psycopg2.connect(
                host='localhost',
                port='5432',
                user='postgres',
                database='agenda',
                password='will2001hh')

            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql,(codigo_fecha,))
                    if cur is not None:
                        self.fila=cur.fetchall()
                        return self.fila
            if conn is not None:
                conn.close()
            
        except(Exception,psycopg2.DatabaseError) as e:
            print(e)
        
        finally:
            if conn is not None:
                conn.close()

    def on_kv_post(self,base_widget):
        self.grid=self.ids['grid_banner']
        self.filas_iniciales=self.consultar_bd(self.fecha_hoy)
        #print(self.filas_iniciales)

        for i in self.filas_iniciales:
            self.banner=Banner(i[0],i[1],on_release=partial(self.borrar_banner,i[0],i[1]))
            self.grid.add_widget(self.banner)

        return self.filas_iniciales

    def actualizar_scroll(self,base_widget):
        self.grid=self.ids['grid_banner']
        self.filas_2=self.consultar_bd(self.fecha_hoy)
        #print(type(self.filas_iniciales))
        #Hallando los valores distintos
        self.nueva_lista=list(set(self.filas_2)-set(self.filas_iniciales))
    
        for i in self.nueva_lista:
            self.banner=Banner(i[0],i[1],on_release=partial(self.borrar_banner,i[0],i[1]))
            self.grid.add_widget(self.banner)
        #print(self.filas_2)
        self.filas_iniciales=self.filas_2


    def borrar_banner(self,hora,actividad,base_widget):
        sql=""" DELETE FROM tareas WHERE hora=%s AND actividad=%s;"""
        conn=None
        try:
            conn=psycopg2.connect(
                host='localhost',
                port='5432',
                user='postgres',
                database='agenda',
                password='will2001hh')

            with conn:
                with conn.cursor() as cur:
                    cur.execute(sql,(hora,actividad))
            if conn is not None:
                conn.close()
            
        except(Exception,psycopg2.DatabaseError) as e:
            print(e)
        
        finally:
            if conn is not None:
                conn.close()

        #Obteniendo filas restantes
        self.filas_restantes=self.consultar_bd(self.fecha_hoy)

        for i in range(len(self.filas_restantes)+1):
            self.grid.remove_widget(self.grid.children[0])

        #self.grid.remove_widget(self.grid.children[0])

        self.on_kv_post(base_widget)
