#     Saves ROI trigger duration for each fish.
#
#     (Python equivalent of Matlab function save_triggers_in_excel)
#
#     Returns:
#         .csv file containing containing trigger information for each fish.
#         Data for stimulus ROI is stored on the Left and data for control ROI
#         is stored on the Right.

import re
import numpy as np
import os
import pandas as pd
import collections
import Tkinter, tkFileDialog

# Set Tmin, Tmax, and Bins:
Tmin = 0 # in seconds
Tmax = 1440 # in seconds
Bin_Lengths = ['0-1000', '1000-2000', '2000-3000', '3000-5000','5000-8000',
               '8000-11000', '11000-15000', '15000-20000'] # in miliseconds

root = Tkinter.Tk()
root.withdraw()
data_folder = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select folder containing fish data:')
data_folder = '%s/FishData' % data_folder
# data_folder = raw_input("Input name of folder containing LoadData output: ")
# data_folder = '/Users/malika/Documents/MATLAB/behavior/%s/FishData' % data_folder

# Define function to sort .csv files in order
_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

# Define function to sort bins
def binstore(File, trigger, num_triggers):
    num_triggers.append(len(np.nonzero(trigger)[0]) * 1/(File['Sampling_Rate'][1]))

    # Save only consecutive 1s in trigger
    trigger = trigger.tolist()
    trigger = ''.join([str(x) for x in trigger])
    num_consec = trigger.split("0")
    num_consec = list(filter(None, num_consec))

    if not num_consec:
        result = [0] * len(Start)
    else:
        length_num_consec = []
        length_num_consec_ms = []
        for k, num in enumerate(num_consec):
            length_num_consec.append(len(num))
            length_num_consec_ms.append(len(num)*(1/File['Sampling_Rate'][1])*1000)

        # Sort into bins
        result = np.digitize(length_num_consec_ms, Bins_for_sorting)
        result = np.bincount(result, minlength=len(Bin_Lengths)+1)
        result = np.delete(result, 0)
    return result


# Save data in folder below data_folder
save_folder=os.path.dirname(data_folder)

Start = []
End = []
# Save upper and lower limits of each bin to lists Start and End
for i, Bin in enumerate(Bin_Lengths):
    indices = re.split('-', Bin)
    Start.append(int(indices[0]))
    End.append(int(indices[1]))

# Add one more bin for data after last bin
Start.append(End[-1])
Bin_Lengths.append('> than ' + str(End[-1]))

if Tmax < End[-1]/1000:
    ValueError('Bin Lengths requested are greater than TMax')

# Load Data
# Get all csv files in the specified folder
csvfiles = []
for File in os.listdir(data_folder):
    if File.endswith('.csv'):
        csvfiles.append(os.path.join(data_folder, File))
csvfiles.sort(key=natural_sort_key)

File = pd.read_csv(csvfiles[0])
Tmin1 = int(round(File['Sampling_Rate'][0]*Tmin))
Tmax1 = int(round(File['Sampling_Rate'][0]*Tmax))

# Initialize variables before loop
count = 1
stim_triggers = []
ctrl_triggers = []
stimbins = {}
ctrlbins = {}
stimlab = []
ctrllab = []

# get csv files for each fish
for i in range(1, len(csvfiles)+1):
    print('Fish..'+str(i))
    File = pd.read_csv(csvfiles[i-1])
    cnames = File.columns.tolist()

    if Tmax1 > len(File[cnames[0]]):
        ValueError('Time bin specified is greater than recording time')

    Bins_for_sorting = Start[:]
    Bins_for_sorting.append(Tmax*1000)

    # Get time taken for different triggers

    for k, j in enumerate(cnames[2:4]):
        ROI = j
        trigger = File[ROI].iloc[Tmin1:Tmax1]

        # Pass to helper function
        if csvfiles[i-1][-5] == 'L' and k == 0 or csvfiles[i-1][-5] == 'R' and k == 1:
            stimbins['Fish %s' % str(i)] = binstore(File, trigger, stim_triggers)
            stimlab.append('Fish %s %s' % (str(i), ROI))
        else:
            ctrlbins['Fish %s' % str(i)] = binstore(File, trigger, ctrl_triggers)
            ctrllab.append('Fish %s %s' % (str(i), ROI))
        count += 1

colnames = Bin_Lengths[:]
colnames.append('Total trigger time (s)')
colnames = colnames*2
colnames.insert(0, 'Fish ID (Stimulus)')
colnames.insert(11, 'Fish ID (Control)')
# double this
stimdata = {}
ctrldata = {}

# Save all information in dictionary "data"
for key in stimbins:
    stimdata[key] = stimbins[key].tolist()
for key in ctrlbins:
    ctrldata[key] = ctrlbins[key].tolist()

osdata = collections.OrderedDict(sorted(stimdata.items()))
ocdata = collections.OrderedDict(sorted(ctrldata.items()))

# build dataframe
df1 = pd.DataFrame(osdata)
df2 = pd.DataFrame(ocdata)
df1 = df1.transpose()
df2 = df2.transpose()

df = pd.concat([df1, df2], axis=1)
# overwrite last row with number_of_triggers
df.insert(0, 'Fish ID', pd.Series(stimlab, index=df.index))
df.insert(10, 'Total triggers', pd.Series(stim_triggers, index=df.index))
df.insert(11, 'Fish ID', pd.Series(ctrllab, index=df.index), allow_duplicates=True)
df['Total triggers 2'] = ctrl_triggers
filename = raw_input('Enter file name: ')

# export as csv
df.to_csv('%s/%s.csv' % (save_folder, filename), float_format= '%.12f', index=False, header=colnames, index_label='Fish ID')
