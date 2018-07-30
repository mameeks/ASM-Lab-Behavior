REQUIRED PACKAGES
The below packages must be installed before running these functions. To install a package, open terminal/command prompt and type "pip install " followed by the name of the package. 
The command should look something like this:
pip install matplotlib

- matplotlib
- nptdms
- numpy
- pandas
- scipy


PYTHON FUNCTIONS
1. `TdmsToCSV` - Required function. Converts each .tdms file into a folder containing extracted data into .csv form.
2. `LoadData` - Required function. Converts raw .csv data into processed .csv file for each fish and saves it in folder called "FishData". Also in this folder saves "Fish_number.txt" which notes which fish number corresponds to which LOG file.
3. `PlotTriggers` - Plots trigger occurrence for each ROI in fish and saves .jpg files in folder "Figures"
4. `SaveTriggers` - Saves data for trigger duration in bins for each ROI in fish
5. `Sparklines` - Plots Sparklines plot depicting trigger occurrence in stimulus and control ROI in fish and saves .jpg files in folder "SparkFigures"
6. `ROIData` - Saves data for ROI (specified by input coordinates) in fish in a .csv file.
7. `DistanceFromSource` - Returns data about distance of fish from source in a .csv file.
8. `DescribeTriggers` - Returns probability density plot or histogram comparing trigger duration between control and stimulus ROIs across all fish
