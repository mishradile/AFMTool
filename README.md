# AFMTool
AFM Tool for automating data analysis for  .spm files

## Target functions
- Generate 2D, 3D plot
- Generate roughness(RA) for Cu and polymer 
- Generate step height
- Automatically generate Excel sheet containing above values


## Timeline
- 6/5/2022: Able to generate 2D, 3D plots using .spm data using Python. Color may need improvement.
- 9/5/2022: 
  - Machine learning script able to recognise circular metal contacts from 2D images generated. 
  - Enabled Excel reports to be automatically generated to show the data/images generated from raw data files.
- 10/5/2022: 
  - Enabled batch processing. User can select multiple files at once from window to be processed, added progress bar to show how many files have been processed in live time (https://github.com/ChenJiakaiIME/AFMTool/pull/4)
  - Auto generate Excel report with all images generated with their file names labelled (https://github.com/ChenJiakaiIME/AFMTool/pull/5)
