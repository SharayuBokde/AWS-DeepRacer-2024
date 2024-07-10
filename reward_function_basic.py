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

    # Reward for higher progress
    if progress == 100:
        reward += 10.0  # bonus for completing the lap
    
    # Reward for maintaining an appropriate speed
    SPEED_THRESHOLD = 1.5
    if speed > SPEED_THRESHOLD:
        reward += 1.5  # higher reward for driving faster

    # Penalize for steering too much to avoid zig-zagging
    if steering_angle > 15:
        reward *= 0.7
    elif steering_angle >= 8 and steering_angle < 15:
        reward *= 0.9
    elif steering_angle == 0:
        reward *= 1.1


    return float(reward)
