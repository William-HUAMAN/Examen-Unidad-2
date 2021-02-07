from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from datetime import datetime
from kivymd.uix.dialog import MDDialog
import psycopg2

class CalendarioScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.app=MDApp.get_running_app()
        
    
    def on_pre_enter(self, *args):
        self.app.title="Agenda"
        self.ids.texto_tarea.text=''
        
    def get_date(self,date):
        self.ids["fecha"].text=date.strftime('%d/%m/%Y')
        self.codigo_fecha=int(date.strftime('%Y%m%d'))#en entero
        self.fecha=str(date.strftime('%d/%m/%Y'))#en texto
        return self.fecha,self.codigo_fecha
    
    def get_time(self,instance,time):
        self.ids["hora"].text=time.strftime('%H:%M')
        self.hora=str(time.strftime('%H:%M'))
        self.codigo_hora=((int(time.strftime('%H')))*60)+int(time.strftime('%M'))
        return self.hora

    def show_date_picker(self):
        date_dialog=MDDatePicker(callback=self.get_date)
        date_dialog.open()
    
    def show_time_picker(self):
        time_dialog=MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()
    
    def reiniciar_valores(self):
        self.ids["fecha"].text='Seleccione la Fecha'
        self.ids["hora"].text='Seleccione la Hora'
        self.ids.texto_tarea.text=''
        
    #Insertar datos
    def insertar_datos(self):
        
        sql=""" INSERT INTO tareas (codigo_fecha,codigo_hora,fecha,hora,actividad) VALUES (%s, %s, %s, %s, %s);"""
        conn=None

        try:
            conn=psycopg2.connect(
                host='localhost',
                database='agenda',
                port ='5432',
                user='postgres',
                password='will2001hh')
            
            cur=conn.cursor()

            cur.execute(sql, (self.codigo_fecha,self.codigo_hora,self.fecha,self.hora,self.ids.texto_tarea.text))

            conn.commit()
            cur.close()

            if conn is not None:
                conn.close()
        
        except(Exception,psycopg2.DatabaseError) as e:
            print(e)
        
        finally:
            if conn is not None:
                conn.close()
        
        #cuadro de confirmacion
        dialog=MDDialog(title='Tarea guardada',size_hint=(.4,.3))
        dialog.open()

        self.reiniciar_valores()
