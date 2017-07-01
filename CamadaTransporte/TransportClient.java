import java.net.*;
import java.io.*;
import java.util.*;
import java.util.zip.CRC32;

public class TransportClient {
  static int appPort = 7899;
  static int appPort2 = 7502, appPort3 = 7123;
  static ServerSocket socketAppTrans, socketTransFisFDP, vem;
  static Socket client, clientF, socketTransFis, socketAppTransEnvioFDP,sos;
  public static String makeUDPHeader(String data) throws SocketException{
      byte[] bytemsg = data.getBytes();
      CRC32 crc = new CRC32();
      crc.update(bytemsg);
      String source, destination, length, checksum, header;
      source = socketAppTrans.getInetAddress().toString();
      destination = client.getInetAddress().toString();
      length =  String.valueOf(client.getReceiveBufferSize());
      checksum = String.valueOf(crc.getValue());
      System.out.println("Source IP: " + source);
      System.out.println("Destination IP: " + destination);
      System.out.println("Length: " + length);
      System.out.println("Checksum: " + checksum);
      header = source + destination + length + checksum;
      System.out.println(source.getBytes()[0]);
      return header;
  }

  public static void main(String[] args) throws UnknownHostException, IOException {
    
    String segment;
    
    // Make a connection
    socketAppTrans = new ServerSocket(appPort);
    client = socketAppTrans.accept();	

    // Get a http request
    Scanner socketData = new Scanner(client.getInputStream());
    String data = socketData.nextLine();

    System.out.println(data);
    // Make a Transport Header
    segment = makeUDPHeader(data);

    socketTransFis = new Socket("127.0.0.1", appPort2);
    DataOutputStream outToNet = new DataOutputStream(socketTransFis.getOutputStream()); 	
    outToNet.writeBytes(data);
    outToNet.close(); 	
 	  
    
    vem = new ServerSocket(appPort3); 
    clientF = vem.accept();
    System.out.println("COLEI");
    Scanner volta = new Scanner(clientF.getInputStream());
    String y = volta.nextLine() + "\n";
    int flag = 1;

    while(volta.hasNextLine()) {
        
        // if(flag){
        //   String[] parts = y.split("OK");
        //   y += parts[0] + "\n" + parts[]
        // }
        // else{
        y += volta.nextLine() + "\n";
        // }

    }
    System.out.print(y);
    socketAppTransEnvioFDP = new Socket("127.0.0.1", appPort);
    PrintWriter outToNets = new PrintWriter(client.getOutputStream());   
    outToNets.print(y);  
    outToNets.flush();
    outToNets.close();
    // socketTransFisFDP.close();
    // socketAppTransEnvioFDP.close();
  }
}
