import java.net.*;
import java.io.*;
import java.util.*;
import java.util.zip.CRC32;

public class TransportClient {
  static int appPort = 5033;
  static int appPort2 = 7897;
  static ServerSocket socketAppTrans;
  static Socket client;
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
    // Make a connection
    socketAppTrans = new ServerSocket(appPort);
    client = socketAppTrans.accept();

    // Get a http request
    Scanner socketData = new Scanner(client.getInputStream());
    String data = socketData.nextLine();

    // Make a Transport Header
    makeUDPHeader(data);


    socketAppTrans.close();
  }
}
