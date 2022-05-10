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

def find_circles(file_name):
    """ 
    Returns coordinate of circles found
    """
    # Read image.
    img = cv2.imread("images/2d_height_plot.png", cv2.IMREAD_COLOR)
    img = ResizeWithAspectRatio(img, width =768)
    # Convert to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.medianBlur(gray,9)
    # Apply Hough transform on the blurred image.
    #TODO: Document assumptions here
    detected_circles = cv2.HoughCircles(gray_blurred, 
                    cv2.HOUGH_GRADIENT, 1, 160, param1 = 50,
                param2 = 22, minRadius = 40, maxRadius = 110)
  
  
    # # Draw circles that are detected.
    if detected_circles is not None:
        
        #Make directory to store images for manual confirmation
        img_dir_path = "../results/ML_identified_contacts/"+format_timestring+"/"
        os.makedirs(img_dir_path)
  
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        
        # cv2.circle(img, (200, 200), 100, (255,0,  0), 2)
        # cv2.circle(img, (200, 200), 50, (255,0,  0), 2)
    
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
    
    #         # Draw the circumference of the circle.
            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
    
    #         # Draw a small circle (of radius 1) to show the center.
            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        cv2.imshow("Detected Circle", img)
        #Save image
        cv2.imwrite(img_dir_path+file_name, img)
        #cv2.waitKey(0)
    else:
        return 0
    
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