import math

# Calculate heading change between consecutive waypoints
def calculate_heading_change(waypoints, closest_waypoints):
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]

    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1],
                                    next_waypoint[0] - prev_waypoint[0])
    track_direction = math.degrees(track_direction)
    heading_change = abs(track_direction - heading)
    if heading_change > 180:
        heading_change = 360 - heading_change

    return heading_change


def reward_function(params):
    '''
    Example of a reward function for AWS DeepRacer on Ross Raceway (counterclockwise).
    '''
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    progress = params['progress']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])  # Only need the absolute value of the steering angle
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Initialize the reward with a small number but not zero
    reward = 1e-3
    
    # Penalize if the car goes off track
    if not all_wheels_on_track:
        return reward  # Reward will be 1e-3 if the car is off track
    
    # Reward car for staying close to the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/close to off track

    # Reward for higher progress
    if progress == 100:
        reward += 10.0  # bonus for completing the lap
    
    # Reward for maintaining an appropriate speed
    SPEED_THRESHOLD = 1.0
    if speed > SPEED_THRESHOLD:
        reward += 0.5  # higher reward for driving faster

    # Penalize for steering too much to avoid zig-zagging
    ABS_STEERING_THRESHOLD = 15
    if steering_angle > ABS_STEERING_THRESHOLD:
        reward *= 0.8
        
    # Determine if the car is approaching a steep curve
    HEADING_THRESHOLD = 15  # Define a threshold for what constitutes a steep curve
    heading_change = calculate_heading_change(waypoints, closest_waypoints)
    is_steep_curve = heading_change > HEADING_THRESHOLD

    # Adjust rewards based on the curve
    if is_steep_curve:
        # Reduce speed and reward accordingly
        SPEED_THRESHOLD = 1.0
        if speed < SPEED_THRESHOLD:
            reward += 2.0  # Higher reward for reducing speed at steep curve
        else:
            reward -= 1.0  # Higher penalty for going too fast

        # Encourage smooth steering through the curve
        STEERING_THRESHOLD = 15
        if steering_angle < STEERING_THRESHOLD:
            reward += 2.0  # Higher reward for smooth steering
        else:
            reward -= 1.0  # Higher penalty for sharp steering

        # Encourage optimal path through the curve
        if distance_from_center < marker_2:
            reward += 1.0  # Bonus for maintaining optimal trajectory
    else:
        # General speed incentive on non-steep sections
        SPEED_THRESHOLD = 2.0
        if speed > SPEED_THRESHOLD:
            reward += 0.5  # reward for maintaining high speed
            
    return float(reward)
