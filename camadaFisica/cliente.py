#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
import re
import binascii

from subprocess import Popen, PIPE
from random import *
def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

def getSize(fileobject):
    fileobject.seek(0,2)
    size = fileobject.tell()
    return size

# Funcao para converter dados ASCII em Binario
def ascii2bin (text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def sendFrame(data,s):
    # Socket para a comunicacao com a camada de rede do server
    msg2bin = ascii2bin(data)



    # Pergunta o tamanho do TMQ
    print 'Asking size of TMQ'
    s.send('Asking size of TMQ')

    # Guardado o valor limite da PDU respondido pelo server
    sizeofPDU = int(s.recv(1024))
    print 'Tamanho da PDU:', sizeofPDU

    sizeofChar = 2


    #Pega o MAC do servidor e Escreve no arquivo
    print host
    if str(host) is not '127.0.0.1': # Caso de uso no local host
        print 'ok'
        pid = Popen(["arp", "-a",host], stdout=PIPE)
    else:
        pid = Popen(["arp", "-a"], stdout=PIPE)
    ms = pid.communicate()[0]
    macServer = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", ms)
    # print 'Mac do Servidor', macServer.group

    # Mac Server Binario
    macS2bin = ascii2bin(macServer.group())

    message = open("mensagem.txt", 'wb')
    message.write(macS2bin)
    message.close()

    #Pega MAC do cliente e Escreve no arquivo
    pid = Popen(["arp", "-a"], stdout=PIPE)
    mc = pid.communicate()[0]
    macClient = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", mc)
    print macClient.group()

    macC2bin = ascii2bin(macClient.group())
    print macC2bin
    message = open("mensagem.txt", 'a')
    message.write("\n")
    message.write(macC2bin)
    message.close()

    #Escreve a mensagem a ser enviada no arquivo
    message = open("mensagem.txt", 'a')
    message.write("\n")
    message.write(msg2bin)
    message.close


    # Intervalo para o envio de arquivo em bytes
    interval = sizeofPDU/sizeofChar
    print interval
    # Leitura do arquivo em binario
    message = open("mensagem.txt", 'rb')

    # Verifica o tamanho do arquivo
    fsize = getSize(message)
    message.seek(0)

    # numero de caracteres no arquivo
    number_chars = fsize + 1

    # Divisao do arquivo em partes e envio do para servidor
    x = 0
    colisao = 5
    i=0
    while(x <= number_chars-interval):

        col = randint(1,5) #tem 20% de chance de colisao

        while(col >= colisao):
            print "Ocorreu colisao"
            time.sleep(3)
            col = randint(0,5)
        message.seek(x)
        x+=interval
        envio = message.read(interval)
        print 'Send',(++i)
        s.send(envio)
        time.sleep(1)

    # envio do restante do arquivo
    message.seek(x)
    if number_chars%interval:
        col = randint(1,5) #tem 20% de chance de colisao

        while(col >= colisao):
            print "Ocorreu colisao"
            time.sleep(3)
            col = randint(0,5)
        print 'Send',(i+1)
        s.send(message.read(number_chars%interval))
    print s.recv(1024)


def reciveFrame(c):

    f = open('resp','wb')
    l = c.recv(1024)
    TMQ = "1000"
    sizeofChar = 2;
    print 'Conectado com o cliente'

    print 'Respondido tamanho do TMQ'
    c.send(TMQ)

    interval = int(TMQ)/int(sizeofChar);
    frame = ''
    # Recebimento dos Quadros
    i=0
    while(1):

        print "Receiving... ", (++i)
        l = c.recv(interval)
        frame += l
        print (l)
        f.write(l)
        if(len(l) < interval):
            break

    print "Done Receiving"
    f.write('\n')
    c.send('Thank you for connecting')
    f.close()
    return frame

# Socket para receber a mensagem da camada de aplicacao
sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.0.4"
port = 7897
sa.bind((host, port))

print 'Conectado com a camada de Aplicacao'
sa.listen(50)
ca, addr = sa.accept()
data = ca.recv(1024).decode("ascii")


host = "127.0.0.1"
port = 8031

socketFF = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketFF.connect((host,port))

sendFrame(data,socketFF)
resp = reciveFrame(socketFF)
# Retira cabecalho e decodifica para mandar para o server
pdu = resp.split('\n')
m = str(pdu[2])
msg2 = decode_binary_string(m)
ca.send(msg2)
