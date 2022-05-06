""" 
Function to calculate roughness(Ra) of a square region
Inputs- (x,y) coordinate the center of square and L, side length of square, in micrometer. 

Machine-learning algorithm in util/shape_recogniser will give the function the center of the Cu connections for input. 
Side length of square will be set by user

From https://www.olympus-ims.com/en/metrology/surface-roughness-measurement-portal/parameters/#!cms[focus]=007, 
Roughness Average (Ra) is given by average of absolute values of deviation from the mean of a given sample. 
"""

import pySPM
#print(pySPM.__version__)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
from IPython import display



