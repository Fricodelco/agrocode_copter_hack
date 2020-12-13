import json
import horizontal_lines

def optimize_time(time_list):
    sum_time = []
    for el in time_list:
        sum_time.append(sum(el))
    
    min_index = sum_time.index(min(sum_time))

    return min_index, sum_time[min_index]

def optimize_trajectory(copter, path):
    k1_start = 0.1
    k2_start = 0.1
    k3_start = 1-k1_start-k2_start

    step = 0.1

    k_iter = int(k3_start//step)

    time_list = []
    k_list = []

    for i in range(k_iter):
        k1 = round(k1_start + i*step, 2)
        k2 = k2_start + i*step
        k3 = 1 - k1 - k2
        k3_iter = int(k3//step)
        for j in range(k3_iter):
            k3_k = round(k3 - step*j,2)
            k2_k = round(k2 + step*j,2)
            k_list.append([k1, k2_k, k3_k])
    
    for el in k_list:
        horizontal_lines.get_figure(*el)
        points = path.get_points()
        copter.points = points
        time_struct = copter.calculate_time()
        time_list.append([time_struct['fig1']['time'], time_struct['fig2']['time'], time_struct['fig3']['time']])#new times 
    
    index, min_time = optimize_time(time_list)
    horizontal_lines.get_figure(*k_list[index])
    points_optimize = path.get_points()
    copter.points = points_optimize
    time_struct = copter.calculate_time()

    stop_time = [time_struct['fig1']['iters_of_stop_points'], time_struct['fig2']['iters_of_stop_points'], time_struct['fig3']['iters_of_stop_points']]

    #get and write points of path with optimize k1 k2 k3
    with open('points.json', 'w') as js:
        json.dump(points_optimize, js)
    
    return stop_time