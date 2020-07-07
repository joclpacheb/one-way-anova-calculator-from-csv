
"""
=========================================================================================================================================
ASIGNACIÓN DEL TERCER PARCIAL
ESTADÍSTICA MATEMÁTICA
UCLA-DCYT

Integrantes:

Anyeli Villareal CI: 26.002.905
Jose Luis Pacheco C.I:26.169.922
Dany Karam C.I: 25.147.670
Marielba Maldonado C.I: 26.088.718 

=========================================================================================================================================
                                                        
                                                        PLANTEAMIENTO:

Realice un programa que permita resolver problemas de análisis de varianza. Elija un ejemplo ilustrativo y realice el análisis.

                                                        MANUAL DE USO:

Al ejecutar con Python este programa, se abrirá una ventana en donde podrá elegir la ubicación en su computadora y las
características(delimitador entre datos y formato decimal) del Archivo CSV con los datos que utilizará para el estudio ANOVA.
Al seleccionar su archivo CSV, el programa indicará por consola la especificación del número de variables categóricas o cualitativas, 
el número de variables cuantitativas o numéricas y el número de registros que se detecten en dicho archivo CSV. Luego, podrá 
seleccionar por consola la variable categórica independiente y la variable cuantitativa dependiente, necesarias para el estudio.
El programa muestra posteriormente una serie de estadísticas descriptivas asociadas a las variables de su archivo, como también
muestra la Tabla ANOVA resultante calculada con uso de librerías para dicho fin y también muestra la tabla ANOVA sin uso de librerías,
calculando y mostrando sus valores respectivos manualmente.

=========================================================================================================================================

"""

import numpy as np  # para la manipulación de métodos numéricos
import os  # os permite limpiar la pantalla de la terminal en donde se ejecuta el código
import csv  # csv permite el manejo de archivos csv
import pandas as pd  # facilita el manejo e interpretación de datos en archivos csv
# gmean de la librería scipy facilita el cálculo de la media geométrica
# facilita el calculo de la media geométrica

import scipy as sp  # scipy permite el cálculo del P-valor
# para generar tablas en consola con caracteres ASCII
from prettytable import PrettyTable

import seaborn as sn  # facilita la generación de gráficas personalizadas
import statsmodels.api as sm  # para el cálculo de la tabla ANOVA con librerías
# para el cálculo de la tabla ANOVA con librerías
from statsmodels.formula.api import ols

# tkinter permite la generación de GUI en Python
from tkinter import Frame, Button, Label, Checkbutton
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    from tkinter import filedialog


os.system("cls")  # limpia la pantalla


print('==================================================================================================')
print('                   RESOLVEDOR DE PROBLEMAS DE ANÁLISIS DE VARIANZA (ANOVA)                        ')
print('==================================================================================================\n')

# dirección en su computadora del archivo CSV a analizar en el estudio
path = "no asignado"
delimiter = ""  # almacenará el caracter que se utiliza como delimitador entredatos en su archivo CSV
decimal = ""  # almacenará el catacter que dicata el formato decimal en el archivo CSV

# =========================================================================================================================================
# En la siguiente sección de código se crea la ventana inicial con una Interfaz Gráfica de Usuario, para la selección del archivo CSV
# =========================================================================================================================================

root = tk.Tk()
root.title("RESOLVEDOR DE PROBLEMAS ANOVA")
style = ttk.Style(root)
style.theme_use("clam")

Chx1 = tk.BooleanVar()
Chx2 = tk.BooleanVar()

Chx1.set(1)
Chx2.set(1)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_height = 160
window_width = 380

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry("{}x{}+{}+{}".format(window_width,
                                   window_height, x_cordinate, y_cordinate))


def c_open_file_old():
    # print('chx1:'+str(Chx1.get()))
    # print('chx2:'+str(Chx2.get()))
    global path
    path = filedialog.askopenfilename(title="Seleccionar Archivo CSV", parent=root, initialdir='/',
                                      filetypes=[("CSV", "*.csv")])
    global delimitadorcsv
    global decimalcsv

    if (Chx1.get() == True):
        delimitadorcsv = ";"
    else:
        delimitadorcsv = ","

    if (Chx2.get() == True):
        decimalcsv = "."
    else:
        decimalcsv = ","

    root.destroy()


