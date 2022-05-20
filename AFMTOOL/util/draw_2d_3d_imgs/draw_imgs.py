import numpy as np
import matplotlib.pyplot as plt

def draw_2d_plot(height_array, filename_formatted):
    #Plot of height data for Excel report 
    fig, ax = plt.subplots(1, 1, figsize=(20, 20))

    #phase_data.show(ax=ax[0])
    plt.imshow(height_array, cmap="copper")
    #amp_error_data.show(ax=ax[2])

    fig.tight_layout()
    
    
    
    img_path_2d = "../AFMTOOL/images/"+str(filename_formatted)+"2d_plot"
    #plt.style.use('dark_background')
    plt.axis('off')
    plt.title('')
    
    plt.savefig(img_path_2d, bbox_inches='tight', pad_inches=0)
    
    return img_path_2d


def draw_3d_plot(height_array, filename_formatted):
    #Plot 3D graph
    # Create figure and add axis

    fig = plt.figure(figsize=(7,7))
    fig.patch.set_facecolor('black')
    #plt.style.use('dark_background')
    ax = plt.subplot(111, projection='3d')
    ax.patch.set_facecolor('black')
    # Remove gray panes and axis grid
    ax.xaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.fill = False
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.fill = False
    ax.zaxis.pane.set_edgecolor('black')
    ax.grid(False)

    ax.set_xlabel('µm')
    ax.set_ylabel('µm')
    ax.set_zlabel('nm')

    ax.w_xaxis.line.set_color('white') 
    ax.w_yaxis.line.set_color('white') 
    ax.w_zaxis.line.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    # Create meshgrid, grid labels will be in micrometer
    X, Y = np.meshgrid(np.linspace(0, 20, len(height_array)), np.linspace(0, 20, len(height_array)))
    # Plot surface
    # TODO: Experiement with different colors
    plot = ax.plot_surface(X=X, Y=Y, Z=height_array, cmap='YlOrBr' ,rstride=1, cstride=1, alpha=None)

    fig.tight_layout()
    img_path_3d = "../AFMTOOL/images/"+str(filename_formatted)+"3d_plot"
    plt.savefig(img_path_3d)  
    plt.close(fig)
    
    return img_path_3d