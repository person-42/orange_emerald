def run_art():
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
    except ValueError:
        zoom=50
    guy = turtle.Turtle()
    face = turtle.Turtle()
    try:
        screen.bgcolor(space)
    except turtle.TurtleGraphicsError:
        screen.bgcolor("black")
    try:
        guy.pencolor(front)
    except turtle.TurtleGraphicsError:
        guy.pencolor("green")
    screen.tracer(0)
    try:
        face.pencolor(back)
    except turtle.TurtleGraphicsError:
        face.pencolor("red")
    guy.speed("fastest")
    face.speed("fastest")
    screen.title("ART")
    f = 3
    guy.hideturtle()
    def update():
        global screen
        screen.update()
    screen.listen()
    face.hideturtle()
    screen.listen()
    trtr=False
    def out():
        global trtr
        trtr=True
    screen.onkey(out,"x")
    while True:
        try:
            for a in range(f):
                guy.left( 360 / f)
                face.right( 360 / f )
                guy.fd(zoom)
                face.fd(zoom)
                if f % 100 == 0 :
                    update()
            f += 1
            if trtr:
                break
        except _tkinter.TclError:
            break