ttk.Label(root, text='==============================================\nRESOLVEDOR DE PROBLEMAS DE ANÁLISIS DE VARIANZA(ANOVA)\n=============================================='
          ).grid(
    row=0, column=0, padx=4, pady=4, sticky='ew')
ttk.Label(root, text='Para hacer el Análisis de Varianza, debe proveer los datos de estudio:').grid(
    row=0, column=0, padx=4, pady=4, sticky='ew')


container1 = tk.Frame(root)
container1.grid(column=0, row=2)

Label(container1, text='Delimitador: ').grid(
    row=0, column=0, sticky='ew')

ttk.Checkbutton(container1, text='Punto y Coma ( ; )',
                variable=Chx1,
                onvalue=1,
                offvalue=0
                ).grid(
    row=0, column=1, padx=4, pady=4, sticky='ew')

ttk.Checkbutton(container1, text='Coma ( , )',
                variable=Chx1,
                onvalue=0,
                offvalue=1
                ).grid(
    row=0, column=2, padx=4, pady=4, sticky='ew')


container2 = tk.Frame(root)
container2.grid(column=0, row=4)

Label(container2, text='Decimal: ').grid(
    row=0, column=0, sticky='ew')

ttk.Checkbutton(container2, text='Punto ( . )',
                variable=Chx2,
                onvalue=1,
                offvalue=0
                ).grid(
    row=0, column=1, padx=4, pady=4, sticky='ew')

ttk.Checkbutton(container2, text='Coma ( , )',
                variable=Chx2,
                onvalue=0,
                offvalue=1
                ).grid(
    row=0,  column=2, padx=4, pady=4, sticky='ew')

ttk.Button(root, text="Abrir Archivo CSV", command=c_open_file_old).grid(
    row=5, column=0, padx=4, pady=4, sticky='ew')


root.mainloop()

# =========================================================================================================================================
# Una vez cerrada la ventana del GUI, se comprueba la selección y debida lectura del archivo CSV
# =========================================================================================================================================

if path != "no asignado":
    dataframe = pd.read_csv(path, delimiter=delimitadorcsv, decimal=decimalcsv)
    print('El archivo CSV seleccionado está en la ruta:\n')
    print(path)
    cantidad_registros = str(dataframe.shape[0])
    nro_categoricas = len(list(dataframe.select_dtypes(include='object')))
    nro_cuantitativas = len(list(dataframe.select_dtypes(exclude='object')))

    print('\n-------------------------------------------------------------------------------------------------\n')
    print('Cantidad de Registros en el CSV: ' + cantidad_registros)
    print('Cantidad de Variables: ' + str(len(dataframe. columns)))
    print('Cantidad de Variables Cuantitativas: ' + str(nro_cuantitativas))
    print('Cantidad de Variables Categóricas: ' + str(nro_categoricas))
    print('\nDelimitador del CSV: ' + delimitadorcsv)
    print('Formato Decimal del CSV: ' + decimalcsv)

# =======================================================================================================================================================
# En la siguiente sección de código se especifica ingresando por consola (y pulsando enter) qué variables serán utilizadas en el estudio ANOVA posterior
# =======================================================================================================================================================

    print('\n-------------------------------------------------------------------------------------------------')
    print('                           SELECCIÓN DE VARIABLES PARA EL ESTUDIO ANOVA                            ')
    print('-------------------------------------------------------------------------------------------------\n')

    cuantitativas = list(dataframe.select_dtypes(exclude='object'))
    n = 1
    for j in cuantitativas:
        print(str(n)+'- ' + str(j))
        n = n+1
    print('\nIntroduza el número correspondiente a la Variable Cuantitativa Dependiente:  ')
    dep = cuantitativas[int(input())-1]

    print('\n-------------------------------------------------------------------------------------------------\n')

    categoricas = list(dataframe.select_dtypes(include='object'))
    n = 1
    for i in categoricas:
        print(str(n)+'- ' + str(i))
        n = n+1
    print('\nIntroduza el número correspondiente a la Variable Categórica Independiente:  ')
    ind = categoricas[int(input())-1]

    print('\n-------------------------------------------------------------------------------------------------')
    print('                           DATAFRAME CREADO A PARTIR DEL ARCHIVO CSV                               ')
    print('-------------------------------------------------------------------------------------------------\n')

    print(dataframe)

