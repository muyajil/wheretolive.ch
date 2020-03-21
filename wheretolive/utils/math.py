import math


def get_distance(s_lat, s_long, t_lat, t_long):
    s_lat = math.radians(s_lat)
    s_long = math.radians(s_long)
    t_lat = math.radians(t_lat)
    t_long = math.radians(t_long)
    a = (1 - math.cos(t_lat - s_lat)) / 2 + math.cos(s_lat) * math.cos(t_lat) * (
        1 - math.cos(t_long - s_long)
    ) / 2
    return 12742 * math.asin(math.sqrt(a))
