from openpyxl import Workbook

from openpyxl.utils import get_column_letter
import numpy as np
import matplotlib.pyplot as plt

#Assumes contacts are in horizontal array
def plot_line_profile(filename_formatted, array, y):
    #Adjusting for coordinate differences between picture and numpy array
    
    y = 256 - int(y*256/768)
    line_data = array[y, :]
    x = np.linspace(0,20,256)
    fig = plt.figure(figsize=(20,20))
    ax = plt.subplot(111)
    ax.plot(x, line_data, color ="blue")
    fig.tight_layout()
    img_path = "../AFMTOOL/line_profile_imgs/"+str(filename_formatted)+"line_plot"
    plt.savefig(img_path, bbox_inches='tight')