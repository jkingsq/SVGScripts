import math
import heapq
import vector2D as vec
import colors
from SVGDocument import SVGDocument as svg

width = 1920.0
height = 1920.0

center = (width/2.0, height/2.0)

background = (192, 0, 0)

start_color = (255, 255, 255)

end_color = (0, 0, 0)

circle_heap = [(1.0, (0.0, 0.0))]

circles = []

target = (math.sin(math.pi/6.0), math.cos(math.pi/6.0))

iterations = 200

theta_offset = math.pi/2.0

thetas = [
    theta_offset,
    math.pi/3.0 + theta_offset,
    2.0 * math.pi/3.0 + theta_offset,
]

def scale_factor(point, step):
    return (vec.dot(vec.normalize(step), target) + 1.0) / 2.0

def expand(neg_radius, point):
    for theta in thetas:
        new_step = vec.fromPolar(-1*neg_radius, theta)
        new_point = vec.sum(point, new_step)
        new_radius = neg_radius * scale_factor(new_point, new_step)
        heapq.heappush(circle_heap, (new_radius, new_point))

for i in range(iterations):
    circle = heapq.heappop(circle_heap)
    circles.append(circle)
    new_circles = expand(*circle)

while circle_heap != []:
    circles.append(heapq.heappop(circle_heap))

max_x = 0.0
min_x = 0.0

max_y = 0.0
min_y = 0.0
min_r = 1.0

for (neg_radius, (x, y)) in circles:
    radius = neg_radius * -1

    max_x = max(max_x, x + radius)
    min_x = min(min_x, x - radius)
    max_y = max(max_y, y + radius)
    min_y = min(min_y, y - radius)
    min_r = min(min_r, radius)

x_span = max_x - min_x

y_span = max_y - min_y

scale_factor = max(width/x_span, height/y_span)

doc = svg(width, height)

doc.setFillColor(*background)
doc.addRect((0, 0), width, height)

doc.setStrokeWidth(0)

for (neg_radius, point) in circles:
    radius = -1 * neg_radius

    color = colors.mixColors(start_color, end_color, radius / (1.0 - min_r))
    doc.setFillColor(*color)

    scaled_radius = abs(radius * scale_factor)
    screen_point = vec.sum(center, vec.scale(scale_factor, point))
    doc.addCircle(screen_point, scaled_radius)

doc.write("greedyRoots.svg")
