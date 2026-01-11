"""
HIT137 Assignment 2 - Question 3
Recursive Geometric Pattern using Turtle Graphics
"""

import turtle

def draw_line(t, length, depth):
    """
    Recursively draws a line with an inward indentation (Inverted Koch-like).
    
    Rule:
    1. Divide the edge into 3 equal segments.
    2. Replace the middle segment with two sides of an equilateral triangle pointing inward.
    3. Transformation: 
       - Forward L/3
       - Left 60
       - Forward L/3
       - Right 120
       - Forward L/3
       - Left 60
       - Forward L/3
    """
    if depth == 0:
        t.forward(length)
    else:
        segment = length / 3
        
        # Segment 1
        draw_line(t, segment, depth - 1)
        
        # Turn Left 60
        t.left(60)
        
        # Segment 2 (Side 1 of indentation)
        draw_line(t, segment, depth - 1)
        
        # Turn Right 120
        t.right(120)
        
        # Segment 3 (Side 2 of indentation)
        draw_line(t, segment, depth - 1)
        
        # Turn Left 60
        t.left(60)
        
        # Segment 4
        draw_line(t, segment, depth - 1)

def main():
    print("HIT137 Assignment 2 - Question 3")
    print("---------------------------------")
    
    # User Inputs
    try:
        num_sides = int(input("Enter the number of sides: "))
        side_length = int(input("Enter the side length: "))
        recursion_depth = int(input("Enter the recursion depth: "))
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    # Setup Turtle
    screen = turtle.Screen()
    screen.title("Recursive Geometric Pattern - Question 3")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)  # Fastest speed
    t.pensize(2)
    
    # Center the shape roughly
    # Move back and down to center a bit, assuming bottom-left start of polygon
    # For a regular polygon, this simple offset helps but isn't perfect for all N
    t.penup()
    t.goto(-side_length / 2, -side_length / 2)
    t.pendown()
    
    # Main Loop to draw Polygon
    # We draw each side using the recursive function
    angle = 360 / num_sides
    
    for _ in range(num_sides):
        draw_line(t, side_length, recursion_depth)
        t.left(angle)
        
    # Finish
    t.hideturtle()
    print("Pattern generated successfully.")
    print("Click on the window to exit.")
    screen.exitonclick()

if __name__ == "__main__":
    main()
