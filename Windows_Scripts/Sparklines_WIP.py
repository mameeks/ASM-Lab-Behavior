#     Plot triggers
#
#     Plots how many times fish triggered odors
#     (Python equivalent of Matlab function plot_triggers)
#
#     Returns:
#        folder containing .jpg plots for each fish

import os
import shutil
import re
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
# import Tkinter, tkFileDialog

Tmin = 10
Tmax = 100

# root = Tkinter.Tk()
# root.withdraw()
# data_folder = tkFileDialog.askdirectory(parent=root,initialdir="/",title='Please select folder containing fish data:')
# data_folder = '%s/FishData' % data_folder
data_folder = raw_input("Input name of folder containing LoadData output: ")
data_folder = '/Users/malika/Documents/MATLAB/behavior/%s/FishData' % data_folder
save_folder=os.path.dirname(data_folder)

Bin_Lengths = ['0-1', '1-1000', '1000-2000', '2000-3000', '3000-5000','5000-8000',
                   '8000-11000', '11000-15000', '15000-20000'] # in miliseconds

if os.path.exists(save_folder+'/SparkFigures'):
        shutil.rmtree(save_folder+'/SparkFigures')
os.makedirs(save_folder+'/SparkFigures')

_nsre = re.compile('([0-9]+)')
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

def binstore(ROI, File):
    # get number of consecutive triggers
    num_consec = df[ROI].tolist()
    num_consec = ''.join([str(x) for x in num_consec])
    # num_consec = num_consec.split("0")
    # num_consec = list(filter(None, num_consec))

    # get number of consecutive triggers in ms
    if not num_consec:
            result = [0] * len(Start)
    else:
        # length_num_consec = []
        length_num_consec_ms = []
        for k, num in enumerate(num_consec):
            # length_num_consec.append(len(num))
            length_num_consec_ms.append(len(num)*(1/File['Sampling_Rate'][1])*1000)
    # bin the data
    result = np.digitize(length_num_consec_ms, Bins_for_sorting)
    # result = np.bincount(result, minlength=len(Bin_Lengths)+1)
    # result = np.delete(result, 0)
    return result

# Create bins
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


csvfiles = []
for File in os.listdir(data_folder):
    if File.startswith('Fish {') and File.endswith('.csv'):
        csvfiles.append(os.path.join(data_folder, File))
csvfiles.sort(key=natural_sort_key)
iMax = len(csvfiles)

# every fish whose data we have
for i in range(0, iMax):
    print('Fish..' + str(i+1))
    df=pd.read_csv(csvfiles[i])
    cnames = df.columns.tolist()
    time = df['T']

    Bins_for_sorting = Start[:]
    Bins_for_sorting.append(Tmax*1000)

    if csvfiles[i][-5] == 'L':
        stimulus = cnames[2]
        control = cnames[3]
    else:
        stimulus = cnames[3]
        control = cnames[2]

    # call helper function to bin data
    s_width = binstore(stimulus, df)
    c_width = binstore(control, df)
    # turn control triggers to negative
    # ctrl = np.array([-x for x in df[control]])

    if stim[-1]!=0:
        stim=stim.append(0)
    if ctrl[-1]!=0:
        ctrl=ctrl.append(0)

    # plot triggers
    x_time = []
    min_time = min(time)
    x_time[:] = [x - min_time for x in time]
    plt.figure(figsize=(5,1), dpi=80)
    plt.fill_between(x_time, 0, stim, where=stim>0, color="black")
    plt.fill_between(x_time, 0, ctrl, where=ctrl<0, color="black")
    plt.ylim(-1.1, 1.1)
    plt.axis('off')

    # save figure
    name_file = save_folder+'/SparkFigures/Sparklines_Fish'+str(i+1)+'.jpg'
    plt.savefig(name_file)
    plt.show()
