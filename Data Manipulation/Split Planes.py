import numpy as np
import matplotlib.pyplot as plt

path = "D:\\Documents\\Northumbria University\\PhD Research\\CFD\\Ahmed Model\\Platoon\\IDDES\\0.125L\\Extracted Data\\xL=0.0625_Follower\\State "

files = 2 
for i in range(0, files):

    i = i+1
    # Convert Number to String
    NumtoStr = str(i)

    # Load the data in
    xSplit = np.genfromtxt('State '+NumtoStr+'.csv', delimiter=',',skip_header=True)

    # Split x coordinates split
    X = xSplit[:,4] = -1.305
    xFollower = xSplit[X,0:7]

    # # Split x coordinates leader
    # X = xSplit[:,1] >= 0
    # xLeader = xSplit[X,0:4]

    print("iteration: ", i,":",files)
    saveData = np.savetxt(path+NumtoStr+".csv", xLeader, delimiter=",", header="U Mean, U0, U1, u2, X, Y, Z", comments='')