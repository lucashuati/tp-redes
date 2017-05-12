import socket
import time
import re
import binascii

from subprocess import Popen, PIPE
from random import *

# Funcao para descobrir o tamanho do arquivo em bytes
def getSize(fileobject):
    fileobject.seek(0,2)
    size = fileobject.tell()
    return size

# Funcao para converter dados ASCII em Binario
def ascii2bin (text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Socket para comunicao com a camada de aplicacao

app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8045
app_socket.bind((host, port))

app_socket.listen(2)
application_msg, application_addr = app_socket.accept()
data = application_msg.recv(1024).decode("ascii")

app_socket.close
# Socket para comunicao com sevidor
net_socket = socket.socket()
host = "127.0.0.1"
port = 8030

net_socket.connect((host, port))


# Pergunta ao Server o tamanho do quadro
print 'Asking size of TMQ'

# Guardado o valor limite da PDU respondido pelo server
sizeofPDU = int(net_socket.recv(1024))
print sizeofPDU
sizeofChar = int(net_socket.recv(1024))
print sizeofChar

#Mensagem a ser enviada para o servidor
msg2bin = ascii2bin(data)

#Pega o MAC do servidor e Escreve no arquivo
if host is not "127.0.0.1":
    pid = Popen(["arp", "-a", host], stdout=PIPE)
else:
    pid = Popen(["arp", "-a"], stdout=PIPE)
ms = pid.communicate()[0]
macServer = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", ms)
print macServer

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

net_socket.close
