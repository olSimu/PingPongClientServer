using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class Partita
{
    Socket a;
    Socket b;
    Partita(Socket a, Socket b)
    {
        this.a = a;
        this.b = b;
    }

}

public class SynchronousSocketListener
{

    // Incoming data from the client.  
    public static string data = null;

    public static void StartListening()
    {


        // Establish the local endpoint for the socket.  
        // Dns.GetHostName returns the name of the   
        // host running the application.  
        IPAddress ipAddress = System.Net.IPAddress.Parse("127.0.0.1");
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, 5000);

        //lista di sockets per gestire le partite
        List <Partita> partita = new List <Partita>();


        // Create a TCP/IP socket.  
        Socket listener = new Socket(ipAddress.AddressFamily,SocketType.Stream, ProtocolType.Tcp);

        Console.WriteLine("Timeout : {0}", listener.ReceiveTimeout);

        // Bind the socket to the local endpoint and   
        // listen for incoming connections.  
        try
        {
            listener.Bind(localEndPoint);
            listener.Listen(10);

            // Start listening for connections.  
            while (true)
            {

                Console.WriteLine("Waiting for a connection...");
                // Program is suspended while waiting for an incoming connection.  
                Socket handler = listener.Accept();
                Socket handler2 = listener.Accept();

                ClientManager clientThread = new ClientManager(handler, 1);
                Thread t = new Thread(new ThreadStart(clientThread.doClient));
                t.Start();

                ClientManager clientThread2 = new ClientManager(handler2, 2);
                Thread t2 = new Thread(new ThreadStart(clientThread2.doClient));
                t2.Start();

            }

        }
        catch (Exception e)
        {
            Console.WriteLine(e.ToString());
        }

        Console.WriteLine("\nPress ENTER to continue...");
        Console.Read();

    }

    public static int Main(String[] args)
    {
        StartListening();
        return 0;
    }


}

public class ClientManager
{

    Socket clientSocket;
    byte[] bytes = new Byte[1024];
    String data = "";
    int role;

    private static List<String> messaggiFrom1=  new List<String>();
    private static List<String> messaggiTo1 = new List<String>();

    private static List<String> messaggiFrom2 = new List<String>();
    private static List<String> messaggiTo2 = new List<String>();

    public ClientManager(Socket clientSocket, int role)
    {
        this.clientSocket = clientSocket;
        this.role = role;
    }

    public void doClient()
    {

        while (data != "Quit$")
        {
            // An incoming connection needs to be processed.  
            data = "";
            while (data.IndexOf("$") == -1)
            {
                int bytesRec = clientSocket.Receive(bytes);
                data += Encoding.ASCII.GetString(bytes, 0, bytesRec);
            }

            // Show the data on the console.  
            Console.WriteLine("Messaggio ricevuto : {0}", data);

            // Echo the data back to the client.  
            byte[] msg = Encoding.ASCII.GetBytes(data);

            clientSocket.Send(msg);
        }
        clientSocket.Shutdown(SocketShutdown.Both);
        clientSocket.Close();
        data = "";

    }
}