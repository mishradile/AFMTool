""" 
Locate the center of the circular Cu contacts given the height data array
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pySPM

from datetime import datetime
import pytz

tz_SG = pytz.timezone('Asia/Singapore') 
datetime_SG = datetime.now(tz_SG)
#For saving files with timestamps 
format_timestring = datetime_SG.strftime("%m%d%Y%H%M")

def find_circles(file_name, target_dir_path, use_phase=False):
    """ 
    Returns coordinate of circles found
    """
    # Read image.
    if(use_phase):
        img = cv2.imread("misc/phase_images/"+file_name+"2d_plot.png", cv2.IMREAD_COLOR)
    else:
        img = cv2.imread("images/"+file_name+"2d_plot.png", cv2.IMREAD_COLOR)
    img = ResizeWithAspectRatio(img, width =768)
    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    gray_blurred = cv2.medianBlur(gray,9)
    # Apply Hough transform on the blurred image.
    #TODO: Document assumptions here
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 200, param1 = 35,
                param2 = 27, minRadius = 40, maxRadius = 110)
  
  
    # # Draw circles that are detected.
    if detected_circles is not None:
        
        
  
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        #cv2.circle(img, (768, 768), 1, (255, 0, 0), 3)
        
        # cv2.circle(img, (200, 200), 100, (255,0,  0), 2)
        # cv2.circle(img, (200, 200), 50, (255,0,  0), 2)
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
    
            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
    
            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        #cv2.imshow("Detected Circle", img)
        #Save image
        cv2.imwrite(target_dir_path+file_name[:-1]+".png", img)
        #cv2.waitKey(0)
        return detected_circles
    else:
        if(use_phase):
            #Only give error photo if using phase data also can't find contact points
            cv2.putText(img,'Error: No circles/copper contacts detected', 
                (50, 370), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1,
                (255,255,255),
                1,
                2)
            cv2.imwrite(target_dir_path+file_name[:-1]+"_error"+".png", img)
        return None
    
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def create_ml_img_dir():
    #Make directory to store images for manual confirmation
    img_dir_path = "../results/ML_identified_contacts/"+format_timestring+"/"
    os.makedirs(img_dir_path)
    return img_dir_path

def identify_from_phase(detected_circles, file_name, target_dir_path, phase_data):
    """ 
    If usual ML script can't identify any contacts, or if radius of contacts identified varied too
    widely (suggesting bad results), we'll try to identify using data from the phase channel, which tends to be 
    much clearer for cases when height channel gives vague images.  
    """
    if(detected_circles is not None):
        max_r = 0
        min_r = 999
        for pt in detected_circles[0, :]:
            r=pt[2]
            max_r = max(max_r,r)
            min_r = min(min_r,r)
        if(max_r/min_r < 1.2 and detected_circles is not None): #If no problem
            return detected_circles
        else:
            #Remove wrong image
            os.remove(target_dir_path+file_name[:-1]+".png")
            #Generate phase image
            
            #Correct data for slope
            #TODO: Check if algorithm is same as currently used
            #phase_data_correct_plane = phase_data.correct_plane(inline=False)
            phase_data_correct_plane = phase_data.correct_plane(inline=False)
            #Plot of phase data for Excel report 
            fig, ax = plt.subplots(1, 1, figsize=(20, 20))

            phase_data_correct_plane.show(ax=ax)

            fig.tight_layout()
            
            img_path_2d = "../AFMTOOL/misc/phase_images/"+str(file_name)+"2d_plot"
            #plt.style.use('dark_background')
            plt.axis('off')
            plt.title('')
            plt.savefig(img_path_2d, bbox_inches='tight', pad_inches=0)
            
            find_circles(file_name, target_dir_path, True)