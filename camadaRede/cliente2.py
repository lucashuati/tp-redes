import socket
import time
import re
import binascii

from subprocess import Popen, PIPE
from random import *

def getSize(fileobject):
    fileobject.seek(0,2)
    size = fileobject.tell()
    return size

# Funcao para converter dados ASCII em Binario
def ascii2bin (text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Socket para receber a mensagem da camada de aplicacao
sa = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8029
sa.bind((host, port))

sa.listen(1)
ca, addr = sa.accept()
data = ca.recv(1024).decode("ascii")
print data
print 'Conectado com a camada de Aplicacao'


# Socket para a comunicacao com a camada de rede do server
msg2bin = ascii2bin(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 8031
s.connect((host, port))

# Pergunta o tamanho do TMQ
print 'Asking size of TMQ'
s.send('Asking size of TMQ')

# Guardado o valor limite da PDU respondido pelo server
sizeofPDU = int(s.recv(1024))
print 'Tamanho da PDU:', sizeofPDU

sizeofChar = 2


#Pega o MAC do servidor e Escreve no arquivo
if host is not "127.0.0.1": # Caso de uso no local host
    pid = Popen(["arp", "-a", host], stdout=PIPE)
else:
    pid = Popen(["arp", "-a"], stdout=PIPE)
ms = pid.communicate()[0]
macServer = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", ms)
print 'Mac do Servidor', macServer.group

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
while(x <= number_chars-interval):

    col = randint(1,5) #tem 20% de chance de colisao

    while(col >= colisao):
	print "Ocorreu colisao"
    	time.sleep(3)
	col = randint(0,5)
    message.seek(x)
    x+=interval
    envio = message.read(interval)
    print envio
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
    print message.read(number_chars%interval)
    s.send(message.read(number_chars%interval))



print "Done Sending"
n = int(msg2bin, 2)
msg2 = binascii.unhexlify('%x' % n)
print msg2
s.close


# Socket para enviar a mensagem da camada de aplicacao

print 'Conectado com a camada de Aplicacao'
f = open('http.txt', 'r')
print f.read()
ca.close
sa.close
