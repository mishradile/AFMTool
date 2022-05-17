""" 
Locate the center of the circular Cu contacts given the height data array
"""
import os
import cv2
import numpy as np

from datetime import datetime
import matplotlib.pyplot as plt
import pytz

tz_SG = pytz.timezone('Asia/Singapore') 
datetime_SG = datetime.now(tz_SG)
#For saving files with timestamps 
format_timestring = datetime_SG.strftime("%m%d%Y%H%M")

def find_circles(file_name, target_dir_path):
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
  
  
    #Draw circles that are detected.
    draw_detected_circles(img, detected_circles, target_dir_path, file_name)
    
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
        return False
    if(len(detected_circles)==1):
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
    if(abs(max_rad -min_rad) >= 1.5*min_rad):
        return False
    avg_radius = radius_sum/len(detected_circles)
    for i in range(len(center_list)):
        for j in range(i+1,len(center_list)):
            dist = ((center_list[i][0]-center_list[j][0])**2 + (center_list[i][1]-center_list[j][1])**2)**0.5
            if dist < avg_radius*3:
                return False
    
    return True


def find_using_phase(file_name, target_dir_path, phase_data):
    
    #Remove existing ML_identified_contacts image
    os.remove(target_dir_path+file_name[:-1]+".png")
    
    #Plot phase image
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    phase_data.show(ax=ax)
    fig.tight_layout()
    img_path_2d = "../AFMTOOL/misc/temp_images/phase/"+str(file_name)+"phase_plot"
    plt.axis('off')
    plt.title('')
    plt.savefig(img_path_2d, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    img = cv2.imread("misc/temp_images/phase/"+file_name+"phase_plot.png", cv2.IMREAD_COLOR)
    
    img = ResizeWithAspectRatio(img, width =768)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    gray_blurred = cv2.medianBlur(gray,9)

    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 200, param1 = 35,
                param2 = 27, minRadius = 40, maxRadius = 110)

    #Use height img from now on to draw detected circles
    img = cv2.imread("images/"+file_name+"2d_plot.png", cv2.IMREAD_COLOR)
    #Clear phase image
    os.remove(img_path_2d+".png")
    # Draw circles that are detected.
    draw_detected_circles(img, detected_circles, target_dir_path, file_name)

def find_using_dif_cmap(file_name, target_dir_path, height_array):
    
    return None

def find_using_binary_filter():
    return None


#Share functions
def draw_detected_circles(img, detected_circles, target_dir_path, file_name):
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        #Save image
        cv2.imwrite(target_dir_path+file_name[:-1]+".png", img)
        return detected_circles
    else:
        write_error_message(img)
        cv2.imwrite(target_dir_path+file_name[:-1]+".png", img)
        return None
            
def write_error_message(img):
    cv2.putText(img,'Error: No circles/copper contacts detected', 
            (50, 370), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1,
            (255,255,255),
            1,
            2)
