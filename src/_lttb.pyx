cdef extern from "math.h":
    double floor(double x)
    double fabs(double x)


def downsample(data, long threshold):
    cdef long data_len,avg_range_start,avg_range_end,avg_range_end_,range_offs, a, next_a, range_to
    cdef float avg_x, avg_y, avg_range_length, point_ax, point_ay,  every
    cdef double area, max_area


    if not (not hasattr(data, "strip") and
            hasattr(data, "__getitem__") or
            hasattr(data, "__iter__")):
         raise ValueError("Data must be listlike.")

    data_len = len(data)


    if data_len <= threshold:
        raise ValueError("Threshold must be smaller than the length of the data.")

    every = (data_len - 2.0)/(threshold - 2.0)

    a = 0  # Initially a is the first point in the triangle
    next_a = 0
    max_area_point = (0.0, 0.0)

    sampled = [data[0]]  # Always add the first point

    for i in range(0, threshold-2):
        # Calculate point average for next bucket (containing c)

        avg_x = 0.0
        avg_y = 0.0
        avg_range_start = (long) (floor((i+1.0)*every) + 1.0)
        avg_range_end_ = (long) (floor((i+2.0)*every) + 1.0)
        if avg_range_end_ < data_len:
            avg_range_end = avg_range_end_
        else:
            avg_range_end = data_len

        avg_range_length = avg_range_end - avg_range_start

        while avg_range_start < avg_range_end:
            avg_x += data[avg_range_start][0]
            avg_y += data[avg_range_start][1]
            avg_range_start += 1

        avg_x /= avg_range_length
        avg_y /= avg_range_length

        # Get the range for this bucket
        range_offs =(long) (floor((i+0.0)*every) + 1.0)
        range_to = (long) (floor((i+1.0)*every) + 1.0)

        # Point a
        point_ax = data[a][0]
        point_ay = data[a][1]

        max_area = -1

        while range_offs < range_to:
            # Calculate triangle area over three buckets
            area = fabs((point_ax - avg_x)*(data[range_offs][1] - point_ay) -
                             (point_ax - data[range_offs][0])*(avg_y-point_ay))*0.5
            if area > max_area:
                max_area = area
                max_area_point = data[range_offs]
                next_a = range_offs  # Next a is this b
            range_offs += 1

        sampled.append(max_area_point)  # Pick this point from the bucket
        a = next_a  # This a is the next a (chosen b)

    sampled.append(data[data_len-1])  # Always add last

    return sampled
