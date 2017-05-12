require "socket"

webserver = TCPServer.new('localhost', 2008) # criando o web server
contents = File.read('template.html') # lendo o template do web server

while (session = webserver.accept)
  print webserver.accept
  session.print(contents)
  session.close
end
