# AFMTool
AFM Tool for automating data analysis for  .spm files

## Target functions
- Generate 2D, 3D plot
- Generate roughness(RA) for Cu and polymer 
- Generate step height
- Automatically generate Excel sheet containing above values


## Timeline
- 6/5/2022: 
    - Able to generate 2D, 3D plots using .spm data using Python. (https://github.com/ChenJiakaiIME/AFMTool/tree/main/AFMTOOL/images) Color may need improvement.
    - Developed machine learning script that is able to recognise locations of Copper contact points from the 2d plots generated. We then know where to calculate roughness. 


## Installation 
- Prerequisites
    - Python 
    - OpenCV
    - numpy
    - matplotlib
    - IPython
    - pySPM
    

## Notes on possible changes to measurement methods
- Obtain step height using height histogram instead of line profile?
