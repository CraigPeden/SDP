from math import tan, pi, hypot, log
from planning.models import Robot

DISTANCE_MATCH_THRESHOLD = 15
ANGLE_MATCH_THRESHOLD = pi/10
BALL_ANGLE_THRESHOLD = pi/20
MAX_DISPLACEMENT_SPEED = 690
MAX_ANGLE_SPEED = 50
BALL_VELOCITY = 3


#constants that we will use below - please note that they should be calibrated

#we will use this speed when we want to do rotation
#the goal is to have a predictable behavior
#and control the rotation by the duration period
#of the run of the motors
MOTOR_ROTATION_SPEED = 3

#we will use this speed when we want to move forwards and backwards
#the goal is to control the length of the movement by the duration
#period of the run of the motors
MOTOR_MOVE_SPEED = 5

#this is the time that the motors need to run at MOTOR_ROTATION_SPEED in order to turn
#the robot at an angle of pi/5
ROTATION_DURATION_CONSTANT = 0.5

#this is the time that the motors need to run at MOTOR_MOVE_SPEED in order to move
#the robot at a distance of 50
MOTOR_MOVE_DURATION_CONSTANT = 1



def is_shot_blocked(world, our_robot, their_robot):
    '''
    Checks if our robot could shoot past their robot
    '''
    predicted_y = predict_y_intersection(
        world, their_robot.x, our_robot, full_width=True, bounce=True)
    if predicted_y is None:
        return True
    print '##########', predicted_y, their_robot.y, their_robot.length
    print abs(predicted_y - their_robot.y) < their_robot.length
    return abs(predicted_y - their_robot.y) < their_robot.length


def is_attacker_shot_blocked(world, our_attacker, their_defender):
    '''
    Checks if our attacker would score if it would immediately turn and shoot.
    '''

    # Acceptable distance that the opponent defender can be relative to our
    # shooting position in order for us to have a clear shot.
    distance_threshold = 40

    # Return True if attacker and defender ar close to each other on
    # the y dimension
    return abs(our_attacker.y - their_defender.y) < distance_threshold


def can_score(world, our_robot, their_goal, turn=0):
    # Offset the robot angle if need be
    robot_angle = our_robot.angle + turn
    goal_zone_poly = world.pitch.zones[their_goal.zone][0]

    reverse = True if their_goal.zone == 3 else False
    goal_posts = sorted(goal_zone_poly, key=lambda x: x[0], reverse=reverse)[:2]
    # Makes goal be sorted from smaller to bigger
    goal_posts = sorted(goal_posts, key=lambda x: x[1])

    goal_x = goal_posts[0][0]

    robot = Robot(
        our_robot.zone, our_robot.x, our_robot.y, robot_angle % (pi * 2), our_robot.velocity)

    predicted_y = predict_y_intersection(world, goal_x, robot, full_width=True)

    return goal_posts[0][1] < predicted_y < goal_posts[1][1]

def predict_y_intersection(world, predict_for_x, robot, full_width=False, bounce=False):
        '''
        Predicts the (x, y) coordinates of the ball shot by the robot
        Corrects them if it's out of the bottom_y - top_y range.
        If bounce is set to True, predicts for a bounced shot
        Returns None if the robot is facing the wrong direction.
        '''
        x = robot.x
        y = robot.y
        top_y = world._pitch.height - 60 if full_width else world.our_goal.y + (world.our_goal.width/2) - 30
        bottom_y = 60 if full_width else world.our_goal.y - (world.our_goal.width/2) + 30
        angle = robot.angle
        if (robot.x < predict_for_x and not (pi/2 < angle < 3*pi/2)) or (robot.x > predict_for_x and (3*pi/2 > angle > pi/2)):
            if bounce:
                if not (0 <= (y + tan(angle) * (predict_for_x - x)) <= world._pitch.height):
                    bounce_pos = 'top' if (y + tan(angle) * (predict_for_x - x)) > world._pitch.height else 'bottom'
                    x += (world._pitch.height - y) / tan(angle) if bounce_pos == 'top' else (0 - y) / tan(angle)
                    y = world._pitch.height if bounce_pos == 'top' else 0
                    angle = (-angle) % (2*pi)
            predicted_y = (y + tan(angle) * (predict_for_x - x))
            # Correcting the y coordinate to the closest y coordinate on the goal line:
            if predicted_y > top_y:
                return top_y
            elif predicted_y < bottom_y:
                return bottom_y
            return predicted_y
        else:
            return None


