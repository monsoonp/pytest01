import random
# Before this code, paste the selection sort and import random
def selection_sort(my_list):
    """ Sort a list using the selection sort """
    # Loop through the entire array
    for cur_pos in range(len(my_list)):
        # Find the position that has the smallest number
        # Start with the current position
        min_pos = cur_pos

        # Scan left to right (end of the list)
        for scan_pos in range(cur_pos + 1, len(my_list)):

            # Is this position smallest?
            if my_list[scan_pos] < my_list[min_pos]:
                # It is, mark this position as the smallest
                min_pos = scan_pos

        # Swap the two values
        temp = my_list[min_pos]
        my_list[min_pos] = my_list[cur_pos]
        my_list[cur_pos] = temp


def insertion_sort(my_list):
    """ Sort a list using the insertion sort """
    # Start at the second element (pos 1).
    # Use this element to insert into the
    # list.
    for key_pos in range(1, len(my_list)):

        # Get the value of the element to insert
        key_value = my_list[key_pos]

        # Scan from right to the left (start of list)
        scan_pos = key_pos - 1

        # Loop each element, moving them up until
        # we reach the position the
        while (scan_pos >= 0) and (my_list[scan_pos] > key_value):
            my_list[scan_pos + 1] = my_list[scan_pos]
            scan_pos = scan_pos - 1

        # Everything's been moved out of the way, insert
        # the key into the correct location
        my_list[scan_pos + 1] = key_value


def print_list(my_list):
    for item in my_list:
        print("{:3}".format(item), end="")
    print()


# Create a list of random numbers
my_list = []
for i in range(10):
    my_list.append(random.randrange(100))

# Try out the sort
print_list(my_list)
selection_sort(my_list)
# insertion_sort(my_list)
print_list(my_list)