import turtle


window = turtle.Screen()
global_turtle = turtle.Turtle()


def draw_something(turtle_object):
    local_turtle = turtle_object.clone()
    local_turtle.circle(radius=50)


draw_something(global_turtle)
window.exitonclick()
