import time

from venv import create
import pySPM
#print(pySPM.__version__)

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("../")
from AFMTOOL.util.excel_utils.create_excel import create_xl_template, insert_xl, style_excel_final
from AFMTOOL.util.mlScripts.circle_identifier import find_circles, create_ml_img_dir
from AFMTOOL.util.roughness.roughness import find_ra, insert_ra
from AFMTOOL.util.line_profile.line_profile import insert_line_profile, plot_line_profile
from alive_progress import alive_bar

import os


#Dialogue box GUI to select file to analyze
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filename_list = list(filedialog.askopenfilenames(parent=root))
#print(filename_list[0])
start_time = time.time()

#Directory to store generated Excel reports
excel_file_path = create_xl_template()
#Directory to store ML generated imgs
ml_result_path = create_ml_img_dir()

#Clear images directory
dir = '../AFMTOOL/images/'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))
dir = '../AFMTOOL/line_profile_imgs/'
for f in os.listdir(dir):
    os.remove(os.path.join(dir, f))   
 
with alive_bar(len(filename_list)) as bar:
    file_no=1
    for filename in filename_list:
        scan = pySPM.Bruker(filename)
        #scan.list_channels()

        #topo = scan.get_channel()
        height_data = scan.get_channel("Height Sensor") 
        #amplitude_error_data = scan.get_channel("Amplitude Error") 
        #phase_data = scan.get_channel("Phase") 

        #Correct data for slope
        #TODO: Check if algorithm is same as currently used
        height_data_correct_plane = height_data.correct_plane(inline=False)
        
        #Plot of height data for Excel report 
        fig, ax = plt.subplots(1, 1, figsize=(20, 20))

        #phase_data.show(ax=ax[0])
        height_data_correct_plane.show(ax=ax, cmap="copper")
        #amp_error_data.show(ax=ax[2])

        fig.tight_layout()
        
        #Format filename for saving
        #Remove .spm at the end and replace '.' and space with '_'
        filename_formatted = filename.split("/")[-1][:-3].replace('.', '_').replace(' ', '_')
        img_path_2d = "../AFMTOOL/images/"+str(filename_formatted)+"2d_plot"
        #plt.style.use('dark_background')
        plt.axis('off')
        plt.title('')
        plt.savefig(img_path_2d, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
    
        #Get height data as numpy array
        #Checked against AtomicJ, height data is in nm. 
        height_array = height_data_correct_plane.pixels
        #print(height_array)
        
        #Identify copper contacts
        detected_circles = find_circles(filename_formatted, ml_result_path)
        
        if(detected_circles is None):
            insert_ra(excel_file_path, "Programme Error: Could not find any contact points", "Programme Error: Could not find any contact points", file_no)
        else:
            ra, pol_ra = find_ra(height_array, detected_circles)
            
            insert_ra(excel_file_path, ra, pol_ra, file_no)
            
            step_height = plot_line_profile(filename_formatted, height_array, detected_circles[0, :][0][0], detected_circles[0, :][0][1],  detected_circles[0, :][0][2])
            insert_line_profile(filename_formatted, excel_file_path, file_no, step_height)

        #Plot 3D graph
        # Create figure and add axis

        fig = plt.figure(figsize=(20,20))
        fig.patch.set_facecolor('black')
        #plt.style.use('dark_background')
        ax = plt.subplot(111, projection='3d')
        ax.patch.set_facecolor('black')
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
        plot = ax.plot_surface(X=X, Y=Y, Z=height_array, cmap='YlOrBr' ,rstride=1, cstride=1, alpha=None)

        fig.tight_layout()
        img_path_3d = "../AFMTOOL/images/"+str(filename_formatted)+"3d_plot"
        plt.savefig(img_path_3d)
        
        insert_xl(excel_file_path, img_path_2d, img_path_3d,file_no)
        plt.close(fig)
        
        
        file_no+=1  
        bar()

style_excel_final(excel_file_path)










print("[Code executed in %s seconds]" % (time.time() - start_time))





