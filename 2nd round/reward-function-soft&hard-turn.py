import math

HARD_TURN_THRESHOLD = 23
STRAIGHT_ROUTE_THRESHOLD = 4
def get_clean_angle(direction):
    direction = math.degrees(direction)
    if direction>180:
        return 360 - direction
    elif direction<-180:
        return direction+360
    return abs(direction)
    # brings the angle within 180 degrees

def is_route_straight(angle):
    return abs(angle)<=STRAIGHT_ROUTE_THRESHOLD

def calc_on_turn(params):
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']

    curr_point = waypoints[closest_waypoints[0]]
    next_point = waypoints[closest_waypoints[1]]
    lookahead_point = waypoints[(closest_waypoints[1]+2)%len(waypoints)]

    curr_direction = math.atan2(next_point[1]-curr_point[1],next_point[0]-curr_point[0])
    lookahead_direction = math.atan2(lookahead_point[1]-next_point[1],lookahead_point[0]-next_point[0])

    curr_angle = get_clean_angle(curr_direction)
    lookahead_angle = get_clean_angle(lookahead_direction)

    route_straight = is_route_straight(curr_angle)

    if curr_angle>=HARD_TURN_THRESHOLD:
        reward = 10*(abs(curr_angle-heading))
        return reward,route_straight
    else:
        avg_direction = (curr_angle+lookahead_angle)//2
        #if its a soft left right now, and a soft right later, 
        #this will encourage the car to go almost straight
        reward = 10*abs(avg_direction-heading)
        return reward,route_straight

def reward_function(params):

    reward,route_straight = calc_on_turn(params)

    if params['is_offtrack']:
        return 1e-3
    else:
        reward+=10
        #this encourages the car to remain on track

        if route_straight:
            # encourage car to remain near the center
            track_width = params['track_width']
            distance_from_center = params['distance_from_center']
            marker_1 = 0.1 * track_width
            marker_2 = 0.25 * track_width
            marker_3 = 0.5 * track_width
            
            # Give higher reward if the car is closer to center line and vice versa
            if distance_from_center <= marker_1:
                reward += 10
            elif distance_from_center <= marker_2:
                reward += 5
            elif distance_from_center <= marker_3:
                reward += 1
            else:
                reward += 0.5  # likely crashed/ close to off track
    
    return reward


