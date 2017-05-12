#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time

# Criação do socket e Criação de Conexão do Server
s = socket.socket()
host = "127.0.0.1"
port = 8031
s.bind((host, port))

s.listen(5)
c, addr = s.accept()
f = open('resp','wb')
l = c.recv(1024)
TMQ = "1000"
sizeofChar = 2;
print 'Conectado com o cliente'

print 'Respondido tamanho do TMQ'
c.send(TMQ)

interval = int(TMQ)/int(sizeofChar);

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
s.close()
