"""
Created on Fri Jul 23 10:20:06 2021

@author: https://github.com/marcosmg2096
"""

import telebot
import unidecode
import re
import requests
from bs4 import BeautifulSoup


from config import TOKEN
lista_comandos=('tiempo', 'semana')

chat_id=1267931674
tgbot=telebot.TeleBot(TOKEN)
tgbot.send_message(chat_id, 'Tiempogram iniciado')


@tgbot.message_handler(commands=['comandos'])
def hola(mensaje):
    tgbot.reply_to(mensaje, 'Utiliza un comando de la siguiente lista seguido'''
                            ' de un espacio y el nombre de tu ciudad:\n'''
                            ''+'\n'.join(lista_comandos))

def comprobacion_sitio(mensaje):
    input=mensaje.text.split()
    if len(input)<2 or input[0].lower() not in lista_comandos:
        return False
    else:
        return True

def acomodar(mensaje):      #llama a normalizar y separa en comando y ciudad
    request_sitio=normalizar(mensaje)
    comando_sitio, sitio = request_sitio.split('-', 1)
    return comando_sitio, sitio

def normalizar(sitio):      #pasa a minúscula, cambia espacios por guiones y elimina acentos
    sitio.text=sitio.text.lower()
    sitio.text=sitio.text.replace(' ', '-')
    sitio.text=unidecode.unidecode(sitio.text)
    return sitio.text

def getURL(sitio):          #devuelve la url de la ciudad seleccionada
    url='https://www.tiempo.com/'+sitio+'.htm'
    return url

def getStringTem(url_sitio):
    page=requests.get(url_sitio)
    soup = BeautifulSoup(page.content, 'html.parser')
    resultTemp=soup.find_all('span', class_='temperatura')   #se crea el objeto ResultSet a partir de la clase temperatura en el html de la pagina tiempo.com
    listTemp=[]
    for i in resultTemp:
        listTemp.append(i.text)        #crea la lista a partir del objeto ResultSet de BeautifulSoup
    listTemp=[i.replace(' ','') for i in listTemp]
    return listTemp

def getSitio(url_sitio):
    page=requests.get(url_sitio)
    soupnom = BeautifulSoup(page.content, 'html.parser')
    nomSoup=soupnom.find_all('span', class_='titulo')
    nomSitio=[]
    for i in nomSoup:
        nomSitio.append(i.text)

    inicio=nomSitio[0].find('El tiempo en ')
    fin=nomSitio[0].find(' hoy')

    nombreSitio=nomSitio[0][(inicio+len('El tiempo en ')):(fin)]
    return nombreSitio

def tbot_tiempo(sitio):     #implementación de la función tiempo
    url_sitio=getURL(sitio)
    listTemp=getStringTem(url_sitio)
    nomSitio=getSitio(url_sitio)
    patronTemp=re.compile(r'\d\d°')
    tempSens=patronTemp.findall(listTemp[0])
    resp_tiempo='La temperatura actual en '+nomSitio+' es de '+tempSens[0]+'\nSensación térmica de '+tempSens[1]
    return resp_tiempo

def tbot_polen(sitio):      #implementación de la función polen
    url_sitio=getURL(sitio)
    #resp_polen='El nivel de polen en '+sitio+' es de _\n'
    resp_polen='Función por implementar\n'
    return resp_polen


@tgbot.message_handler(func=comprobacion_sitio)
def responder_comando(mensaje):
    comando_sitio, sitio = acomodar(mensaje)
    if comando_sitio in lista_comandos[0]:
        respuesta=tbot_tiempo(sitio)
    
    elif comando_sitio in lista_comandos[1]:
        respuesta=tbot_polen(sitio)
    else:
        pass
    tgbot.send_message(chat_id, respuesta)
    #tgbot.send_message(chat_id, 'Comando: '+comando_sitio+'\nCiudad: '+sitio)

@tgbot.message_handler(func=lambda message: True)
def echo_all(message):
	tgbot.reply_to(message, 'Usa /comandos para ver los comandos disponibles')

def tiempo_sitio(ciudad):
    pass

tgbot.polling()