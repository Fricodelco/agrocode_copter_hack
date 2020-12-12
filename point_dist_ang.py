#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json
import math


def get_distance(start,finish):
    distance = math.sqrt((math.pow((finish[0]-start[0]),2)+math.pow((finish[1]-start[1]),2)))
    return distance

def get_ang_cost(first, second, third):
    ang1 = math.atan2(second[1] - first[1], second[0] - first[0])
    ang2 = math.atan2(third[1] - second[1], third[0] - second[0])

    ang3 = ang1 + ang2 - math.pi/2

    return ang3

def load_points_from_json(id_):
    x_y = []
    with open('points.json','r') as js:
        data = json.load(js)
    for k, v in data.items():
        if(k.endswith(str(id_))):
            x_y = v
    return x_y

def get_distance_angle_between_points(x_points=0, y_points=0, id_=-1):
    if type(x_points) is int:
        x_y = load_points_from_json(id_)
        x_points = x_y['x']
        y_points = x_y['y']
    
    dist = []
    angle = []

    for i in range(len(x_points)-1):
        dist.append(get_distance([x_points[i],y_points[i]],[x_points[i+1],y_points[i+1]]))
        if(i == len(x_points)-2):
            angle.append(0.0)
        else:
            angle.append(get_ang_cost([x_points[i],y_points[i]],[x_points[i+1],y_points[i+1]],[x_points[i+2],y_points[i+2]]))
    
    return dist, angle