def grab_ball():
    return {'left_motor_speed': 0, 'right_motor_speed': 0, 'kicker_activated': 0, 'catcher_activated': 1, 'duration': 0.5}


def kick_ball():
    return {'left_motor_speed': 0, 'right_motor_speed': 0, 'kicker_activated': 1, 'catcher_activated': 0, 'duration': 0.5}


def open_catcher():
       return {'left_motor_speed': 0, 'right_motor_speed': 0, 'kicker_activated': 1, 'catcher_activated': 0, 'duration': 0.5}


def turn_shoot(orientation):
    turn_duration = 2.5 * ROTATION_DURATION_CONSTANT #since pi/2 is 2.5 * pi/5
    #if orientation == -1 then turn left 90 degrees, i.e. pi/2 and shoot
    if orientation == -1 :
     return {'left_motor_speed': -MOTOR_ROTATION_SPEED, 'right_motor_speed': MOTOR_ROTATION_SPEED, 'kicker_activated': 1, 'catcher_activated': 0, 'duration': turn_duration}
   #else turn right 90 degrees and shoot
    else :
     return {'left_motor_speed': MOTOR_ROTATION_SPEED, 'right_motor_speed': -MOTOR_ROTATION_SPEED, 'kicker_activated': 1, 'catcher_activated': 0, 'duration': turn_duration}

def has_matched(robot, x=None, y=None, angle=None,
                angle_threshold=ANGLE_MATCH_THRESHOLD, distance_threshold=DISTANCE_MATCH_THRESHOLD):
    dist_matched = True
    angle_matched = True
    if not(x is None and y is None):
        dist_matched = hypot(robot.x - x, robot.y - y) < distance_threshold
    if not(angle is None):
        angle_matched = abs(angle) < angle_threshold
    return dist_matched and angle_matched


def calculate_motor_speed(distance, angle, backwards_ok=False, careful=False):
    '''
    Simplistic view of calculating the speed: no modes or trying to be careful
    '''
    moving_backwards = False
    angle_thresh = BALL_ANGLE_THRESHOLD if careful else ANGLE_MATCH_THRESHOLD

    if backwards_ok and abs(angle) > pi/2:
        angle = (-pi + angle) if angle > 0 else (pi + angle)
        moving_backwards = True

    if not (distance is None):

        if distance < DISTANCE_MATCH_THRESHOLD:
             return {'left_motor_speed': 0, 'right_motor_speed': 0, 'kicker_activated': 0, 'catcher_activated': 0, 'duration': 1}

        elif abs(angle) > angle_thresh:
            duration = (abs(angle)/(pi/5)) * ROTATION_DURATION_CONSTANT
            if angle > 0 :
              return {'left_motor_speed': -MOTOR_ROTATION_SPEED, 'right_motor_speed': MOTOR_ROTATION_SPEED, 'kicker_activated': 0, 'catcher_activated': 0, 'duration': duration}
            elif angle <0 :
              return {'left_motor_speed': MOTOR_ROTATION_SPEED, 'right_motor_speed': -MOTOR_ROTATION_SPEED, 'kicker_activated': 0, 'catcher_activated': 0, 'duration': duration}

        else:
            motor_run_duration = log(distance, 10) * MOTOR_MOVE_DURATION_CONSTANT
            speed = -MOTOR_MOVE_SPEED if moving_backwards else MOTOR_MOVE_SPEED
            # print 'DISP:', displacement
            if careful:
                return {'left_motor': speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'duration': motor_run_duration}
            return {'left_motor': speed, 'right_motor': speed, 'kicker': 0, 'catcher': 0, 'duration': motor_run_duration}

    else:

        if abs(angle) > angle_thresh:
            duration = (abs(angle)/(pi/5)) * ROTATION_DURATION_CONSTANT
            if angle > 0 :
              return {'left_motor_speed': -MOTOR_ROTATION_SPEED, 'right_motor_speed': MOTOR_ROTATION_SPEED, 'kicker_activated': 0, 'catcher_activated': 0, 'duration': duration}
            elif angle <0 :
              return {'left_motor_speed': MOTOR_ROTATION_SPEED, 'right_motor_speed': -MOTOR_ROTATION_SPEED, 'kicker_activated': 0, 'catcher_activated': 0, 'duration': duration}

        else:
             return {'left_motor_speed': 0, 'right_motor_speed': 0, 'kicker_activated': 0, 'catcher_activated': 0, 'duration': 1}



def do_nothing():
    return calculate_motor_speed(0, 0)
