def run():
    import turtle
    import _tkinter
    screen = turtle.Screen()
    space = screen.textinput(title = "COLOR" , prompt = "enter space color:")
    back = screen.textinput(title = "COLOR" , prompt = "enter bottom color:")
    front = screen.textinput( "COLOR" , "enter top color:")
    try:
        zoom = int(screen.textinput("ZOOM" , "enter zoom level:"))
        if zoom < 20:
            zoom=20
    except:
        zoom=50
    guy = turtle.Turtle()
    face = turtle.Turtle()
    try:
        screen.bgcolor(space)
    except :
        screen.bgcolor("black")
    try:
        if front=="":
            front = "green"
        guy.pencolor(front)
    except :
        guy.pencolor("green")
    screen.tracer(0)
    try:
        if back=="":
            back = "red"
        face.pencolor(back)
    except :
        face.pencolor("red")
    guy.speed("fastest")
    face.speed("fastest")
    screen.title("ART")
    f = 3
    guy.hideturtle()
    screen.listen()
    face.hideturtle()
    screen.listen()
    trtr=True
    def out():
        global trtr, guy
        trtr=False
    screen.onkey(out,"x")
    while trtr:
        try:
            for a in range(f):
                guy.left( 360 / f)
                face.right( 360 / f )
                guy.fd(zoom)
                face.fd(zoom)
                if f % 100 == 0 :
                    screen.update()
            f += 1
        except _tkinter.TclError:
            del guy
            del face
            del screen
            break

if __name__ == "__main__":
    run()
    run()