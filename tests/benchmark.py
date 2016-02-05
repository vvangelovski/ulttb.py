import time
from math import fabs, floor, sin, cos
from ulttb import downsample

class Timer(object):
    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

DATA = [
zip((sin(x)-2*cos(x-10) for x in xrange(512)), xrange(512)),
zip((sin(x)-2*cos(x-10) for x in xrange(10000)), xrange(10000)),
zip((sin(x)-2*cos(x-10) for x in xrange(100000)), xrange(100000)),
zip((sin(x)-2*cos(x-10) for x in xrange(1000000)), xrange(1000000))

]

def downsample_py(data, threshold):

    data_len = len(data)

    if data_len <= threshold:
        return data

    every = (data_len - 2.0)/(threshold - 2.0)

    a = 0  # Initially a is the first point in the triangle
    next_a = 0

    sampled = [data[0]]  # Always add the first point

    for i in range(0, threshold-2):
        # Calculate point average for next bucket (containing c)

        avg_x = 0.0
        avg_y = 0.0
        avg_range_start = (long) (floor((i+1.0)*every) + 1.0)
        avg_range_end = (long) (floor((i+2.0)*every) + 1.0)
        if avg_range_end > data_len:
            avg_range_end = data_len

        avg_range_length = avg_range_end - avg_range_start

        while avg_range_start < avg_range_end:
            avg_x += data[avg_range_start][0]
            avg_y += data[avg_range_start][1]
            avg_range_start += 1

        avg_x /= avg_range_length
        avg_y /= avg_range_length

        # Get the range for this bucket
        range_offs =long( (floor((i+0.0)*every) + 1.0))
        range_to =  long( (floor((i+1.0)*every) + 1.0))

        # Point a
        point_ax = data[a][0]
        point_ay = data[a][1]

        max_area = -1.0

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

def main():
    print 'Doing 25 passes of each downsampling call'
    print '%-14s|  %-14s|  %-14s|  %-14s|  %-14s'%\
        ('data length', 'result length', 'ulttb (sec)', 'python (sec)', 'speedup')
    for dataset in DATA:
        for threshold in (32, 64, 512, 1024, 4*1024):
            if threshold < len(dataset):
                with Timer() as t1:
                    for i in range(25): downsample(dataset, threshold)
                with Timer() as t2:
                    for i in range(25): downsample_py(dataset, threshold)
                print '======================================='*3
                print '%-14i|  %-14i|  %-14f|  %-14f|  %-14f'%\
                    (len(dataset), threshold, t1.interval, t2.interval, (t2.interval/t1.interval))


if __name__ == '__main__':
    main()
