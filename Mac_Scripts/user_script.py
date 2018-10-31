import numpy as np
from TdmsToCSV import TdmsToCSV
from LoadData import LoadData
from PlotTriggers import PlotTriggers
from SaveTriggers import SaveTriggers
from ROIData import ROIData
from DistanceFromSource import DistanceFromSource
from DescribeTriggers import DescribeTriggers
from Sparklines import Sparklines
from Sparklines_full import Sparklines_full

# TdmsToCSV()
# LoadData()
# PlotTriggers()
# SaveTriggers(TMin=0, TMax=1000, Bin_Lengths=['0-1000', '1000-2000', '2000-3000', '3000-5000','5000-8000',
#                    '8000-11000', '11000-15000', '15000-20000'])
#
# DescribeTriggers()
#
# ROIData(Coordinates = np.array([ [0,50], [0,75], [15,50], [15,75] ]), TMin = 0, TMax = 180)
# ROIData(Coordinates = np.array([ [15,50], [15,75], [30,50], [30,75] ]), TMin = 0, TMax = 180)
# ROIData(Coordinates = np.array([ [0,50], [0,75], [15,50], [15,75] ]), TMin = 180, TMax = 1260)
# ROIData(Coordinates = np.array([ [15,50], [15,75], [30,50], [30,75] ]), TMin = 180, TMax = 1260)
# ROIData(Coordinates = np.array([ [0,50], [0,75], [15,50], [15,75] ]), TMin = 1260, TMax = 1440)
# ROIData(Coordinates = np.array([ [15,50], [15,75], [30,50], [30,75] ]), TMin = 1260, TMax = 1440)
#
# DistanceFromSource(TMin=5,TMax=180)
# DistanceFromSource(TMin=0,TMax=1440)
# Sparklines()
# Sparklines_fuller()
