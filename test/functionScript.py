# functionScript.py
import sys
# You can use the triple-quote string in a print statement to
# print multiple lines.
print("""
Welcome to Mudball! The idea is to hit the other player with a mudball.
Enter your angle (in degrees) and the amount of PSI to charge your gun
with.""", 123)

for i in sys.path:
    print(i)

x = 5
y = 66
z = 777
print("C - '{2}' A - '{0}' B - '{1}' C again - '{2}'".format(x, y, z))
print("C - '{2:4}' A - '{0:4}' B - '{1:4}' C again - '{2:4}'".format(x, y, z))

my_fruit = ["Apples", "Oranges", "Grapes", "Pears"]
my_calories = [4, 300, 70, 30]

for i in range(4):
    print("{:>7} are {:<3} calories.".format(my_fruit[i], my_calories[i]))

# for hours in range(1,13):
#     for minutes in range(0,60):
#         print("Time {}:{}".format(hours, minutes))
#         print("Time {:02}:{:02}".format(hours, minutes)) # count 0

# ASCII
print(ord('A'))
