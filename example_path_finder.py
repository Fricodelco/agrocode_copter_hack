#!/usr/bin/env python3  
import matplotlib.pyplot as plt
from math import sqrt
import json
from math import atan2, sin, cos
from horizontal_lines import get_figure
class PathFinder():
    def __init__(self):
        a = 1
        # self.points = points
        # for i in range(0,len(self.points)):
            # self.points[i][0] = self.points[i][0]/5 
            # self.points[i][1] = self.points[i][1]/5 
        
    def find_max_length(self, points):
        x, y = self.distract_coords(points)
        # plt.plot(x,y, '')
        max_dist = 0
        n = 0 #number_of_max_line
        lines = []
        for i in range(1,len(x),1):
            euclidian_distance = sqrt((x[i]-x[i-1])**2 + (y[i]-y[i-1])**2)
            line = {'a': (y[i] - y[i-1]),'b': (x[i-1] - x[i]), 'c': (x[i]*y[i-1] - x[i-1]*y[i]),'x1': x[i],'y1': y[i], 'x2': x[i-1], 'y2': y[i-1]}
            
            lines.append(line)
            # print(euclidian_distance)
            if euclidian_distance > max_dist:
                max_dist = euclidian_distance
                n = i
        # coord_1 = [x[number_of_max_line], y[number_of_max_line]]
        # coord_2 = [x[number_of_max_line-1], y[number_of_max_line-1]]
        x_of_max = [x[n],x[n-1]]
        y_of_max = [y[n],y[n-1]]
        # plt.plot(x_of_max, y_of_max, 'r--')
        # plt.grid(True)

        n_for_line = n-1
        temp = lines[0]
        lines[0] = lines[n_for_line]
        lines[n_for_line] = temp
        del temp
        line_max = lines[0]
        # print(line_max)
        #find perpendikular ot samoi dalnei tochki do samoi bolshoi priamoi
        distance = []
        for i in range(1, len(x),1):
            if x[i] != line_max['x1'] and x[i] != line_max['x2']:
                # plt.plot(x[i], y[i], 'bo') 
                ortoganal = {'a':line_max['b'],
                            'b': line_max['a'],
                            'c': (-(line_max['b']*x[i])-(line_max['a']*y[i]))}
                x_cross_x, y_cross_y = self.find_cross(ortoganal, line_max)
                # plt.plot([x[i],x_cross_x], [y[i],y_cross_y], 'r--')
                euclidian_distance = sqrt((x[i]-x_cross_x)**2 + (y[i]-y_cross_y)**2)
                distance.append(euclidian_distance)
        # print(max(distance))
        iterations = round(max(distance)*2)
        #stroim parallelnie linii
        x_cross = []
        y_cross = []
        # print(it)
        for d in range(1,iterations,1):
            if d%2 == 0 :
                continue
            else:
                parallel_line = {'a': line_max['a'], 'b': line_max['b'], 'c': line_max['c']-d/2*sqrt(line_max['a']**2+line_max['b']**2)} 
                #finde cross of parallel with previous line and next line
                for i in range(1, len(lines),1):
                
                    x_cross_x, y_cross_y = self.find_cross(parallel_line, lines[i]) 
                    # print(lines[i]['x1'])
                    # print(x_cross_x, lines[i]['x1'])
                    if (x_cross_x > lines[i]['x1'] and x_cross_x < lines[i]['x2']) or (x_cross_x < lines[i]['x1'] and x_cross_x > lines[i]['x2']):
                    # if (y_cross_y < lines[i-1]['y1'] and y_cross_y > lines[i-1]['y2']):
                        if x_cross_x != 0:                        
                            x_cross.append(x_cross_x)
                            y_cross.append(y_cross_y)

                parallel_line = {'a': line_max['a'], 'b': line_max['b'], 'c': line_max['c']+d/2*sqrt(line_max['a']**2+line_max['b']**2)} 
                #finde cross of parallel with previous line and next line
                for i in range(1, len(lines),1):
                
                    x_cross_x, y_cross_y = self.find_cross(parallel_line, lines[i]) 
                    # print(lines[i]['x1'])
                    # print(x_cross_x, lines[i]['x1'])
                    if (x_cross_x > lines[i]['x1'] and x_cross_x < lines[i]['x2']) or (x_cross_x < lines[i]['x1'] and x_cross_x > lines[i]['x2']):
                    # if (y_cross_y < lines[i-1]['y1'] and y_cross_y > lines[i-1]['y2']):
                        if x_cross_x != 0:                        
                            x_cross.append(x_cross_x)
                            y_cross.append(y_cross_y)

        i = 2
        while i < len(x_cross)-1:
            euql_1 = sqrt(x_cross[i-1]**2 + y_cross[i-1]**2)
            euql_2 = sqrt(x_cross[i+1]**2 + y_cross[i+1]**2)
            if abs(euql_1 - euql_2) < 10:
                temp = x_cross[i]
                x_cross[i] = x_cross[i+1]
                x_cross[i+1] = temp
                temp = y_cross[i]
                y_cross[i] = y_cross[i+1]
                i+=4
            else:
                # print(abs(euql_1 - euql_2))
                i+=2
        #optimize points 
        # plt.plot(x_cross, y_cross, 'g--')
        for i in range(0, len(x_cross)-1,2):
            alpha = atan2(y_cross[i] - y_cross[i+1], x_cross[i] - x_cross[i+1])
            delta_x = -abs(0.5*cos(alpha))     #0.4 its 2/5 of 5 meters (1 cell = 5 meter)
            delta_y = -abs(0.5*sin(alpha))
            if x_cross[i] > x_cross[i+1]:
                x_cross[i] -= delta_x
                x_cross[i+1] += delta_x
            else:
                x_cross[i] += delta_x
                x_cross[i+1] -= delta_x
            if y_cross[i] > y_cross[i+1]:
                y_cross[i] -= delta_y
                y_cross[i+1] += delta_y
            else:
                y_cross[i] += delta_y
                y_cross[i+1] -= delta_y
            
        """x_1 = [x_cross[0], x_cross[1]]
        x_2 = []
        y_1 = [y_cross[0], y_cross[1]]
        y_2 = []
        for i in range(4,len(x_cross)-2,2):
            x_1.append(x_cross[i+1])
            x_1.append(x_cross[i]) 
            y_1.append(y_cross[i+1])
            y_1.append(y_cross[i]) 
            x_1.append(x_cross[i+2]) 
            y_1.append(y_cross[i+2])
            
        print(x_cross)
        print(x_1)
        l = len(x_1)
        return x_1, y_1, x_of_max, y_of_max, l"""
    
        return x_cross, y_cross, x_of_max, y_of_max
    
    def find_cross(self, line1, line2):
        if (line2['a']*line1['b'] - line1['a']*line2['b']) != 0:
            x = (line1['c']*line2['b'] - line1['b']*line2['c'])/(line2['a']*line1['b'] - line1['a']*line2['b'])
        else:
            x = 0
        if (line2['b']*line1['a'] - line1['b']*line2['a']) != 0:
            y = (line1['c']*line2['a'] - line1['a']*line2['c'])/(line2['b']*line1['a'] - line1['b']*line2['a'])
        else:
            y = 0
        return x,y
    def distract_coords(self, points):
        x = []
        y = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
        x.append(points[0][0])
        y.append(points[0][1])
        return x, y
    def get_points(self):
        # with open('points.json', 'w') as write_file:
        with open('figure.json', 'r') as read_file:
            data = json.load(read_file)
        # print(data)
        points = [data['figure1'], data['figure2'], data['figure3']]
    
        data = {'points_0': 0,'points_1':0, 'points_2':0}
        j = 0
        with open('points.json', 'w') as write_file:
            for point in points:
                for i in range(0,len(point)):
                    point[i][0] = point[i][0]/5 
                    point[i][1] = point[i][1]/5 
            
                x, y, x_max, y_max = self.find_max_length(point)
                for i in range(0,len(x)):
                    x[i] = x[i]*5 
                    y[i] = y[i]*5 
                data_local = {"x": x, "y": y}
                data['points_'+str(j)] = data_local 
                j+=1
            json.dump(data,write_file)
        return data
    def sign(self, number):
        if number < 0:
            return(-1)
        else:
            return(1)

