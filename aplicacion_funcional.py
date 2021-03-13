from ttkwidgets.autocomplete import AutocompleteCombobox
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import font
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename
import matplotlib.backends.backend_pdf
from sqlalchemy import create_engine
from PIL import Image, ImageTk
import os
import matplotlib.pyplot as plt

conn = sqlite3.connect('anla.db') #Conectar a la base de datos, exportar csv a SQL

anla = pd.read_csv("diccionario.csv", sep = ";",encoding = "ISO-8859-1")
anla["COMPONENTE"] = anla["COMPONENTE"].str.replace("<<", "").str.replace(">>", "")
anla = anla.loc[anla["CÓDIGO"] != "R"]
#anla.to_sql('diccionario_nuevo', con=conn, index=False)


class Interfaz(object):

    """ Programa para la filtración de bases de datos SQL, la personalización a través
    de una interfaz gráfica y la exportación de esos resultados en HTML"""

    def __init__(self, root): #Widgets que conformarán la interfaz gráfica del programa.
        
        self.root = root
        self.root.title("Programa base de datos Anla")
        self.root.iconbitmap(r'icono.ico')
        self.canvas = tk.Canvas(self.root, height = 500, width =1000)
        self.canvas.pack()
        self.imagen_fondo = PhotoImage(file='montaña.png')
        self.frame = tk.Frame(self.root, bg = None ) #"#20CDC8"
        self.frame.place(relheight = 1, relwidth= 1)
        self.imagen_Label = tk.Label(self.frame, image= self.imagen_fondo)
        self.imagen_Label.place(relheight = 1, relwidth= 1)
        self.autocompletar = AutocompleteCombobox(self.frame, completevalues = self.combo())
        self.autocompletar.place(relheight = 0.07, relwidth = 0.65, relx = 0.2, rely = 0.08)
        self.boton = tk.Button(self.frame, text = "Agregar Componente", relief="flat", fg = "#FFDBA9", bg = "#578FBE", font=("Helvetica", 10, "bold"), bd = 1, command = self.adicionar_componentes)
        self.boton.place(relheight = 0.07, relwidth = 0.18, relx = 0.018, rely = 0.08) 
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Helvetica', 11)) # Modify the font of the body
        self.arbol = ttk.Treeview(self.frame, height = 5, style = "mystyle.Treeview")
        self.arbol.place(relheight = 0.65, relwidth = 0.7, relx = 0.15, rely = 0.25)
        self.arbol.heading('#0', text = 'COMPONENTES SELECCIONADOS', anchor = CENTER)
        self.fuente = font.Font(family='Helvetica', size=10, weight='bold')
        self.boton_delete = tk.Button(self.frame, text = "Eliminar componente", bg = "#FFC16B", fg = "#4F3F2A", relief="flat", font=("Helvetica", 10, "bold"), command = self.eliminar_seleccion)
        self.boton_delete.place(relheight = 0.07, relwidth = 0.15, relx = 0.15, rely = 0.92 )
        self.boton_delete_all = tk.Button(self.frame, text = "Eliminar todo", relief="flat", bg = "#FF976B", fg = "#4F3F2A", font=("Helvetica", 10, "bold"), command = self.eliminar_todo)
        self.boton_delete_all.place(relheight = 0.07, relwidth = 0.14, relx = 0.72, rely = 0.92)
        self.mensaje = tk.Label(self.frame, text = "", anchor = "center", font = self.fuente, bg = "#20CDC8" )
        self.mensaje.place(relx = 0.2, rely = 0.15)
        self.boton_prueba = tk.Button(self.frame, text = "Conoce tus requisitos", relief="flat", bg = "#52C496", fg = "#4F3F2A", font=("Helvetica", 10, "bold"), command = self.otra_cosa)
        self.boton_prueba.place(relheight = 0.07, relwidth = 0.16, relx = 0.43, rely = 0.92)
    
    def combo(self): #Formar una lista de los elementos seleccionados en la tabla de la base de datos
        #Función para desplegar los datos en un Autocomplete Combobox
        conn = sqlite3.connect("anla.db")
        c = conn.cursor()
        lista_nueva = c.execute("SELECT DISTINCT COMPONENTE FROM diccionario_nuevo WHERE CÓDIGO != 'T' ORDER BY COMPONENTE")
        vacio = []
        for componente in lista_nueva:
            vacio.append(componente[0])
        return vacio
    
    def adicionar_componentes(self): #Función que despliega los elementos seleccionados del Combobox
        #La información es desplegada en un Treeview widget

        add = self.autocompletar.get()
        if add not in self.combo():
            self.mensaje = tk.Label(self.frame, text = "", anchor = "center", font = self.fuente, bg = "#20CDC8" )
            self.mensaje["text"] = "{} no es un componente".format(add)
            self.mensaje.place(relx = 0.2, rely = 0.15)
            return self.mensaje
        else:
            return self.arbol.insert('', tk.END , text = add, value = ""), self.mensaje.destroy()
    
    def eliminar_seleccion(self): #Función para el botón de eliminar la selección una por una
        selected_item = self.arbol.selection() 
        
        try:
            self.arbol.delete(selected_item)
            self.mensaje_seleccion.destroy()
        except:
            self.mensaje_seleccion = tk.Label(self.frame, text = "Seleccione un componente", font = self.fuente, bg = "#20CDC8")
            self.mensaje_seleccion.place(relx = 0.8, rely = 0.17)
            
            
    def eliminar_todo(self): #Botón para eliminar todas las selecciones presentes en el Treeview
        for componente in self.arbol.get_children():
            eliminar = self.arbol.delete(componente)
        return eliminar
            
    
    def otra_cosa(self): #Crea una ventana en donde se desplegarán los resultados de la selección hecha
        
        self.otra_ventana = Toplevel()
        self.otra_ventana.title("Resultados")
        self.otra_ventana.iconbitmap(r'icono.ico')
        self.otro_canvas = Canvas(self.otra_ventana, height = 600, width =1000)
        self.otro_canvas.pack()
        self.imagen_otro = PhotoImage(file='rosa.png')
        self.imagen_Label_otro = tk.Label(self.otra_ventana, image= self.imagen_otro)
        self.imagen_Label_otro.place(relheight = 1, relwidth= 1)
        self.arbol_otro = ttk.Treeview(self.otra_ventana, height = 20, column=("column1", "column2", "column3"), show='headings')
        self.arbol_otro.column("#0", width = 500, stretch = 0, anchor = "w")
        self.arbol_otro.place(relheight = 0.65, relwidth = 0.7, relx = 0.15, rely = 0.25)
        
        self.arbol_otro.heading("column1", text="Capas geográficas")
        self.arbol_otro.heading("column2", text="Tipo de información")
        self.arbol_otro.heading("column3", text="Geometría")
        self.boton_exportar = tk.Button(self.otra_ventana, text = "Exportar", command = self.exportar)
        self.boton_exportar.place(relheight = 0.07, relwidth = 0.15, relx = 0.15, rely = 0.92)
        

        conn = sqlite3.connect("anla.db")
        c = conn.cursor()
        
        for componente in self.arbol.get_children(): #Filtra la información de la tabla, de acuerdo a la selección hecha.
            c_individual = self.arbol.item(componente)["text"]
            insert = self.arbol_otro.insert("", tk.END, values = c_individual)
            
            if c_individual == "ANALISIS_RIESGO":
                anali_riesgo = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'ANALISIS_RIESGO' ")
                for i in anali_riesgo.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
            elif c_individual == "AREAS_CONSER_PROTEC_AMBIENTAL":
                area_conservacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'AREAS_CONSER_PROTEC_AMBIENTAL'")
                for i in area_conservacion.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "AREAS_REGLAMENTACION_ESPECIAL":
                areas_reglamentacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'AREAS_REGLAMENTACION_ESPECIAL'")
                for i in areas_reglamentacion.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "ARQUEOLOGIA":
                arqueologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'ARQUEOLOGIA'")
                for i in arqueologia.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
            elif c_individual == "ATMOSFERA":
                atmosfera = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'ATMOSFERA' OR Medio = 'ATMOSFERA'")
                for i in atmosfera.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
            elif c_individual == "BIOTICO_CONTI_COSTE":
                biotico = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'BIOTICO_CONTI_COSTE' or Medio = 'BIOTICO_CONTI_COSTE'")
                for i in biotico.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
            elif c_individual == "CLIMA":
                clima = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'CLIMA' or Medio = 'CLIMA'")
                for i in clima.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
            elif c_individual == "COMPENSACION":
                compensacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'COMPENSACION' OR Medio = 'COMPENSACION'")
                for i in compensacion.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "CONTINGENCIAS":
                contingencias = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'CONTINGENCIAS' OR Medio = 'CONTINGENCIAS'")
                for i in contingencias.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "ECONOMICO":
                economico = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'ECONOMICO'")
                for i in economico.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "GEOLOGIA":
                geologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'GEOLOGIA' OR Medio = 'GEOLOGIA'")
                for i in geologia.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
            elif c_individual == "GEOMORFOLOGIA":
                geomorfologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'GEOMORFOLOGIA'")
                for i in geomorfologia.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "GEOTECNIA":
                geotecnia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'GEOTECNIA'")
                for i in geotecnia.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
                
                
            elif c_individual == "GESTION_RIESGO":
                gestion_riesgo = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'GESTION_RIESGO'")
                for i in gestion_riesgo.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "HIDROGEOLOGIA":
                hidrogeologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'HIDROGEOLOGIA' OR Medio = 'HIDROGEOLOGIA'")
                for i in hidrogeologia.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "HIDROLOGIA":
                hidrologia = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'HIDROLOGIA' OR Medio = 'HIDROLOGIA'")
                for i in hidrologia.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "INVERSION_1_POR_CIENTO":
                inversion1 = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'INVERSION_1_POR_CIENTO' OR Medio = 'INVERSION_1_POR_CIENTO'")
                for i in inversion1.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "MARINO":
                marino = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'MARINO' OR Medio = 'MARINO'")
                for i in marino.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "PAISAJE":
                paisaje = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'PAISAJE'")
                for i in paisaje.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2

            elif c_individual == "POLITICO_ADMINISTRATIVO ":
                politico = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'POLITICO_ADMINISTRATIVO ' OR Medio = 'POLITICO_ADMINISTRATIVO'")
                for i in politico.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "PROYECTO":
                proyecto = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'PROYECTO' OR Medio = 'PROYECTO'")
                for i in proyecto.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "SOCIOCULTURAL":
                sociocultural = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'SOCIOCULTURAL'")
                for i in sociocultural.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "SUELOS":
                suelos = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'SUELOS' OR Medio = 'SUELOS'")
                for i in suelos.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            elif c_individual == "ZONIFICACION":
                zonificacion = c.execute("SELECT DISTINCT CAPAS, CÓDIGO, GEOMETRÍA FROM diccionario_nuevo WHERE COMPONENTE = 'ZONIFICACION'")
                for i in zonificacion.fetchall():
                    insert_2 = self.arbol_otro.insert(insert, tk.END, values=(i[0], i[1], i[2]), open=True)   
                insert_2
            
            else:
                pass
            
        
    def export_pdf(self): #Extrae la información del Treeview en un Dataframe
        vacio = []
        
        valores = self.arbol_otro.get_children()
        for individuos in valores:
            c_individual = self.arbol_otro.item(individuos)["values"]
            vacio.append(c_individual)
            for child in self.arbol_otro.get_children(individuos):
                data = self.arbol_otro.item(child)["values"]
                vacio.append(data)
                
        df = pd.DataFrame(vacio, columns = ["Capas geográficas", "Tipo de información", "Geometria"])
        mask = df.applymap(lambda x: x is None)
        cols = df.columns[(mask).any()]
        for col in df[cols]:
            df.loc[mask[col], col] = ''
        
        return df
    
    
    def boton_pdf(self): #Devuelve la información como una tabla HTML 
        
        df_2 = self.export_pdf()
        
        tabla = df_2.to_html("Resultados.html", justify = "center", index = False)
        return tabla
        
  
    def exportar(self):  #Exporta la selección    
        return self.boton_pdf()
                
           
root = Tk()
C = Interfaz(root)
root.mainloop()