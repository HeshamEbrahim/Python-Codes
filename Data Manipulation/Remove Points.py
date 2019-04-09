import numpy as np
import matplotlib.pyplot as plt

path = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\0.125L\\Extracted Data\\yL=0\\NewData\\State "


files = 480 
for i in range(0, files):
    i = i+1
    NumtoStr = str(i)
    # Load the data in
    xSplit = np.genfromtxt('State '+NumtoStr+'.csv', delimiter=',',skip_header=False)

    # Remove first point
    X = np.delete(xSplit, 19310, 0)
    X = np.delete(X, 7851, 0)

    print("iteration: ", i,":",files)
    saveData = np.savetxt(path+NumtoStr+".csv", X, delimiter=",", header="U Mean, U0, U1, U2, X, Y, Z", comments='')
   