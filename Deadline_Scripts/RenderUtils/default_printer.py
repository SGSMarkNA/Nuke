"""
This file is called in not script file is passed to the 'Script' plugin in Deadline.
Prints any arguments you wish to pass in.  It is useful for debugging to test these against this file.
If you want to use argument parsing
"""
import sys

print('Your system arguments are:')

for i, j in enumerate(sys.argv):
    print("{}: {}".format(i, j))

print("You can also run an argument parser as normal")