else:  # si no se actualizó el valor de path, significa que no se leyó ningún archivo y se termina la ejecución
    print('No se seleccionó ningún archivo')
    quit()

# =========================================================================================================================================
# En la siguiente sección de código se muestran los resultados del estudio descriptivo y de las tablas ANOVA
# =========================================================================================================================================

print('\n-------------------------------------------------------------------------------------------------')
print('                               ESTADÍSTICAS DESCRIPTIVAS DEL DATAFRAME                             ')
print('-------------------------------------------------------------------------------------------------\n')

print(dataframe.describe(include=[np.number]))
print('\n')
print(dataframe.describe(include=['O']))
print('\n')

print('\n-------------------------------------------------------------------------------------------------')
print('                        TABLA ANOVA CALCULADA CON LIBRERÍA STATMODELS                              ')
print('-------------------------------------------------------------------------------------------------\n')

lm = ols(dep + '~' + ind, data=dataframe).fit()
tabla = sm.stats.anova_lm(lm)
print(tabla)

print('\n-------------------------------------------------------------------------------------------------')
print('                       CÁLCULO DE VALORES PARA CONSTRUIR LA TABLA ANOVA                            ')
print('-------------------------------------------------------------------------------------------------\n')

# cálculo de Media General
overall_mean = dataframe[dep].mean()

# Cálculo para el total de la Suma de Cuadrados
dataframe['overall_mean'] = overall_mean
ss_total = sum((dataframe[dep] - dataframe['overall_mean'])**2)

# Medias Grupales
# se sustituye el nombre de la columna bmi en el df original
group_means = dataframe.groupby(ind)['overall_mean', dep].mean()
group_means = group_means.rename(columns={dep: 'group_mean'})


# Se agrega las medias grupales como columna al dataframe original
dataframe = dataframe.merge(group_means, left_on=ind, right_index=True)
# Cálculo de la Suma de Cuadrados Residual
ss_residual = sum((dataframe[dep] - dataframe['group_mean'])**2)

ss_explained = ss_total-ss_residual

# Grados de Libertad
valores_unicos = dataframe[ind].nunique()  # número de grupos
df_explained = valores_unicos-1
df_residual = int(cantidad_registros)-valores_unicos

# Cálculo del Cuadrado Medio Intragrupal
ms_residual = ss_residual / df_residual

# Cálculo del Cuadrado Medio Intergrupal
df_explained = valores_unicos - 1
ms_explained = ss_explained / df_explained

# Cálculo del Estadístico F
f = ms_explained / ms_residual

# Se calcula el  p-valor
p_value = 1 - sp.stats.f.cdf(f, df_explained, df_residual)

# Impresión en Pantalla de los Resultados
print('Media General: ' + str(overall_mean))
print('\n' + 'Medias Grupales:' + '\n\n' +
      str(group_means['group_mean'].to_string()))
print('\n' + 'Total de la Suma de Cuadrados: ' + str(ss_total))
print('Suma de Cuadrados Intragrupal: ' + str(ss_residual))
print('Suma de Cuadrados Intergrupal: ' + str(ss_explained))
print('Grados de Libertad Intergrupal: ' + str(df_explained))
print('Grados de Libertad Intragrupal: ' + str(df_residual))
print('Cuadrado Medio Intergrupal: ' + str(ms_explained))
print('Cuadrado Medio Intragrupal: ' + str(ms_residual))
print('Estadístico F: ' + str(f))
print('P-Valor: ' + str(p_value))

print('\n============================================================================================================================================')
print('                                                 TABLA ANOVA CALCULADA MANUALMENTE                                                              ')
print('==============================================================================================================================================\n')

print('Variable Cuantitativa Dependiente: '+dep)
print('Variable Categórica Independiente: '+ind)

print('==============================================================================================================================================\n')

x = PrettyTable()

x.field_names = [
    "Origen", "Grados de Libertad", "Suma de Cuadrados", "Cuadrado Medio", "Estadístico F", "P-Valor / PR(>F)"]

x.add_row(['Intergrupal', df_explained, ss_explained, ms_explained, f, p_value])
x.add_row(['Intragrupal (Residual)', df_residual,
           ss_residual, ms_residual, '-', '-'])
print(x)

print('\n============================================================================================================================================\n')
