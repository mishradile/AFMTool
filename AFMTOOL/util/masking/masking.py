import numpy as np
import matplotlib.pyplot as plt

def get_mask(detected_circles):
    mask = np.ones((256,256))
    for pt in detected_circles[0, :]:
        #Get x, y, r in pixels
        x,y, r = int(pt[0]*256/768), int(pt[1]*256/768), int(pt[2]*256/768)
        #Mask out contact points
        mask[max(0, y-r): min(256, y+r+1), max(0,x-r):min(256, x+r+1)] =0

    plt.imshow(mask)
    plt.show()
    return mask ==1