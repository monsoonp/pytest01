class utill:
    # def __init__(self):

    def binary_search(arr, value):

        low = 0
        high = len(arr) - 1
        try:
            while low <= high:
                mid = (low + high) // 2

                if arr[mid] > value:
                    high = mid - 1
                elif arr[mid] < value:
                    low = mid + 1
                else:
                    return mid

            return -1
        except IOError:
            print("binary_search error occured!")

    # This program calculates a factorial
    # WITH recursion
    def factorial_recursive(n):
        if n == 1:
            return 1
        elif n > 1:
            return n * utill.factorial_recursive(n - 1)


# arr = [1, 5, 7, 10, 25, 32, 79, 80, 125]
# print(utill.binary_search(arr, 7))
# print(utill.binary_search(arr, 80))
# print(utill.binary_search(arr, 8))

