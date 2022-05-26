import time


import pySPM
#print(pySPM.__version__)

import sys
sys.path.append("../")
from AFMTOOL.util.excel_utils.create_excel import create_xl_template, insert_xl, style_excel_final
from AFMTOOL.util.mlScripts.circle_identifier import find_circles
from AFMTOOL.util.roughness.roughness import find_ra, insert_ra, insert_ref_image
from AFMTOOL.util.line_profile.line_profile import insert_line_profile, plot_line_profile
from AFMTOOL.util.ref_imgs.draw_ref_imgs import draw_ref_imgs
from AFMTOOL.util.draw_2d_3d_imgs.draw_imgs import draw_2d_plot, draw_3d_plot
from AFMTOOL.util.masking.masking import get_mask, create_mask_img_dir
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
mask_file_path = create_mask_img_dir()

#Clear data that no need to be stored/will be stored in Excel sheet
dir_to_clear = ['../AFMTOOL/images/', '../AFMTOOL/line_profile_imgs/', '../results/ref_regions_imgs/', '../AFMTOOL/misc/temp_images/binary_filter/', '../AFMTOOL/misc/temp_images/diff_cmap/', '../AFMTOOL/misc/temp_images/phase/']
for dir in dir_to_clear:
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))   
 
 
with alive_bar(len(filename_list)) as bar:
    file_no=1
    for filename in filename_list:
        scan = pySPM.Bruker(filename)
        #Uncomment below to show all channels provided by AFM 
        #scan.list_channels()
        
        #Format filename for saving
        #Remove .spm at the end and replace '.' and space with '_'
        filename_formatted = filename.split("/")[-1][:-3].replace('.', '_').replace(' ', '_')

        #topo = scan.get_channel()
        height_data = scan.get_channel("Height Sensor") 
        phase_data = scan.get_channel("Phase") 

        #Correct data for slope
        #TODO: Check if algorithm is same as currently used
        height_data_correct_plane = height_data.corr_fit2d(inline=False, nx=2, ny=2).filter_scars_removal()
        
        #Get height data as numpy array
        #Checked against AtomicJ, height data is in nm. 
        height_array = height_data_correct_plane.pixels
        
        #Plot of height data for Excel report 
        img_path_2d = draw_2d_plot(height_array, filename_formatted)
        
        #Identify copper contacts
        detected_circles = find_circles(filename_formatted, height_array, phase_data)
        
        
        
        if(detected_circles is None):
            insert_ra(excel_file_path, "Programme Error: Could not find any contact points", "Programme Error: Could not find any contact points", file_no)
        else:
            
            #Mask is a binary numpy array with 0 in squares containing a detected circle
            mask = get_mask(detected_circles, mask_file_path, filename_formatted)
            
            height_data_flattened_with_mask = height_data.corr_fit2d(mask = mask, inline=False, nx=3, ny=3).filter_scars_removal()
            height_array = height_data_flattened_with_mask.pixels
            
            #Use only best 3 circles detected for roughness calculations
            detected_circles = detected_circles[:, 0:3]
            ra, pol_ra, take_bottom_left, cu_ra_list, pol_ra_list = find_ra(height_array, detected_circles)
            
            insert_ra(excel_file_path, ra, pol_ra, file_no, cu_ra_list, pol_ra_list)
            
            step_height, pol_left_lim, pol_right_lim, roll_off= plot_line_profile(filename_formatted, height_array, detected_circles[0, :][0][0], detected_circles[0, :][0][1],  detected_circles[0, :][0][2])
            insert_line_profile(filename_formatted, excel_file_path, file_no, step_height, roll_off)
            
            draw_ref_imgs(height_array, detected_circles, filename_formatted, pol_left_lim, pol_right_lim, take_bottom_left)
            insert_ref_image(filename_formatted, excel_file_path, file_no)

        #Plot 3D graph
        img_path_3d = draw_3d_plot(height_array, filename_formatted)
        
        insert_xl(excel_file_path, img_path_2d, img_path_3d,file_no)
        
        file_no+=1  
        bar()

style_excel_final(excel_file_path)










print("[Code executed in %s seconds]" % (time.time() - start_time))





