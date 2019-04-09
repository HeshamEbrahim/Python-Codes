import numpy as np
import matplotlib.pyplot as plt

pathLeading = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\0.125L\\Extracted Data\\Leading Cp\\State "
pathTrailing = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\0.125L\\Extracted Data\\Trailing Cp\\State "

files = 1
for i in range(0, files):

    i = i+1
    NumtoStr = str(i)
    # Load the data in
    # xSplit = np.genfromtxt('State '+NumtoStr+'.csv', delimiter=',',skip_header=True)
    xSplit = np.genfromtxt('Mean.csv', delimiter=',',skip_header=True)

    # Split x coordinates follower
    X = xSplit[:,1] < 0
    xFollower = xSplit[X,0:4]

    # Split x coordinates leader
    X = xSplit[:,1] >= 0
    xLeader = xSplit[X,0:4]

    print("iteration: ", i,":",files)
    saveData = np.savetxt(pathLeading+"Mean.csv", xLeader, delimiter=",", header="Cp, X, Y, Z", comments='')
    saveData = np.savetxt(pathTrailing+"Mean.csv", xFollower, delimiter=",", header="Cp, X, Y, Z", comments='')