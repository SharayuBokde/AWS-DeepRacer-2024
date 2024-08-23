import math

def reward_function(params):
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steering_angle = abs(params['steering_angle'])
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    # Define constants
    OFF_TRACK_PENALTY = 1e-3
    MAX_SPEED = 3.5
    SPEED_THRESHOLD = 2.5
    STEERING_THRESHOLD = 10.0
    DIRECTION_THRESHOLD = 5.0
    STEEP_ANGLE_THRESHOLD = 15.0
    STEEP_ANGLE_REWARD = 1.2
    PROGRESS_REWARD_MULTIPLIER = 2.0

    marker_1 = 0.05 * track_width
    marker_2 = 0.1 * track_width
    marker_3 = 0.2 * track_width

    if distance_from_center <= marker_1:
        center_line_reward = 2.0
    elif distance_from_center <= marker_2:
        center_line_reward = 1.0
    elif distance_from_center <= marker_3:
        center_line_reward = 0.5
    else:
        center_line_reward = OFF_TRACK_PENALTY

    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    track_direction = math.degrees(math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0]))

    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    if direction_diff < DIRECTION_THRESHOLD:
        direction_reward = 1.2
    else:
        direction_reward = 0.8

    if direction_diff > STEEP_ANGLE_THRESHOLD:
        steep_angle_reward = STEEP_ANGLE_REWARD
    else:
        steep_angle_reward = 1.0

    if direction_diff > STEEP_ANGLE_THRESHOLD:
        if speed > SPEED_THRESHOLD:
            speed_penalty = 0.5 * (MAX_SPEED - speed) / MAX_SPEED
        else:
            speed_penalty = 1.0
    else:
        if speed > SPEED_THRESHOLD:
            speed_penalty = 1.0
        else:
            speed_penalty = 1.5

    if steering_angle > STEERING_THRESHOLD:
        steering_penalty = 0.5
    else:
        steering_penalty = 1.0

    reward = center_line_reward * direction_reward * steep_angle_reward * speed_penalty * steering_penalty

    if not all_wheels_on_track:
        reward = OFF_TRACK_PENALTY

    return float(reward)
