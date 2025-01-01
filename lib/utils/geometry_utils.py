import math
import random

class GeometryUtils:
    @staticmethod
    def smallest_angle_difference(angle1: float, angle2: float):
        PI = math.pi
        angle = (angle2 - angle1) % (2 * PI)
        if angle >= PI:
            return angle - (2 * PI)
        elif angle < -PI:
            return angle + (2 * PI)
        return angle

    @staticmethod
    def normalize_angle(
        value: float,
        center: float,
        amplitude: float):
        
        value = value % (2 * amplitude)
        if value < -amplitude + center:
            value += 2 * amplitude
        elif value > amplitude + center:
            value -= 2 * amplitude
        return value

    @staticmethod
    def normalize_in_pi(radians: float):
        return GeometryUtils.normalize_angle(radians, 0, math.pi)

    @staticmethod
    def distance(
        position1: 'tuple[float, float]',
        position2: 'tuple[float, float]'
    ):
        x1, y1 = position1
        x2, y2 = position2

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    @staticmethod
    def angle_between_points(
        position1: 'tuple[float, float]',
        position2: 'tuple[float, float]'
    ):
        x1, y1 = position1
        x2, y2 = position2

        return math.atan2(y2 - y1, x2 - x1)

    @staticmethod
    def is_close(
        position1: 'tuple[float, float]', 
        position2: 'tuple[float, float]',
        tolerance: float
    ):
        return GeometryUtils.distance(position1, position2) < tolerance
    
    @staticmethod
    def circunferences_intersect(
        center1: 'tuple[float, float]',
        radius1: float,
        center2: 'tuple[float, float]',
        radius2: float
    ):
        distance = GeometryUtils.distance(center1, center2)
        return distance <= radius1 + radius2 and distance >= abs(radius1 - radius2)
    
    @staticmethod
    def find_intersection(
        line1: 'tuple[float, float, float]',
        line2: 'tuple[float, float, float]'
    ):
        """
        Extract coefficients (a, b, c) from line equations (ax + by = c)
        """
        a1, b1, c1 = line1
        a2, b2, c2 = line2

        determinant = a1 * b2 - a2 * b1

        if determinant == 0:
            return None

        x = (c1 * b2 - c2 * b1) / determinant
        y = (a1 * c2 - a2 * c1) / determinant

        return x, y
    
    @staticmethod
    def line_equation(
        point1: 'tuple[float, float]',
        point2: 'tuple[float, float]'
    ):
        """
        Return the equation of the line passing through two points in the form (a, b, c): (ax + by = c).
        """
        x1, y1 = point1
        x2, y2 = point2
        
        if x2 - x1 != 0:
            m = (y2 - y1) / (x2 - x1)
        else:
            return None
        
        b = y1 - m * x1

        return -m, 1, b
    
    @staticmethod
    def point_to_line_distance(
        point: 'tuple[float, float]',
        line_equation: 'tuple[float, float, float]'
    ):
        x, y = point
        a, b, c = line_equation
        return abs(a * x + b * y - c) / math.sqrt(a ** 2 + b ** 2)

    @staticmethod
    def is_between(
        point: 'tuple[float, float]',
        endpoint1: 'tuple[float, float]',
        endpoint2: 'tuple[float, float]',
        tolerance: float = 1e-10
    ):
        px, py = point
        x1, y1 = endpoint1
        x2, y2 = endpoint2
    
        cross_product = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)

        if abs(cross_product) > tolerance:
            return False
        
        dot_product = (px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)

        if dot_product < 0:
            return False
        
        squared_length = (x2 - x1) ** 2 + (y2 - y1) ** 2

        if dot_product > squared_length:
            return False
        
        return True
        
    @staticmethod
    def find_y(
        line_equation: 'tuple[float, float, float]',
        x: float
    ):
        a, b, c = line_equation

        if b == 0:
            None

        return (c - a * x) / b
    
    @staticmethod
    def line_equation_by_point_and_angle(
        point: 'tuple[float, float]',
        angle: float
    ):
        x, y = point
        m = math.tan(angle)
        b = y - m * x

        return -m, 1, b
    
    @staticmethod
    def get_midpoint(
        point1: 'tuple[float, float]',
        point2: 'tuple[float, float]'
    ):
        x1, y1 = point1
        x2, y2 = point2

        return (x1 + x2) / 2, (y1 + y2) / 2
    
    @staticmethod
    def get_vector_coordinates(
        magnitude: float,
        angle: float,
        x: float,
        y: float
    ):
        delta_x = magnitude * math.cos(angle)
        delta_y = magnitude * math.sin(angle)
        
        new_x = x + delta_x
        new_y = y + delta_y
        
        return new_x, new_y
    
    @staticmethod
    def angle_between_vectors(
        v1: 'list[float]',
        v2: 'list[float]'
    ):
        dot_prod = GeometryUtils.dot_product(v1, v2)

        mag_v1 = GeometryUtils.vector_magnitude(v1)
        mag_v2 = GeometryUtils.vector_magnitude(v2)

        cosine_angle = dot_prod / (mag_v1 * mag_v2)

        return math.acos(cosine_angle)
    
    @staticmethod
    def dot_product(
        v1: 'list[float]',
        v2: 'list[float]'
    ):
        return sum((a * b) for a, b in zip(v1, v2))

    @staticmethod
    def vector_magnitude(vector: 'list[float]'):
        return math.sqrt(sum(a**2 for a in vector))
    
    @staticmethod
    def get_random_uniform(min_value: float, max_value: float):
        return random.uniform(min_value, max_value)

    @staticmethod
    def closest_point_on_line_segment(
        point: 'tuple[float, float]',
        endpoint1: 'tuple[float, float]',
        endpoint2: 'tuple[float, float]'
    ):
        px, py = point
        x1, y1 = endpoint1
        x2, y2 = endpoint2

        if (x1, y1) == (x2, y2):
            return endpoint1

        dx = x2 - x1
        dy = y2 - y1

        t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)

        t = max(0, min(1, t))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return closest_x, closest_y
