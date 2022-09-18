import turtle

count1 = 6
count2 = 6
gap = 0

while( count1 > 0 ):
    gap += 100
    turtle.forward(500)
    turtle.penup()
    turtle.goto(0, gap)
    turtle.pendown()
    count1 -= 1

gap = 0

turtle.penup()
turtle.goto(0, 0)
turtle.pendown()
turtle.left(90)

while(count2 > 0):
    gap += 100
    turtle.forward(500)
    turtle.penup()
    turtle.goto(gap, 0)
    turtle.pendown()
    count2 -= 1

turtle.exitonclick()