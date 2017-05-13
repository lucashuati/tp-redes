#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time

# Criação do socket e Criação de Conexão do Server
s = socket.socket()
host = "127.0.0.1"
port = 8030
s.bind((host, port))

f = open('resp','wb')
s.listen(5)
c, addr = s.accept()

# Negociação da TMQ
TMQ = "6"
szChar = "2"

c.send(TMQ)
time.sleep(1)
c.send(szChar)

interval = int(TMQ)/int(szChar)

print 'Got connection from', addr

# Recebimento dos Quadros
while(1):
    print "Receiving..."
    l = c.recv(interval)
    print (l)
    f.write(l)
    if(len(l) == 0):
        break

print "Done Receiving"
f.write('\n')
c.send('Thank you for connecting')
f.close()
c.close()
