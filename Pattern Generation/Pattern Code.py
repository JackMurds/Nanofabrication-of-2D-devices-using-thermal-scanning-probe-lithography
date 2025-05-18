import pya
import math

# Initialise layout
app = pya.Application.instance()
view = app.main_window().current_view()
if view is None:
    raise RuntimeError("No layout is open!")
layout = view.active_cellview().layout()

# Lattice constant
a = 1  # µm

# Circle parameters
diameter = 0.4  # µm
radius = diameter / 2

# Create a top cell with formatted title
cell = layout.create_cell(f"a={a}_d={diameter}_Hex_Lattice")
layer = layout.layer(1, 0)  # Define layer (LAYER 1, datatype 0)

# Function to create a full circle
def create_circle(cx, cy, r, num_points=32):
    points = [
        pya.DPoint(cx + r * math.cos(2 * math.pi * i / num_points),
                   cy + r * math.sin(2 * math.pi * i / num_points))
        for i in range(num_points)
    ]
    return pya.DPolygon(points)

# Lattice size
rows = 20  # Number of rows
cols = 10  # Number of columns

# Initialise y starting position
y = 0

# Generate hexagonal lattice
for row in range(rows):
    if (row+3) % 2 == 1:
        y += a / math.sqrt(3)
    else:
        y += a / (2 * math.sqrt(3))

    for col in range(cols):
        x = a * (0.5 + col)
        if (row+3) % 4 > 1:
            if col == cols - 1:  # Prevent extra circles appearing on rhs via shift (line 46)
                continue
            x += a / 2

        # Default case: full circle
        circle = create_circle(x, y, radius)
        cell.shapes(layer).insert(circle)

# Update the view
view.add_missing_layers()
