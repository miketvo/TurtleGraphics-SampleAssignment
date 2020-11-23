# RMIT University Vietnam
# Course: COSC2429 Introduction to Programming
# Semester: 2020C
# Assignment: 1 (Problem 1)
# Author: Tuong-Minh Vo (s3877562)
# Created date: 20/11/2020
# Last modified date: 22/11/2020


from turtle import Turtle, Screen
from math import sin, radians, sqrt


# Flag colors
# Sources:
# - https://www.fotw.info/flags/gb_col.html#col
# - https://www.fotw.info/flags/au'.html#col
# There are differences in the shades of red and blue between the United Kingdom flag comparing to that of other
# commonwealth nations due to historical color drifting
uk_blue = "#012169"  # Pantone 280 C
uk_red = "#c8102e"  # Pantone 186 C
australian_blue = "#00205b"  # Pantone 281 C
australian_red = "#e4002b"  # Pantone 185 C
white = "#ffffff"  # Pantone SAFE
bgcolor = "#000000"  # Default window background color
debug_color = "#f420e9"  # Ugly purple for debug purposes


class Rectangle:
    def __init__(self, pen, x1, y1, x2, y2, fill_color="white", border_color="black", border_width=1):
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
        self.p = pen.clone()
        self.p.width(border_width)
        self.p.color(border_color)
        self.p.fillcolor(fill_color)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self):
        self.p.penup()
        self.p.setposition(self.x1, self.y1)
        self.p.pendown()

        self.p.begin_fill()
        self.p.setposition(self.x2, self.y1)
        self.p.setposition(self.x2, self.y2)
        self.p.setposition(self.x1, self.y2)
        self.p.setposition(self.x1, self.y1)
        self.p.end_fill()


class Polygon:
    def __init__(self, pen, vertices, fill_color="white", border_color="black", border_width=1):
        """
        Draw a polygon given a list of vertices
        :param pen: turtle.Turtle object used for drawing
        :param vertices: List of vertices to be drawn
        :param fill_color: Fill color
        :param border_color: Border color
        :param border_width: Border width
        """
        if len(vertices) < 3:
            raise ValueError("Polygon object requires 3 or more vertices")

        self.p = pen.clone()
        self.p.width(border_width)
        self.p.color(border_color)
        self.p.fillcolor(fill_color)
        self.vertices = vertices

    def draw(self):
        self.p.penup()
        self.p.setposition(self.vertices[0])
        self.p.pendown()

        self.p.begin_fill()
        for i in range(len(self.vertices)):
            self.p.setposition(self.vertices[i])
        self.p.setposition(self.vertices[0])
        self.p.end_fill()


class Star:
    def __init__(self, pen, xcor, ycor, m, n, radius: int, fill_color="white", border_color="black", border_width=1):
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
        self.p = pen.clone()
        self.p.width(border_width)
        self.p.color(border_color)
        self.p.fillcolor(fill_color)

        self.xcor = xcor
        self.ycor = ycor
        self.m = m
        self.n = n
        self.radius = radius

    def draw(self):
        # Mathematical formulae
        inner_angle = 180 - 360 / (self.m / self.n)

        # Mathematical formulae
        side_length = 2 * (sin(radians(360 / self.m)) * self.radius)

        self.p.penup()
        self.p.setposition(self.xcor, self.ycor)
        self.p.setheading(90)
        self.p.forward(self.radius)
        self.p.pendown()

        self.p.begin_fill()
        self.p.left(inner_angle / 2 + 180 - inner_angle)
        for i in range(self.m):
            self.p.forward(side_length)
            self.p.left(180 - inner_angle)
        self.p.end_fill()


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
        self.scr = pen.getscreen()

    def draw(self):
        pass  # To be overridden and implemented in children classes


