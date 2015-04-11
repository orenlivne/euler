'''Pete has some trouble slicing a 20-inch (diameter) pizza. His first two cuts (from center to circumference of the pizza) make a 30 degree slice. He continues making cuts until he has gone around the whole pizza, each time trying to copy the angle of the previous slice but in fact adding 2 degrees each time. That is, he makes adjacent slices of 30 degrees, 32 degrees, 34 degrees, and so on. What is the area of the smallest slice?'''

def slice_locations(initial_angle, angle_increment, max_slices=1000):
    slice_size, end_of_current_slice, slice_angles, i = initial_angle, 0, set([]), 0
    #  while end_of_current_slice not in slice_angles:
    while i < max_slices:
        print 'slice', end_of_current_slice, 'to', (end_of_current_slice + slice_size) % 360, 'size', slice_size
        slice_angles.add(end_of_current_slice)
        end_of_current_slice = (end_of_current_slice + slice_size) % 360
        slice_size += angle_increment
        i += 1
    return sorted(slice_angles)

def min_slice_size(slice_angles):
    return min((slice_angles[i+1]-slice_angles[i]) % 360 for i in xrange(len(slice_angles)-1))

if __name__ == '__main__':
    print min_slice_size(slice_locations(30, 2))
