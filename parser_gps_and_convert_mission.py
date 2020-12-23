from pykml import parser
from os import path
import re
import math
import matplotlib.pyplot as plt
import json
import numpy as np

rad = 6365446.4253514


NAV_LEG_TAKEOFF = 'NAV_LEG_TAKEOFF'
NAV_LEG_SIMPLE = 'NAV_LEG_SIMPLE'
NAV_LEG_TO_LAND = 'NAV_LEG_TO_LAND'
NAV_LEG_NON_STOP = 'NAV_LEG_NON_STOP'

def points_distance(point1, point2):
    llat1 = point1[1]
    llong1 = point1[0]
    
    llat2 = point2[1]
    llong2 = point2[0]
    
    #в радианах
    lat1 = llat1*math.pi/180.
    lat2 = llat2*math.pi/180.
    long1 = llong1*math.pi/180.
    long2 = llong2*math.pi/180.
    
    #косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)
    
    #вычисления длины большого круга
    y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
    x = sl1*sl2+cl1*cl2*cdelta
    ad = math.atan2(y,x)
    dist = ad*rad
    
    return dist

def turn_point(x,y,angle):
    x_ = x*math.cos(angle) - y*math.sin(angle)
    y_ = x*math.sin(angle) + y*math.cos(angle)

    return x_,y_

def from_meter_to_gps(x_point, y_point, pr_angle, base_point):
    gps_point = []
    for i,el in enumerate(x_point):
        #x_point[i], y_point[i]  = turn_point(x_point[i], y_point[i], pr_angle)
        gps_point.append([base_point[0]+x_point[i]/rad*180.0/math.pi, base_point[1]+y_point[i]/rad*180.0/math.pi])
    return gps_point

def point_lx(number, type_, lat, lon, alt, radius, waitTime, maxhspeed, maxvspeed, 
                pOILat, pOILon, pOIAltitude, pOIHeading, pOIPitch, pOIRoll, flg1, photo, panoSectors, delta):
    point = ('[{}]\nType={}\nLat={}\nLon={}\nAlt={}\nRadius={}\n' + \
            'WaitTime={}\nMaxHSpeed={}\nMaxVSpeed={}\nPOILat={}\n' + \
            'POILon={}\nPOIAltitude={}\nPOIHeading={}\nPOIPitch={}\n' + \
            'POIRoll={}\nFlg1={}\nPhoto={}\nPanoSectors={}\nDelta={}\n\n').format(number, type_, lat, lon,
                                                                            alt, radius, waitTime, maxhspeed, maxvspeed, 
                                                                            pOILat, pOILon, pOIAltitude, pOIHeading, pOIPitch,
                                                                            pOIRoll, flg1, photo, panoSectors, delta)

    return point

def point_lx_for_task(number, type_, lat, lon, alt, radius):
    point = point_lx(number=number, type_=type_, lat=lat, lon=lon, 
            alt=alt, radius=radius, waitTime=0.1, maxhspeed=6.0, 
            maxvspeed=2.0, pOILat=0, pOILon=0, pOIAltitude=0, 
            pOIHeading=0, pOIPitch=-90, pOIRoll=0, flg1=160, 
            photo=0, panoSectors=0, delta=0)
    return point

def write_path_mission(file_name, j, start_index, points_in_gps, i, el, ind_angle, radius):
    with open(file_name+str(j)+'.txt','w') as wr:
        for k in range(start_index,len(points_in_gps[i][0])):#point
            if k == start_index:
                wr.write(point_lx_for_task(k-start_index, NAV_LEG_TAKEOFF, points_in_gps[i][0][k][1], points_in_gps[i][0][k][0], 2.0, 2.0))
            elif k == el:
                wr.write(point_lx_for_task(k-start_index, NAV_LEG_TO_LAND, points_in_gps[i][0][k][1], points_in_gps[i][0][k][0], 2.0, 2.0))
                start_index = el
                break
            else:
                try:
                    index = ind_angle[i].index(k-1)
                    wr.write(point_lx_for_task(k-start_index, NAV_LEG_NON_STOP, points_in_gps[i][0][k][1], points_in_gps[i][0][k][0], 2.0, radius[i][index]))
                except ValueError:
                    wr.write(point_lx_for_task(k-start_index, NAV_LEG_SIMPLE, points_in_gps[i][0][k][1], points_in_gps[i][0][k][0], 2.0, 2.0))
    return start_index

