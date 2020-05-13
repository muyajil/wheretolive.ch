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


def add_thousands_sep(total_amount_str):
    splits = total_amount_str.split(".")
    if len(splits) < 2:
        main = total_amount_str
    else:
        main, decimal = splits
    if len(main) > 3:
        main_reversed = main[::-1]
        idx = 3
        while idx < len(main):
            main_reversed = main_reversed[:idx] + "'" + main_reversed[idx:]
            idx += 4
        main = main_reversed[::-1]
    if len(splits) < 2:
        return main
    else:
        return main + "." + decimal
