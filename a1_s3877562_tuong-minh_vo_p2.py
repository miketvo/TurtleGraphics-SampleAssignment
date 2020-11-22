# RMIT University Vietnam
# Course: COSC2429 Introduction to Programming
# Semester: 2020C
# Assignment: 1 (Problem 2)
# Author: Tuong-Minh Vo (s3877562)
# Created date: 20/11/2020
# Last modified date: 22/11/2020


from turtle import Turtle, Screen


# Colors taken from https://en.wikipedia.org/wiki/List_of_colors_(compact)#A
color_scheme = [
    "#B284BE",  # African violet
    "#72A0C1",  # Air superiority blue
    "#C46210",  # Alloy orange
    "#E52B50",  # Amaranth
    "#3B7A57",  # Amazon
    "#FFBF00",  # Amber
    "#D3212D",  # Amaranth red
    "#FF7E00",  # Amber (SAE/ECE)
    "#9966CC",  # Amethyst
    "#AB274F",  # Amaranth purple
    "#A4C639",  # Android green
    "#9F2B68",  # Amaranth deep purple
    "#CD9575",  # Antique brass
    "#665D1E",  # Antique bronze
    "#915C83",  # Antique fuchsia
    "#F19CBB",  # Amaranth pink
    "#841B2D",  # Antique ruby
    "#008000",  # Ao (English)
    "#8DB600",  # Apple green
    "#7FFFD4",  # Aquamarine
    "#D0FF14",  # Arctic lime
    "#4B5320",  # Army green
    "#8F9779",  # Artichoke
    "#B2BEB5",  # Ash grey
    "#87A96B",  # Asparagus
    "#FF9966",  # Atomic tangerine
    "#A52A2A",  # Auburn
    "#568203",  # Avocado
    "#007FFF",  # Azure
]

# Settings
chart_size = 400
chart_resolution = 1000
bg_color = "#333333"  # dark grey
text_color = "#ffffff"  # white
label_font = ("Arial", 10, "bold")
emptylistmessage_font = ("Arial", 24, "bold")


class PieChart:
    def __init__(self, valuelist, pen, text_pen, radius: int):
        """
        Stores the list of values to be rendered into a pie chart of radius pixels. Rendering mechanism uses two Turtle
        objects: pen for graphical rendering and text_pen for text rendering.
        """
        # Dataset migration
        self.radius = radius
        self.valuelist = valuelist.copy()
        self.valuelist_len = len(valuelist)

        # Calculate the number sequence total
        self.total = 0
        for i in range(self.valuelist_len):
            self.total += valuelist[i]

        # Calculate the percentage of each number in the sequence
        self.percentagelist = []
        for i in range(self.valuelist_len):
            self.percentagelist.append(valuelist[i] / self.total)

        # Graphical initialization
        self.pen = pen.clone()
        self.text_pen = text_pen.clone()

    def draw(self):
        color_scheme_size = len(color_scheme)

        if self.valuelist_len == 0:
            self.text_pen.write("EMPTY SEQUENCE!", align="center", font=emptylistmessage_font)
        else:
            # Prepare to render
            self.pen.penup()
            self.pen.setheading(90)
            self.pen.forward(self.radius)
            current_arc_pos = self.pen.position()

            # Render next pie chart section
            for i in range(self.valuelist_len):
                # Pre-drawing
                self.pen.setposition(0, 0)
                self.pen.color(color_scheme[i % color_scheme_size])
                self.pen.fillcolor(color_scheme[i % color_scheme_size])

                # Drawing
                self.pen.pendown()
                self.pen.begin_fill()
                self.pen.setheading(self.pen.towards(current_arc_pos))
                self.pen.forward(self.radius)
                self.pen.setheading(self.pen.towards(0, 0) - 90)
                self.pen.circle(radius=self.radius, extent=((360 * self.percentagelist[i]) / 2), steps=chart_resolution)
                current_arc_midpos = self.pen.position()  # Record middle arc coordinates for later text label placement
                self.pen.circle(radius=self.radius, extent=((360 * self.percentagelist[i]) / 2), steps=chart_resolution)
                current_arc_pos = self.pen.position()
                self.pen.end_fill()
                self.pen.penup()

                # Add percentage text label, placed inside the chart if percentage > 5%, outside if percentage <= 5% to
                # improve readability
                self.text_pen.penup()
                if self.percentagelist[i] > 0.05:
                    self.text_pen.setposition(
                        int(current_arc_midpos[0] / 2),
                        int(current_arc_midpos[1] / 2)
                    )
                else:
                    self.text_pen.setposition(
                        current_arc_midpos[0] + int(current_arc_midpos[0] / 10),
                        current_arc_midpos[1] + int(current_arc_midpos[1] / 10)
                    )
                self.text_pen.pendown()
                self.text_pen.write(
                    "{:.1f}%".format(self.percentagelist[i] * 100),
                    align="center",
                    font=label_font
                )


# This program generates a percentage pie chart via the Python Turtle graphic module from a sequence of number the user
# entered through a console menu
class Application:
    def __init__(self, apptitle):
        self.apptitle = apptitle
        self.number_list = []

    def __init_gui__(self):
        """
        Initialize the Turtle graphic engine and create a window containing two centered Turtle objects, one for graphic
        rendering and the other for text rendering.
        :return: None
        """
        # Screen initializations
        self.win = Screen()
        self.win.title(self.apptitle)
        self.win.bgcolor(bg_color)
        self.win.tracer(0)  # Instant rendering

        # Pen initializations
        self.pen = Turtle()
        self.pen.hideturtle()
        self.text_pen = Turtle()
        self.text_pen.color(text_color)
        self.text_pen.hideturtle()

    # Main application loop
    def main(self):
        # Console interface
        print("This program generates a percentage pie chart from a sequence of number you entered. Enter a negative, \
zero or non-numeric value to end the sequence.")
        while True:
            try:
                usr_input = float(input(">> "))
                if usr_input <= 0:
                    break
                self.number_list.append(usr_input)
            except ValueError:
                break
            finally:
                print("Current number(s): {}\n".format(self.number_list))
        print("\nEnd user input, generating pie chart...")

        # Graphical interface
        self.__init_gui__()
        chart = PieChart(self.number_list, pen=self.pen, text_pen=self.text_pen, radius=int(chart_size / 2))
        chart.draw()
        self.win.update()
        self.win.exitonclick()


if __name__ == "__main__":
    app = Application(apptitle="Pie chart generator")
    app.main()
