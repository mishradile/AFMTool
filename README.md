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

## Installation 
- Download the entire AFMTOOL folder onto Desktop. If you're downloading from Github, click the green `Code` button on top of the list of files, and click `Download Zip`. Move the downloaded folder onto your Desktop
- You need to have Python version>=3.9 to run the script. 
- Check if Python is installed in your computer:
    - Open command line. In Windows, press Windows logo + S to launch search window, and search `cmd`. 
    - In command line, type: `python --version`
    - If Python has been installed, the version that is in your computer will be returned. 
![Check python ver](https://user-images.githubusercontent.com/105037297/169487975-c7da6c6f-da46-44d2-bda3-5d8dd35987d7.PNG)
    - If an error message is returned, Python has not been installed. You can download it here: https://www.python.org/downloads/
- If Python has been installed in your computer, you need to proceed to install the required Python libraries that is needed to run the script. In the command line, type `cd %HOMEPATH%/Desktop/AFMTOOL` and press Enter. After that, type `pip install -r requirements.txt`. Please wait for installation to be completed.
- If no error messages appeared on the terminal, you have successfully installed the packages needed to run the script, please refer to Usage section below on how to run the script. 

## Usage

## Notes on possible changes to measurement methods
- Obtain step height using height histogram instead of line profile?
