require "socket"
host = "localhost"
port = 2008
socket = TCPServer.new host,port
# request = "GET / HTTP/1.1\r\nHost:#{host}\r\n\r\n"
session = socket.accept
# session.print request
session.print(File.read('template.html'))
session.close_write
print session.read
# response = socket.read
