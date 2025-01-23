from math import cos, pi, sin, sqrt, atan2, exp
import numpy as np
from lib.domain.univector_field_navigation.obstacle import Obstacle

d_e = 0.0537
kr = 0.0415
k0 = 0.0012
d_min = 0.0948
gaussian_delta = 0.0457

def get_vector(
    point1: 'tuple[float, float]',
    point2: 'tuple[float, float]'
):
    return point2[0] - point1[0], point2[1] - point1[1]

def gaussian(r: float):
    return exp(-(r ** 2 / (2 * gaussian_delta ** 2)))

def get_vector_norm(vector: 'tuple[float, float]'):
    return sqrt(vector[0] ** 2 + vector[1] ** 2)

def wrap_to_pi(angle: float):
    if angle > pi:
        return angle - 2 * pi
    if angle < -pi:
        return 2 * pi + angle
    else:
        return angle

def get_closest_obstacle(
    position: 'tuple[float, float]',
    obstacles: 'list[Obstacle]'
):
    last_ro = 0
    count = 0
    returned_obstacle = None

    for obstacle in obstacles:
        vector = get_vector(position, obstacle.position)
    
        if not count:
            last_ro = get_vector_norm(vector)
    
        if get_vector_norm(vector) <= last_ro:
            returned_obstacle = obstacle
            last_ro = get_vector_norm(vector)

        count += 1

    return returned_obstacle

def n_h(phi: float):
    return np.array([cos(phi), sin(phi)])

def phi_auf(
    obstacle: Obstacle,
    robot_position: 'tuple[float, float]',
    robot_velocity: 'tuple[float, float]',
    point_obstacle_distance: float
):
    obstacle_position = np.array(obstacle.position)
    obstacle_velocities = np.array(obstacle.velocities)
    velocities = np.array(robot_velocity)

    shifting_vector = k0 * (obstacle_velocities - velocities)
    shifting_vector_norm = get_vector_norm(shifting_vector)

    if point_obstacle_distance >= shifting_vector_norm:
        virtual_obstacle_position = obstacle_position + shifting_vector
    else:
        virtual_obstacle_position = obstacle_position \
            + point_obstacle_distance * shifting_vector / shifting_vector_norm

    vector = get_vector(virtual_obstacle_position, robot_position)
    phi_auf = phi_r(vector)
    
    return wrap_to_pi(phi_auf)

def phi_composed(
    phi_tuf_value: float,
    phi_auf_value: float,
    distance: 'float | None',
    obstacle: 'Obstacle | None'
):
    if obstacle is None:
        phi_composed_value = wrap_to_pi(phi_tuf_value)
    else:
        gaussian_value = gaussian(distance - d_min)
        
        if distance <= d_min:
            phi_composed_value = phi_auf_value
        else:
            diff = wrap_to_pi(phi_auf_value - phi_tuf_value)
            phi_composed_value = wrap_to_pi(gaussian_value * diff + phi_tuf_value)  

    return wrap_to_pi(phi_composed_value)

def phi_h(
    rho: float,
    theta: float,
    clockwise: bool
):
    if rho > d_e:
        angle = (pi / 2) * (2 - ((d_e + kr) / (rho + kr)))
    elif 0 <= rho <= d_e:
        angle = (pi / 2) * sqrt(rho / d_e)

    if clockwise:
        return wrap_to_pi(theta + angle)
    else:
        return wrap_to_pi(theta - angle)

def phi_r(vector: 'tuple[float, float]'):
    return atan2(vector[1], vector[0])

def phi_tuf(
    theta: float,
    vector: 'tuple[float, float]'
):
    y_l = vector[1] + d_e
    y_r = vector[1] - d_e

    ro_l = get_vector_norm((vector[0], vector[1] - d_e))
    ro_r = get_vector_norm((vector[0], vector[1] + d_e))

    phi_counter_clockwise = phi_h(ro_l, theta, False)
    phi_clockwise = phi_h(ro_r, theta, True)

    nh_counter_clockwise = n_h(phi_counter_clockwise)
    nh_clockwise = n_h(phi_clockwise)

    spiral_merge = (abs(y_l) * nh_counter_clockwise + abs(y_r) * nh_clockwise) / (2 * d_e) 

    if -d_e <= vector[1] < d_e:
        phi_tuf_value = atan2(spiral_merge[1], spiral_merge[0])
    elif vector[1] < -d_e:
        phi_tuf_value = phi_h(ro_l, theta, True)
    else:
        phi_tuf_value = phi_h(ro_r, theta, False)

    return wrap_to_pi(phi_tuf_value)

def get_univector_field_point(
    robot_position: 'tuple[float, float]',
    robot_velocity: 'tuple[float, float]',
    desired_position: 'tuple[float, float]',
    obstacles: 'list[Obstacle]'
):
    point_desired_vector = get_vector(
        desired_position,
        robot_position)

    theta = phi_r(point_desired_vector)

    phi_tuf_value = phi_tuf(
        theta,
        point_desired_vector)

    return get_phi_composed_value(
        phi_tuf_value,
        robot_position,
        robot_velocity,
        obstacles)

def get_phi_composed_value(
    phi_tuf_value: float,
    robot_position: 'tuple[float, float]',
    robot_velocity: 'tuple[float, float]',
    obstacles: 'list[Obstacle]'
):
    if len(obstacles) == 0:
        return wrap_to_pi(phi_tuf_value)

    return get_phi_composed_value_when_there_exists_obstacle(
        phi_tuf_value,
        robot_position,
        robot_velocity,
        obstacles)

def get_phi_composed_value_when_there_exists_obstacle(
    phi_tuf_value: float,
    robot_position: 'tuple[float, float]',
    robot_velocity: 'tuple[float, float]',
    obstacles: 'list[Obstacle]'
):
    obstacle = get_closest_obstacle(robot_position, obstacles)
    obstacle_point_vector = get_vector(
        obstacle.position,
        robot_position)

    obstacle_point_distance = get_vector_norm(obstacle_point_vector)

    phi_auf_value = phi_auf(
        obstacle,
        robot_position,
        robot_velocity,
        obstacle_point_distance)

    return phi_composed(
        phi_tuf_value,
        phi_auf_value,
        obstacle_point_distance,
        obstacle)
