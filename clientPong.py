import socket
import threading
import turtle

# configurazione finestra e componenti
# finestra
wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("green")
wn.setup(width=725, height=600)
wn.tracer(0)

# punteggio
global score_a
global scor_b
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5,stretch_len=0.7)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5,stretch_len=0.7)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.5
ball.dy = 0.5


# Pen(il testo in alto)
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Indirizzo IP e numero di porta di deault 
SERVER = "127.0.0.1"
PORT = 5000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
# Creazione socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# False = nessun movimento, True = movimento
# [paddle_a_up, paddle_a_down, paddle_b_up, paddle_b_down]
paddles = [False, False, False, False]
gameloop = [False]
synCoor = [False]

# Input indirizzo IP e porta
SERVER = turtle.textinput("Pong", "indirizzo ip")
PORT = turtle.textinput("Pong", "porta")

# Funzioni di movimento delle paddle
def paddle_a_up():
    y = paddle_a.ycor()
    y += 40
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 40
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 40
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 40
    paddle_b.sety(y)


# Fuzioni di invio messaggio di movimetno tramite socket
def socket_paddle_a_up():
    if paddle_a.ycor() <= 220:
        msg = "a_up" + "$"
        client.send(bytes(msg,FORMAT))

def socket_paddle_a_down():
    if paddle_a.ycor() >= -220:
        msg = "a_down" + "$"
        client.send(bytes(msg,FORMAT))

def socket_paddle_b_up():
    if paddle_b.ycor() <= 220:
        msg = "b_up" + "$"
        client.send(bytes(msg,FORMAT))

def socket_paddle_b_down():
    if paddle_b.ycor() >= -220:
        msg = "b_down" + "$"
        client.send(bytes(msg,FORMAT))

# Configurazione comandi tastiera
wn.listen()
wn.onkeypress(socket_paddle_a_up, "w")
wn.onkeypress(socket_paddle_a_down, "s")
wn.onkeypress(socket_paddle_b_up, "Up")
wn.onkeypress(socket_paddle_b_down, "Down")

# Loop di ricezione dal server (gestito da thread)
def receiveMessage(paddles, gameloop, synCoor):
    while True:
        msg = client.recv(1024).decode(FORMAT)
        msgDollarSplit = msg.split('$')
        msg = msgDollarSplit[0]
        if(msg == "a_up"):
            paddles[0] = True
        elif(msg == "a_down"):
            paddles[1] = True
        elif(msg == "b_up"):
            paddles[2] = True
        elif(msg == "b_down"):
            paddles[3] = True
        elif(msg == "startGame"):
            gameloop[0] = True
        elif(msg == "stopGame"):
            gameloop[0] = False     
        elif(msg == "SYN"):
            msg = "SYN;" + str(ball.xcor()) + ";" + str(ball.ycor()) + ";" + str( ball.dx) + ";" + str(ball.dy) + ";" + str(score_a)  +"$"
            client.send(bytes(msg,FORMAT))
        elif(msg.split(';')[0] == "COOR"):
            global msgSplit 
            msgSplit = msg.split(';')
            synCoor[0] = True
            
# Thread di attesa messaggi       
x = threading.Thread(target = receiveMessage, args=(paddles, gameloop, synCoor))
x.start()


# Main game loop
while True:
    wn.update()
     
    if gameloop[0]:
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        if synCoor[0] == True:
            ball.goto(float(msgSplit[1]), float(msgSplit[2]))
            ball.dx = float(msgSplit[3])
            ball.dy = float(msgSplit[4])
            synCoor[0] = False

        # Movimento paddle
        if paddles[0] == True:
            paddle_a_up()
            paddles[0] = False
        elif paddles[1] == True:
            paddle_a_down()
            paddles[1] = False
        elif paddles[2] == True:
            paddle_b_up()
            paddles[2] = False
        elif paddles[3] == True:
            paddle_b_down()
            paddles[3] = False

        # Controlli bordi
        # Sopra e sotto
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
        elif ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        # Destra e sinistra
        if ball.xcor() > 350:
            score_a += 1
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
            ball.goto(0, 0)
            ball.dx *= -1

        elif ball.xcor() < -350:
            score_b += 1
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))
            ball.goto(0, 0)
            ball.dx *= -1

        # Collisione pallina con paddle
        if ball.xcor() < -340 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50:
            ball.dx *= -1 
        
        elif ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
            ball.dx *= -1

        # Controllo Vincita
        if score_a >= 5:
            gameloop[0] = False
            pen.clear()
            pen.write("Ha vinto il Player A!",  align="center", font=("Courier", 24, "normal"))
            client.shutdown(socket.SHUT_RDWR)
            client.close()

        if score_b >= 5:
            gameloop[0] = False
            pen.clear()
            pen.write("Ha vinto il Player B!",  align="center", font=("Courier", 24, "normal"))
            client.shutdown(socket.SHUT_RDWR)
            client.close()
    