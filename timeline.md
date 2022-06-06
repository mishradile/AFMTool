## Development Timeline
- 6/5/2022: 
    - Able to generate 2D, 3D plots using .spm data using Python. (https://github.com/ChenJiakaiIME/AFMTool/tree/main/AFMTOOL/images) Color may need improvement.

- 9/5/2022: 
  - Machine learning script able to recognise circular metal contacts from 2D images generated. 
  - Enabled Excel reports to be automatically generated to show the data/images generated from raw data files.

- 10/5/2022: 
  - Enabled batch processing. User can select multiple files at once from window to be processed, added progress bar to show how many files have been processed in live time (https://github.com/ChenJiakaiIME/AFMTool/pull/4)
  - Auto generate Excel report with all images generated with their file names labelled (https://github.com/ChenJiakaiIME/AFMTool/pull/5)
  - Fine tuned ML scripts for contact points that are not nicely circular (https://github.com/ChenJiakaiIME/AFMTool/pull/2)
  - Enabled auto-saving of images of circles identified for manual checking of ML results

- 11/5/2022:
  - Enabled auto generation of line profile plot 
  - Auto calculation of roughness (Ra) at center of copper contacts

- 12/5/2022:
  - Able to calculate step height
  - Able to plot vertical lines on line profile denoting areas of copper contact and polymer
  - Insert line profile image and step height into Excel sheet
  - Able to calculate polymer roughness

- 13/5/2022:
  - Fixed decimal points to 2
  - Generated requirements.txt

- 19/5/2022:
  - Corrected for quadratic background 
  - Corrected coordinates for taking Ra
  - Added reference pictures row in Excel report to mark out on 2D diagram which areas are used for Ra calculations
  - Correct d.p to 3
  - Enlarged axis for 3D plot

- 20/5/2022:
  - Added ref image to mark regions for line profile and step height calculations
  - Corrected errors in step height calculations
  - Implemented multiple checks for circle recognition (If height data fail, use different color mapping, if fail again use phase data, if still fail use binary filter)
  - Updated docs for usage and installation instructions

- 23/5/2022:
  - Added calculations for roll off

- 30/5/2022:
  - Implemented flags that can be used to customize output. 

- 1/6/2022:
  - Included support for .000, .001, .00 files

- 3/6/2022:
  - Developed GUI using PySimpleGUI
 
- 6/6/2022:
  - Allowed users to customize square size used to take roughness measurements
