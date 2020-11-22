# RMIT University Vietnam
# Course: COSC2429 Introduction to Programming
# Semester: 2020C
# Assignment: 1 (Problem 1)
# Author: Tuong-Minh Vo (s3877562)
# Created date: 20/11/2020
# Last modified date: 22/11/2020


from turtle import Turtle, Screen
from math import sin, radians


# Color constants, taken from Canvas sample flag outputs using an eyedropper tool
blue = "#001b69"
red = "#c9082a"
white = "#ffffff"
black = "#000000"


def draw_rectangle(pen, x1, y1, x2, y2, fill_color="white", border_color="black", border_width=1):
    """
    Draw a rectangle given 2 opposite vertices
    :param pen: turtle.Turtle object used for drawing
    :param x1: x coordinate of 1st vertex
    :param y1: y coordinate of 1st vertex
    :param x2: x coordinate of 2nd vertex
    :param y2: y coordinate of 2nd vertex
    :param fill_color: Fill color
    :param border_color: Border color
    :param border_width: Border width
    """

    p = pen.clone()
    p.width(border_width)
    p.color(border_color)
    p.fillcolor(fill_color)

    p.penup()
    p.setposition(x1, y1)
    p.pendown()

    p.begin_fill()
    p.setposition(x2, y1)
    p.setposition(x2, y2)
    p.setposition(x1, y2)
    p.setposition(x1, y1)
    p.end_fill()


def draw_polygon(pen, vertices, fill_color="white", border_color="black", border_width=1):
    """
    Draw a polygon given a list of vertices
    :param pen: turtle.Turtle object used for drawing
    :param vertices: List of vertices to be drawn
    :param fill_color: Fill color
    :param border_color: Border color
    :param border_width: Border width
    """

    p = pen.clone()
    p.width(border_width)
    p.color(border_color)
    p.fillcolor(fill_color)

    p.penup()
    p.setposition(vertices[0])
    p.pendown()

    p.begin_fill()
    for i in range(1, len(vertices)):
        p.setposition(vertices[i])
    p.setposition(vertices[0])
    p.end_fill()


def draw_star(pen, xcor, ycor, m, n, radius: int, fill_color="white", border_color="black", border_width=1):
    """
    Draw a regular {m/n} star (non-convex) polygon
    (Schlafli notation - source: https://en.wikipedia.org/wiki/Schl%C3%A4fli_symbol#Regular_polygons_(plane))
    :param pen: turtle.Turtle object used for drawing
    :param xcor: x coordinate of the circumscribed circle center
    :param ycor: y coordinate of the circumscribed circle center
    :param m: vertices
    :param n: number of vertices skipped when drawing each edge
    :param radius: Radius of the circumscribed circle
    :param fill_color: Fill color
    :param border_color: Border color
    :param border_width: Border width
    :return:
    """

    # Mathematical formulae
    inner_angle = 180 - 360 / (m / n)

    # Mathematical formulae
    side_length = 2 * (sin(radians(360 / m)) * radius)

    p = pen.clone()
    p.width(border_width)
    p.color(border_color)
    p.fillcolor(fill_color)

    p.penup()
    p.setposition(xcor, ycor)
    p.setheading(90)
    p.forward(radius)
    p.pendown()

    p.begin_fill()
    p.left(inner_angle / 2 + 180 - inner_angle)
    for i in range(m):
        p.forward(side_length)
        p.left(180 - inner_angle)
    p.end_fill()


class Flag:
    def __init__(self, pen, xcor=0, ycor=0, scale=1.0):
        """
        :param pen turtle.Turtle object used for rendering
        :param xcor x coordinate position (Default 0 - center)
        :param ycor y coordinate position (Default 0 - center)
        :param scale render scale relative to window (Default 1.0 - fit screen)
        """
        self.xcor = xcor
        self.ycor = ycor
        self.scale = scale
        self.pen = pen.clone()

    def draw(self):
        pass  # To be overridden and implemented in children classes


class UKFlag(Flag):
    """
    Render the UK flag
    :param pen turtle.Turtle object used for rendering
    :param xcor x coordinate position (Default 0 - center)
    :param ycor y coordinate position (Default 0 - center)
    :param scale render scale relative to window (Default 1.0 - fit screen)
    """
    def __init__(self, pen, xcor=0, ycor=0, scale=1.0):
        super(UKFlag, self).__init__(pen, xcor, ycor, scale=scale)  # Python 2 backward compatibility syntax
        # super().__init__(self.pen, xcor, ycor)  # Python 3 only syntax

    def draw(self):
        draw_rectangle(self.pen, 0, 0, 50, 20, fill_color=red, border_color=red)


class AustraliaFlag(Flag):
    """
    Render the Australian flag
    :param pen turtle.Turtle object used for rendering
    :param xcor x coordinate position (Default 0 - center)
    :param ycor y coordinate position (Default 0 - center)
    :param scale render scale relative to window (Default 1.0 - fit screen)
    """
    def __init__(self, pen, xcor=0, ycor=0, scale=1.0):
        super(AustraliaFlag, self).__init__(pen, xcor, ycor, scale=scale)  # Python 2 backward compatibility syntax
        # super().__init__(self.pen, xcor, ycor, scale=scale)  # Python 3 only syntax

    def draw(self):
        draw_rectangle(self.pen, 0, 0, 50, 20, fill_color=blue, border_color=blue)


# This program renders either the UK or Australia flag using the Python Turtle graphic module. The user chooses which
# flag is rendered via a console menu
class Application:
    def __init__(self, apptitle):
        # Constants
        self.task_list = [
            "1",  # Draw the UK Flag
            "2",  # Draw the Australia flag
            "3",  # Exit
        ]

        # Variable initializations
        self.task = ""
        self.apptitle = apptitle

    # Initialize Turtle graphic engine
    def __init_gui__(self):
        # Screen initializations
        self.win = Screen()
        self.win.title(self.apptitle)
        self.win.tracer(0)  # Turn off turtle animation for instant rendering, to be used with win.update()

        # Set ratio to 1:2 for accurate UK/Australian flag ratio
        self.win.setup(width=self.win.window_width(), height=self.win.window_width() / 2)

        # Pen initializations
        self.pen = Turtle()
        self.pen.hideturtle()

    # Main loop
    def main(self):
        # Menu loop: Display a console menu in this format:
        #
        #       ***************************
        #       1. Draw UK flag
        #       2. Draw Australia flag
        #       3. Exit
        #       Enter an option (1/2/3):
        #
        # Then execute the task according to user input, display an error message if user input is invalid
        while self.task not in self.task_list:
            print("***************************\n1. Draw UK flag\n2. Draw Australia flag\n3. Exit")
            self.task = input("Enter an option (1/2/3): ")
            if self.task == self.task_list[0]:
                self.__init_gui__()
                self.win.title("United Kingdoms Flag")
                flag = UKFlag(self.pen)
                flag.draw()
                self.win.update()
                self.win.exitonclick()
            elif self.task == self.task_list[1]:
                self.__init_gui__()
                self.win.title("Australia Flag")
                flag = AustraliaFlag(self.pen)
                flag.draw()
                self.win.update()
                self.win.exitonclick()
            elif self.task == self.task_list[2]:
                print("Program exits. Have a nice day!")
            else:
                print("Invalid option")


if __name__ == "__main__":
    app = Application(apptitle="Draw a flag")
    app.main()
