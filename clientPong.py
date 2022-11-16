# Simple Pong in Python 3 for Beginners
# By @TokyoEdTech

import os
import socket
import threading
import turtle

import invoke

SERVER = "127.0.0.1"
PORT = 5000
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#False = nessun movimento, True = movimento
#[paddle_a_up, paddle_a_down, paddle_b_up, paddle_b_down]
paddles = [False, False, False, False]
print(paddles)

# Functions
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)


#loop di ricezione dal server
def receiveMessage(paddles):
    while True:
        msg = client.recv(1024).decode(FORMAT)
        print(msg)
        if(msg == "a_up<EOF>"):
            paddles[0] = True
        elif(msg == "a_down<EOF>"):
            paddles[1] = True
        elif(msg == "b_up<EOF>"):
            paddles[2] = True
        elif(msg == "b_down<EOF>"):
            paddles[3] = True
        print(paddles)

#thread di attesa messaggi       
x = threading.Thread(target = receiveMessage, args=[paddles])
x.start()


#msg = str(input())
#client.send(bytes(msg,FORMAT))

wn = turtle.Screen()
wn.title("Pong")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5,stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5,stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.5
ball.dy = 0.5

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))



#socket functions
def socket_paddle_a_up():
    msg = "a_up" + "<EOF>"
    client.send(bytes(msg,FORMAT))
    #paddle_a_up()

def socket_paddle_a_down():
    msg = "a_down" + "<EOF>"
    client.send(bytes(msg,FORMAT))
    #paddle_a_down()

def socket_paddle_b_up():
    msg = "b_up" + "<EOF>"
    client.send(bytes(msg,FORMAT))
    #paddle_b_up()

def socket_paddle_b_down():
    msg = "b_down" + "<EOF>"
    client.send(bytes(msg,FORMAT))
    #paddle_b_down()

# Keyboard bindings
wn.listen()
wn.onkeypress(socket_paddle_a_up, "w")
wn.onkeypress(socket_paddle_a_down, "s")
wn.onkeypress(socket_paddle_b_up, "Up")
wn.onkeypress(socket_paddle_b_down, "Down")



# Main game loop
while True:
    #receiveMessage()
    wn.update()
    
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    #move paddles
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

    # Border checking
    # Top and bottom
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1
        os.system("afplay bounce.wav&")
    
    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1
        os.system("afplay bounce.wav&")

    # Left and right
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

    # Paddle and ball collisions
    if ball.xcor() < -340 and ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50:
        ball.dx *= -1 
        os.system("afplay bounce.wav&")
    
    elif ball.xcor() > 340 and ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50:
        ball.dx *= -1
        os.system("afplay bounce.wav&")
    