class UKFlag(Flag):
    """
    Render the UK flag (Union Jack) using its default shades of red and blue or different shades in case of derivative
    flags i.e. Australia, New Zealand,... so this class can be used as a component of flags derived from the Union Jack.
    Flag construction follows this document: http://www.jdawiseman.com/papers/union-jack/union-jack.html
    :param pen turtle.Turtle object used for rendering
    :param xcor x coordinate position (Default 0 - center)
    :param ycor y coordinate position (Default 0 - center)
    :param scale render scale relative to window (Default 1.0 - fit screen)
    :param blue specify a shade of blue to use instead of the default Pantone 260 C
    :param red specify a shade of red to use instead of the default Pantone 186 C
    """
    def __init__(self, pen, xcor=0, ycor=0, scale=1.0, blue=uk_blue, red=uk_red):
        super(UKFlag, self).__init__(pen, xcor, ycor, scale=scale)  # Python 2 backward compatibility syntax
        # super().__init__(self.pen, xcor, ycor)  # Python 3 only syntax
        self.blue = blue
        self.red = red

        # Ratio between height and width for UK flag
        self.ratio = 1 / 2
        # Set ratio to 1:2 for accurate UK flag ratio
        self.scr.setup(width=self.scr.window_width(), height=self.scr.window_width() * self.ratio)

        # Flag components
        self.background = Rectangle(
            self.pen,
            self.xcor - (self.scr.window_width() / 2) * self.scale,
            self.ycor + (self.scr.window_height() / 2) * self.scale,
            self.xcor + (self.scr.window_width() / 2) * self.scale,
            self.ycor - (self.scr.window_height() / 2) * self.scale,
            fill_color=blue, border_color=blue
        )
        self.standrew_cross_downslash = Polygon(
            self.pen,
            [
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2 * (1 - sqrt(11.25) / 15)) * self.scale
                ),
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor - (self.scr.window_width() / 2 * (1 - sqrt(5) / 10)) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2 * (1 - sqrt(11.25) / 15)) * self.scale
                ),
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor + (self.scr.window_width() / 2 * (1 - sqrt(5) / 10)) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                )
            ],
            fill_color=white, border_color=white
        )
        self.standrew_cross_upslash = Polygon(
            self.pen,
            [
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2 * (1 - sqrt(11.25) / 15)) * self.scale
                ),
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor + (self.scr.window_width() / 2 * (1 - sqrt(5) / 10)) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2 * (1 - sqrt(11.25) / 15)) * self.scale
                ),
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor - (self.scr.window_width() / 2 * (1 - sqrt(5) / 10)) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                )
            ],
            fill_color=white, border_color=white
        )
        self.stpatrick_cross_upperleft = Polygon(
            self.pen,
            [
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2 * (1 - (2 / 3) * sqrt(11.25) / 15)) * self.scale
                ),
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor,
                    self.ycor
                ),
                (
                    self.xcor - (self.scr.window_width() / 2 * ((2 / 3) * sqrt(5) / 10)) * self.scale,
                    self.ycor
                )
            ],
            fill_color=red, border_color=red
        )
        self.stpatrick_cross_upperright = Polygon(
            self.pen,
            [
                (
                    self.xcor + (self.scr.window_width() / 2 * (1 - ((2 / 3) * sqrt(5)) / 10)) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor + (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor,
                    self.ycor
                ),
                (
                    self.xcor - (self.scr.window_width() / 2 * ((2 / 3) * sqrt(5) / 10)) * self.scale,
                    self.ycor
                )
            ],
            fill_color=red, border_color=red
        )
        self.stpatrick_cross_lowerright = Polygon(
            self.pen,
            [
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor,
                    self.ycor
                ),
                (
                    self.xcor + (self.scr.window_width() / 2 * ((2 / 3) * sqrt(5) / 10)) * self.scale,
                    self.ycor
                ),
                (
                    self.xcor + (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2 * (1 - (2 / 3) * sqrt(11.25) / 15)) * self.scale
                )
            ],
            fill_color=red, border_color=red
        )
        self.stpatrick_cross_lowerleft = Polygon(
            self.pen,
            [
                (
                    self.xcor - (self.scr.window_width() / 2) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                ),
                (
                    self.xcor,
                    self.ycor
                ),
                (
                    self.xcor + (self.scr.window_width() / 2 * ((2 / 3) * sqrt(5) / 10)) * self.scale,
                    self.ycor
                ),
                (
                    self.xcor - (self.scr.window_width() / 2 * (1 - (2 / 3) * sqrt(5) / 10)) * self.scale,
                    self.ycor - (self.scr.window_height() / 2) * self.scale
                )
            ],
            fill_color=red, border_color=red
        )
        self.stgeorge_cross_fimbriation_vertical = Rectangle(
            self.pen,
            self.xcor - (self.scr.window_width() / 2) * self.scale * (1 / 6),
            self.ycor + (self.scr.window_height() / 2) * self.scale,
            self.xcor + (self.scr.window_width() / 2) * self.scale * (1 / 6),
            self.ycor - (self.scr.window_height() / 2) * self.scale,
            fill_color=white, border_color=white
        )
        self.stgeorge_cross_fimbriation_horizontal = Rectangle(
            self.pen,
            self.xcor - (self.scr.window_width() / 2) * self.scale,
            self.ycor + (self.scr.window_height() / 2) * self.scale * (1 / 3),
            self.xcor + (self.scr.window_width() / 2) * self.scale,
            self.ycor - (self.scr.window_height() / 2) * self.scale * (1 / 3),
            fill_color=white, border_color=white
        )
        self.stgeorge_cross_vertical = Rectangle(
            self.pen,
            self.xcor - (self.scr.window_width() / 2) * self.scale * (1 / 10),
            self.ycor + (self.scr.window_height() / 2) * self.scale,
            self.xcor + (self.scr.window_width() / 2) * self.scale * (1 / 10),
            self.ycor - (self.scr.window_height() / 2) * self.scale,
            fill_color=red, border_color=red
        )
        self.stgeorge_cross_horizontal = Rectangle(
            self.pen,
            self.xcor - (self.scr.window_width() / 2) * self.scale,
            self.ycor + (self.scr.window_height() / 2) * self.scale * (2 / 10),
            self.xcor + (self.scr.window_width() / 2) * self.scale,
            self.ycor - (self.scr.window_height() / 2) * self.scale * (2 / 10),
            fill_color=red, border_color=red
        )

    def draw(self):
        self.background.draw()

        # Cross of Saint Andrew
        self.standrew_cross_downslash.draw()
        self.standrew_cross_upslash.draw()

        # Cross of Saint Patrick
        self.stpatrick_cross_upperleft.draw()
        self.stpatrick_cross_upperright.draw()
        self.stpatrick_cross_lowerright.draw()
        self.stpatrick_cross_lowerleft.draw()

        # Cross of Saint George (with white fimbriation)
        self.stgeorge_cross_fimbriation_vertical.draw()
        self.stgeorge_cross_fimbriation_horizontal.draw()
        self.stgeorge_cross_vertical.draw()
        self.stgeorge_cross_horizontal.draw()


