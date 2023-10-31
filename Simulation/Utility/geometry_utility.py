from math import sin
import numpy as np

def bezier_curve(p0, p1, p2, t):
			x = int(round((1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]))
			y = int(round((1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
			return x, y

def trace_courbe_bezier(p0, p1, p2):
    return [bezier_curve(p0, p1, p2, t) for t in np.linspace(0, 1, 100)]

def ondulation(courbe, amplitude=9, frequence=0.2):
    return [(x, int(y + amplitude * sin(frequence * x))) for x, y in courbe]


def add_points(courbe):
    
    new_courbe = [courbe[0]]
    for i in range(1, len(courbe)):
        previous_point  = courbe[i - 1]
        current_point  = courbe[i]
        
        x = (previous_point[0] + current_point[0]) // 2
        y = (previous_point[1] + current_point[1]) // 2
        mid_point = (x, y)
        
        new_courbe.extend([mid_point, current_point])

    return new_courbe