require 'socket'
include Socket::Constants

Port_phy_conn = 8040
Port_tra_conn = 7502
Destination = "172.16.17.143"
Host = '127.0.0.1'
#Making connectio via socket

puts "Quantas redes farao parte da tabela de roteamento"
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
		puts packet
		puts "So vai ou nao "

		dest_is_in_table = false 

		table.each do |ip_dest|
			if ip_dest == Destination
				dest_is_in_table = true
			end
		end 

		if dest_is_in_table == false
			puts "Ip not in the router table! check Ip"
			continue 
		end 

		socket_2 = Socket.new(AF_INET, SOCK_STREAM, 0)
		socketaddr = Socket.pack_sockaddr_in(Port_phy_conn, Host)
		socket_2.connect(socketaddr)

		puts "Connected with destination"

		socket_2.write(packet)

		puts "message sent to destination"

		packet2 = socket_2.recv(1024)

		client.write(packet2) #message resent to origin

	end
}