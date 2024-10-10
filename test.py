import math

def get_angle_and_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    
    return angle, distance

# Example usage
point1 = (0, 0)
point2 = (-3, -1)

angle, distance = get_angle_and_distance(point1, point2)
print(f"Angle: {angle:.2f} degrees")
print(f"Distance: {distance:.2f} meters")
