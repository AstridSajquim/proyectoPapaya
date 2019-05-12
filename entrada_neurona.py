"""
programa para leer los recortes de las carpetas especificas
redimensionar las imgaenes con un algoritmo sin perdida
tamaño 40 x 10
normaliza los datos entre 0 y 1 con tres decimales
agrega 3 datos al final 
1 0 0 podrido
0 1 0 maduro
0 0 1 verde
lee todos los pixeles de cada imagen y los guarda en datos-entrenamiento-csv
"""
"""1"""

from PIL import Image
from os import listdir
import os

def sacar_pixels(direccion, entrada):
    #se abre la imagen
    im = Image.open(direccion)
    #redimensiona la imagen con ANTIALIS algoritmo con menos perdida
    im = im.resize((40, 10), Image.ANTIALIAS)
    #im = im.resize((100, 50), Image.ANTIALIAS)
    #im.save("hola.jpg")
    #lectura de pixels
    pixels = im.load()
    #se abre el archivo para lectura escritura
    archivo_entrenamiento = open("datos-entrenamiento.csv", "a")
    filas, columnas = im.size
    decimales = 4
    for columna in range (columnas):
        for fila in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            rojo = str(normalizar(pixels[fila,columna][0]))
            verde = str(normalizar(pixels[fila,columna][1]))
            azul = str(normalizar(pixels[fila,columna][2]))
            cadena = rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "
            archivo_entrenamiento.write(cadena)

    #pix[x,y] = value # Set the RGBA Value of the image (tuple) 
    archivo_entrenamiento.write(entrada)
    archivo_entrenamiento.write("\n")
    archivo_entrenamiento.close()

def recorrer_directorio(carpeta_entrada, lista_imagenes, salida):
    for nombre_imagen in lista_imagenes:
        print (nombre_imagen)
        sacar_pixels(carpeta_entrada + "/" +nombre_imagen, salida)

def normalizar(valor):
    salida = (valor*1.)/255.
    return salida
    

if(os.path.exists("datos-entrenamiento.csv")== True):
    os.remove("datos-entrenamiento.csv")
recorrer_directorio("papaya-recortes-buenos", listdir("./papaya-recortes-buenos"), "0 1 0")
recorrer_directorio("papaya-recortes-malos",  listdir("./papaya-recortes-malos"), "1 0 0")
recorrer_directorio("papaya-recortes-verdes", listdir("./papaya-recortes-verdes"), "0 0 1" )
