#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time

# Socket para receber a mensagem da camada de aplicacao
sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 7897
sa.connect((host, port))

print 'Conectado com a camada de Aplicacao'
f = open('http.txt', 'r')
msg = f.read()
msg = msg + '\r\n\r\n'
print msg

sa.send(msg);

data = sa.recv(1024)
print 's'
print data
print 'Conectado com a camada de Aplicacao'
