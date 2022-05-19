""" 
Locate the center of the circular Cu contacts given the height data array
"""
import os
import cv2
import numpy as np

from datetime import datetime
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
  
  
    # # Draw circles that are detected.
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