import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_ref_imgs(height_array, detected_circles, filename_formatted, pol_left_lim, pol_right_lim, take_bottom_left = False, exclude=[], best_circle_index=0, cwinsize=1, polwinsize=2, vert_line=False):
    #Note pol_left_lim, pol_right_lim are measured in um, need to convert to pixels
    pol_left_lim = pol_left_lim*256/20
    pol_right_lim = pol_right_lim*256/20
    #Plot of height data for Excel report 
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))
    #phase_data.show(ax=ax[0])
    plt.imshow(height_array, cmap="copper")
    cu_count = 1
    pol_count=1
    
    for i in [x for x in range(len(detected_circles[0, :])) if x+1 not in exclude]:
        pt = detected_circles[0,i]
        x,y, r = int(pt[0]*256/768), int(pt[1]*256/768), int(pt[2]*256/768)
        half_window_size_pix = int(256*(0.5)*cwinsize/20)
        #Square where copper Ra is calculated
        ax.add_patch(Rectangle((x-half_window_size_pix, y-half_window_size_pix),
                        2*half_window_size_pix, 2*half_window_size_pix,
                        fc ='none', 
                        ec ='g',
                        lw = 3) )

        plt.text(x-half_window_size_pix, y-half_window_size_pix+4, cu_count, fontsize=25)
        cu_count+=1
        #Square where polymer Ra is calculated
        half_pol_win_size_pix  = int(256*(0.5)*polwinsize/20)
        if(not take_bottom_left):
            if(x+2*r-half_pol_win_size_pix<256 and y-2*r+half_pol_win_size_pix>0):
                ax.add_patch(Rectangle((x+2*r-half_pol_win_size_pix, y-2*r-half_pol_win_size_pix),
                                2*half_pol_win_size_pix, 2*half_pol_win_size_pix,
                                fc ='none', 
                                ec ='r',
                                lw = 3) )
                #Place text at bottom left of box
                plt.text(x+2*r-half_pol_win_size_pix, y-2*r+half_pol_win_size_pix, pol_count, fontsize=25)
                pol_count+=1
        else:
            x_pol = x-2*r
            y_pol = y+2*r
            #If all polymer area out of bound, try take bottom left of each circle
            if(y_pol-half_pol_win_size_pix<256 and (x_pol)-half_pol_win_size_pix<256):
                ax.add_patch(Rectangle((x-2*r-12, y+2*r-12),
                    2*half_pol_win_size_pix, 2*half_pol_win_size_pix,
                    fc ='none', 
                    ec ='r',
                    lw = 3) )
                plt.text(x-2*r+half_pol_win_size_pix, y+2*r-half_pol_win_size_pix, pol_count, fontsize=25)
                pol_count+=1          
    #Draw boundaries where line profile is taken 
    best_circle_x = int(detected_circles[0][best_circle_index][0]*256/768)
    best_circle_y = int(detected_circles[0][best_circle_index][1]*256/768)
    best_circle_r = int(detected_circles[0][best_circle_index][2]*256/768)
    
    if not vert_line: 
        line_profile_upper_lim = best_circle_y-best_circle_r/2
        line_profile_lower_lim = best_circle_y+best_circle_r/2
    
        #Two horizontal lines denoting line profile data 
        ax.add_patch(Rectangle((pol_left_lim, line_profile_upper_lim),
                            pol_right_lim-pol_left_lim, best_circle_r,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
        ax.add_patch(Rectangle((best_circle_x-0.8*best_circle_r, line_profile_upper_lim),
                            1.6*best_circle_r, best_circle_r,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
        
        #Two boxes denoting areas where step height is calculated from
        
        ax.add_patch(Rectangle((0, line_profile_lower_lim),
                            256, 0,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
        ax.add_patch(Rectangle((0, line_profile_upper_lim),
                            256, 0,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
    
    else:
        #Draw lines for vertical line profile
        line_profile_left_lim = best_circle_x-best_circle_r/2
        line_profile_right_lim = best_circle_x+best_circle_r/2
    
        
        #Two boxes denoting areas where step height is calculated from
        #Polymer box
        ax.add_patch(Rectangle((line_profile_left_lim, pol_left_lim),
                            best_circle_r,pol_right_lim-pol_left_lim,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
        #Copper box
        ax.add_patch(Rectangle((line_profile_left_lim, best_circle_y-0.8*best_circle_r),
                            best_circle_r,1.6*best_circle_r, 
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
        
        
        #Two horizontal lines denoting line profile data 
        ax.add_patch(Rectangle((line_profile_left_lim, 0),
                            0, 256,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )
        ax.add_patch(Rectangle((line_profile_right_lim, 0),
                            0, 256,
                            fc ='none', 
                            ec ='b',
                            lw = 3) )     
    
    ref_img_path = "../results/ref_regions_imgs/"+str(filename_formatted)+"ref_plot"
    plt.axis('off')
    plt.title('')
    fig.tight_layout()
    plt.savefig(ref_img_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)