require 'socket'

Port_phy_conn = 8031
Port_tra_conn = 8035

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

# table.each do |test|
# 	puts test
# end


socket_1 = TCPServer.new(Host,Port_tra_conn)

puts "waiting..."


loop{
	Thread.start(socket_1.accept) do |client|
		puts "Connected with layer"

		packet = client.recv(1024)

		destination = packet[/Host: (.*):/, 1]

		dest_is_in_table = false 

		table.each do |ip_dest|
			if ip_dest = destination
				dest_is_in_table = true
			end
		end 

		if dest_is_in_table = false
			puts "Ip not in the router table! check Ip"
			continue 
		end 

		socket_2 = TPCSocket.new(Host,Port_phy_conn)

		puts "Connected with destination"

		socket_2.write(packet + "\n")

		puts "message sent to destination"

		packet2 = socket_2.recv(1024)

		client.write(packet2 + "\n") #message resent to origin

	end
}