class AustraliaFlag(Flag):
    """
    Render the Australian flag
    Construction template: https://en.wikipedia.org/wiki/Flag_of_Australia#/media/File:Flag_of_Australia_template.svg
    :param pen turtle.Turtle object used for rendering
    :param xcor x coordinate position (Default 0 - center)
    :param ycor y coordinate position (Default 0 - center)
    :param scale render scale relative to window (Default 1.0 - fit screen)
    """
    def __init__(self, pen, xcor=0, ycor=0, scale=1.0):
        super(AustraliaFlag, self).__init__(pen, xcor, ycor, scale=scale)  # Python 2 backward compatibility syntax
        # super().__init__(self.pen, xcor, ycor, scale=scale)  # Python 3 only syntax

        # Ratio between height and width for Australian flag
        self.ratio = 1 / 2
        # Set ratio to 1:2 for accurate Australian flag ratio
        self.scr.setup(width=self.scr.window_width(), height=self.scr.window_width() * self.ratio)

        self.background = Rectangle(
            self.pen,
            self.xcor - (self.scr.window_width() / 2) * self.scale,
            self.ycor + (self.scr.window_height() / 2) * self.scale,
            self.xcor + (self.scr.window_width() / 2) * self.scale,
            self.ycor - (self.scr.window_height() / 2) * self.scale,
            fill_color=australian_blue, border_color=australian_blue
        )
        self.canton = UKFlag(
            self.pen,
            xcor=self.xcor - (self.scr.window_width() / 4) * self.scale,
            ycor=self.ycor + (self.scr.window_height() / 4) * self.scale,
            scale=0.5,
            blue=australian_blue,
            red=australian_red
        )
        self.commonwealth_star = Star(
            self.pen,
            self.xcor - (self.scr.window_width() / 4) * self.scale,
            self.ycor - (self.scr.window_height() / 4) * self.scale,
            m=7, n=3, radius=(self.scr.window_width() * (3 / 40)) * self.scale,
            fill_color=white, border_color=white
        )
        self.alpha_crucis = Star(
            self.pen,
            self.xcor + (self.scr.window_width() / 4) * self.scale,
            self.ycor - ((self.scr.window_height() / 2) * (2 / 3)) * self.scale,
            m=7, n=3, radius=(self.scr.window_width() / 28) * self.scale,
            fill_color=white, border_color=white
        )
        self.beta_crucis = Star(
            self.pen,
            self.xcor + (self.scr.window_width() / 4) * self.scale,
            self.ycor + ((self.scr.window_height() / 2) * (2 / 3)) * self.scale,
            m=7, n=3, radius=(self.scr.window_width() / 28) * self.scale,
            fill_color=white, border_color=white
        )
        self.gamma_crucis = Star(
            self.pen,
            self.xcor + (self.scr.window_width() / 8) * self.scale,
            self.ycor + (self.scr.window_height() / 16) * self.scale,
            m=7, n=3, radius=(self.scr.window_width() / 28) * self.scale,
            fill_color=white, border_color=white
        )
        self.delta_crucis = Star(
            self.pen,
            self.xcor + (self.scr.window_width() * (13/36)) * self.scale,
            self.ycor + (self.scr.window_height() * (31 / 240)) * self.scale,
            m=7, n=3, radius=(self.scr.window_width() / 28) * self.scale,
            fill_color=white, border_color=white
        )
        self.epsilon_crucis = Star(
            self.pen,
            self.xcor + (self.scr.window_width() * (3 / 10)) * self.scale,
            self.ycor - (self.scr.window_height() / 24) * self.scale,
            m=5, n=2, radius=(self.scr.window_width() / 48) * self.scale,
            fill_color=white, border_color=white
        )

    def draw(self):
        self.background.draw()
        self.canton.draw()
        self.commonwealth_star.draw()
        self.alpha_crucis.draw()
        self.beta_crucis.draw()
        self.gamma_crucis.draw()
        self.delta_crucis.draw()
        self.epsilon_crucis.draw()


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
        self.win.bgcolor(bgcolor)
        self.win.tracer(0)  # Turn off turtle animation for instant rendering, to be used with win.update()

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
