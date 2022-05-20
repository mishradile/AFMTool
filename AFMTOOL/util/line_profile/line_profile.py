import openpyxl

from openpyxl.utils import get_column_letter
import numpy as np
import matplotlib.pyplot as plt

#Assumes contacts are in horizontal array
def plot_line_profile(filename_formatted, array, x, y, r):
    #Adjusting for coordinate differences between picture and numpy array
    
    #Convert from image scale to array index
    y_index = int(y*256/768)
    r_index = int(r*256/768)
    #Take average within band of width r/2
    line_data = array[int(y_index-r_index/2): int(y_index+r_index/2), :]
    line_data = np.mean(line_data, axis=0)
    
    avg_height = np.mean(line_data)
    
    fig_x = np.linspace(0,20,256)
    fig = plt.figure(figsize=(18,12))
    ax = plt.subplot(111)
    ax.plot(fig_x, line_data, color ="blue")
    ax.set_ylabel('nm', fontsize=10)
    ax.set_xlabel('μm', fontsize=10)
    
    #Plot vertical lines denoting copper contact
    r_um = r*20/768 #Get radius in um
    x_um = x*20/768
    #Take range slightly smaller than r to be safe
    left_lim = x_um-r_um*0.8
    right_lim = x_um+r_um*0.8
    ax.plot((left_lim, left_lim), (min(line_data), max(line_data)), color='black', linestyle='-.')
    ax.plot((right_lim, right_lim), (min(line_data), max(line_data)), color='black', linestyle='-.')
    
    left_lim_index = int(left_lim*256/20)
    right_lim_index = int(right_lim*256/20)
    avg_copper_height = np.mean(line_data[int(left_lim_index):int(right_lim_index)])
    
    dishing = True if (avg_copper_height<avg_height) else False
    
    
    #Plot vertical lines denoting polymer
    #Note that polymer limits are shifted inwards (towards each other) by 0.2*r from the 
    #calculated "ideal" positions, to be safe not to touch regions of copper contacts in case 
    #centers or radius of circles identified are not accurate 
    if(x_um>=10): 
        pol_right_lim = x_um-r_um*1.2
        ax.plot((pol_right_lim, pol_right_lim), (min(line_data), max(line_data)), color='red', linestyle='-.')
        #Note that find_pol_limit gives index, need to convert to um
        
        pol_left_lim = (20/256)*find_pol_limit(line_data, int((pol_right_lim)*256/20), avg_height, dishing, False)+0.2*r_um
        ax.plot((pol_left_lim, pol_left_lim), (min(line_data), max(line_data)), color='red', linestyle='-.')
    else:
        pol_left_lim = x_um+r_um*1.2
        ax.plot((pol_left_lim, pol_left_lim), (min(line_data), max(line_data)), color='red', linestyle='-.')
        pol_right_lim = (20/256)*find_pol_limit(line_data, int((pol_left_lim)*256/20), avg_height, dishing, True)-0.2*r_um
        ax.plot((pol_right_lim, pol_right_lim), (min(line_data), max(line_data)), color='red', linestyle='-.')
    img_path = "../AFMTOOL/line_profile_imgs/"+str(filename_formatted)+"line_plot"

    plt.savefig(img_path, bbox_inches='tight')
    
    plt.close(fig)
    
    avg_pol_height = np.mean(line_data[int(pol_left_lim*256/20):int(pol_right_lim*256/20)])
    
    return avg_copper_height -avg_pol_height, pol_left_lim, pol_right_lim
    
def insert_line_profile(filename_formatted, excel_file_path, col_num, step_height):
    
    img_path  = "../AFMTOOL/line_profile_imgs/"+str(filename_formatted)+"line_plot.png"
    wb = openpyxl.load_workbook(excel_file_path)
    ws = wb["Sheet"]
    
    col_letter = get_column_letter(col_num+1)
    
    line_img = openpyxl.drawing.image.Image(img_path)
    line_img.height = 93
    line_img.width = 140
    
    line_img.anchor = col_letter + '10'
    ws.add_image(line_img)
    
    #Insert step height
    ws[col_letter + '9'] = "{:.3f}".format(step_height)
    
    wb.save(excel_file_path)
    

def find_pol_limit(array, first_limit, avg_height, dishing, search_right):
    
    index = first_limit

    if(dishing):
        if(search_right):
            while(index<=256 and not all(i<avg_height for i in array[index:index+5])):
                index+=1
        else:
            while(index>=0 and not all(i<avg_height for i in array[index-5:index])):
                index-=1
    else:
        if(search_right):
            while(index<=256 and not all(i>avg_height for i in array[index:index+5])):
                index+=1
        else:
            while(index>=0 and not all(i>avg_height for i in array[index-5:index])):
                index-=1
    
    return index

