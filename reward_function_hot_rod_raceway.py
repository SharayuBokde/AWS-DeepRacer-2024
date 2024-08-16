def reward_function(params):

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    progress = params['progress']
    
    # Constants
    CENTER_LINE_REWARD = 1.0
    OFF_TRACK_PENALTY = 1e-3
    MAX_SPEED = 4.0  
    SPEED_THRESHOLD = 3.0  
    STEERING_THRESHOLD = 15.0  
    SMOOTH_STEERING_REWARD = 1.2
    PROGRESS_REWARD_MULTIPLIER = 1.5

    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    if distance_from_center <= marker_1:
        CENTER_LINE_REWARD = CENTER_LINE_REWARD
    elif distance_from_center <= marker_2:
        CENTER_LINE_REWARD = CENTER_LINE_REWARD * 0.5
    elif distance_from_center <= marker_3:
        CENTER_LINE_REWARD = CENTER_LINE_REWARD * 0.1
    else:
        CENTER_LINE_REWARD = OFF_TRACK_PENALTY  
    
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1],
                                 next_waypoint[0] - prev_waypoint[0])
    heading = params['heading']
    direction_diff = abs(track_direction - heading)
    
    if direction_diff < 10.0:  
        if speed >= SPEED_THRESHOLD:
            speed_reward = speed / MAX_SPEED
        else:
            speed_reward = 0.5
    else:
        if speed <= SPEED_THRESHOLD:
            speed_reward = speed / MAX_SPEED
        else:
            speed_reward = 0.5

    if steering_angle > STEERING_THRESHOLD:
        steering_penalty = 0.7
    else:
        steering_penalty = SMOOTH_STEERING_REWARD
    
    progress_reward = progress * PROGRESS_REWARD_MULTIPLIER
    
    reward = CENTER_LINE_REWARD * speed_reward * steering_penalty + progress_reward
    
    if not all_wheels_on_track:
        reward = OFF_TRACK_PENALTY
    
    return float(reward)
