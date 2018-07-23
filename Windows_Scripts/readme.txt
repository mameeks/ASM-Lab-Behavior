These scripts are run from the terminal/command prompt on a computer and require you to have python2 installed.

WINDOWS SETUP:
To run these scripts, open terminal and type "cd" followed by a space. Then drag the folder containing the functions into the terminal and hit enter to run.The command should look something like this:cd C:\Users\malika\Documents\Python_Scripts
After doing this, you can run the python scripts below by typing in their names. Do not omit the ".py" extension.


MAC SETUP:
To run these scripts, open terminal and "cd" followed by a space. Then drag the folder containing the functions into the terminal and hit enter to run.The command should look something like this:cd /Users/malika/Documents/Python_Scripts
To run python scripts, type "./" followed by the script's name. Do not omit the ".py" extension.

REQUIRED PACKAGES
The below packages must be installed before running these functions. To install a package, open terminal/command prompt and type "pip install " followed by the name of the package. 
The command should look something like this:
pip install matplotlib

- matplotlib
- nptdms
- numpy
- pandas
- scipy


PYTHON SCRIPTS1. TdmsToCSV.py - extracts data from all .tdms files in specified folder. Returns a folder for each .tdms file containing its data in .csv form.

2. LoadData.py - extracts useful information from all extracted .csv files in specified folders. Saves data for all fish in "FishData" folder. Also created Fish_number.txt to record which fish number corresponds to which log file.3. PlotTriggers.py - plots trigger duration for ROI3 and 4/ROI5 and 6 for each fish and saves plots as .jpg files in "Figures" folder.
4. SaveTriggers.py - saves trigger duration in bins for each fish. Returns .csv file containing trigger information for stimulus ROI on the Left and control ROI on the Right.
	> Note: by default, SaveTriggers saves triggers for the duration of the experiment 	(24 minutes). To change this, open the SaveTriggers.py file and change the Tmin 	(start time) and Tmax (end time) at the top of the script.