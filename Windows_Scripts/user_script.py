import numpy as np
from ROIData import ROIData
from SaveTriggers import SaveTriggers
from DistanceFromSource import DistanceFromSource

# SaveTriggers(Tmin=0, Tmax=1000, Bin_Lengths=['0-1000', '1000-2000', '2000-3000', '3000-5000','5000-8000',
#                    '8000-11000', '11000-15000', '15000-20000'])
#
# ROIData(Coordinates = np.array([ [0,50], [0,75], [15,50], [15,75] ]), TMin = 0, TMax = 180)
# ROIData(Vertices = np.array([ [15,50], [15,75], [30,50], [30,75] ]), TMin = 0, TMax = 180)
#
# ROIData(Vertices = np.array([ [0,50], [0,75], [15,50], [15,75] ]), TMin = 180, TMax = 1260)
# ROIData(Vertices = np.array([ [15,50], [15,75], [30,50], [30,75] ]), TMin = 180, TMax = 1260)
#
# ROIData(Vertices = np.array([ [0,50], [0,75], [15,50], [15,75] ]), TMin = 1260, TMax = 1440)
# ROIData(Vertices = np.array([ [15,50], [15,75], [30,50], [30,75] ]), TMin = 1260, TMax = 1440)
#
# DistanceFromSource(TMin=0,TMax=1000)