def distract_coords(points):
        x = []
        y = []
        for point in points:
            x.append(point[0])
            y.append(point[1])
        x.append(points[0][0])
        y.append(points[0][1])
        return x, y

if __name__ == '__main__':
    x_field = [0, -92.90069267118855, 140.84355006431937, 353.1844363236166, 433.09813506117024, 425.66284007499496, 0]
    y_field = [0, 276.2304132311622, 304.56447871509005, 223.57025571008904, 160.2219372171964, 0.0, 0]
    # get_figure(0.2, 0.4, 0.4)
    # plt.plot(x_field, y_field, 'b')
    with open('figure.json', 'r') as read_file:
        data = json.load(read_file)
    # print(data)
    points = [data['figure1'], data['figure2'], data['figure3']]
    # points = [data['figure1']]
    # points.reverse()
    j = 0
    # flag = True
    plt.plot(x_field, y_field, 'b')
    
    for point in points:
        x_part, y_part = distract_coords(point)
        plt.plot(x_part, y_part, 'r')
        # if flag == True:
            # flag = False
    j = 0

    with open('points.json', 'w') as write_file:
        data = {'points_0': 0,'points_1':0, 'points_2':0}
        
        for point in points:
            for i in range(0,len(point)):
                point[i][0] = point[i][0]/5 
                point[i][1] = point[i][1]/5 
        
            path = PathFinder()
            x, y, x_max, y_max = path.find_max_length(point)
            # print(len(x))
            for i in range(0,len(x)):
            # for i in range(0,l):
                x[i] = x[i]*5 
                y[i] = y[i]*5 
            if j == 0:
                plt.plot(x, y, 'g--')
            if j == 1:
                plt.plot(x, y, 'm--')
            if j == 2:
                plt.plot(x, y, 'y--')
                
            plt.plot([x_max[0]*5,x_max[0]*5], [y_max[0]*5,y_max[0]*5], 'ro')
            # plt.plot(x[0], y[0], 'ro')
            
            data_local = {"x": x, "y": y}
            data['points_'+str(j)] = data_local 
            j+=1
        
        json.dump(data,write_file)
    plt.grid()
    plt.show()
    j = 0
    