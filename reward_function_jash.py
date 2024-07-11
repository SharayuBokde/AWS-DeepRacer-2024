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

def angle_between_points(first_point, x, third_point):
    """Calculates the angle between two line segments formed by three points."""
    first_dx = first_point[0] - x
    first_dy = first_point[1] - 0
    third_dx = third_point[0] - x
    third_dy = third_point[1] - 0
    angle = math.atan2(third_dy, third_dx) - math.atan2(first_dy, first_dx)
    return math.degrees(angle)


def find_next_three_waypoints(params):
    waypoints = params['waypoints']
    next_points = (list(range(params['closest_waypoints'][1], params['closest_waypoints'][1] + 3)))
    for i in range(len(next_points)):
        if next_points[i] > len(waypoints):
            next_points[i] -= len(waypoints)
    return next_points

def calculate_optimal_angle(params,best_stearing_angle):
    steering_angle = params['steering_angle']
    error = abs((abs(steering_angle) - abs(best_stearing_angle))) / 50.0 
    score = 1.0 - abs(error)
    return max(score, 0.01) 


def reward_function(params):
    # steering
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])  # Only need the absolute value of the steering angle

    # Initialize the reward with a small number but not zero
    reward = 1e-3
    
    # Penalize if the car goes off track
    if not all_wheels_on_track:
        return reward  # Reward will be 1e-3 if the car is off track
    else:
        reward += 5.0

    # Reward car for staying close to the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if distance_from_center <= marker_1:
        reward += 2.5
    elif distance_from_center <= marker_2:
        reward += 1.5
    elif distance_from_center <= marker_3:
        reward += 0.1
    else:
        reward += 1e-3  # likely crashed/close to off track

    # Off track penalty
    is_offtrack = params['is_offtrack']
    if is_offtrack:
        reward = reward*0.5
        
    # Reward for higher progress
    if progress == 100:
        reward += 10.0  # bonus for completing the lap
    
    # Reward for maintaining an appropriate speed
    SPEED_THRESHOLD = 1.5
    if speed > SPEED_THRESHOLD:
        reward += 1.5
    waypoints = params['waypoints']
    # Get current position
    x = params['x']
    y = params['y']

    next_points = find_next_three_waypoints(params)
    
    first_point = waypoints[next_points[0]]
    third_point = waypoints[next_points[2]]
    curvature = angle_between_points(first_point, x, third_point)

    # Optimal speed based on curvature
    min_speed, max_speed = 1, 4
    # Changed to continuous function for optimal speed calculation
    optimal_speed = max_speed - (curvature / 180) * (max_speed - min_speed)

    # Calculate reward for speed
    speed_diff = abs(params['speed'] - optimal_speed)
    reward += 5*math.exp(-0.5 * speed_diff)
    
    # closest_waypoints = params['closest_waypoints']
    # heading = params['heading']
    
    # reward += calculate_optimal_angle(params,curvature)

    # reward = check_direction(waypoints,closest_waypoints,heading,reward)

        
    return float(reward)
