# 1
"""
Core formula:   1 degre * pi / 180 
"""

import math

def converter(degree):
    radian  = degree * math.pi / 180
    return radian

print(converter(15))