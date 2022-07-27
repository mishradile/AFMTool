import time

import sys
import PySimpleGUI as sg
sys.path.append("../")
from AFMTOOL.util.excel_utils.create_excel import create_xl_template, insert_xl, style_excel_final
from AFMTOOL.util.mlScripts.circle_identifier import find_circles
from AFMTOOL.util.roughness.roughness import find_ra, insert_ra, insert_ref_image
from AFMTOOL.util.line_profile.line_profile import insert_line_profile, plot_line_profile
from AFMTOOL.util.ref_imgs.draw_ref_imgs import draw_ref_imgs
from AFMTOOL.util.draw_2d_3d_imgs.draw_imgs import draw_2d_plot, draw_3d_plot
from AFMTOOL.util.masking.masking import get_mask, create_mask_img_dir
from AFMTOOL.util.file_reader.file_reader import Bruker
from AFMTOOL.util.gui.gui import launch_gui, done_gui
from AFMTOOL.util.makedirs import gen_dir
from alive_progress import alive_bar
import os

#Launch GUI, and get any optional inputs given
filename_list, show_all, pitch, minRadius, maxRadius, exclude, cwinsize, polwinsize, vert_line, cu_sh_width = launch_gui()

start_time = time.time()

#Directory to store generated Excel reports
gen_dir()
excel_file_path = create_xl_template()
mask_file_path = create_mask_img_dir()


#Clear data that no need to be stored/will be stored in Excel sheet
dir_to_clear = ['../AFMTOOL/images/', '../AFMTOOL/line_profile_imgs/', '../results/ref_regions_imgs/', '../AFMTOOL/misc/temp_images/binary_filter/', '../AFMTOOL/misc/temp_images/diff_cmap/', '../AFMTOOL/misc/temp_images/phase/', '../AFMTOOL/misc/temp_images/phase_binary/']
for dir in dir_to_clear:
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))   
 
 

file_no=1
sg.one_line_progress_meter('Progress Meter', 0, len(filename_list),'No. of files processed', orientation = 'h')
for filename in filename_list:
    scan = Bruker(filename)
    #Uncomment below to show all channels provided by AFM 
    #scan.list_channels()
    
    #Format filename for saving
    #Remove .spm at the end and replace '.' and space with '_'
    filename_formatted = filename.split("/")[-1][:-3].replace('.', '_').replace(' ', '_')

    #topo = scan.get_channel()
    try:
        height_data = scan.get_channel("Height Sensor") 
        phase_data = scan.get_channel("Phase") 
    except:
        height_data = scan.get_channel("Height") 
        phase_data = None
    #Correct data for slope
    #TODO: Check if algorithm is same as currently used
    height_data_correct_plane = height_data.corr_fit2d(inline=False, nx=2, ny=2).filter_scars_removal()
    
    #Get height data as numpy array
    #Checked against AtomicJ, height data is in nm. 
    height_array = height_data_correct_plane.pixels
    
    #Plot of height data for Excel report 
    img_path_2d = draw_2d_plot(height_array, filename_formatted)
    
    #Identify copper contacts
    detected_circles = find_circles(filename_formatted, height_array, phase_data, minRadius, maxRadius, pitch)
    
    
    
    if(detected_circles is None):
        insert_ra(excel_file_path, "Programme Error: Could not find any Cu pads. Skipping to next file", "", file_no, "nil", "nil")
    else:
        
        #Mask is a binary numpy array with 0 in squares containing a detected circle
        mask = get_mask(detected_circles, mask_file_path, filename_formatted)
        
        height_data_flattened_with_mask = height_data.corr_fit2d(mask = mask, inline=False, nx=3, ny=3).filter_scars_removal()
        height_array = height_data_flattened_with_mask.pixels
        
        #Unless user specify useALL flag, use only best 3 circles detected for roughness calculations
        if not show_all:
            detected_circles = detected_circles[:, 0:3]
        else:
            detected_circles = detected_circles[:, 0:15]
        
        #Convert string to list, if None give empty list
        exclude_list = [] if exclude is None else list(map(int, exclude.split(',')))
        #Find index of best cirlce not excluded
        best_circle_index =0
        while(best_circle_index+1 in exclude_list):
            best_circle_index+=1
        ra, pol_ra, take_bottom_left, cu_ra_list, pol_ra_list = find_ra(height_array, detected_circles, exclude_list, cwinsize, polwinsize)
        
        insert_ra(excel_file_path, ra, pol_ra, file_no, cu_ra_list, pol_ra_list)
        
        #Outputs in um
        step_height, pol_left_lim, pol_right_lim, roll_off= plot_line_profile(filename_formatted, height_array, vert_line, cu_sh_width, detected_circles[0, :][best_circle_index][0], detected_circles[0, :][best_circle_index][1],  detected_circles[0, :][best_circle_index][2])
        
        insert_line_profile(filename_formatted, excel_file_path, file_no, step_height, roll_off)
        
        draw_ref_imgs(height_array, detected_circles, filename_formatted, pol_left_lim, pol_right_lim, take_bottom_left, exclude_list, best_circle_index, cwinsize, polwinsize, vert_line,cu_sh_width )
        insert_ref_image(filename_formatted, excel_file_path, file_no)

    #Plot 3D graph
    img_path_3d = draw_3d_plot(height_array, filename_formatted)
    
    insert_xl(excel_file_path, img_path_2d, img_path_3d,file_no)
    
    file_no+=1 
    completed=True 
    if not sg.one_line_progress_meter('My Meter', file_no-1, len(filename_list),'No. of files processed', orientation = 'h'):
        completed=False
        break


style_excel_final(excel_file_path)
print("[Code executed in %s seconds]" % (time.time() - start_time))


done_gui(excel_file_path, completed)












