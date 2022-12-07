using System.Net;
using System.Net.Sockets;
using System.Text;

public class SynchronousSocketListener
{

    // Dati provenienti dal client  
    public static string data = null;

    public static void StartListening()
    {
        // Indirizzo ip e numero di porta di default
        string tempIP = "127.0.0.1";
        int tempPort = 5000;
        string tempPortStr;

        // Impostazione indirizzi
        Console.WriteLine("Indirizzo IP di default: {0}", tempIP);
        Console.WriteLine("Porta di default: {0}", tempPort);

        Console.WriteLine("Nuovo indirizzo IP: ");
        tempIP = Console.ReadLine();
        if (tempIP == "")
            tempIP = "127.0.0.1";

        Console.WriteLine("Nuova porta: ");
        tempPortStr = Console.ReadLine();
        if (tempPortStr == "")
            tempPort = 5000;
        else
            tempPort = int.Parse(tempPortStr);

        Console.WriteLine("Indirizzo IP: {0}", tempIP);
        Console.WriteLine("Porta: {0}", tempPort);

        // Assegnazione indirizzi al seerver
        IPAddress ipAddress = System.Net.IPAddress.Parse(tempIP);
        IPEndPoint localEndPoint = new IPEndPoint(ipAddress, tempPort);

        // crea la socket TCP/IP   
        Socket listener = new Socket(ipAddress.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

        // Lega la socket al Endpoint locale e  
        // ascolta le connessioni in entrata
        try
        {
            listener.Bind(localEndPoint);
            listener.Listen(10);

            // Inizia ad ascoltare le connessioni
            while (true)
            {
                // Il programma è sospeso durante l'attesa di una connessione in entrata
                Console.WriteLine("Aspettando il primo player...");
                Socket handler = listener.Accept();
                Console.WriteLine("Aspettando il secondo player...");
                Socket handler2 = listener.Accept();

                // Avvia il Thread che gestitsce il primo Client
                ClientManager clientThread = new ClientManager(handler, handler2);
                Thread t = new Thread(new ThreadStart(clientThread.doClient));
                t.Start();
                Console.WriteLine("Player 1 partito");

                // Avvia il Thread che gestitsce il secondo Client
                ClientManager clientThread2 = new ClientManager(handler2, handler);
                Thread t2 = new Thread(new ThreadStart(clientThread2.doClient));
                t2.Start();
                Console.WriteLine("Player 2 partito");

                // Avvia il Thread che si occupa della sincronizzazione
                // dei due Client
                Thread SYN = new(new ThreadStart(clientThread.syncronise));
                SYN.Start();




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
    Socket clientSocket2;
    byte[] bytes = new Byte[1024];
    String data = "";


    public ClientManager(Socket clientSocket, Socket clientSocket2)
    {
        this.clientSocket = clientSocket;
        this.clientSocket2 = clientSocket2;
    }

    //metodo che manda un messaggio di sincronizzazione al client1
    public void syncronise()
    {

        byte[] msg;
        while (true)
        {
            Thread.Sleep(500);
            data = "SYN$";
            msg = Encoding.ASCII.GetBytes(data);
            clientSocket.Send(msg);
            data = "";
        }
    }

    public void doClient()
    {
        // Avvia la partita sul Client dopo 5 Secondi
        Thread.Sleep(5000);
        byte[] msg = Encoding.ASCII.GetBytes("startGame$");
        clientSocket.Send(msg);

        while (data != "Quit$")
        {
            // An incoming connection needs to be processed.  
            data = "";
            while (data.IndexOf("$") == -1)
            {
                int bytesRec = clientSocket.Receive(bytes);
                data += Encoding.ASCII.GetString(bytes, 0, bytesRec);
            }

            // mostra il messaggio ricevuto a console 
            Console.WriteLine("Messaggio ricevuto : {0}", data);
            string[] ss = data.Split(';');
            if (ss[0] == "SYN")
            {
                data = "COOR" + ";" + ss[1] + ";" + ss[2] + ";" + ss[3] + ";" + ss[4];
            }
            // risponde con un messaggio al client  
            msg = Encoding.ASCII.GetBytes(data);
            clientSocket.Send(msg);
            clientSocket2.Send(msg);

        }
        //chiude la connessiome
        clientSocket.Shutdown(SocketShutdown.Both);
        clientSocket.Close();
        data = "";

    }
}

