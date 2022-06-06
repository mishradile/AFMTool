# AFMTool
AFM Tool for automating data analysis for  .spm files

## Functionailites
- Generate 2D, 3D plot
- Generate roughness(RA) for Cu and polymer 
- Generate step height
- Generate roll-off
- Automatically generate Excel sheet containing above values

## Installation 
- Download the entire AFMTOOL folder onto Desktop. If you're downloading from Github, click the green `Code` button on top of the list of files, and click `Download Zip`. Move the downloaded folder onto your Desktop
- You need to have Python version>=3.9 to run the script. 
- Check if Python is installed in your computer:
    - Open command line. In Windows, press Windows logo + S to launch search window, and search `cmd`. 
    - In command line, type: `python --version`
    - If Python has been installed, the version that is in your computer will be returned. 
![Check python ver](https://user-images.githubusercontent.com/105037297/169487975-c7da6c6f-da46-44d2-bda3-5d8dd35987d7.PNG)
    - If an error message is returned, Python has not been installed. You can download it here: https://www.python.org/downloads/
- If Python has been installed in your computer, you need to proceed to install the required Python libraries that is needed to run the script. In the command line, type `cd %HOMEPATH%/Desktop/AFMTOOL` and press Enter. After that, type `pip install -r requirements.txt` and wait for installation to be completed.
- If no error messages appeared on the terminal, you have successfully installed the packages needed to run the script, please refer to Usage section below on how to run the script. 

## Usage

1. Open the main `AFMTOOL` folder, and click into the `AFMTOOL` folder inside.
2. Double click the `AFMTool.vbs` file. 
3. User interface pops up. Click the `Browse` button. 

![Capture12](https://user-images.githubusercontent.com/105037297/172102326-240144ce-2b42-4ade-acab-78fd969adb2e.PNG)

4. File Explorer window pops up. Drag and select files to be analyzed, and click `Open`. 
5. Click the `Optional inputs` tab to customize output. See `Additional Functions` section below for more details, or click the `Help` button in the user interface. 

![Capture31](https://user-images.githubusercontent.com/105037297/172102610-0a8f6212-7f56-451a-978f-fbe5ac68467c.PNG)

6. After selecting additional functions needed, go back to the main tab and click `Submit` button. 
7. Scripts starts to process files. You can see in the progress bar how many files it has processed. Time needed is approximately 12s per file. 
9. After all scripts has been processed, the window below pops up. You can select either to view the file in File Explorer, open the Excel file directly, or just close the windows. Alternatively, you can find the Excel file generated by clicking into the `AFMTOOL` folder in your Desktop, click into  `results` folder and then into `xlSheets` folder. The Excel file name is of the timestamped format `DDMMYYYYHHMM_AFMResults`, where the timestamp is the time when you started running the script (after you click `Open` in step 4). 

![Captur1212e](https://user-images.githubusercontent.com/105037297/172103141-0317de68-8593-4b8b-a501-959386691266.PNG)

11. The script may not be able to detect the copper contact points perfectly, especialy for noisy data. It is recommended to do a quick check of the results produced by going to the `ML_identified_contacts` folder under `results` folder to check the copper metal contacts detected by the algorithm. If your Excel file is `DDMMYYYYHHMM_AFMResults`, then the corresponding folder to check under `ML_identified_contacts` has name `DDMMYYYYHHMM` with the same timestamp. As well as the center of the cirlces detected are not close to the edge of the actual contact, and the radius is not off by more than 20% the script should be able to obtain the corect regions for calculations. For a more accurate check, you can also check the folder `ref_regions_imgs` under `results` to see the exact regions used by the algorithm for calculations of the roughness, plotting line profile, and finding step height. 

### Video demo of script running

https://user-images.githubusercontent.com/105037297/172103580-801b7fb3-b9a1-44b1-9f6f-367aa81be378.mp4

### Additional Functions (Flags in CLI have been replaced by GUI, to be updated)

One can customize the output of the script in several ways by going to the `Optional inputs` tab of the user interface. Below is a non-exhaustive list of options included. For a complete list, click the `Help` button under the same `Optional inputs` tab. 

Options: 
  - Use all circles: Evaluate roughness over all detected circles
  - Minimum radius: Specify minimum radius of circles to be evaluated. Should be followed by a decimal/integer. `python3 AFMTOOL.py -mr 3` specifies a minimum radius of 3um. 
  -  Maximum radius: Specify maximum radius of circles to be evaluated. 
  - Pitch: Specify pitch (um). This will set the minimum distance between detected circles. 
  - Exclude: Exclude circles from calculation. If by looking at the reference images we find a small number of contacts are identified wrongly and we want to exclude them, we can use the `-E` flag followed by the list of indexes (Displayed at the bottom left of each green square) of circles to be excluded, separated by commas and not spaces. The listed circles will then be excluded from roughness calculations and will not be chosen for generation of line profile. E.g. If we want to exclude the first, third and fourth circles, type `1,3,4` into the input box. 
  Note: The `exclude` option should only be used if you're only selected one file to analyse, as it will be applied for all files selected. i.e The above code will exclude the first, third and fourth circles for all files selected. 

## Troubleshooting
- If after typing in `python3 AFMtool.py`, the File Explorer windows does not pop up after a long time (~20s), try pressing Ctrl+C to terminate the process. If the process terminates successfully, there should be a prompt message stating so. Then type in `python3 AFMtool.py` again to restart the process. If the terminal doesn't respond to Ctrl+C also, close the terminal and restart from step 1. 

## Assumptions made of AFM raw data formats
- x,y axis have range 20um (Hardcoded to eliminate user's need of entering range. If need to change, open root AFMTOOL folder in VSCode or other text editors and search '20' to see the places being hardcoded.)
- Diameter:Pitch ratio is at least 1:2 (Used in choosing area to calculate polymer roughness. If need to change, go to util/roughness/roughness.py and change the section on getting polymer roughness.)
- Contacts are circular. (Used in identifying copper contacts.)

## Notes for future maintenance/updates
### Functions of key folders/files
```
AFMTOOL/
├── /AFMTOOL/ 
│   ├── /util/              # Folder containing scripts grouped by their general functions (Draw 2D/3D plots, find roughness, find step height, etc)
│   ├── AFMtool.py          # Script that will be ran from command line, it'll call other scripts in the process of running when needed
├── /results/               # Test files (alternatively `spec` or `tests`)
    ├── /ref_regions_imgs/  # Place to store images indicating regions which are used for calculation of copper/polymer roughness and step height. 
    ├── /ML_identified_contacts  # Raw output from OpenCV Houghcircles indicating the circles identified, used to quickly check if script is giving correct result for each file. (Maybe can remove after completely verifying accuracy of ref_regions_imgs)                            
    └── /xlSheets           # Folder storing final Excel reports

```