def flight_mission(pr_angle, base_point, stop_point, ind_angle, radius):
    file_name_lx = ['first_mission_lx_','second_mission_lx_','third_mission_lx_']
    with open('points.json') as js:
        data = json.load(js)

    points_part = [data['points_0'], data['points_1'], data['points_2']]
    points_in_gps = [[],[],[]]
    for i, points_i in enumerate(points_part):
        points_in_gps[i].append(from_meter_to_gps(points_i['x'], points_i['y'], pr_angle, base_point))
    
    start_index = 0

    for i, file_name in enumerate(file_name_lx):#index copter
        for j, el in enumerate(stop_point[i]):#stop point
            start_index = write_path_mission(file_name, j, start_index, points_in_gps, i, el, ind_angle, radius)
        write_path_mission(file_name, len(stop_point[i]), start_index, points_in_gps, i, len(points_in_gps[i][0])-1, ind_angle, radius)
                    
    # for j, f_name in enumerate(file_name_ardu):
    #     with open(f_name, 'w') as wr:
    #         wr.write('QGC WPL 110\n')
    #         key1 = 1
    #         key2 = 0
    #         hig = 0
    #         for i in range(len(points_in_gps[j][0])):
    #             if i != 0:
    #                 key1 = 0
    #                 key2 = 3
    #                 hig = 50.0
    #             wr.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
    #                 i, key1, key2, 16, 1.0,
    #                 0, 0, 0, points_in_gps[j][0][i][1],
    #                 points_in_gps[j][0][i][0],
    #                 hig,1))

def parse_kml_file(name_file):
    kml_file = path.join(name_file)
    hight_p = 0
    width_p = 0

    points = []
    x_point = []
    y_point = []

    with open(kml_file) as f:
        doc = parser.parse(f).getroot()

    points_str = doc.Document.Placemark.Polygon.outerBoundaryIs.LinearRing.coordinates.text
    points_str = re.sub('[^0-9. ,]','',points_str)[:-1]
    points_str_list = points_str.split(' ')[:-1]

    for el in points_str_list:
        points.append(list(map(float,el.split(',')))[:-1])

    test_points = points.copy()
    base_point = test_points.pop(4)
    x_point.append(width_p)
    y_point.append(hight_p)

    test_points.reverse()
    test_points = test_points[1:] + [test_points[0]] 

    pr_angle = math.atan2(points[5][1]-base_point[1],points[5][0]-base_point[0])

    # b_x = rad * math.cos(base_point[1])*math.cos(base_point[0])
    # b_y = rad * math.cos(base_point[1])*math.sin(base_point[0])
    for point in test_points:
        distance = points_distance(base_point,point)
        #angle = math.atan2(point[1]-base_point[1],point[0]-base_point[0]) 
        #x_point.append(distance*math.cos(angle)+width_p)
        #y_point.append(distance*math.sin(angle)+hight_p)
        x_point.append(rad * (point[0] - base_point[0])*math.pi/180.0)
        y_point.append(rad * (point[1] - base_point[1])*math.pi/180.0)

    x_point.append(width_p)
    y_point.append(hight_p)

    plt.plot(x_point,y_point)
    plt.show()

    temp = []

    for i in range(len(x_point)):
        temp.append([x_point[i], y_point[i]])

    return temp, pr_angle, base_point

#parse_kml_file('pole.kml')
#flight_mission(0.57, [45.7695, 50.0658], [[10,21],[11, 25],[13,28]], [[1,3,5,9,7],[1,3,5,9,7],[1,3,5,9,7]],[[10,2,58,96,6],[10,2,58,96,6],[10,2,58,96,6]])