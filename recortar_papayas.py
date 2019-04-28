"""
Aplicacion para extraer un recorte de la imagen donde se encuentra
un tomate.

"""

from __future__ import division
import cv2
import numpy as np
from os import listdir


def mostar(imagen):
    imagen = cv2.resize(imagen, (600, 400))
    cv2.imshow('papaya', imagen)
    cv2.waitKey(0)

"""
    rrecoore el directorio
"""
def recorrer_directorio(carpeta_entrada, carpeta_salida, lista_imagenes):
    for nombre_imagen in lista_imagenes:
        imagen = cv2.imread(carpeta_entrada + "/" +nombre_imagen)
        encontrar = ecnontrar_papaya(imagen)
        cv2.imwrite(carpeta_salida + "/" + nombre_imagen, encontrar)


"""
    Encuentra el contorno de a imagen
"""
def encontar_contorno(imagen):
    imagen = imagen.copy()
    contornos, jerarquia =cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
 
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara

"""
    con los datos encontrados de la imagen en su controno
    se cacula las dimensiones del cuadrdo y su hubicacion
"""

def contorno_rectangulo(imagen, contorno):
    imagenConElipse = imagen.copy()
    elipse = cv2.fitEllipse(contorno)
    factor_redn = 0.5
    sx = int((elipse[1][0]*factor_redn)/2)
    sy = int((elipse[1][1]*factor_redn)/2)
    x = int(elipse[0][0]) - sy
    y = int(elipse[0][1]) - sx
#    img = cv2.ellipse(imagenConElipse,elipse,0,0,180,255,-1)
 #   cv2.imshow('tomate', img)
  #  cv2.waitKey(0)
    #cv2.elipse(imagenConElipse, elipse, green, 2, cv2.LINE_AA)
    #cv2.rectangle(imagenConElipse, (x,y), ((x + sy*2), (y + sx*2)), (255,0,0),2)
    imagenConElipse = imagenConElipse[y:(y + sx*2), x:(x + sy*2)]
    return imagenConElipse

"""
    Trata la imagen para poder encontrar el cuadrado
"""
def ecnontrar_papaya(imagen):
    imagen2 = imagen.copy()
    imagen3 = imagen.copy()
    imagen2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2HSV)
    max_dimension = max(imagen2.shape)
    scale = 700/max_dimension
    imagen2 = cv2.resize(imagen2, None, fx=scale, fy=scale)
    imagen3 = cv2.resize(imagen3, None, fx=scale, fy=scale)
    imagen_azul = cv2.GaussianBlur(imagen2, (7, 7), 0)
    min_rojo = np.array([0, 155, 25])
    max_rojo = np.array([256, 256, 256])

    mascara1 = cv2.inRange(imagen_azul, min_rojo, max_rojo)
   
#    cv2.imshow('papaya', imagen_azul)
 #  cv2.waitKey(0)
  #  cv2.imshow('papaya', mascara1)
  #  cv2.waitKey(0)
    #min_rojo2 = np.array([170, 100, 80])
    #max_rojo2 = np.array([180, 256, 256])

    #mascara2 = cv2.inRange(imagen_azul, min_rojo2, max_rojo2)

    #mascara = mascara1 + mascara2
    mascara = mascara1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mascara_cerrada = cv2.morphologyEx(mascara, cv2.MORPH_CLOSE, kernel)
    mascara_limpia = cv2.morphologyEx(mascara_cerrada, cv2.MORPH_OPEN, kernel)

    contorno_papaya_gramde, mascara_papaya = encontar_contorno(mascara_limpia)

    rectangulo_papaya = contorno_rectangulo(imagen3, contorno_papaya_gramde)
    #rectangulo_tomate = cv2.resize(rectangulo_tomate, (100, 50))
    # recortar(rectangulo_tomate)
    return rectangulo_papaya

recorrer_directorio("papayaBuena", "papaya-recortes-buenos", listdir("./papayaBuena"))
recorrer_directorio("papayaVerde", "papaya-recortes-verdes", listdir("./papayaVerde"))
recorrer_directorio("papayaMalas", "papaya-recortes-malos", listdir("./papayaMalas"))
