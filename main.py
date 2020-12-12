import parser_gps_and_convert_mission
import optimize
from copter import Copter
from example_path_finder import PathFinder

if __name__=="__main__":
    name_file = 'pole.kml'
    path = PathFinder()
    copter = Copter([])
    points_pole, proection_angle, base_point_gps = parser_gps_and_convert_mission.parse_kml_file(name_file)
    stop_iter_point = optimize.optimize_trajectory(copter, path)
    parser_gps_and_convert_mission.flight_mission(proection_angle,base_point_gps, stop_iter_point)