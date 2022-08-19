import numpy as np
import matplotlib.pyplot as plt

import os

from datetime import datetime
import pytz
tz_SG = pytz.timezone('Asia/Singapore') 
datetime_SG = datetime.now(tz_SG)
#For saving files with timestamps 
format_timestring = datetime_SG.strftime("%m%d%Y%H%M")


def get_mask(detected_circles, mask_dir, filename_formatted, scan_pixels_len):
    mask = np.ones((scan_pixels_len,scan_pixels_len))
    for pt in detected_circles[0, :]:
        #Get x, y, r in pixels
        x,y, r = int(pt[0]*scan_pixels_len/768), int(pt[1]*scan_pixels_len/768), int(pt[2]*scan_pixels_len/768)
        #Mask out contact points
        mask[max(0, y-r): min(scan_pixels_len, y+r+1), max(0,x-r):min(scan_pixels_len, x+r+1)] =0
    plt.imshow(mask)
    plt.axis('off')
    plt.title('')
    mask_path = mask_dir+str(filename_formatted)+"mask"
    plt.savefig(mask_path,  bbox_inches='tight', pad_inches=0)
    plt.close()
    return mask ==1

def create_mask_img_dir():
    #Make directory to store images for manual confirmation
    img_dir_path = "../results/masks/"+format_timestring+"/"
    os.makedirs(img_dir_path)
    return img_dir_path