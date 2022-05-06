import pySPM
#print(pySPM.__version__)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
from util.mlScripts.circle_identifier import find_circles

import os
from IPython import display

filename = "data/3.spm"
scan = pySPM.Bruker(filename)
#scan.list_channels()

topo = scan.get_channel()
height_data = scan.get_channel("Height Sensor") 
amp_error_data = scan.get_channel("Amplitude Error") 
phase_data = scan.get_channel("Phase") 

#Correct data for slope
#TODO: Check if algorithm is same as currently used
height_data_correct_plane = height_data.correct_plane(inline=False)

fig, ax = plt.subplots(1, 1, figsize=(20, 20))

#phase_data.show(ax=ax[0])
height_data_correct_plane.show(ax=ax, cmap="copper")
#amp_error_data.show(ax=ax[2])

fig.tight_layout()
fig_path_2d = "../AFMTOOL/images/2d_height_plot"
plt.savefig(fig_path_2d)


#Get height data as numpy array
#Checked against AtomicJ, height data is in nm. 
height_array = height_data_correct_plane.pixels
#print(height_array)


#Plot 3D graph
# Create figure and add axis

fig = plt.figure(figsize=(20,20))
ax = plt.subplot(111, projection='3d')
# Remove gray panes and axis grid
ax.xaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.fill = False
ax.yaxis.pane.set_edgecolor('black')
ax.zaxis.pane.fill = False
ax.zaxis.pane.set_edgecolor('black')
ax.grid(False)
# Create meshgrid, grid labels will be in micrometer
X, Y = np.meshgrid(np.linspace(0, 20, len(height_array)), np.linspace(0, 20, len(height_array)))
# Plot surface
# TODO: Experiement with different colors
plot = ax.plot_surface(X=X, Y=Y, Z=height_array, cmap='copper')

fig.tight_layout()
fig_path_3d = "../AFMTOOL/images/3d_height_plot"
plt.savefig(fig_path_3d)


#Identify circles
find_circles(fig_path_2d)

