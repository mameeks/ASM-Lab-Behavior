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
    if csvfiles[i][-5] == 'L':
        stimulus = cnames[2]
        control = cnames[3]
    else:
        stimulus = cnames[3]
        control = cnames[2]

    stim = np.asarray(df[stimulus].tolist())
    ctrl = np.asarray([ -x for x in df[control]])

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
