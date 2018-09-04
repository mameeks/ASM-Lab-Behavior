def Sparklines_full():
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

    duration = 1440 # total experiment duration (s)
    pre = 180 # pre-stimulus duration (s)
    post = 180 # post-stimulus duration (s)

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

        TMin = copy(pre)
        TMax = duration - post
        TMin1 = int(round(df['Sampling_Rate'][0]*TMin))
        TMax1 = int(round(df['Sampling_Rate'][0]*TMax))

        time = df['T']
        x_time = []
        min_time = min(time)
        x_time[:] = [x - min_time for x in time]

        if csvfiles[i][-5] == 'L':
            stimulus = cnames[2]
            control = cnames[3]
            stimcoords = np.array([ [0,50], [0,75], [15,50], [15,75] ])
            ctrlcoords = np.array([ [15,50], [15,75], [30,50], [30,75] ])
        else:
            stimulus = cnames[3]
            control = cnames[2]
            stimcoords = np.array([ [15,50], [15,75], [30,50], [30,75] ])
            ctrlcoords = np.array([ [0,50], [0,75], [15,50], [15,75] ])

        stimulus = stimulus.iloc[TMin1:TMax1]
        control = control.iloc[TMin1:TMax1]
        stim = np.asarray(stimulus.tolist())
        ctrl = np.asarray([ -x for x in control])

        Min = 0
        TMax = copy(pre)
        MinPre = round(df['Sampling_Rate'][0]*TMin)
        MaxPre = round(df['Sampling_Rate'][0]*TMax)
        stim_pre = InROI(df, Coordinates=stimcoords, TMin=MinPre, TMax=MaxPre)
        ctrl_pre = InROI(df, Coordinates=ctrlcoords, TMin=MinPre, TMax=MaxPre)

        TMin = duration - post
        TMax = copy(duration)
        MinPost = round(df['Sampling_Rate'][0]*TMin)
        MaxPost = round(df['Sampling_Rate'][0]*TMax)
        stim_post = InROI(df, Coordinates=stimcoords, TMin=MinPost, TMax=MaxPost)
        ctrl_post = InROI(df, Coordinates=ctrlcoords, TMin=MinPost, TMax=MaxPost)

        stim = np.append(stim_pre, stim)
        ctrl = np.append(ctrl_pre, ctrl)

        stim = np.append(stim, stim_post)
        ctrl = np.append(ctrl, ctrl_post)

        if stim[-1]!=0 or ctrl[-1]!=0:
           stim=np.append(stim, 0)
           ctrl=np.append(ctrl, 0)
           x_time.insert(0,0)

        # plot triggers
        fill1 = copy(pre)
        fill2 = duration - post
        fill3 = copy(duration)
        plt.figure(figsize=(5,1), dpi=80)
        plt.fill([0,fill1,fill1,0], [-1,-1,1,1], 'b', alpha=0.2)
        plt.fill([fill2,fill3,fill3,fill2], [-1,-1,1,1], 'b', alpha=0.2)
        plt.fill_between(x_time, 0, stim, where=stim>0, color="black")
        plt.fill_between(x_time, 0, ctrl, where=ctrl<0, color="black")
        plt.text(-100, 0.5, 'S', fontsize=12)
        plt.text(-100, -0.6, 'C',fontsize=12)
        plt.ylim(-1.1, 1.1)
        plt.axis('off')

        # save figure
        filename = save_folder+'/SparkFigures_Full/Sparklines_Fish'+str(i+1)+'.jpg'
        plt.savefig(filename)

def InROI(file, Coordinates, TMin, TMax):
    from matplotlib import path
    import numpy as np
    from scipy import spatial as sp
    import itertools

    K = sp.ConvexHull(Coordinates).vertices
    K = np.append(K, K[0])
    XVert = Coordinates[K,0]
    YVert = Coordinates[K,1]
    XY = np.stack((XVert, YVert), axis=1)

    data_in = [0]*len(file['T'].iloc[int(TMin):int(TMax)])
    X_dat = file['X'].iloc[int(TMin):int(TMax)]
    Y_dat = file['Y'].iloc[int(TMin):int(TMax)]
    p = path.Path(XY)

    for i, (x, y) in enumerate(itertools.izip(X_dat, Y_dat)):
        data_in[i] = int(p.contains_points([(x, y)]))
    return np.asarray(data_in)
