# -*- coding: utf-8 -*-
"""
Created on Sun May 10 16:17:24 2020

@author: ASUS
"""

from ttkwidgets.autocomplete import AutocompleteCombobox
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import font
from sqlalchemy import create_engine
from PIL import Image, ImageTk

conn = sqlite3.connect('anla.db')

anla = pd.read_csv("diccionario.csv", sep = ";",encoding = "ISO-8859-1")
anla["COMPONENTE"] = anla["COMPONENTE"].str.replace("<<", "").str.replace(">>", "")
anla = anla.loc[anla["CÓDIGO"] != "R"]
#anla.to_sql('diccionario_nuevo', con=conn, index=False)

class Interfaz(object):
    def __init__(self, root):
        
        self.root = root
        self.root.title("Programa base de datos Anla")
        self.canvas = tk.Canvas(self.root, height = 400, width =700)
        self.canvas.pack()
        self.imagen_fondo = PhotoImage(file='fondo.png')
        self.frame = tk.Frame(self.root, bg = None ) #"#20CDC8"
        self.frame.place(relheight = 1, relwidth= 1)
        self.imagen_Label = tk.Label(self.frame, image= self.imagen_fondo)
        self.imagen_Label.place(relheight = 1, relwidth= 1)
        #self.desplegable = ttk.Combobox(self.frame, height = 10, textvariable = StringVar, values = self.combo())
        #self.desplegable.place(relheight = 0.05, relwidth = 0.65, relx = 0.2, rely = 0.08)
        self.autocompletar = AutocompleteCombobox(self.frame, completevalues = self.combo())
        self.autocompletar.place(relheight = 0.05, relwidth = 0.65, relx = 0.2, rely = 0.08)
        self.boton = tk.Button(self.frame, text = "Agregar Componente", bg = "#4CE37C", bd = 0.5, command = self.adicionar_componentes)
        self.boton.place(relheight = 0.07, relwidth = 0.18, relx = 0.018, rely = 0.08)
        #self.new_frame = tk.Frame(self.frame, bd = 2, bg = "white")
        #self.new_frame.place(relheight = 0.65, relwidth = 0.7, relx = 0.15, rely = 0.3)
        
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        
        self.arbol = ttk.Treeview(self.frame, height = 5)
        self.arbol.place(relheight = 0.65, relwidth = 0.7, relx = 0.15, rely = 0.25)
        self.arbol.heading('#0', text = 'COMPONENTES SELECCIONADOS', anchor = CENTER)
        
        self.fuente = font.Font(family='Helvetica', size=10, weight='bold')
        
        self.boton_delete = tk.Button(self.frame, text = "Eliminar componente", command = self.eliminar_seleccion)
        self.boton_delete.place(relheight = 0.07, relwidth = 0.18)
        
        self.boton_delete_all = tk.Button(self.frame, text = "Eliminar todo", command = self.eliminar_todo)
        self.boton_delete_all.place(relheight = 0.07, relwidth = 0.18, relx = 0.5, rely = 0.5)
        self.mensaje = tk.Label(self.frame, text = "", anchor = "center", font = self.fuente, bg = "#20CDC8" )
        self.mensaje.place(relx = 0.2, rely = 0.15)
        
    
    def combo(self):
        conn = sqlite3.connect("anla.db")
        c = conn.cursor()
        lista_nueva = c.execute("SELECT DISTINCT COMPONENTE FROM diccionario_nuevo WHERE CÓDIGO != 'T' ORDER BY COMPONENTE")
        vacio = []
        for componente in lista_nueva:
            vacio.append(componente[0])
        return vacio
    
    def adicionar_componentes(self):
        add = self.autocompletar.get()
        if add not in self.combo():
            self.mensaje = tk.Label(self.frame, text = "", anchor = "center", font = self.fuente, bg = "#20CDC8" )
            self.mensaje["text"] = "{} no es un componente".format(add)
            self.mensaje.place(relx = 0.2, rely = 0.15)
            return self.mensaje
        else:
            return self.arbol.insert('', 0, text = add, value = ""), self.mensaje.destroy()
    
    def eliminar_seleccion(self):
        selected_item = self.arbol.selection() 
        
        try:
            self.arbol.delete(selected_item)
            self.mensaje_seleccion.destroy()
        except:
            self.mensaje_seleccion = tk.Label(self.frame, text = "Seleccione un componente", font = self.fuente)
            self.mensaje_seleccion.place(relx = 0.8, rely = 0.9, anchor = "se")
            
            
    def eliminar_todo(self):
        for componente in self.arbol.get_children():
            eliminar = self.arbol.delete(componente)
        return eliminar
    
     def otra_cosa(self):
        
        self.otra_ventana = Toplevel()
        self.otra_ventana.title("Resultados")
        self.otro_canvas = Canvas(self.otra_ventana, height = 400, width =700)
        self.otro_canvas.pack()
        self.imagen_otro = PhotoImage(file='cielo.png')
        self.imagen_Label_otro = tk.Label(self.otra_ventana, image= self.imagen_otro)
        self.imagen_Label_otro.place(relheight = 1, relwidth= 1)

        conn = sqlite3.connect("anla.db")
        c = conn.cursor()
        
        for componente in self.arbol.get_children():
            c_individual = self.arbol.item(componente)["text"]
            
            if c_individual == "ANALISIS_RIESGO":
                anali_riesgo = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'ANALISIS_RIESGO' ")
                print(anali_riesgo)
            
            elif c_individual == "AREAS_CONSER_PROTEC_AMBIENTAL":
                area_conservacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'AREAS_CONSER_PROTEC_AMBIENTAL'")
                print(area_conservacion)
            
            elif c_individual == "AREAS_REGLAMENTACION_ESPECIAL":
                areas_reglamentacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'AREAS_REGLAMENTACION_ESPECIAL'")
                print(areas_reglamentacion)
            
            elif c_individual == "ARQUEOLOGIA":
                arqueologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'ARQUEOLOGIA'")
                print(arqueologia)
            
            elif c_individual == "ATMOSFERA":
                atmosfera = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'ATMOSFERA' OR Medio = 'ATMOSFERA'")
                print(atmosfera)
                
            elif c_individual == "BIOTICO_CONTI_COSTE":
                biotico = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'BIOTICO_CONTI_COSTE' or Medio = 'BIOTICO_CONTI_COSTE'")
                print(biotico)
                
            elif c_individual == "CLIMA":
                clima = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'CLIMA' or Medio = 'CLIMA'")
                print(clima)
                
            elif c_individual == "COMPENSACION":
                compensacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'COMPENSACION' OR Medio = 'COMPENSACION'")
                print(compensacion)
            
            elif c_individual == "CONTINGENCIAS":
                contingencias = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'CONTINGENCIAS' OR Medio = 'CONTINGENCIAS'")
                print(contingencias)
            
            elif c_individual == "ECONOMICO":
                economico = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'ECONOMICO'")
                print(economico)
            
            elif c_individual == "GEOLOGIA":
                geologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'GEOLOGIA' OR Medio = 'GEOLOGIA'")
                print(geologia)
                
            elif c_individual == "GEOMORFOLOGIA":
                geomorfologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'GEOMORFOLOGIA'")
                print(geomorfologia)
            
            elif c_individual == "GEOTECNIA":
                geotecnia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'GEOTECNIA'")
                print(geotecnia)
                
            elif c_individual == "GESTION_RIESGO":
                gestion_riesgo = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'GESTION_RIESGO'")
                print(gestion_riesgo)
            
            elif c_individual == "HIDROGEOLOGIA":
                hidrogeologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'HIDROGEOLOGIA' OR Medio = 'HIDROGEOLOGIA'")
                print(hidrogeologia)
            
            elif c_individual == "HIDROLOGIA":
                hidrologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'HIDROLOGIA' OR Medio = 'HIDROLOGIA'")
                print(hidrologia)
            
            elif c_individual == "INVERSION_1_POR_CIENTO":
                inversion1 = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'INVERSION_1_POR_CIENTO' OR Medio = 'INVERSION_1_POR_CIENTO'")
                print(inversion1)
            
            elif c_individual == "MARINO":
                marino = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'MARINO' OR Medio = 'MARINO'")
                print(marino)
            
            elif c_individual == "PAISAJE":
                paisaje = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'PAISAJE'")
            
            elif c_individual == "POLITICO_ADMINISTRATIVO":
                politico = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'POLITICO_ADMINISTRATIVO' Medio = 'POLITICO_ADMINISTRATIVO'")
                print(politico)
            
            elif c_individual == "PROYECTO":
                proyecto = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'PROYECTO' OR Medio = 'PROYECTO'")
                print(proyecto)
            
            elif c_individual == "SOCIOCULTURAL":
                sociocultural = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'SOCIOCULTURAL'")
                print(sociocultural)
            
            elif c_individual == "SUELOS":
                suelos = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'SUELOS' OR Medio = 'SUELOS'")
                print(suelos)
            
            elif c_individual == "ZONIFICACION":
                zonificacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO FROM diccionario_nuevo WHERE COMPONENTE = 'ZONIFICACION'")
                print(zonificacion)
            
            else:
                pass
            
    
    
root = Tk()
C = Interfaz(root)
root.mainloop()

