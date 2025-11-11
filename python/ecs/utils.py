def map_range(value, range1=(0, 0), range2=(0, 0)):
    ''' Returns the equivalent of value in range1 in range2 '''
    return float((value - range1[0]) * ((range2[1] - range2[0]) / (range1[1] - range1[0])) + range2[0])


def calculate_points_on_circle(pos=(0, 0), r=10, num=10):
    result = []
    if num < 2: num = 2

    import math
    angle_part = (math.pi * 2) / int(num)
    actual_angle = 0

    for i in range(0, int(num)):
        x = pos[0] + r * math.sin(actual_angle)
        y = pos[1] + r * math.cos(actual_angle)
        actual_angle += angle_part
        result.append((x, y))
    return result