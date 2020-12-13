#!/usr/bin/env python3  
import matplotlib.pyplot as plt
import json
from math import atan2, sin, cos, pi, pow, sqrt
from example_path_finder import PathFinder
from time import sleep
class Copter():
    def __init__(self, points):
        self.v_max = 6
        self.a = 1
        self.w = pi/4
        self.time_inc = 0.005
        self.points = points
        self.extra_time = [20*60,10*60,0] #time for copters to launch
        # self.extra_time = [0,0,0] #time for copters to launch
        
        self.bak = (10/50)*60*60
        # print(self.points)
        # self.x_y = self.load_points_from_json(0)
        # print(x_y)
    def time_for_line_movement(self, length):
        current_time = 0
        current_velocity = 0
        current_path = 0
        time_inc = self.time_inc
        first = True
        while current_path < length:
            current_time+=time_inc
            time_to_stop = current_velocity/self.a
            s_to_stop = current_velocity*time_to_stop-(self.a*(time_to_stop)**2)/2
            delta_s = length - current_path
            if s_to_stop > delta_s:
                if first == True:
                    # print(current_time, s_to_stop, time_to_stop, current_velocity)
                    first = False
                if current_velocity >= 0:
                    current_velocity -= time_inc*self.a
                else:
                    break
            else:
                if current_velocity < self.v_max:
                    current_velocity += time_inc*self.a
            # print(current_velocity,current_time, current_path)
            current_path += current_velocity * time_inc    
        return current_time, current_velocity, current_path
    def time_for_turn(self, angle):
        current_time = 0
        current_angle = 0
        time_inc = self.time_inc
        while abs(current_angle) < abs(angle):
            current_time += time_inc
            if angle > 0:
                current_angle += self.w*time_inc
            else:
                current_angle -= self.w*time_inc
        return current_time
    def load_points_from_json(self, id_):
        x_y = []
        with open('points.json','r') as js:
            data = json.load(js)
        for k, v in data.items():
            if(k.endswith(str(id_))):
                x_y = v
        return x_y
    def get_distance(self, start,finish):
        distance = sqrt((pow((finish[0]-start[0]),2)+pow((finish[1]-start[1]),2)))
        return distance

    def get_ang_cost(self, first, second, third):
        ang1 = atan2(second[1] - first[1], second[0] - first[0])
        ang2 = atan2(third[1] - second[1], third[0] - second[0])
        ang3 = -ang1 + ang2
        return ang3
    def get_distance_angle_between_points(self, x_points=0, y_points=0, id_=-1):
        if type(x_points) is int:
            x_y = self.load_points_from_json(id_)
            x_points = x_y['x']
            y_points = x_y['y']
        dist = []
        angle = []
        for i in range(len(x_points)-1):
            dist.append(self.get_distance([x_points[i],y_points[i]],[x_points[i+1],y_points[i+1]]))
            if(i == len(x_points)-2):
                angle.append(0.0)
            else:
                angle.append(self.get_ang_cost([x_points[i],y_points[i]],[x_points[i+1],y_points[i+1]],[x_points[i+2],y_points[i+2]]))
        return dist, angle
    def calculate_time(self):
        answer = {'fig1':0,
                'fig2':0,
                'fig3':0}
        angle_indexis = [[],[],[]]
        radiuss = [[],[],[]]
        for j in range(0,3):
            points_cur = self.points['points_'+str(j)]
            dist, angle = self.get_distance_angle_between_points(x_points=points_cur['x'], y_points=points_cur['y'])
            # print(len(dist), len(angle))
            time = 0
            time_inc = 0
            iters_of_stop_points = []
            time_of_each_land = []
            time_of_turns = 0
            first_land = True
            # print(angle)
            for i in range(0, len(dist), 1):
                time_length = 0
                time_angle = 0
                if(abs(angle[i]) <= pi/2):
                    angle_indexis[j].append(i)
                    r = (18)/(angle[i]-pi/2)
                    radiuss[j].append(abs(r))
                    time_length, _, _ = self.time_for_line_movement(dist[i])
                    time_angle = self.time_for_turn(angle[i])
                    time_inc += time_length
                    time_inc += time_angle

                else:
                    time_length, _, _ = self.time_for_line_movement(dist[i])
                    time_angle = self.time_for_turn(angle[i])
                    time_inc += time_length
                    time_inc += time_angle
                if time_inc > self.bak:
                    iters_of_stop_points.append(i-1)
                    if first_land == True:
                        time+=self.extra_time[j]
                        first_land = False
                    time_of_each_land.append(time)
                    time_inc = 0
                    time+=180
                time += time_length
                time += time_angle
                time_of_turns +=time_angle
            # time = time + self.extra_time[j]
            # print(time_of_turns)
            ans = {'time': time, 'iters_of_stop_points': iters_of_stop_points, 'time_of_each_land': time_of_each_land}
            answer['fig'+str(j+1)] = ans
            # print(time)
        # print(len(angle_indexis))
        return answer, angle_indexis, radiuss
        # return answer

if __name__ == '__main__':
    path = PathFinder()
    
    points = path.get_points()
    # print(points)
    copter = Copter(points)
    # print(copter.time_for_line_movement(5))
    # print(copter.time_for_turn(-1))
    # for j in range(0,3):
    print(copter.calculate_time())