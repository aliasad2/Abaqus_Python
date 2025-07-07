# -*- coding: utf-8 -*-

from math import cos, sin, pi

model = mdb.models['Model-1']
part = model.parts['Part-1']

# Circle parameters
x_center = 200.0
y_center = 200.0
z_top = 3.0
radius = 100.0
num_vertices = 32

# Start from bottom
theta_start = 3 * pi / 2

# Choose rotation: +1 = counter-clockwise, -1 = clockwise
rotation = -1  # ← change to -1 for clockwise (bottom to right)

for i in range(num_vertices):
    angle = theta_start + rotation * 2 * pi * i / num_vertices
    x = x_center + radius * cos(angle)
    y = y_center + radius * sin(angle)
    z = z_top
    try:
        vertex = part.vertices.findAt(((x, y, z),))
        set_name = 'S{}'.format(i + 1)
        part.Set(vertices=(vertex,), name=set_name)
        print("Created set:", set_name)
    except:
        print(" Could not find vertex near:", (x, y, z))


