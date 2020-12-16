#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import json
import numpy as np
import math


iter_step = 0.3

class Figure:
    def __init__(self,points):
        self.points = points
        self.y = 0
        self.x_min = 500 
        self.x_max = -500
        self.y_min = 500 
        self.y_max = -500
        self.i_min = 500
        self.i_max = -500
        self.j_min = 500
        self.j_max = -500
        self.func_list = []
    def get_minmax_in_field(self):
        
        for i,point in enumerate(self.points):
            if (point[0] < self.x_min):
                self.i_min = i
                self.x_min = point[0]
            if (point[0] > self.x_max):
                self.i_max = i
                self.x_max = point[0]
            if (point[1] < self.y_min):
                self.j_min = i
                self.y_min = point[1]
            if (point[1] > self.y_max):
                self.j_max = i
                self.y_max = point[1]

    def get_line_func(self,two_points):
        def foo(x):
            y = (x - two_points[0][0])*(two_points[1][1] - two_points[0][1])/(two_points[1][0] - two_points[0][0]) + two_points[0][1]
            return y
        return foo    

    def get_function_list(self):
        for i, point in enumerate(self.points):
            if (point == self.points[-1]):
                self.func_list.append(self.get_line_func([point,self.points[0]]))
            else:
                self.func_list.append(self.get_line_func([point,self.points[i+1]]))
        
    def get_y(self, x):
        count = 0
        func_minus = 0
        func_plus = 0
        for i,point in enumerate(self.points):
            if point[0] == x:
                func_plus = self.func_list[i]
            if point[0] > x:
                func_plus = self.func_list[i-1]
                count = i
                break
        for a in range (count, len(self.points)+1):
            if (a == len(self.points)):
                a = 0
            if self.points[a][0] <= x:
                func_minus = self.func_list[a-1]
                break

        return func_plus(x) - func_minus(x)

    def func_y(self, x):
        count = 0
        func_minus = 0
        func_plus = 0
        for i,point in enumerate(self.points):
            if point[0] == x:
                func_plus = self.func_list[i]
            if point[0] > x:
                func_plus = self.func_list[i-1]
                count = i
                break
        for a in range (count, len(self.points)+1):
            if (a == len(self.points)):
                a = 0
            if self.points[a][0] <= x:
                func_minus = self.func_list[a-1]
                break
        return func_minus(x),func_plus(x)

def get_area(figure, x_start, x_finish):
    area = 0
    while (x_start < x_finish):
        area += figure.get_y(x_start)*iter_step
        x_start += iter_step
    return area

def find_lines(figure, global_area, k1 = 1/3, k2 = 1/3, k3 = 1/3):
    i = figure.x_min
    while (get_area(figure,figure.x_min,i) < global_area*k1):
        i+= iter_step
    j = i
    while (get_area(figure,i,j) < global_area*k2):
        j+= iter_step
    return i,j


def rotate(points, angle):
    new_points = []
    for i in range(0, len(points)):
        new_points.append([points[i][0] * math.cos(angle) - points[i][1] * math.sin(angle), points[i][0] * math.sin(angle) + points[i][1] * math.cos(angle)])
    return new_points

def euklide(point1, point2):
    distance = math.sqrt((math.pow((point2[0]-point1[0]),2))+math.pow((point2[1]-point1[1]),2))
    return distance

def sort(points):
    
    point_d = {}
    for i in range (1, len(points)):
        point_d[str(i)] = euklide(points[0], points[i])
    points_list = list(point_d.items())
    points_list.sort(key=lambda i: i[1])

    index_point = []
    for el in points_list:
        index_point.append(int(el[0]))
    index_point.insert(0,0)

    new_points = []
    for ind in index_point:
        new_points.append(points[ind])
    return new_points

def get_figure(k1, k2, k3):
    #points_vert = [[-92.90069267118855, 276.2304132311622], [140.84355006431937, 304.56447871509005], [353.1844363236166, 223.57025571008904], [433.09813506117024, 160.2219372171964], [425.66284007499496, 0.0], [0, 0]]
    points = [[-304.56447872, 140.84355006], [-223.57025571, 353.18443632] , [-160.22193722, 433.09813506], [0,425.66284007],[ 0,0],[-276.23041323, -92.90069267]]
    figure = Figure(points)
    figure.get_minmax_in_field()
    figure.get_function_list()
    global_area = get_area(figure, points[figure.i_min][0], points[figure.i_max][0])
    x1,x2 = find_lines(figure, global_area, k1, k2, k3)
    y11, y12 = figure.func_y(x1)
    y21, y22 = figure.func_y(x2)

    first_countour = [[x1,y12]]
    for point in points:
        if point[0] < x1:
            first_countour.append(point)
    first_countour = sort(first_countour)
    first_countour.append([x1,y11])
    
    second_countour = [[x1,y12]]
    for point in points:
        if (point[0] > x1) and (point[0] < x2):
            second_countour.append(point)
    second_countour.append([x2, y22])
    second_countour.append([x2, y21])
    second_countour = sort(second_countour)
    second_countour.insert(0,[x1, y11])
    second_countour.append([x1, y11])
    
    third_countour = [[x2,y22]]
    for point in points:
        if (point[0] > x2):
            third_countour.append(point)
    third_countour = sort(third_countour)
    third_countour.append([x2,y21])

    new_contour1 = rotate(first_countour, -math.pi/2)
    new_contour2 = rotate(second_countour, -math.pi/2)
    new_contour3 = rotate(third_countour, -math.pi/2)

    figures = {}
    figures["figure1"] = new_contour1
    figures["figure2"] = new_contour2
    figures["figure3"] = new_contour3
    with open("figure.json","w") as js:
        json.dump(figures,js)
    

    
    

if __name__ == "__main__":
    # execute only if run as a script
    get_figure()

