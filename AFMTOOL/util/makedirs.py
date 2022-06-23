"""
Generate emtpy directories for storing working data 
"""
import os

def gen_dir():
    dirs_needed = [
        "../results/masks/",
        "../results/ML_identified_contacts/",
        "../results/ref_regions_imgs/",
        "../results/xlSheets/",
        "../AFMTOOL/images/",
        "../AFMTOOL/line_profile_imgs/",
        "../AFMTOOL/misc/temp_images/binary_filter/",
        "../AFMTOOL/misc/temp_images/diff_cmap/",
        "../AFMTOOL/misc/temp_images/k_means/",
        "../AFMTOOL/misc/temp_images/phase/",
    ]
    for dir_path in dirs_needed:
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path) 