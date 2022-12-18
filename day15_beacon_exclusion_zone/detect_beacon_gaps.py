import os
import sys
from typing import List, Tuple, Union
from tqdm import tqdm
from multiprocessing import Pool, Process

SENSORS_MEMOIZATION = []


def to_tuple(string) -> Tuple:
    return (int(string[string.find('x=')+2:string.find(',')]),
            int(string[string.find('y=')+2:]))


def parse_measures(filename: str):
    data = []
    n_cols = 0
    n_rows = 0
    sensors = []
    beacons = []
    positions = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            sensor, beacon = line.split(':')
            sensors.append(to_tuple(sensor))
            beacons.append(to_tuple(beacon))
    return sensors, beacons


def dist(a, b):
    x_a, y_a = a
    x_b, y_b = b
    dist_x = abs(x_b - x_a)
    dist_y = abs(y_b - y_a)
    return dist_x+dist_y


def check_in(value, min, max):
    # print('value', value)
    # print('min', min)
    # print('max', max)
    return True if (value > min) and (value < max) else False


def find_limits(sensors, beacons):
    x_lims = [0, 0]
    y_lims = [0, 0]
    positions = sensors.copy()
    positions.extend(beacons.copy())

    for s, b in zip(sensors, beacons):
        d = dist(s, b)
        x_mi, y_mi = s[0] - d, s[1]-d
        x_ma, y_ma = s[0] + d, s[1] + d
        if x_lims[0] > x_mi:
            x_lims[0] = x_mi
        if x_lims[1] < x_ma:
            x_lims[1] = x_ma
        if y_lims[0] > y_mi:
            y_lims[0] = y_mi
        if y_lims[1] < y_ma:
            y_lims[1] = y_ma

    return x_lims, y_lims


def check_line(line, sensors: List, beacons: List, x_lims, y_lims) -> List:
    positions = sensors.copy()
    positions.extend(beacons.copy())
    x_min, x_max = x_lims
    # print(x_min, ',', x_max)
    scan = ['.']*(x_max-x_min+1)
    # print(' '.join(scan))
    for s, b in zip(sensors, beacons):
        d = dist(s, b)
        x_mi, y_mi = s[0] - d, s[1]-d
        x_ma, y_ma = s[0] + d, s[1] + d
        for i in range(x_min, x_max+1):
            # print(i, s[0], s[1])
            if (s[1] == line and s[0] == i):
                scan[i-x_min] = 'S'
            elif (b[1] == line and b[0] == i):
                scan[i-x_min] = 'B'
            elif check_in(line, y_mi-1, y_ma+1) and check_in(i, x_mi-1, x_ma+1) and \
                    dist(s, (i, line)) <= d:
                scan[i-x_min] = '#'
    return scan


def find_beacon(interval, measures, x_lims, y_lims, result):
    beacon = None
    for i in tqdm(range(interval[0], interval[1]+1)):
        line = check_line(i, measures[0], measures[1], x_lims, [])
        try:
            a = line.index('.')
            beacon = (a, i)
            print('beacon found at ', beacon)
            result.append(beacon)
            return
        except:
            pass
    if beacon is not None:
        x, y = beacon
        print(f'beacon possibility found at {beacon}')
        print(f'beacon freq is {x*4000000+y}')
    result.append(beacon)


def compute_sensors(sensors, beacons):
    sensors_list = []
    positions = sensors.copy()
    positions.extend(beacons.copy())

    for s, b in zip(sensors, beacons):
        d = dist(s, b)
        sensors_list.append((s, d))

    return sensors_list


def find_nearest(line: int, x: int, sensors: List[Tuple]) -> Tuple:
    import math
    min_dist = math.inf
    index = -1
    index_dist = -1
    advance_capabilities = 0

    for i, sensor in enumerate(sensors):
        s_pos = sensor[0]
        relative_distance = dist((x, line), s_pos)
        advance = sensor[1] - relative_distance
        # print(d)
        if relative_distance < min_dist:
            min_dist = relative_distance
            index_dist = i
        if advance > advance_capabilities:
            advance_capabilities = advance
            index = i

    # print(
    #     f'position{(x,line)} has the nearest sensor at {sensors[index][0]} with a distance {sensors[index][1]}')
    return sensors[index] if index >= 0 else sensors[index_dist]


def check_if_empty(point, sensors):
    out = True
    for sensor in sensors:
        out &= dist(point, sensor[0]) > sensor[1]
    return out


def analyze_line(line, x_max, sensors):
    index = 0
    while index < x_max:
        nearest_sensor = find_nearest(line, index, sensors)
        if check_if_empty((index, line), sensors):
            print(f'\nfound at {index,line}')
            print(f'Tuning freq = {index*4000000 + line}')
            return
        y_diff = abs(nearest_sensor[0][1]-line)
        x_diff = abs(nearest_sensor[0][0]-index)
        new_x = nearest_sensor[0][0] + nearest_sensor[1] - y_diff
        if new_x > index:
            index = new_x+1
        else:
            index += 1


if __name__ == "__main__":
    # Read the input file in the first argument
    input_file = ""
    visualize = False
    if len(sys.argv) > 2:
        input_file = sys.argv[1]
        visualize = bool(sys.argv[2])
    elif len(sys.argv) > 1:
        input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print("file provided does not exists")
        sys.exit(1)
    measures = parse_measures(input_file)

    # Part1
    x_lims, y_lims = find_limits(*measures)
    print('x_lims=', x_lims)
    print('y_lims=', y_lims)
    if visualize:
        lines = []
        for i in range(0, x_lims[1]+1):
            lines.append(check_line(i, *measures, x_lims, y_lims))

        for line in lines:
            print(' '.join(line))

    line = 10
    # line = 2000000
    n_empty = check_line(line, *measures, x_lims, y_lims).count('#')
    print(
        f' the number of positions that cannot contain beacons at line {line} is {n_empty}')

    # Part2
    x_lims = [0, 20]
    y_lims = [0, 20]
    # x_lims = [0, 4000000]
    # y_lims = [0, 4000000]

    sensors = compute_sensors(*measures)
    lines = []
    # analyze_line(0, x_lims[1]+1, sensors)
    for i in tqdm(range(0, x_lims[1]+1)):
        analyze_line(i, x_lims[1]+1, sensors)
