""" 
Locate the center of the circular Cu contacts given the height data array
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
import pytz

tz_SG = pytz.timezone('Asia/Singapore') 
datetime_SG = datetime.now(tz_SG)
#For saving files with timestamps 
format_timestring = datetime_SG.strftime("%m%d%Y%H%M")

#Main function
def find_circles(file_name, target_dir_path, height_array, phase_data):
    """ 
    Returns coordinate of circles found
    """
    # Read image.
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
    
  
    if(check_radius_and_distance_and_number(detected_circles) == False):
        detected_circles = find_using_dif_cmap(file_name, target_dir_path, height_array)
    if(check_radius_and_distance_and_number(detected_circles) == False):
        detected_circles = find_using_phase(file_name, target_dir_path, phase_data)
    if(check_radius_and_distance_and_number(detected_circles) == False):
        detected_circles = find_using_binary_filter(file_name, target_dir_path, height_array)
        
    # Draw circles that are detected.
    if detected_circles is not None:
        
  
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))

    
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

def check_radius_and_distance_and_number(detected_circles):
    #Check if radius of circles detected varies too much, and if distance between
    #circles are too small
    #Also return false if only one circle detected
    if(detected_circles is None):
        #print("none detected")
        return False
    if(len(detected_circles[0])==1):
        #print("one detected")
        return False
    radius_sum =0
    max_rad = 0
    min_rad = 999
    center_list = []
    for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            radius_sum += r
            center_list.append((a,b))
            max_rad = max(r,max_rad)
            min_rad = min(r,min_rad)
    if(abs(max_rad -min_rad) >= 0.5*min_rad):
        #print("radius too different")
        return False
    avg_radius = radius_sum/len(detected_circles[0])
    for i in range(len(center_list)-1):
        for j in range(i+1,len(center_list)):
            dist = ((center_list[i][0]-center_list[j][0])**2 + (center_list[i][1]-center_list[j][1])**2)**0.5
            if dist < avg_radius*3:
                #print("too near")
                return False
    
    return True

def find_using_dif_cmap(file_name, target_dir_path, height_array):
    
    #print("diff cmap used for " + file_name)
    
    
    #Plot image
    img_path = "../AFMTOOL/misc/temp_images/diff_cmap/"+str(file_name)+"2d_plot"
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    plt.imshow(height_array, cmap="gist_rainbow")
    fig.tight_layout()
    plt.axis('off')
    plt.title('')
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    #Image processing and detecting circles
    img = cv2.imread("misc/temp_images/diff_cmap/"+file_name+"2d_plot.png", cv2.IMREAD_COLOR)
    img = ResizeWithAspectRatio(img, width =768)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.medianBlur(gray,15)
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 200, param1 = 35,
                param2 = 27, minRadius = 40, maxRadius = 110)

    #Only returns best 3 circles detected
    return detected_circles

def find_using_phase(file_name, target_dir_path, phase_data):
    
    #print("Phase used for file: " + file_name)

    #Converting phase data to array
    phase_data_correct_plane = phase_data.corr_fit2d(inline=False, nx=2, ny=2).filter_scars_removal()
    phase_array = phase_data_correct_plane.pixels
    
    #Plot image
    img_path =  "../AFMTOOL/misc/temp_images/phase/"+str(file_name)+"phase_plot"
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    plt.imshow(phase_array)
    fig.tight_layout()
    plt.axis('off')
    plt.title('')
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    
    #Image processing and detecting circles
    img = cv2.imread("misc/temp_images/phase/"+file_name+"phase_plot.png", cv2.IMREAD_COLOR)
    img = ResizeWithAspectRatio(img, width =768)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.medianBlur(gray,19)
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 200, param1 = 70,
                param2 = 27, minRadius = 40, maxRadius = 110)
    
    return detected_circles
    


def find_using_binary_filter(file_name, target_dir_path, height_array):
    #print("Binary filter used for " + file_name)
    
    #Generate binary array    
    height_avg = np.mean(height_array)
    binary_height_array = height_array>height_avg
    
    #Plot image
    img_path = "../AFMTOOL/misc/temp_images/binary_filter/"+str(file_name)+"2d_plot"
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    plt.imshow(binary_height_array)
    fig.tight_layout()
    plt.axis('off')
    plt.title('')
    plt.savefig(img_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    
    #Image processing and detecting circles
    img = cv2.imread("misc/temp_images/binary_filter/"+file_name+"2d_plot.png", cv2.IMREAD_COLOR)
    img = ResizeWithAspectRatio(img, width =768)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.medianBlur(gray,135)
    detected_circles = cv2.HoughCircles(gray_blurred,
                    cv2.HOUGH_GRADIENT, 2, 200, param1 = 70,
                param2 = 10, minRadius = 0, maxRadius = 110)
    
    return detected_circles


