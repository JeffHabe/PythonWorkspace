# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 01:40:23 2018

@author: Jeff PC
"""

from math import pi
import numpy as np
rad=45*(pi/180)
tan=np.tan(rad)
angle=np.arctan(tan)*180/pi
print(tan)
print(angle)