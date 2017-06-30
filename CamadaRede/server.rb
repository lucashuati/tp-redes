require 'socket'

Port_phy_conn = 7897
Port_tra_conn = 7899

Host = '127.0.0.1'
#Making connectio via socket

puts "Quantas redes farão parte da tabela de roteamento"
x = gets.chomp
y = x.to_i
table = []
#Get Router Table  
while y > 0 do 
	puts "digite o ip desejado"
	ip_typed = gets.chomp 
	table.push(ip_typed)
	y = y - 1
end



connection = TCPServer.new(Host,Port_phy_conn)

puts "waiting..."


loop{
	Thread.start(connection.accept) do |client|
		puts "Connected with layer"

		packet = client.recv(1024)

		connection_2 = TCPSocket.new(Host,Port_tra_conn)

		puts "Connected with destination"

		connection_2.write(packet + "\n")

		puts "Message sent"

		packet_2 = connection_2.recv(1024)

		client.write(packet_2)

	end


}