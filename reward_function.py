import math

def check_direction(waypoints,closest_waypoints,heading,reward):
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 10.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward *= 0.5

    return reward

def dist(pt1, pt2):
    return ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5


def rect(r, theta):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def polar(x, y):
    r = (x ** 2 + y ** 2) ** .5
    theta = math.degrees(math.atan2(y,x))
    return r, theta


def angle_mod_360(angle):
    n = math.floor(angle/360.0)
    angle_between_0_and_360 = angle - n*360.0

    if angle_between_0_and_360 <= 180.0:
        return angle_between_0_and_360
    else:
        return angle_between_0_and_360 - 360


def get_waypts_ordered_in_driving_direction(params):
    if params['is_reversed']: 
        return list(reversed(params['waypoints']))
    else: 
        return params['waypoints']


def up_sample(waypts, factor):
    p = waypts
    n = len(p)
    return [[i / factor * p[(j+1) % n][0] + (1 - i / factor) * p[j][0],
             i / factor * p[(j+1) % n][1] + (1 - i / factor) * p[j][1]] for j in range(n) for i in range(factor)]


def get_target_pt(params):
    waypts = up_sample(get_waypts_ordered_in_driving_direction(params), 20)
    car = [params['x'], params['y']]
    distances = [dist(p, car) for p in waypts]
    min_dist = min(distances)
    i_closest = distances.index(min_dist)
    n = len(waypts)
    waypts_starting_with_closest = [waypts[(i+i_closest) % n] for i in range(n)]
    r = params['track_width'] * 0.7
    is_inside = [dist(p, car) < r for p in waypts_starting_with_closest]
    i_first_outside = is_inside.index(False)
    if i_first_outside < 0:  
        return waypts[i_closest]

    return waypts_starting_with_closest[i_first_outside]


def get_target_steering_degree(params):
    tx, ty = get_target_pt(params)
    car_x = params['x']
    car_y = params['y']
    dx = tx-car_x
    dy = ty-car_y
    heading = params['heading']
    _, target_angle = polar(dx, dy)
    steering_angle = target_angle - heading
    return angle_mod_360(steering_angle)


def score_steer_to_pt_ahead(params):
    best_stearing_angle = get_target_steering_degree(params)
    steering_angle = params['steering_angle']
    error = (steering_angle - best_stearing_angle) / 50.0  
    score = 1.0 - abs(error)
    return max(score, 0.01) 


def reward_function(params):
    # steering
    reward = 2*score_steer_to_pt_ahead(params)
    
    # # speed
    # speed = params['speed']
    # if(speed>=2.5):
    #     reward+=1
    # elif(speed>1.5):
    #     reward+=0.5
    # else:
    #     reward+=0.2

    # # steps
    # steps = params['steps']
    # progress = params['progress']
    # if (steps % 100) == 0 and progress < (steps / 4):
    #     reward -= 0.5
        
    # distance from center
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    if distance_from_center <= marker_1:
        reward += 1.0
    elif distance_from_center <= marker_2:
        reward += 0.8
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += 0
        

    # all wheels on track
    all_wheels_on_track = params['all_wheels_on_track']
    if not all_wheels_on_track:
        reward = 0
    else:
        reward += 1.0
        
    # reading all inputs
    heading = params['heading']
    track_width = params['track_width']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    
    reward = check_direction(waypoints,closest_waypoints,heading,reward)

        
    return float(reward)
